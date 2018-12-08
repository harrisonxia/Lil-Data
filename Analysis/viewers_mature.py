from pyspark.sql import SparkSession, functions, types
import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+

import json
import datetime as dt
spark = SparkSession.builder.appName('data analysis').getOrCreate()
assert spark.version >= '2.3' # make sure we have Spark 2.3+
spark.sparkContext.setLogLevel('WARN')



def main():
    #data_stream = spark.read.json('stream_cleanned')
    #data_channel = spark.read.json('channel_cleanned')
    data_stream = spark.read.json('/user/rishengw/stream_cleanned/')
    data_channel = spark.read.json('/user/rishengw/channel_cleanned/')

    data_stream.createOrReplaceTempView('data_s')
    data_channel.createOrReplaceTempView('data_c')


    popular_time_stream_non_mature = spark.sql(
        """SELECT s.time_frame, SUM(s.viewers) AS viewers
        FROM data_s s
        JOIN data_c c on c.stream_id = s.stream_id
        WHERE c.mature = "true"
        GROUP BY s.time_frame
        ORDER BY s.time_frame DESC
        """
            )
    popular_time_stream_non_mature.show()

    popular_time_stream_mature = spark.sql(
        """SELECT s.time_frame, SUM(s.viewers) AS viewers
        FROM data_s s
        JOIN data_c c on c.stream_id = s.stream_id
        WHERE c.mature = "false"
        GROUP BY s.time_frame
        ORDER BY s.time_frame DESC
        """
            )
    popular_time_stream_mature.show()
    #popular_time_stream_mature.show()
    popular_time_stream_non_mature.coalesce(1).write.json('popular_time_stream_non_mature', mode = 'overwrite')
    popular_time_stream_mature.coalesce(1).write.json('popular_time_stream_mature', mode = 'overwrite')

if __name__ == '__main__':
    #output = sys.argv[1]
    main()



