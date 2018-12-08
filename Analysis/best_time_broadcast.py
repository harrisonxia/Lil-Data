from pyspark.sql import SparkSession, functions, types
from pyspark.sql.types import StringType, LongType, IntegerType, BooleanType, FloatType, DateType
import sys

import json
import datetime as dt
from pyspark.sql.types import DateType

from pyspark.sql.functions import explode


def main():
    data_stream = spark.read.json('stream_cleanned')
    data_channel = spark.read.json('channel_cleanned')
    data_game = spark.read.json('real_game_info').cache()
    data_genre = spark.read.json('game_genre').cache()
    #data_stream = spark.read.json('/user/rishengw/stream_cleanned/')
    #data_channel = spark.read.json('/user/rishengw/channel_cleanned/')
    #data_game = spark.read.json('/user/rishengw/real_game_info/').cache()
    #data_genre = spark.read.json('/user/rishengw/game_genre/').cache()

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
            ).createOrReplaceTempView('categories_time_stream_viewers')

    #getting most popular category for time frames
    popular_categories_time_frames = spark.sql(
        """SELECT c.time_frame, c.genres, c.viewers
        FROM (
        SELECT g.time_frame, MAX(g.viewers) as max_viewers from categories_time_stream_viewers g
        GROUP BY g.time_frame
        ) as x INNER JOIN categories_time_stream_viewers as c on c.time_frame = x.time_frame and c.viewers = x.max_viewers        
        """
            )
    #popular_categories_time_frames.show()

    #getting most popular time frame for categories
    popular_categories_time_frames = spark.sql(
        """SELECT c.genres, c.time_frame, c.viewers
        FROM (
        SELECT g.genres, MAX(g.viewers) as max_viewers from categories_time_stream_viewers g
        GROUP BY g.genres
        ) as x INNER JOIN categories_time_stream_viewers as c on c.genres = x.genres and c.viewers = x.max_viewers        
        """
            )
    #popular_categories_time_frames.show()
    popular_categories_time_frames.coalesce(1).write.json('popular_categories_time_frames', mode = 'overwrite')

    #------------Languages------------------
    #number of viewers for each language and time frame
    language_time_frame_viewers = spark.sql(
        """SELECT s.time_frame, c.language, SUM(s.viewers) AS viewers
        FROM data_s s
        JOIN data_c c on c.stream_id = s.stream_id
        WHERE language != ''
        GROUP BY s.time_frame, c.language
        ORDER BY language ASC
        """
            )
    language_time_frame_viewers.coalesce(1).write.json('viewers_for_language_time_frames', mode = 'overwrite')
    language_time_frame_viewers.createOrReplaceTempView('language_time_frame_viewers')

    #getting most popular time frames for each language
    popular_time_frames_for_languages= spark.sql(
        """SELECT language, time_frame FROM (SELECT c.time_frame, c.language, c.viewers
        FROM (
        SELECT g.language, MAX(g.viewers) as max_viewers from language_time_frame_viewers g
        GROUP BY g.language
        ) as x INNER JOIN language_time_frame_viewers as c on c.language = x.language and c.viewers = x.max_viewers 
        ORDER BY language  )     
        """
            )
    popular_time_frames_for_languages.coalesce(1).write.json('popular_time_frames_for_languages', mode = 'overwrite')

    #getting number of languages and number of viewers for each time frame
    time_frame_languages_viewers= spark.sql(
        """SELECT c.time_frame, COUNT(c.language) as total_languages, SUM(c.viewers) as total_viewers
        FROM language_time_frame_viewers c 
        GROUP BY c.time_frame
        ORDER BY c.time_frame       
        """
            )
    time_frame_languages_viewers.coalesce(1).write.json('time_frame_languages_viewers', mode = 'overwrite')


if __name__ == '__main__':
    spark = SparkSession.builder.appName('data analysis').getOrCreate()
    spark.sparkContext.setLogLevel('WARN')
    main()
