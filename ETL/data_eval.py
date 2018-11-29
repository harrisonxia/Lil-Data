
from pyspark.sql import SparkSession, functions, types
from pyspark.sql.types import StringType, LongType, IntegerType, BooleanType, FloatType, DateType
import sys
import json
import datetime as dt

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


def main():

	stream_sch, channel_sch = createSchema()

	convertTime = functions.udf(timeToFrame)

	data_s = spark.read.json('stream_base', schema = stream_sch).cache()
	data_c = spark.read.json('channel_base', schema = channel_sch).cache()

	data_s = data_s.withColumn('time_frame', convertTime(data_s.created_at))
	game_df = data_s.select('game').distinct()

	#game_count = data_s.groupBy('game_name').count()
	#game_count = game_count.orderBy(game_count['count'].desc())
	#view_count = data_s.groupBy('game_name').agg(functions.sum('viewers').alias('sum'))
	#view_count = view_count.orderBy(view_count.sum.desc())

	#game_count_by_time = data_s.groupBy('time_frame', 'game_name').count()
	#game_count_by_time = game_count_by_time.orderBy(game_count_by_time['count'].desc())
	#game_count_by_time.coalesce(1).write.json('game_count_by_time', mode = 'overwrite')

	data_s.coalesce(10).write.json('stream_cleanned', mode = 'overwrite')
	data_c.coalesce(10).write.json('channel_cleanned', mode = 'overwrite')
	game_df.coalesce(10).write.json('game_cleanned', mode = 'overwrite')


if __name__ == '__main__':
	spark = SparkSession.builder.appName('reconstruct data').getOrCreate()
	spark.sparkContext.setLogLevel('WARN')
	main()