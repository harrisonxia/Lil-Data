from pyspark.sql import SparkSession, functions, types
from pyspark.sql.types import StringType, LongType, IntegerType, BooleanType, FloatType, DateType
import sys
import json
import datetime as dt

import matplotlib.pyplot as plt

morningStart = dt.time(5, 0, 1)
morningEnd = dt.time(11, 0, 0)
noonStart = dt.time(11, 0, 1)
noonEnd = dt.time(14, 0, 0)
afternoonStart = dt.time(14, 0, 1)
afternoonEnd = dt.time(18, 0, 0)
eveningStart = dt.time(18, 0, 1)
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
	if morningStart <= time <= morningEnd:
		timeframe = "morning"
	elif noonStart <= time <= noonEnd:
		timeframe = "Noon"
	elif afternoonStart <= time <= afternoonEnd:
		timeframe = "Afternoon"
	elif eveningStart <= time <= eveningEnd:
		timeframe =  "Evening"
	else:
		timeframe =  "Late Night"

	return timeframe

def timeToFrame(dateStr):
	date = dt.datetime.strptime(dateStr, '%Y-%m-%dT%H:%M:%SZ')
	time = date.time()

	return getTimeFrame(time)

def main(output):
    stream_sch, channel_sch = createSchema()

    # data_s = spark.read.json('stream_base/part*', schema = stream_sch)
    # data_c = spark.read.json('channel_base/part*', schema = channel_sch)
    
    convertTime = functions.udf(timeToFrame)

    data_s = spark.read.json('stream_info.json', schema = stream_sch)
    data_c = spark.read.json('channel_info.json', schema = channel_sch).cache()
    
	data_s = data_s.withColumn('time_frame', convertTime(data_s.created_at)).cache()

    data_s.createOrReplaceTempView('data_s')
    data_c.createOrReplaceTempView('data_c')

    game_count_by_time = data_s.groupBy('time_frame', 'game_name').count()
	game_count_by_time = game_count_by_time.orderBy(game_count_by_time['count'].desc())
    
    view_count_by_time = data_s.groupBy('time_frame', 'game_name').agg(functions.sum('viewers').alias('total_view'))
    view_count_by_time = view_count_by_time.orderBy(view_count_by_time['total_view'].desc())
    
	game_count_by_time.coalesce(1).write.json('game_count_by_time', mode = 'overwrite')
    view_count_by_time.coalesce(1).write.json('view_count_by_time', mode = 'overwrite')


    view_num_by_game = data_c.groupby(data_c['game']).agg(functions.sum(data_c['views']),functions.sum(data_c['followers']))

    view_num_by_streamer = data_c\
        .select('stream_id','channel_id','game','name','views','followers','created_at','updated_at','partner')\
        .orderBy(functions.desc('views'),'game')

    print(view_num_by_streamer.show(5))

    viewcount_by_game = view_num_by_game\
        .select('game', view_num_by_game['sum(views)'].alias('total_views'), view_num_by_game['sum(followers)'].alias('total_followers'))\
        .orderBy(functions.desc('total_views'))
    print(viewcount_by_game.show(5))

    yuyan = spark.sql(
        """SELECT broadcaster_language, game, SUM(views) AS total_views
        FROM data_c
        WHERE broadcaster_language != 'en'
        GROUP BY broadcaster_language, game
        ORDER BY total_views DESC
        """
            )
    yuyan.createOrReplaceTempView('yuyan')
    print(yuyan.show(5))

    yuyan_by_game = spark.sql(
        """SELECT broadcaster_language, game, count(*) AS total_streamer
        FROM data_c
        GROUP BY broadcaster_language, game
        ORDER BY total_streamer DESC
        """
            )
    yuyan.createOrReplaceTempView('yuyan_by_game')
    print(yuyan_by_game.show(5))


# -------------------------ow jonning the 2 tables---------------------------------------
    # joint_df = t_max.join(t_min, (t_max.stationmax == t_min.stationmin) & (t_max.date == t_min.date), 'inner')


    #put WHERE above ORDER BY ,stream.game is dropped since some streamers are playing games different than what are shown in stream.game
    cs_joint_table = spark.sql(
        """
        SELECT s.stream_id AS stream_id, c.game AS playing, c.name AS name, s.viewers AS watchings, c.views AS views,
        c.followers AS followers, c.updated_at AS channel_last_updated, c.broadcaster_language, c.language, 
        c.created_at AS channel_created_date, s.created_at AS stream_created_date, c.display_name, c.status,
        c.mature, c.partner, s.average_fps, s.delay, s.video_height, c.broadcaster_software
        FROM data_c AS c JOIN data_s AS s
        ON s.stream_id = c.stream_id
        ORDER BY watchings DESC
        """).cache()

    cs_joint_table.createOrReplaceTempView('cs_joint_table')


    cs_joint_table.coalesce(1).write.csv(output, mode='overwrite')
    #cs_joint_table.coalesce(1).write.json(output, mode='overwrite')


if __name__ == '__main__':
    spark = SparkSession.builder.appName('clean data').getOrCreate()
    spark.sparkContext.setLogLevel('WARN')

    output = sys.argv[1]

    main(output)
