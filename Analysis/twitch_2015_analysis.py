from pyspark.sql import SparkSession, functions, types
from pyspark import SparkConf, SparkContext

from pyspark.sql.types import StringType, LongType, IntegerType, BooleanType, FloatType, DateType
import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
import re


import json
import datetime as dt
from pyspark.sql.types import DateType
from pyspark.sql.functions import date_format, desc, col
conf = SparkConf().setAppName('twitch')
spark = SparkSession.builder.appName('stream by weekdays').getOrCreate()
sc = spark.sparkContext
assert spark.version >= '2.3' # make sure we have Spark 2.3+
spark.sparkContext.setLogLevel('WARN')

import matplotlib.pyplot as plt

from pyspark.sql.functions import explode

def main():
    twitch_2015_schema = types.StructType([
        types.StructField('stream_id', types.StringType()),
        types.StructField('current_views', types.IntegerType()),
        types.StructField('created_at', types.DateType()),
        types.StructField('game', types.StringType()),
        types.StructField('broadcaster_id', types.StringType()),
        types.StructField('broadcaster_name', types.StringType()),
        types.StructField('delay_setting', types.IntegerType()),
        types.StructField('followers', types.IntegerType()),
        types.StructField('partner', types.IntegerType()),
        types.StructField('broadcaster_language', types.StringType()),
        types.StructField('views', types.IntegerType()),
        types.StructField('language', types.StringType()),
        types.StructField('broadcaster_created_time', types.DateType()),
        types.StructField('playback_bitrate', types.FloatType()),
        types.StructField('source_resolution', types.StringType()),
        types.StructField('temp', types.StringType()),
    ])

    data_stream = spark.read.json('stream_cleanned')
    
    #data_channel = spark.read.json('channel_cleanned')
    pattern = re.compile("\t+")
    #data_2015 = sc.textFile("twitch_2015")

    data_2015 = sc.textFile('/user/chengxil/twitch_2015/')
    data_proccessed = data_2015.map(lambda x: pattern.split(x))
    df = spark.createDataFrame(data_proccessed, twitch_2015_schema)

    data_stream.createOrReplaceTempView('data_s')
    
    df.cache()
    df.createOrReplaceTempView('twitch_2015')

    languages_old = spark.sql(
        """SELECT SUBSTRING(t.language, 1, 2) as lang, sum(INT(t.current_views)) as total_viewers
        FROM twitch_2015 t
        WHERE language != '-1'
        GROUP BY SUBSTRING(t.language, 1, 2)
        ORDER BY total_viewers DESC
        """
            )

    #languages_old.show()
    languages_old.coalesce(1).write.json('popular_languages_2015', mode = 'overwrite')

    #most popular games 
    popular_games_old = spark.sql(
        """SELECT game, sum(INT(t.current_views)) as total_viewers
        FROM twitch_2015 t
        GROUP BY game
        ORDER BY total_viewers DESC
        """
            )

    #popular_games_old.show()
    popular_games_old.coalesce(1).write.json('popular_games_2015', mode = 'overwrite')
    popular_games_old.createOrReplaceTempView('popular_games_old')

    spark.sql(
        """SELECT game, sum(viewers) as total_viewers
        FROM data_s 
        GROUP BY game
        ORDER BY total_viewers DESC
        """
            ).createOrReplaceTempView('popular_games_new')
    #popular_games_new.show()


    #comparison of most popular games of 2015 to 2018
    comparison_games = spark.sql(
        """SELECT n.game, o.total_viewers as data_2015, n.total_viewers as data_2018
        FROM popular_games_new n 
        LEFT JOIN popular_games_old o on n.game = o.game
        ORDER BY n.total_viewers DESC
        """
            )
    #comparison_games.show()

    comparison_games.coalesce(1).write.json('comparison_games_viewers_1518', mode = 'overwrite')


if __name__ == '__main__':
    main()



