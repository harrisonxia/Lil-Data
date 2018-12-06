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

from pyspark.sql.functions import explode


def main():
    data_stream = spark.read.json('stream_cleanned')
    data_channel = spark.read.json('channel_cleanned')
    data_game = spark.read.json('real_game_info').cache()
    data_genre = spark.read.json('game_genre').cache()

    data_stream.createOrReplaceTempView('data_s')

    data_channel.createOrReplaceTempView('data_c')
    data_game.createOrReplaceTempView('data_g')
    data_genre.createOrReplaceTempView('data_genre')


    #joining stream info with game info and categories
    game_with_channel = spark.sql(
        """SELECT s.stream_id, c.language, s.game, s.viewers, s.time_frame, g.guid, genre.genres
            FROM data_s s
            JOIN data_c c on s.stream_id = c.stream_id
            JOIN data_g g on s.game = g.gen_name
            JOIN data_genre genre on g.guid = genre.guid
        """
            )

    #game_with_channel.show()

    #to flatten the categories
    games_with_genres_languages = game_with_channel.select(
        game_with_channel['stream_id'], 
        game_with_channel['game'], 
        game_with_channel['language'], 
        game_with_channel['viewers'], 
        game_with_channel['time_frame'], 
        game_with_channel['guid'], 
        explode(game_with_channel['genres']).alias('genres'))
    #games_with_genres_languages.show()

    games_with_genres_languages.createOrReplaceTempView('games_with_genres_languages')

    #grouping by languages and categories
    spark.sql(
        """SELECT language, genres, SUM(viewers) AS viewers
        FROM games_with_genres_languages
        WHERE language != ''
        GROUP BY genres, language
        ORDER BY language ASC
        """
            ).createOrReplaceTempView('categories_languages_viewers')

    #categories_languages_viewers.show()

    #getting most popular category for each language
    popular_category_for_languages= spark.sql(
        """SELECT language, genres, viewers FROM (SELECT c.genres, c.language, c.viewers
        FROM (
        SELECT g.language, MAX(g.viewers) as max_viewers from categories_languages_viewers g
        GROUP BY g.language
        ) as x INNER JOIN categories_languages_viewers as c on c.language = x.language and c.viewers = x.max_viewers 
        ORDER BY language  )     
        """
            )
    #popular_category_for_languages.show()
    popular_category_for_languages.coalesce(1).write.json('popular_category_for_languages', mode = 'overwrite')


if __name__ == '__main__':
    main()



