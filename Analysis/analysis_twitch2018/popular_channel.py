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




#---------------------------------------------most_popular_channel_by_follower------------------------------------------

    most_popular_channel_by_follower = cs_joint_table.groupBy('channel_id', 'name', 'broadcaster_language'
                                                              , 'partner', 'mature').agg(
        functions.max('channel_total_views').alias('channel_total_views'),
        functions.max('channel_followers').alias('total_followers')
    ).select('channel_id', 'name', 'broadcaster_language', 'channel_total_views',
             'total_followers', 'partner', 'mature')

    most_popular_channel_by_follower = most_popular_channel_by_follower.where(
        most_popular_channel_by_follower.total_followers > 1100000
    ).orderBy(most_popular_channel_by_follower['total_followers'].desc())

    most_popular_channel_by_follower.show(20)

    most_popular_channel_by_follower_output = most_popular_channel_by_follower.toJSON().collect()
    filename = 'bigdata1_' + 'most_popular_channel_by_follower'
    with open(filename, 'w') as output:
        json.dump(most_popular_channel_by_follower_output, output)
        output.close()

#----------------------------------popular mature channel by total follower count---------------------------------------

    most_popular_mature_channel_by_follower = spark.sql(
        """
        SELECT channel_id, name, broadcaster_language,
        MAX(channel_total_views), MAX(channel_followers) AS total_followers, partner, mature
        FROM cs_joint_table
        WHERE mature = true
        GROUP BY channel_id, name, broadcaster_language, partner, mature
        HAVING total_followers > 200
        ORDER BY total_followers DESC
        """)

    print(most_popular_mature_channel_by_follower.show(20))

    most_popular_mature_channel_by_follower_output = most_popular_mature_channel_by_follower.toJSON().collect()
    filename = 'bigdata1_' + 'most_popular_mature_channel_by_follower'
    with open(filename, 'w') as output:
        json.dump(most_popular_mature_channel_by_follower_output, output)
        output.close()


#--------------------------popular none twitch partner(can't make money for their contents)-----------------------------
    most_popular_none_partner_channel_by_follower = spark.sql(
        """
        SELECT channel_id, name, broadcaster_language,
        MAX(channel_total_views), MAX(channel_followers) AS total_followers, partner, mature
        FROM cs_joint_table
        WHERE partner = false
        GROUP BY channel_id, name, broadcaster_language, partner,mature
        HAVING total_followers > 20000
        ORDER BY total_followers DESC
        """)

    print(most_popular_none_partner_channel_by_follower.show(20))

    most_popular_none_partner_channel_by_follower_output = \
        most_popular_none_partner_channel_by_follower.toJSON().collect()

    filename = 'bigdata1_' + 'most_popular_none_partner_channel_by_follower'
    with open(filename, 'w') as output:
        json.dump(most_popular_none_partner_channel_by_follower_output, output)
        output.close()




if __name__ == '__main__':
    spark = SparkSession.builder.appName('clean data').getOrCreate()
    spark.sparkContext.setLogLevel('WARN')

    input1 = sys.argv[1]
    input2 = sys.argv[2]

    main(input1, input2)