import sys

from pyspark.sql import SparkSession, functions, types
from pyspark.sql.functions import date_format
import json


def views_in_dow():
    data_stream = spark.read.json('stream_cleanned')
    data_channel = spark.read.json('channel_cleanned')
    
    data_stream.createOrReplaceTempView('data_s')
    data_channel.createOrReplaceTempView('data_c')

    #using date_format() extract day of the week for each date
    data_stream_weekdays = data_stream.select('*', date_format('created_at', 'u').alias('dow_number'), date_format('created_at', 'E').alias('dow_string'))
    data_stream_weekdays.createOrReplaceTempView('data_stream_weekdays')

    #select sum of viewers grouping by day of week
    views_per_weekdays = spark.sql(
        """SELECT dow_string, sum(viewers) as viewers
        FROM data_stream_weekdays
        GROUP BY dow_string 
        """
            )
    views_per_weekdays.coalesce(1).write.json('views_in_dow', mode='overwrite')
    
if __name__ == '__main__':
    spark = SparkSession.builder.appName('views_in_dow').getOrCreate()
    spark.sparkContext.setLogLevel('WARN')
    views_in_dow()
