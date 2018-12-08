import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+

from pyspark.sql import SparkSession, functions, types
spark = SparkSession.builder.appName('viewers predictions').getOrCreate()
assert spark.version >= '2.3' # make sure we have Spark 2.3+
spark.sparkContext.setLogLevel('WARN')

from pyspark.ml import PipelineModel
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql.types import StringType, LongType, IntegerType, BooleanType, FloatType, DateType
from pyspark.sql import SQLContext
from pyspark.sql.types import FloatType
from pyspark.ml.feature import StringIndexer, VectorAssembler, SQLTransformer
from pyspark.sql.functions import unix_timestamp
from pyspark.ml import Pipeline
from datetime import datetime
from pyspark.sql.functions import to_timestamp


def test_model(model_file):
    input_19 = spark.read.json('input_19.json')

    input_19.createOrReplaceTempView('test_followers')

    input_transformed = input_19.select(to_timestamp(input_19['date_create'], 'yyyy-MM-dd').alias('date_create'), input_19['game'], input_19['viewers'])
    input_transformed.show()

    # load the model
    model = PipelineModel.load(model_file)
    
    # use the model to make predictions
    predictions = model.transform(input_transformed)

    #predictions.show()
    predictions.createOrReplaceTempView('predictions')

    #predictions on most popular games
    data_joined = spark.sql(
        """SELECT t.date_create as date_predict, t.game, p.prediction
        FROM predictions p
        JOIN test_followers t
        ON p.hashed_game = hash(t.game)

        ORDER BY p.prediction DESC
        """
            )

    #data_joined.show()

    data_joined.coalesce(1).write.json('prediction_jan_1', mode = 'overwrite')


if __name__ == '__main__':
    test_model('viewers_model')
