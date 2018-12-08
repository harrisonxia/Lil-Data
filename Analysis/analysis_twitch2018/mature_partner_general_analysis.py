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



#-------partnership and average streaming fps and current audiences(num of people watching) by game and streamer--------


    each_partner = spark.sql(
        """
        SELECT channel_id, LOWER(game) as game, average_fps, video_height,
        MAX(channel_total_views) AS channel_total_views,
        AVG(channel_followers) AS channel_followers, partner, name, AVG(video_height)
        FROM cs_joint_table
        GROUP BY channel_id, game, partner, name, average_fps, video_height
        """).cache()

    each_partner.createOrReplaceTempView('each_partner')


    partner = spark.sql(
        """
        SELECT game, partner, COUNT(DISTINCT name) AS number_of_steamer,
        AVG(average_fps) AS average_fps,
        AVG(video_height) AS average_video_height
        FROM each_partner
        GROUP BY partner, game
        HAVING number_of_steamer > 10
        ORDER BY game DESC
        """)

    print('partnership and average streaming fps and current audiences(num of people watching) by game and streamer')
    print(partner.show(20))

    partner_output = partner.toJSON().collect()
    filename = 'bigdata1_' + 'partner'
    with open(filename, 'w') as output:
        json.dump(partner_output, output)
        output.close()
    print('file saved')

#---------------------------------------------mature vs non-mature contents--------------------------------------------

    each_mature = spark.sql(
        """
        SELECT channel_id, mature, LOWER(game) as game, name,
        MAX(channel_total_views) AS channel_total_views,
        AVG(channel_followers) AS channel_followers
        FROM cs_joint_table
        GROUP BY channel_id, game, name, mature
        """).cache()

    each_mature.createOrReplaceTempView('each_mature')

    print('mature vs non-mature')
    mature = spark.sql(
        """
        SELECT game, mature, COUNT(name), SUM(channel_total_views), SUM(channel_followers)
        FROM each_mature
        GROUP BY mature, game
        ORDER BY game DESC
        """)
    print(mature.show(20))

    mature_output = mature.toJSON().collect()
    filename = 'bigdata1_' + 'mature'
    with open(filename, 'w') as output:
        json.dump(mature_output, output)
        output.close()
    print('file saved')


    mature_tal = spark.sql(
        """
        SELECT mature, COUNT(name) AS total_streamers
        FROM each_mature
        GROUP BY mature
        ORDER BY total_streamers DESC
        """)
    print('mature_total')
    print(mature_tal.show(3))



    mature_total = spark.sql(
        """
        SELECT mature, COUNT(name), SUM(channel_total_views), SUM(channel_followers)
        FROM each_mature
        GROUP BY mature
        """)
    print('mature_total')
    print(mature_total.show(3))

    mature_total_output = mature_total.toJSON().collect()
    filename = 'bigdata_' + 'mature_total'
    with open(filename, 'w') as output:
        json.dump(mature_total_output, output)
        output.close()
    print('file saved')


if __name__ == '__main__':
    spark = SparkSession.builder.appName('clean data').getOrCreate()
    spark.sparkContext.setLogLevel('WARN')

    input1 = sys.argv[1]
    input2 = sys.argv[2]

    main(input1, input2)

