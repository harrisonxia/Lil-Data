from pyspark.sql import SparkSession, functions, types
from pyspark.sql.types import StringType, LongType, IntegerType, BooleanType, FloatType, DateType
import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+

import json
import datetime as dt
from pyspark.sql.types import DateType

spark = SparkSession.builder.appName('data analysis').getOrCreate()
assert spark.version >= '2.3' # make sure we have Spark 2.3+
spark.sparkContext.setLogLevel('WARN')

import matplotlib.pyplot as plt

def main():
    data_stream = spark.read.json('stream_cleanned')
    data_channel = spark.read.json('channel_cleanned')

    data_stream.createOrReplaceTempView('data_s')
    data_channel.createOrReplaceTempView('data_c')

    #----1
    #most popular languages on twitch
    popular_languages = spark.sql(
        """SELECT language, COUNT(channel_id) AS numberOfChannels
        FROM data_c
        GROUP BY language
        ORDER BY numberOfChannels DESC
        """
            )
    #popular_languages.show()
    popular_languages.createOrReplaceTempView('popular_languages')

    #games for most popular language (to change)
    popular_language_games = spark.sql(
        """SELECT game
        FROM data_c
        WHERE language in 
            (SELECT FIRST(language)
            FROM popular_languages
            )
        """
            )
    #popular_language_games.show()

    #number of viewers for each language
    popular_language_viewers = spark.sql(
        """SELECT c.language, sum(s.viewers) as numberOfViewers
        FROM data_c c
        JOIN data_s s on c.stream_id = s.stream_id
        
        GROUP BY c.language
        """
            )
    #popular_language_viewers.show()

    popular_languages.coalesce(1).write.json('popular_languages', mode = 'overwrite')
    popular_language_games.coalesce(1).write.json('popular_language_games', mode = 'overwrite')
    popular_language_viewers.coalesce(1).write.json('popular_language_viewers', mode = 'overwrite')



if __name__ == '__main__':
    main()
