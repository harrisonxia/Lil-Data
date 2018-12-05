from pyspark.sql import SparkSession, functions, types
import sys
import json

def main():
	stream_df = spark.read.json('stream_cleanned')
	stream_df = stream_df.withColumn('Day', functions.dayofmonth('created_at'))

	result_dfs = []

	#--Number of streams in each time frame everyday
	stream_count_by_timeframe = stream_df.groupBy('Day', 'time_frame').agg(functions.countDistinct(
		'stream_id').alias('count'))
	result_dfs.append(stream_count_by_timeframe)

	#--Number of viewers in each time frame everyday
	stream_view_by_timeframe = stream_df.groupBy('Day', 'time_frame', 'stream_id').agg(
		functions.avg('viewers').alias('avg_viewers'))
	stream_view_by_timeframe = stream_view_by_timeframe.groupBy('Day', 'time_frame').agg(
		functions.sum('avg_viewers').alias('total_viewers'))
	result_dfs.append(stream_view_by_timeframe)

	#--Number of streams in each time frame throughout entire collecting period
	stream_count_all_days = stream_count_by_timeframe.groupBy('time_frame').agg(
		functions.sum('count').alias('total_count_through_all_days'))
	#--Number of viewers in each time frame throughout entire collecting period
	stream_view_all_days = stream_view_by_timeframe.groupBy('time_frame').agg(
		functions.sum('total_viewers').alias('total_viewers_through_all_days'))
	result_dfs.append(stream_count_all_days)
	result_dfs.append(stream_view_all_days)

	#--Trend of number of streams for each time frame
	stream_count_earlymorning = stream_count_by_timeframe.where(
		stream_count_by_timeframe.time_frame == 'Early Morning')
	stream_count_morning = stream_count_by_timeframe.where(
		stream_count_by_timeframe.time_frame == 'Morning')
	stream_count_noon = stream_count_by_timeframe.where(
		stream_count_by_timeframe.time_frame == 'Noon')
	stream_count_afternoon = stream_count_by_timeframe.where(
		stream_count_by_timeframe.time_frame == 'Afternoon')
	stream_count_evening = stream_count_by_timeframe.where(
		stream_count_by_timeframe.time_frame == 'Evening')
	stream_count_latenight = stream_count_by_timeframe.where(
		stream_count_by_timeframe.time_frame == 'Late Night')

	#--Trend of number of viewers for each time frame
	stream_view_earlymorning = stream_view_by_timeframe.where(
		stream_view_by_timeframe.time_frame == 'Early Morning')
	stream_view_morning = stream_view_by_timeframe.where(
		stream_view_by_timeframe.time_frame == 'Morning')
	stream_view_noon = stream_view_by_timeframe.where(
		stream_view_by_timeframe.time_frame == 'Noon')
	stream_view_afternoon = stream_view_by_timeframe.where(
		stream_view_by_timeframe.time_frame == 'Afternoon')
	stream_view_evening = stream_view_by_timeframe.where(
		stream_view_by_timeframe.time_frame == 'Evening')
	stream_view_latenight = stream_view_by_timeframe.where(
		stream_view_by_timeframe.time_frame == 'Late Night')

	result_dfs += [stream_view_morning, stream_count_earlymorning, stream_view_latenight, stream_view_evening
					, stream_view_afternoon, stream_view_noon, stream_count_earlymorning,
					stream_count_latenight, stream_count_evening, stream_count_afternoon, 
					stream_count_noon, stream_count_morning]

	print(result_dfs)


	for i in range(len(result_dfs)):
		rdf = result_dfs[i].toJSON().collect()
		filename = 'result_btos_' + str(i)
		with open(filename, 'w') as output:
			json.dump(rdf, output)
			output.close()




if __name__ == '__main__':
	spark = SparkSession.builder.appName('Best Time to Stream').getOrCreate()
	spark.sparkContext.setLogLevel('WARN')
	main()