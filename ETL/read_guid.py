
from pyspark.sql import SparkSession, functions, types
import sys
import json

def read_guid():
	guids = spark.read.json('guids', multiLine=True).repartition(10)
	guids = guids.select('results.guid', 'results.genres')
	guids = guids.select('guid', functions.explode('genres').alias('genres'))
	guids = guids.select('guid', 'genres.name')
	guids = guids.groupBy('guid').agg(functions.collect_set('name').alias('genres'))
	guids.coalesce(1).write.json('game_genre', mode = 'overwrite')
  
if __name__ == '__main__':
	spark = SparkSession.builder.appName('join data').getOrCreate()
	spark.sparkContext.setLogLevel('WARN')
	read_guid()