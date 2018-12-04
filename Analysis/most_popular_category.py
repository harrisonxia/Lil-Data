from pyspark.sql import SparkSession, functions, types
import sys
import json

def most_popular_category():
	game_df = spark.read.json('real_game_info').cache()
	channel_df = spark.read.json('channel_cleanned').cache()
	stream_df = spark.read.json('stream_cleanned').cache()

	game_with_channel = channel_df.join(game_df, functions.lower(channel_df.game) == game_df.gen_name)

	#get 20 most reviewed game/streamed game
	game_group = game_df.groupBy('deck')
	top_20_game_cat_re = game_group.agg(functions.sum('number_of_user_reviews').alias(
		'total_reviews'))
	#by reviewers
	top_20_game_cat_re = top_20_game_cat_re.orderBy(top_20_game_cat_re.total_reviews.desc()).limit(20)

	top_20_game_cat_count = game_group.agg(functions.sum('count').alias('total_counts'))
	#by total streamers
	top_20_game_cat_count = top_20_game_cat_count.orderBy(top_20_game_cat_count.total_counts.desc()).limit(20)

	#get 20 most followed channel with that game
	top_20_game_channel = game_with_channel.groupBy('deck').agg(functions.sum('followers').alias(
		'total_followers'))
	top_20_game_channel = top_20_game_channel.orderBy(top_20_game_channel.total_followers.desc()).limit(20)

	#get 20 most viewed stream with that game
	view_count_by_id = stream_df.groupBy('stream_id', 'game').agg(functions.max('viewers').alias('max_viewrs'))
	view_count_by_id = view_count_by_id.groupBy('game').agg(functions.sum('max_viewrs').alias('sum_viewers')).cache()
	game_selected_df = game_df.select('gen_name', 'deck')
	game_with_stream = view_count_by_id.join(
		game_selected_df, functions.lower(view_count_by_id.game) == game_selected_df.gen_name).cache()
	top_20_game_stream = game_with_stream.groupBy('deck').agg(functions.sum('sum_viewers').alias('total_viewers'))
	top_20_game_stream = top_20_game_stream.orderBy(top_20_game_stream.total_viewers.desc()).limit(20)

	top_20_game_cat_re.coalesce(1).write.json('top20gamecatre', mode = 'overwrite')
	top_20_game_cat_count.coalesce(1).write.json('top20gamecatcount', mode = 'overwrite')
	top_20_game_channel.coalesce(1).write.json('top20gamechannel', mode = 'overwrite')
	top_20_game_stream.coalesce(1).write.json('top20gamestream', mode = 'overwrite')



if __name__ == '__main__':
	spark = SparkSession.builder.appName('most_popular_category').getOrCreate()
	spark.sparkContext.setLogLevel('WARN')
	most_popular_category()