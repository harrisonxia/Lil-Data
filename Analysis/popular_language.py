from pyspark.sql import SparkSession, functions, types
from pyspark.sql.types import StringType, LongType, IntegerType, BooleanType, FloatType, DateType
import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+

import json
import datetime as dt
from pyspark.sql.types import DateType

spark = SparkSession.builder.appName('data analysis').getOrCreate()
assert spark.version >= '2.3' # make sure we have Spark 2.3+
spark.sparkContext.setLogLevel('WARN')

import matplotlib.pyplot as plt

earlymorningStart = dt.time(3,0,1)
earlymorningEnd = dt.time(7,0,0)
morningStart = dt.time(7, 0, 1)
morningEnd = dt.time(11, 0, 0)
noonStart = dt.time(11, 0, 1)
noonEnd = dt.time(15, 0, 0)
afternoonStart = dt.time(15, 0, 1)
afternoonEnd = dt.time(19, 0, 0)
eveningStart = dt.time(19, 0, 1)
eveningEnd = dt.time(23, 0, 0)


def createSchema():
    stream_sch = types.StructType([
        types.StructField('stream_id', StringType(), True),
        types.StructField('game', StringType(), True),
        types.StructField('viewers', LongType(), True),
        types.StructField('video_height', StringType(), True),
        types.StructField('average_fps', FloatType(), True),
        types.StructField('delay', IntegerType(), True),
        types.StructField('created_at', StringType(), True),
    ])

    channel_sch = types.StructType([
        types.StructField('stream_id', StringType(), True),
        types.StructField('channel_id', StringType(), True),
        types.StructField('display_name', StringType(), True),
        types.StructField('name', StringType(), True),
        types.StructField('game', StringType(), True),
        types.StructField('views', LongType(), True),
        types.StructField('followers', LongType(), True),
        types.StructField('status', StringType(), True),
        types.StructField('broadcaster_language', StringType(), True),
        types.StructField('language', StringType(), True),
        types.StructField('broadcaster_software', StringType(), True),
        types.StructField('created_at', StringType(), True),
        types.StructField('updated_at', StringType(), True),
        types.StructField('mature', BooleanType(), True),
        types.StructField('partner', BooleanType(), True),
    ])

    return [stream_sch, channel_sch]

def getTimeFrame(time):
    if earlymorningStart <= time <= earlymorningEnd:
        timeframe = "Early Morning"
    elif morningStart <= time <= morningEnd:
        timeframe = "Morning"
    elif noonStart <= time <= noonEnd:
        timeframe = "Noon"
    elif afternoonStart <= time <= afternoonEnd:
        timeframe = "Afternoon"
    elif eveningStart <= time <= eveningEnd:
        timeframe = "Evening"
    else:
        timeframe = "Late Night"

    return timeframe

def timeToFrame(dateStr):
    date = dt.datetime.strptime(dateStr, '%Y-%m-%dT%H:%M:%SZ')
    time = date.time()

    return getTimeFrame(time)

def timeToDate(dateStr):
    date = dt.datetime.strptime(dateStr, '%Y-%m-%dT%H:%M:%SZ')
    time = date.date()

    return time

def main():
    stream_sch, channel_sch = createSchema()

    # data_s = spark.read.json('stream_base/part*', schema = stream_sch)
    # data_c = spark.read.json('channel_base/part*', schema = channel_sch)

    convertTime = functions.udf(timeToFrame)
    convertDate = functions.udf(timeToDate, DateType())

    #data = spark.read.json('input', schema = stream_sch)

    data_stream = spark.read.json('stream_cleanned', schema = stream_sch)
    data_channel = spark.read.json('channel_cleanned', schema = channel_sch)
    data_stream = data_stream.withColumn('time_frame', convertTime(data_stream.created_at)).cache()
    data_stream = data_stream.withColumn('date', convertDate(data_stream.created_at)).cache()

    data_stream.createOrReplaceTempView('data_s')

    data_channel.createOrReplaceTempView('data_c')

    #data_stream.show()

    #data_channel.show()
    '''

    popular_languages = data_channel\
        .select('language', 'sum(language)',
                )\
        .orderBy(functions.desc('language_count'))
    popular_languages.show()
    '''

    #----1
    #most popular languages on twitch
    popular_languages = spark.sql(
        """SELECT language, COUNT(channel_id) AS numberOfChannels
        FROM data_c
        GROUP BY language
        ORDER BY numberOfChannels DESC
        """
            )
    #popular_languages.show()
    popular_languages.createOrReplaceTempView('popular_languages')

    #games for most popular language (to change)
    popular_language_games = spark.sql(
        """SELECT game
        FROM data_c
        WHERE language in 
            (SELECT FIRST(language)
            FROM popular_languages
            )
        """
            )
    #popular_language_games.show()

    #number of viewers for each language
    popular_language_viewers = spark.sql(
        """SELECT c.language, sum(s.viewers) as numberOfViewers
        FROM data_c c
        JOIN data_s s on c.stream_id = s.stream_id
        
        GROUP BY c.language
        """
            )
    #popular_language_viewers.show()

    popular_languages.coalesce(1).write.json('popular_languages', mode = 'overwrite')
    popular_language_games.coalesce(1).write.json('popular_language_games', mode = 'overwrite')
    popular_language_viewers.coalesce(1).write.json('popular_language_viewers', mode = 'overwrite')



if __name__ == '__main__':
    #output = sys.argv[1]
    main()



