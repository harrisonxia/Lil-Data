from pyspark.sql import SparkSession, functions, types
from pyspark.sql.types import StringType, LongType, IntegerType, BooleanType, FloatType, DateType
import sys
import json

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

def main():
	stream_sch, channel_sch = createSchema()

	data_s = spark.read.json('stream_base/part*', schema = stream_sch)
	data_c = spark.read.json('channel_base/part*', schema = channel_sch)



if __name__ == '__main__':
	spark = SparkSession.builder.appName('clean data').getOrCreate()
	spark.sparkContext.setLogLevel('WARN')
	main()