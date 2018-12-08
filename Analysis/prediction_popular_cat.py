import sys
from pyspark.sql import SparkSession, functions, types
import json
import datetime as dt
from pyspark.sql.types import DateType
from pyspark.sql.functions import unix_timestamp

from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler, SQLTransformer
from pyspark.ml.regression import DecisionTreeRegressor, GBTRegressor
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql.functions import explode

def timeToDate(dateStr):
    date = dt.datetime.strptime(dateStr, '%Y-%m-%dT%H:%M:%SZ')
    time = date.date()
    return time

def main():
    convertDate = functions.udf(timeToDate, DateType())
    data_stream = spark.read.json('stream_cleanned')
    #data_stream = spark.read.json('/user/rishengw/stream_cleanned/')
    #data_game = spark.read.json('/user/rishengw/real_game_info/').cache()
    #data_genre = spark.read.json('/user/rishengw/game_genre/').cache()
    data_stream = data_stream.withColumn('date_create', convertDate(data_stream.created_at))

    data_game = spark.read.json('real_game_info').cache()
    data_genre = spark.read.json('game_genre').cache()

    data_game.createOrReplaceTempView('data_g')
    data_genre.createOrReplaceTempView('data_genre')
    data_stream.createOrReplaceTempView('data_s')

    #joining stream data with categories
    game_with_stream = spark.sql(
        """SELECT s.date_create, s.viewers, genre.genres
            FROM data_s s
            JOIN data_g g on s.game = g.gen_name
            JOIN data_genre genre on g.guid = genre.guid
        """
            )

    #to flatten the categories
    games_with_genres_languages = game_with_stream.select(
        game_with_stream['date_create'], 
        game_with_stream['viewers'], 
        explode(game_with_stream['genres']).alias('genres'))
    #games_with_genres_languages.show()

    games_with_genres_languages.createOrReplaceTempView('games_with_genres_languages')

    #grouping by date and categories
    data_joined = spark.sql(
        """SELECT date_create, genres, SUM(viewers) AS viewers
        FROM games_with_genres_languages
        GROUP BY date_create, genres
        ORDER BY viewers DESC
        """
            )
    #data_joined.show()

    #transforming data to unix format, hashing name of the game
    sqlTrans = SQLTransformer(statement="""
        SELECT UNIX_TIMESTAMP(date_create) as created_at_unix, hash(genres) as hashed_genres, viewers
        FROM __THIS__ 
        """)

    #pipeline = Pipeline(stages=[sqlTrans, language_indexer, game_indexer])
    #data_transformed = pipeline.fit(data_channel).transform(data_channel)

    train, validation = data_joined.randomSplit([0.75, 0.25])
    train = train.cache()
    validation = validation.cache()

    viewers_assembler = VectorAssembler(
        inputCols=['created_at_unix', 'hashed_genres'],
        outputCol='features')
    
    dt_regressor = DecisionTreeRegressor(
        maxDepth=20, varianceCol="variance", labelCol='viewers')
    
    viewers_pipeline = Pipeline(
        stages=[sqlTrans, viewers_assembler, dt_regressor])
    viewers_model = viewers_pipeline.fit(train)

    predictions = viewers_model.transform(validation)
    predictions.show()

    eval = RegressionEvaluator(
        labelCol="viewers", predictionCol="prediction", metricName="rmse")

    # Root Mean Square Error
    rmse = eval.evaluate(predictions)
    print("RMSE: %.3f" % rmse)

    # r2 - coefficient of determination
    r2 = eval.evaluate(predictions, {eval.metricName: "r2"})
    print("r2: %.3f" %r2)

    viewers_model.write().overwrite().save('categories_model')
    
if __name__ == '__main__':
    spark = SparkSession.builder.appName('data analysis').getOrCreate()
    spark.sparkContext.setLogLevel('WARN')
    main()