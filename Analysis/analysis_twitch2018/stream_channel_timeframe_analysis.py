from pyspark.sql import SparkSession, functions, types
from pyspark.sql.types import StringType, LongType, IntegerType, BooleanType, FloatType, DateType
import sys
import json
import datetime as dt


def getDate(dateStr):
    date = dt.datetime.strptime(dateStr, '%Y-%m-%dT%H:%M:%SZ')
    just_date = date.date()
    jd = just_date.strftime('%Y-%m-%d')
    return jd


def main(input1, input2):

    stream_creation_date = functions.udf(getDate)
    data_s = spark.read.json(input1)
    data_c = spark.read.json(input2)
    data_s = data_s.repartition(40)
    data_c = data_c.repartition(40)
    data_s = data_s.withColumn('stream_create_date',stream_creation_date(data_s.created_at))
    data_c = data_c.withColumn('last_updated_at', stream_creation_date(data_c.updated_at))
    data_s.createOrReplaceTempView('data_s')
    data_c.createOrReplaceTempView('data_c')



    data_stream = data_s.select('stream_id', 'game', 'viewers', 'video_height',
                           'average_fps', 'created_at','time_frame')\
        .where(functions.lower(data_s['game'])
                               .isin('fortnite','league of legends','call of duty: black ops 4',
                                      'overwatch', 'counter-strike: global offensive',
                                      'playerunknown\'s battlegrounds','just chatting', 'fallout 76',
                                      'tom clancy\'s rainbow six: siege',
                                      'world of warcraft','red dead redemption 2', 'destiny 2',
                                      'dota 2', 'fifa 19', 'battlefield v', 'dead by daylight',
                                      'rocket league','spyro reignited trilogy','grand theft auto v',
                                      'nba 2k19')).cache()

    data_ch = data_c.select('stream_id', 'channel_id','name', 'game', 'views',
                           'followers', 'broadcaster_language',
                           'created_at', 'last_updated_at', 'mature', 'partner')\
        .where(functions.lower(data_c['game'])
                               .isin('fortnite','league of legends','call of duty: black ops 4',
                                      'overwatch', 'counter-strike: global offensive',
                                      'playerunknown\'s battlegrounds','just chatting', 'fallout 76',
                                      'tom clancy\'s rainbow six: siege',
                                      'world of warcraft','red dead redemption 2', 'destiny 2',
                                      'dota 2', 'fifa 19', 'battlefield v', 'dead by daylight',
                                      'rocket league','minecraft','grand theft auto v',
                                      'nba 2k19')).cache()

    data_stream.createOrReplaceTempView('data_stream')
    data_ch.createOrReplaceTempView('data_ch')


#-------------------------------------------now jonning the 2 tables----------------------------------------------------

    cs_joint_table = data_stream.join(data_ch, ['stream_id', 'game'])\
        .select('channel_id', 'stream_id', 'game', 'name',
                data_stream['viewers'].alias('watchings'),
                data_stream['time_frame'].alias('stream_starting_time_frame'),
                data_ch['views'].alias('channel_total_views'),
                data_ch['followers'].alias('channel_followers'),
                data_stream['created_at'].alias('stream_create_date'),
                data_ch['last_updated_at'].alias('channel_last_updated'),
                'broadcaster_language',
                data_ch['created_at'].alias('channel_created_date'),
                'mature', 'partner', 'average_fps','video_height').cache()

    cs_joint_table = cs_joint_table.repartition(40)
    cs_joint_table.cache()
    cs_joint_table.createOrReplaceTempView('cs_joint_table')



#--------------------------------------------Get the Viewer_distribution_by_date.---------------------------------------

    viewer_distribution_by_date = spark.sql(
        """
        SELECT stream_id, LOWER(game) AS game, name, MAX(watchings) AS max_audiences,
        MIN(watchings) AS min_audiences, stream_starting_time_frame, stream_create_date
        FROM cs_joint_table
        GROUP BY stream_id, game, stream_create_date, stream_starting_time_frame, name
        HAVING max_audiences > 1000
        ORDER BY stream_create_date DESC, max_audiences DESC
        """)

    viewer_distribution_by_date = viewer_distribution_by_date.repartition(40)
    viewer_distribution_by_date.cache()

    print('From stream_data, get the max and min viewers for each streamer in each day')
    print(viewer_distribution_by_date.show(20))

    viewer_distribution_by_date_output = viewer_distribution_by_date.toJSON().collect()
    filename = 'bigdata_' + 'viewer_distribution_by_date'
    with open(filename, 'w') as output:
        json.dump(viewer_distribution_by_date_output, output)
        output.close()
    print('file saved')
    viewer_distribution_by_date.createOrReplaceTempView('viewer_distribution_by_date')



