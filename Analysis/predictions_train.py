import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+

from pyspark.sql import SparkSession, functions, types
from pyspark.sql.types import StringType, LongType, IntegerType, BooleanType, FloatType, DateType
spark = SparkSession.builder.appName('weather').getOrCreate()
spark.sparkContext.setLogLevel('WARN')
assert spark.version >= '2.3' # make sure we have Spark 2.3+

import json
import datetime as dt
from pyspark.sql.types import DateType

from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler, SQLTransformer
from pyspark.ml.classification import MultilayerPerceptronClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.regression import DecisionTreeRegressor, GBTRegressor
from pyspark.ml.evaluation import RegressionEvaluator

#-------------IN PROGRESS---------------------


earlymorningStart = dt.time(3,0,1)
earlymorningEnd = dt.time(7,0,0)
morningStart = dt.time(7, 0, 1)
morningEnd = dt.time(11, 0, 0)
noonStart = dt.time(11, 0, 1)
noonEnd = dt.time(15, 0, 0)
afternoonStart = dt.time(15, 0, 1)
afternoonEnd = dt.time(19, 0, 0)
eveningStart = dt.time(19, 0, 1)
eveningEnd = dt.time(23, 0, 0)


def createSchema():
    stream_sch = types.StructType([
        types.StructField('stream_id', StringType(), True),
        types.StructField('game', StringType(), True),
        types.StructField('viewers', LongType(), True),
        types.StructField('video_height', StringType(), True),
        types.StructField('average_fps', FloatType(), True),
        types.StructField('delay', IntegerType(), True),
        types.StructField('created_at', StringType(), True),
    ])

    channel_sch = types.StructType([
        types.StructField('stream_id', StringType(), True),
        types.StructField('channel_id', StringType(), True),
        types.StructField('display_name', StringType(), True),
        types.StructField('name', StringType(), True),
        types.StructField('game', StringType(), True),
        types.StructField('views', LongType(), True),
        types.StructField('followers', LongType(), True),
        types.StructField('status', StringType(), True),
        types.StructField('broadcaster_language', StringType(), True),
        types.StructField('language', StringType(), True),
        types.StructField('broadcaster_software', StringType(), True),
        types.StructField('created_at', StringType(), True),
        types.StructField('updated_at', StringType(), True),
        types.StructField('mature', BooleanType(), True),
        types.StructField('partner', BooleanType(), True),
    ])

    return [stream_sch, channel_sch]

def getTimeFrame(time):
    if earlymorningStart <= time <= earlymorningEnd:
        timeframe = "Early Morning"
    elif morningStart <= time <= morningEnd:
        timeframe = "Morning"
    elif noonStart <= time <= noonEnd:
        timeframe = "Noon"
    elif afternoonStart <= time <= afternoonEnd:
        timeframe = "Afternoon"
    elif eveningStart <= time <= eveningEnd:
        timeframe = "Evening"
    else:
        timeframe = "Late Night"

    return timeframe

def timeToFrame(dateStr):
    date = dt.datetime.strptime(dateStr, '%Y-%m-%dT%H:%M:%SZ')
    time = date.time()

    return getTimeFrame(time)

def timeToDate(dateStr):
    date = dt.datetime.strptime(dateStr, '%Y-%m-%dT%H:%M:%SZ')
    time = date.date()

    return time

def main():
    stream_sch, channel_sch = createSchema()

    convertTime = functions.udf(timeToFrame)
    convertDate = functions.udf(timeToDate, DateType())

    data_stream = spark.read.json('stream_cleanned', schema = stream_sch)
    data_channel = spark.read.json('channel_cleanned', schema = channel_sch)
    data_stream = data_stream.withColumn('time_frame', convertTime(data_stream.created_at)).cache()
    data_stream = data_stream.withColumn('date', convertDate(data_stream.created_at)).cache()

    data_stream.createOrReplaceTempView('data_s')

    data_channel.createOrReplaceTempView('data_c')

    data_joined = spark.sql(
        """SELECT s.stream_id, s.viewers, DAYOFYEAR(s.date) as day, s.time_frame, c.channel_id, c.views, c.followers
        FROM data_c c
        JOIN data_s s on c.stream_id = s.stream_id
        """
            )
    #data_joined.show()

    #time_indexer = StringIndexer(inputCol='time_frame', outputCol='time_fr')
    #df_ind = time_indexer.transform(data_joined)


    #indexers = [StringIndexer(inputCol=column, outputCol=column+"_index").fit(data_joined) for column in list(set(data_joined.columns)-set(['views'])) ]
    indexers = [StringIndexer(inputCol='time_frame', outputCol= "tf_index").fit(data_joined) ]


    pipeline = Pipeline(stages=indexers)
    df_r = pipeline.fit(data_joined).transform(data_joined)

    #df_r.show()

    train, validation = df_r.randomSplit([0.75, 0.25])
    train = train.cache()
    validation = validation.cache()


    viewers_assembler = VectorAssembler(
        inputCols=['views', 'followers', 'day', 'tf_index'],
        outputCol='features')

    dt_regressor = DecisionTreeRegressor(
        maxDepth=7, varianceCol="variance", labelCol='viewers')
    
    viewers_pipeline = Pipeline(
        stages=[viewers_assembler, dt_regressor])
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

    #viewers_model.write().overwrite().save(model_file)

    #data_stream.show()

    #data_channel.show()

    
if __name__ == '__main__':
    #inputs = sys.argv[1]
    #model_file = sys.argv[2]
    main()