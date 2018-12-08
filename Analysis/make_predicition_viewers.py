import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+

from pyspark.sql import SparkSession, functions, types
spark = SparkSession.builder.appName('viewers predictions').getOrCreate()
assert spark.version >= '2.3' # make sure we have Spark 2.3+
spark.sparkContext.setLogLevel('WARN')

from pyspark.ml import PipelineModel
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql import SQLContext
from pyspark.sql.types import FloatType


def test_model(model_file):
    # get the data
    inp = [('2019 -11-14', 0)]
    test_followers = spark.createDataFrame(inp, ['date_create', 'viewers'])

    # load the model
    model = PipelineModel.load(model_file)
    
    # use the model to make predictions
    predictions = model.transform(test_followers)

    #print('Predicted tmax tomorrow:', predictions.rdd.collect()[0][7])
    print(predictions.rdd.collect())


if __name__ == '__main__':
    #model_file = sys.argv[1]
    #inputs = sys.argv[2]
    test_model('viewers_model')
