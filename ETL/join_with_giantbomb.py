from pyspark.sql import SparkSession, functions, types
import sys
import json

def join(path):
	game_info_df = spark.read.json(path + 'game_info_base')
	game_df = spark.read.json(path + 'game_cleanned')

	real_game_df = game_df.join(game_info_df, functions.lower(game_df.game) == functions.lower(game_info_df.name), 'left')
	real_game_df.coalesce(1).write.json('real_game_info', mode = 'overwrite')
  
  
if __name__ == '__main__':
	spark = SparkSession.builder.appName('join data').getOrCreate()
	spark.sparkContext.setLogLevel('WARN')

	path = sys.argv[1]
	join(path)
