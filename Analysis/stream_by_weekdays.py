from pyspark.sql import SparkSession, functions, types
from pyspark.sql.types import StringType, LongType, IntegerType, BooleanType, FloatType, DateType
import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+

import json
import datetime as dt
from pyspark.sql.types import DateType
from pyspark.sql.functions import date_format, desc, col

spark = SparkSession.builder.appName('stream by weekdays').getOrCreate()
assert spark.version >= '2.3' # make sure we have Spark 2.3+
spark.sparkContext.setLogLevel('WARN')

import matplotlib.pyplot as plt

from pyspark.sql.functions import explode

def main():
    #data_stream = spark.read.json('stream_cleanned')
    #data_channel = spark.read.json('channel_cleanned')
    #data_stream = spark.read.json(['/user/rishengw/stream_cleanned/part-00000-8325adf2-0829-40ac-bffe-01fd713899ee-c000.json', '/user/rishengw/stream_cleanned/part-00001-8325adf2-0829-40ac-bffe-01fd713899ee-c000.json', '/user/rishengw/stream_cleanned/part-00002-8325adf2-0829-40ac-bffe-01fd713899ee-c000.json'])
    data_stream = spark.read.json('/user/rishengw/stream_cleanned/')
    #data_channel = spark.read.json(['/user/rishengw/channel_cleanned/part-00000-7d918195-013e-4ff6-a0f7-2c92302fc9bd-c000.json', '/user/rishengw/channel_cleanned/part-00001-7d918195-013e-4ff6-a0f7-2c92302fc9bd-c000.json', '/user/rishengw/channel_cleanned/part-00002-7d918195-013e-4ff6-a0f7-2c92302fc9bd-c000.json'])

    data_stream_weekdays = data_stream.select('stream_id', 'viewers', 'created_at', date_format('created_at', 'u').alias('dow_number'), date_format('created_at', 'E').alias('dow_string'))
    #data_stream_weekdays.show()
    data_stream_weekdays.createOrReplaceTempView('data_s')


    #grouping by time frames and categories
    dow_viewers = spark.sql(
        """SELECT dow_string, COUNT(viewers) as total_viewers
        FROM data_s
        GROUP BY dow_string
        ORDER BY dow_string DESC
        """
            )

    #dow_viewers.show()
    #popular_categories_time_stream.show()
    dow_viewers.coalesce(1).write.json('total_viewers_weekdays', mode = 'overwrite')


if __name__ == '__main__':
    main()



