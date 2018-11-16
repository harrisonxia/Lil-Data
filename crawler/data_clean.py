from pyspark.sql import SparkSession, functions, types
import sys
import json

def main():
	df = spark.read.json('all-2018-11-08-11-55-01.txt')
	data = df.select(functions.explode('streams').alias('streams_info')).select('streams_info.*')
	data_s = data.select(
		data['_id'].alias('stream_id'), data['game'], data['viewers'], data['video_height'],
		data['average_fps'], data['delay'], data['created_at'])
	data_c = data.select(data['_id'].alias('stream_id'), data['channel._id'].alias('channel_id'), 
		'channel.display_name', 'channel.name', 'channel.game', 'channel.views', 'channel.followers',
		'channel.status', 'channel.broadcaster_language', 'channel.language', 'channel.broadcaster_software',
		'channel.created_at', 'channel.updated_at', 'channel.mature', 'channel.partner')

	data_s.coalesce(1).write.json('stream_base', mode = 'overwrite')
	data_c.coalesce(1).write.json('channel_base', mode = 'overwrite')




if __name__ == '__main__':
	spark = SparkSession.builder.appName('clean data').getOrCreate()
	spark.sparkContext.setLogLevel('WARN')
	main()