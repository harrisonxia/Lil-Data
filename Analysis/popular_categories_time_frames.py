from pyspark.sql import SparkSession, functions, types
from pyspark.sql.types import StringType, LongType, IntegerType, BooleanType, FloatType, DateType
import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+

import json
import datetime as dt
from pyspark.sql.types import DateType

spark = SparkSession.builder.appName('popular_categories_time_frames').getOrCreate()
assert spark.version >= '2.3' # make sure we have Spark 2.3+
spark.sparkContext.setLogLevel('WARN')

import matplotlib.pyplot as plt

from pyspark.sql.functions import explode

def main():
    data_stream = spark.read.json('stream_cleanned')

    data_channel = spark.read.json('channel_cleanned').cache()
    data_game = spark.read.json('real_game_info').cache()
    data_genre = spark.read.json('game_genre').cache()

    data_stream.createOrReplaceTempView('data_s')
    data_channel.createOrReplaceTempView('data_c')
    data_game.createOrReplaceTempView('data_g')
    data_genre.createOrReplaceTempView('data_genre')


    #joining stream info with game info and categories
    game_with_channel = spark.sql(
        """SELECT s.stream_id, s.game, s.viewers, s.time_frame, g.guid, genre.genres
            FROM data_s s
            JOIN data_g g on s.game = g.gen_name
            JOIN data_genre genre on g.guid = genre.guid
        """
            )

    #to flatten the categories
    games_with_genres = game_with_channel.select(
        game_with_channel['game'], 
        game_with_channel['viewers'], 
        game_with_channel['time_frame'], 
        game_with_channel['guid'], 
        explode(game_with_channel['genres']).alias('genres'))

    games_with_genres.createOrReplaceTempView('games_genres')

    #grouping by time frames and categories
    spark.sql(
        """SELECT time_frame, genres, SUM(viewers) AS viewers
        FROM games_genres
        GROUP BY genres, time_frame
        ORDER BY viewers DESC
        """
            ).createOrReplaceTempView('categories_time_frame_viewers')

    #getting most popular category for time frames
    popular_categories_time_frames = spark.sql(
        """SELECT c.time_frame, c.genres, c.viewers
        FROM (
        SELECT g.time_frame, MAX(g.viewers) as max_viewers from categories_time_frame_viewers g
        GROUP BY g.time_frame
        ) as x INNER JOIN categories_time_frame_viewers as c on c.time_frame = x.time_frame and c.viewers = x.max_viewers        
        """
            )
    #popular_categories_time_stream.show()
    popular_categories_time_frames.coalesce(1).write.json('popular_categories_time_frames', mode = 'overwrite')


if __name__ == '__main__':
    main()
