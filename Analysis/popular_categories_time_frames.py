from pyspark.sql import SparkSession, functions, types
from pyspark.sql.types import StringType, LongType, IntegerType, BooleanType, FloatType, DateType
import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+

import json
import datetime as dt
from pyspark.sql.types import DateType

spark = SparkSession.builder.appName('popular_categories_time_frames').getOrCreate()
assert spark.version >= '2.3' # make sure we have Spark 2.3+
spark.sparkContext.setLogLevel('WARN')

import matplotlib.pyplot as plt

from pyspark.sql.functions import explode

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

    convertTime = functions.udf(timeToFrame)
    convertDate = functions.udf(timeToDate, DateType())


    data_stream = spark.read.json('stream_cleanned', schema = stream_sch)
    data_stream = data_stream.withColumn('time_frame', convertTime(data_stream.created_at))
    data_stream = data_stream.withColumn('date', convertDate(data_stream.created_at)).cache()

    data_channel = spark.read.json('channel_cleanned', schema = channel_sch).cache()
    data_game = spark.read.json('real_game_info').cache()
    data_genre = spark.read.json('game_genre').cache()

    data_stream.createOrReplaceTempView('data_s')
    data_channel.createOrReplaceTempView('data_c')
    data_game.createOrReplaceTempView('data_g')
    data_genre.createOrReplaceTempView('data_genre')


    #joining stream info with game info and categories
    game_with_channel = spark.sql(
        """SELECT s.stream_id, s.game, s.viewers, s.time_frame, g.guid, genre.genres
            FROM data_s s
            JOIN data_g g on s.game = g.gen_name
            JOIN data_genre genre on g.guid = genre.guid
        """
            )

    #to flatten the categories
    games_with_genres = game_with_channel.select(
        game_with_channel['game'], 
        game_with_channel['viewers'], 
        game_with_channel['time_frame'], 
        game_with_channel['guid'], 
        explode(game_with_channel['genres']).alias('genres'))

    games_with_genres.createOrReplaceTempView('games_genres')

    #grouping by time frames and categories
    spark.sql(
        """SELECT time_frame, genres, SUM(viewers) AS viewers
        FROM games_genres
        GROUP BY genres, time_frame
        ORDER BY viewers DESC
        """
            ).createOrReplaceTempView('categories_time_frame_viewers')

    #getting most popular category for time frames
    popular_categories_time_frames = spark.sql(
        """SELECT c.time_frame, c.genres, c.viewers
        FROM (
        SELECT g.time_frame, MAX(g.viewers) as max_viewers from categories_time_frame_viewers g
        GROUP BY g.time_frame
        ) as x INNER JOIN categories_time_frame_viewers as c on c.time_frame = x.time_frame and c.viewers = x.max_viewers        
        """
            )
    #popular_categories_time_stream.show()
    popular_categories_time_frames.coalesce(1).write.json('popular_categories_time_frames', mode = 'overwrite')


if __name__ == '__main__':
    main()



