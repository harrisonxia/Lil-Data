from pyspark.sql import SparkSession, functions, types
import sys
import json

def main(filename):
	game_df = spark.read.json(filename, multiLine = True)
	game_df = game_df.select(functions.explode('results').alias('game_info')).select('game_info.*')
	game_df = game_df.select('guid', 'aliases', 'deck', 'description', 'name', 'number_of_user_reviews',
		'original_release_date')

	game_df.coalesce(1).write.json('game_info_base', mode = 'overwrite')
 

if __name__ == '__main__':
  spark = SparkSession.builder.appName('clean data').getOrCreate()
	spark.sparkContext.setLogLevel('WARN')

	filename = sys.argv[1]
	main(filename)
