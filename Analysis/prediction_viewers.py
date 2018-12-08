import sys
from pyspark.sql import SparkSession, functions, types

import json
import datetime as dt
from pyspark.sql.types import DateType
from pyspark.sql.functions import date_format, desc, col
from pyspark.sql.functions import unix_timestamp
from pyspark.sql.functions import hash
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler, SQLTransformer
from pyspark.ml.regression import DecisionTreeRegressor, GBTRegressor, LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator

def timeToDate(dateStr):
    date = dt.datetime.strptime(dateStr, '%Y-%m-%dT%H:%M:%SZ')
    time = date.date()
    return time

def main():
    convertDate = functions.udf(timeToDate, DateType())
    data_stream = spark.read.json('stream_cleanned')
    #data_stream = spark.read.json('/user/rishengw/stream_cleanned/')
    
    data_stream = data_stream.withColumn('date_create', convertDate(data_stream.created_at)).cache()
    data_stream.show()

    data_stream.createOrReplaceTempView('data_s')

    #join stream data with game data
    data_joined = spark.sql(
        """SELECT s.date_create, lower(s.game) as game, sum(s.viewers) as viewers
        FROM data_s s
        GROUP BY s.date_create, s.game
        """
            )

    sqlTrans = SQLTransformer(statement="""
        SELECT UNIX_TIMESTAMP(date_create) as created_at_unix, 
            hash(lower(game)) as hashed_game, 
            int(date_format(date_create, 'u')) as dow_number, viewers
        FROM __THIS__ 
        """)

    #game time_frame dow_number views followers predict viewers
    #game_indexer = StringIndexer(inputCol='game', outputCol='game_ind').fit(data_joined)
    #created_at_indexer = StringIndexer(inputCol='created_at', outputCol='created_at_ind').fit(data_joined)

    #indexers = [StringIndexer(inputCol='time_frame', outputCol= "tf_index").fit(data_joined) ]

    train, validation = data_joined.randomSplit([0.75, 0.25])
    train = train.cache()
    validation = validation.cache()

    #features used to train a model - date, game name, day of the week
    viewers_assembler = VectorAssembler(
        inputCols=['created_at_unix', 'hashed_game', 'dow_number'],
        outputCol='features')
    
    #gbtr_regressor = GBTRegressor(labelCol='followers')
    #linear_regressor = LinearRegression(maxIter=10, labelCol='viewers')

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

    viewers_model.write().overwrite().save('viewers_model')
    
if __name__ == '__main__':
    spark = SparkSession.builder.appName('ml').getOrCreate()
    spark.sparkContext.setLogLevel('WARN')
    main()