from pyspark.sql import SparkSession, functions, types
import sys
import json

def most_popular_category(game, channel, stream):
	game_df = spark.read.json(game)
	channel_df = spark.read.json(channel)
	stream_df = spark.read.json(stream)

	game_gern_df = spark.read.json('/user/rishengw/game_genre')
	game_gern_df = game_gern_df.select('guid', functions.explode('genres').alias('genre'))
	functions.broadcast(game_gern_df)

	real_game_df = game_df.join(game_gern_df, 'guid', 'right')
	real_game_df = real_game_df.select('gen_name', 'genre', 'count', 'number_of_user_reviews').cache()
	functions.broadcast(real_game_df)

	#---get 20 most reviewed game/streamed game---
	game_group = real_game_df.groupBy('genre')
	top_20_game_cat_re = game_group.agg(functions.sum('number_of_user_reviews').alias(
		'total_reviews'))
	#by reviewers
	top_20_game_cat_re = top_20_game_cat_re.orderBy(top_20_game_cat_re.total_reviews.desc()).limit(20)

	top_20_game_cat_count = game_group.agg(functions.sum('count').alias('total_counts'))
	#by total streamers
	top_20_game_cat_count = top_20_game_cat_count.orderBy(top_20_game_cat_count.total_counts.desc()).limit(20)


	game_selected_df = real_game_df.select('gen_name', 'genre')
	#---get 20 most followed channel with that game---
	avg_follower_by_id = channel_df.groupBy('channel_id', 'game').agg(
		functions.avg('followers').alias('avg_followers'))
	avg_follower_by_id = avg_follower_by_id.groupBy('game').agg(
		functions.sum('avg_followers').alias('sum_followers')).cache()


	game_with_channel = avg_follower_by_id.join(
		game_selected_df, functions.lower(avg_follower_by_id.game) == game_selected_df.gen_name)
	top_20_game_channel = game_with_channel.groupBy('genre').agg(functions.sum('sum_followers').alias(
		'total_followers'))
	top_20_game_channel = top_20_game_channel.orderBy(
		top_20_game_channel.total_followers.desc()).limit(20)

	#---get 20 most viewed stream with that game---

	#A stream could appears multiple times in the table, 
	#because we grab the data per half an hour and
	#the stream just kept broadcasting.
	#So we treat the peek viewers as final number of viewers for a stream
	view_count_by_id = stream_df.groupBy(
		'stream_id', 'game').agg(functions.max('viewers').alias('max_viewrs'))
	#Then add up number of viewers for the same game
	view_count_by_id = view_count_by_id.groupBy('game').agg(
		functions.sum('max_viewrs').alias('sum_viewers')).cache()

	game_with_stream = view_count_by_id.join(
		game_selected_df, functions.lower(view_count_by_id.game) == game_selected_df.gen_name).cache()
	top_20_game_stream = game_with_stream.groupBy('genre').agg(
		functions.sum('sum_viewers').alias('total_viewers'))
	top_20_game_stream = top_20_game_stream.orderBy(
		top_20_game_stream.total_viewers.desc()).limit(20)

	top_20_game_cat_re.coalesce(1).write.json('top20gamecatre', mode = 'overwrite')
	top_20_game_cat_count.coalesce(1).write.json('top20gamecatcount', mode = 'overwrite')
	top_20_game_channel.coalesce(1).write.json('top20gamechannel', mode = 'overwrite')
	top_20_game_stream.coalesce(1).write.json('top20gamestream', mode = 'overwrite')



if __name__ == '__main__':
	spark = SparkSession.builder.appName('most_popular_category').getOrCreate()
	spark.sparkContext.setLogLevel('WARN')
	
	game = sys.argv[1]
	channel = sys.argv[2]
	stream = sys.argv[3]
	most_popular_category(game, channel, stream)
