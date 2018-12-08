import sys
from pyspark.sql import SparkSession, functions, types
import json


import matplotlib.pyplot as plt

def popular_languages():
    data_stream = spark.read.json('stream_cleanned')
    data_channel = spark.read.json('channel_cleanned').cache()
    #data_stream = spark.read.json('/user/rishengw/stream_cleanned/')
    #data_channel = spark.read.json('/user/rishengw/channel_cleanned/')

    data_stream.createOrReplaceTempView('data_s')
    data_channel.createOrReplaceTempView('data_c')

    #most popular languages on twitch
    popular_languages = spark.sql(
        """SELECT language, COUNT(channel_id) AS numberOfChannels
        FROM data_c
        WHERE language != ''
        GROUP BY language
        ORDER BY numberOfChannels DESC
        """
            )
    popular_languages.createOrReplaceTempView('popular_languages')

    #games for most popular language
    popular_language_games = spark.sql(
        """SELECT game
        FROM data_c
        WHERE language != '' AND language in 
            (SELECT FIRST(language)
            FROM popular_languages
            )
        """
            )

    #number of viewers for each language
    popular_language_viewers = spark.sql(
        """SELECT c.language, sum(s.viewers) as numberOfViewers
        FROM data_c c
        JOIN data_s s on c.stream_id = s.stream_id
        GROUP BY c.language
        """
            )

    popular_languages.coalesce(1).write.json('popular_languages', mode = 'overwrite')
    popular_language_games.coalesce(1).write.json('popular_language_games', mode = 'overwrite')
    popular_language_viewers.coalesce(1).write.json('popular_language_viewers', mode = 'overwrite')

if __name__ == '__main__':
    spark = SparkSession.builder.appName('data analysis').getOrCreate()
    spark.sparkContext.setLogLevel('WARN')
    popular_languages()
