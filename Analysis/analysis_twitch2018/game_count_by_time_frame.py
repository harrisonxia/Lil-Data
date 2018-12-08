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


def main(input1):

    stream_creation_date = functions.udf(getDate)
    data_s = spark.read.json(input1)
    data_s = data_s.withColumn('stream_create_date',stream_creation_date(data_s.created_at))
    data_s.createOrReplaceTempView('data_s')

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

    data_stream = data_s.repartition(40)

#------------------------------------Counting games by time frame---------------------------------------------

    game_count_by_time = data_stream.groupBy('time_frame', 'game').count()
    game_count_by_time = game_count_by_time.orderBy(game_count_by_time['count'].desc())
    print(game_count_by_time.show(20))


    game_count_by_time_output = game_count_by_time.toJSON().collect()
    filename = 'bigdata_' + 'game_count_by_time'
    with open(filename, 'w') as output:
        json.dump(game_count_by_time_output, output)
        output.close()



if __name__ == '__main__':
    spark = SparkSession.builder.appName('game_count_by_time').getOrCreate()
    spark.sparkContext.setLogLevel('WARN')
    input1 = sys.argv[1]

    main(input1)
