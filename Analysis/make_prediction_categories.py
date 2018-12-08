import sys
from pyspark.sql import SparkSession, functions, types

from pyspark.ml import PipelineModel
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql import SQLContext
from pyspark.sql.functions import unix_timestamp
from datetime import datetime
from pyspark.sql.functions import to_timestamp

def test_model(model_file):
    input_cat_19 = spark.read.json('input_cat_19.json')
    input_cat_19.createOrReplaceTempView('input_cat_19')
    data_predict = input_cat_19.select(
        to_timestamp(input_cat_19['date_create'], 'yyyy-MM-dd').alias('date_create'), 
        input_cat_19['genres'], 
        input_cat_19['viewers'])

    # load the model
    model = PipelineModel.load(model_file)
    
    # use the model to make predictions
    predictions = model.transform(data_predict)
    predictions.createOrReplaceTempView('predictions')

    data_joined = spark.sql(
        """SELECT t.date_create as date_predict, t.genres, p.prediction as predicted_viewers
        FROM predictions p
        JOIN input_cat_19 t
        ON p.hashed_genres = hash(t.genres)

        ORDER BY p.prediction DESC
        """
            )

    #data_joined.show()
    data_joined.coalesce(1).write.json('prediction_genres_jan_1', mode = 'overwrite')

if __name__ == '__main__':
    spark = SparkSession.builder.appName('viewers predictions').getOrCreate()
    spark.sparkContext.setLogLevel('WARN')
    test_model('categories_model')