#--------------------------------------------stream_viewer_count_by_timeframe-------------------------------------------

    stream_viewer_count_by_timeframe = spark.sql(
        """
        SELECT COUNT(DISTINCT stream_id) as total_streamer,
        SUM((max_audiences + min_audiences)/2) AS average_audiences,
        stream_starting_time_frame
        FROM viewer_distribution_by_date
        GROUP BY stream_starting_time_frame
        ORDER BY total_streamer DESC
        """)
    print('stream_viewer_count_by_timeframe')
    print(stream_viewer_count_by_timeframe.show(20))
    stream_viewer_count_by_timeframe_output = stream_viewer_count_by_timeframe.toJSON().collect()
    filename = 'bigdata_' + 'stream_viewer_count_by_timeframe'
    with open(filename, 'w') as output:
        json.dump(stream_viewer_count_by_timeframe_output, output)
        output.close()
    print('file saved')



#--------------------------------------------stream_viewer_count_by_date------------------------------------------------

    stream_viewer_count_by_date = spark.sql(
        """
        SELECT COUNT(DISTINCT stream_id) as total_streamer,
        SUM((max_audiences + min_audiences)/2) AS average_audiences,
        stream_create_date
        FROM viewer_distribution_by_date
        GROUP BY stream_create_date
        ORDER BY stream_create_date, total_streamer DESC
        """)
    print('stream_viewer_count_by_date')
    print(stream_viewer_count_by_date.show(20))
    stream_viewer_count_by_date_output = stream_viewer_count_by_date.toJSON().collect()
    filename = 'bigdata_' + 'stream_viewer_count_by_date'
    with open(filename, 'w') as output:
        json.dump(stream_viewer_count_by_date_output, output)
        output.close()
    print('file saved')



#--------------------------------------------stream_viewer_count_by_game_timeframe--------------------------------------

    stream_viewer_count_by_game_timeframe = spark.sql(
        """
        SELECT game, COUNT(DISTINCT stream_id) as total_streamer,
        SUM((max_audiences + min_audiences)/2) AS average_audiences,
        stream_starting_time_frame
        FROM viewer_distribution_by_date
        GROUP BY stream_starting_time_frame, game
        ORDER BY total_streamer DESC
        """)
    print('stream_viewer_count_by_game_timeframe')
    print(stream_viewer_count_by_game_timeframe.show(20))
    stream_viewer_count_by_game_timeframe_output = stream_viewer_count_by_game_timeframe.toJSON().collect()
    filename = 'bigdata_' + 'stream_viewer_count_by_game_timeframe'
    with open(filename, 'w') as output:
        json.dump(stream_viewer_count_by_game_timeframe_output, output)
        output.close()
    print('file saved')




#--------------------------------------------stream_viewer_count_by_game_date-------------------------------------------

    stream_viewer_count_by_game_date = spark.sql(
        """
        SELECT game, COUNT(DISTINCT stream_id) as total_streamer,
        SUM((max_audiences + min_audiences)/2) AS average_audiences,
        stream_create_date
        FROM viewer_distribution_by_date
        GROUP BY stream_create_date, game
        ORDER BY average_audiences DESC
        """)
    print('stream_viewer_count_by_game_date')
    print(stream_viewer_count_by_game_date.show(20))
    stream_viewer_count_by_game_date_output = stream_viewer_count_by_game_date.toJSON().collect()
    filename = 'bigdata_' + 'stream_viewer_count_by_game_date'
    with open(filename, 'w') as output:
        json.dump(stream_viewer_count_by_game_date_output, output)
        output.close()
    print('file saved')




#--------------------------------------------stream_viewer_count_by_game------------------------------------------------

    stream_viewer_count_by_game = spark.sql(
        """
        SELECT game, COUNT(DISTINCT stream_id) as total_streamer,
        SUM((max_audiences + min_audiences)/2) AS audiences
        FROM viewer_distribution_by_date
        GROUP BY game
        ORDER BY total_streamer DESC
        """)
    print('stream_viewer_count_by_game')
    print(stream_viewer_count_by_game.show(20))
    stream_viewer_count_by_game_output = stream_viewer_count_by_game.toJSON().collect()
    filename = 'bigdata_' + 'stream_viewer_count_by_game'
    with open(filename, 'w') as output:
        json.dump(stream_viewer_count_by_game_output, output)
        output.close()
    print('file saved')




if __name__ == '__main__':
    spark = SparkSession.builder.appName('clean data').getOrCreate()
    spark.sparkContext.setLogLevel('WARN')

    input1 = sys.argv[1]
    input2 = sys.argv[2]

    main(input1, input2)