from pyspark.sql import SparkSession, functions, types
import sys
import json

def most_popular_category():
	game_df = spark.read.json('real_game_info')
	game_df = game_df.where(game_df['gen_name'] != '')
	game_df = game_df.orderBy(game_df['count'].desc()).select('gen_name', 'count', 'guid').limit(21)
	
	game_gern_df = spark.read.json('game_genre')
	game_gern_df = game_gern_df.select('guid', functions.explode('genres').alias('genre'))

	real_game_df = game_df.join(game_gern_df, 'guid').select('gen_name', 'count', 'genre')
	real_game_df = real_game_df.orderBy(real_game_df['count'].desc())
	
	real_game_df.coalesce(1).write.json('top20game_with_cat', mode = 'overwrite')



if __name__ == '__main__':
	spark = SparkSession.builder.appName('most_popular_category').getOrCreate()
	spark.sparkContext.setLogLevel('WARN')
	most_popular_category()
