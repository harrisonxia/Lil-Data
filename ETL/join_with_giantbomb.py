from pyspark.sql import SparkSession, functions, types
import sys
import json

def join():
	stream_df = spark.read.json('stream_cleanned')
	giant_df = spark.read.json('game_info_base')

	stream_df = stream_df.withColumn('gen_name', functions.lower(stream_df.game))
	game_info = stream_df.groupBy('gen_name').count().cache()

	real_game_info = game_info.join(giant_df, game_info.gen_name == functions.lower(giant_df.name), 'left')

	real_game_info.coalesce(1).write.json('real_game_info', mode = 'overwrite')
  
if __name__ == '__main__':
	spark = SparkSession.builder.appName('join data').getOrCreate()
	spark.sparkContext.setLogLevel('WARN')
	join()
