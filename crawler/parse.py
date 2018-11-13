#
#  Author: Lil Data
#  Email: cxa25@sfu.ca
#  CMPT 732 Lab Final Project
#  Date: 11/13/2018
#
import sys
assert sys.version_info >= (3, 5) 

from pyspark.sql.types import StructType, StructField, BooleanType, StringType,\
    IntegerType, LongType, ArrayType
from pyspark.sql import SparkSession, functions as fn
import json
spark = SparkSession.builder.appName('parse twitch response').getOrCreate()
assert spark.version >= '2.3' 
spark.sparkContext.setLogLevel('WARN')
sc = spark.sparkContext


def main(inputs, output):
    df=spark.read.json(inputs)
    data = df.select(fn.explode('streams').alias('tmp')).select('tmp.*')
    data.printSchema()
    # data.show(10)
    # print(df.select('streams').rdd.collect())
    # new_df = spark.read.json(df.select('streams').rdd.map(lambda r: r.streams))
    # new_df.printSchema()

    # twitch_schema = StructType([ # commented-out fields won't be read
    #     StructField('total_streams', BooleanType(), True),
    #     types.StructField('stream', types.ArrayType(
    #         types.StringType()), False),
    #     # types.StructField('subreddit_id', types.StringType(), True),
    #     # types.StructField('ups', types.LongType(), True),
    #     #types.StructField('year', types.IntegerType(), False),
    #     #types.StructField('month', types.IntegerType(), False),
    # ])
    # df=spark.read.json(inputs)
    # df.createOrReplaceTempView('df')
    # data = spark.sql(
    #     """
    #         SELECT _total AS total from df
    #     """)
    # data.show(10)

    # input_data = sc.textFile(inputs).map(json.loads)
    # reddit = spark.read.json(inputs, schema=twitch_schema)
    # print(input_data.collect())
    # reddit.show(10)
    # input_data.map(json.dumps).saveAsTextFile(output)

    data.coalesce(1).write.json(output, mode='overwrite')

# root
#  |-- _id: long (nullable = true)
#  |-- _links: struct (nullable = true)
#  |    |-- self: string (nullable = true)
#  |-- average_fps: long (nullable = true)
#  |-- channel: struct (nullable = true)
#  |    |-- _id: long (nullable = true)
#  |    |-- _links: struct (nullable = true)
#  |    |    |-- chat: string (nullable = true)
#  |    |    |-- commercial: string (nullable = true)
#  |    |    |-- editors: string (nullable = true)
#  |    |    |-- features: string (nullable = true)
#  |    |    |-- follows: string (nullable = true)
#  |    |    |-- self: string (nullable = true)
#  |    |    |-- stream_key: string (nullable = true)
#  |    |    |-- subscriptions: string (nullable = true)
#  |    |    |-- teams: string (nullable = true)
#  |    |    |-- videos: string (nullable = true)
#  |    |-- background: string (nullable = true)
#  |    |-- banner: string (nullable = true)
#  |    |-- broadcaster_language: string (nullable = true)
#  |    |-- broadcaster_software: string (nullable = true)
#  |    |-- created_at: string (nullable = true)
#  |    |-- delay: string (nullable = true)
#  |    |-- display_name: string (nullable = true)
#  |    |-- followers: long (nullable = true)
#  |    |-- game: string (nullable = true)
#  |    |-- language: string (nullable = true)
#  |    |-- logo: string (nullable = true)
#  |    |-- mature: boolean (nullable = true)
#  |    |-- name: string (nullable = true)
#  |    |-- partner: boolean (nullable = true)
#  |    |-- profile_banner: string (nullable = true)
#  |    |-- profile_banner_background_color: string (nullable = true)
#  |    |-- status: string (nullable = true)
#  |    |-- updated_at: string (nullable = true)
#  |    |-- url: string (nullable = true)
#  |    |-- video_banner: string (nullable = true)
#  |    |-- views: long (nullable = true)
#  |-- created_at: string (nullable = true)
#  |-- delay: long (nullable = true)
#  |-- game: string (nullable = true)
#  |-- is_playlist: boolean (nullable = true)
#  |-- preview: struct (nullable = true)
#  |    |-- large: string (nullable = true)
#  |    |-- medium: string (nullable = true)
#  |    |-- small: string (nullable = true)
#  |    |-- template: string (nullable = true)
#  |-- stream_type: string (nullable = true)
#  |-- video_height: long (nullable = true)
#  |-- viewers: long (nullable = true)

if __name__ == '__main__':
    inputs = sys.argv[1] # input raw data
    output = sys.argv[2] # output path
    main(inputs, output)
