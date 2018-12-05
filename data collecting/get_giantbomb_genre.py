
#from pyspark.sql import SparkSession, functions, types
import sys
import json
import requests

#def join():
#	real_game_info = spark.read.json('real_game_info')
#	real_game_info = real_game_info.orderBy(real_game_info['count'].desc()).where(real_game_info.guid != '')
#	real_game_info.select('guid').coalesce(1).write.json('game_id.txt', mode = 'overwrite')
	
def load_genre():
	guid = []
	with open('game_id.txt/game_id.json', 'r') as jf:
		for line in jf:
			guid.append(json.loads(line))


	session = requests.Session()
	session.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0'})

	for i in range(len(guid)):
		gid = guid[i]['guid']
		req = 'https://www.giantbomb.com/api/game/'+ str(gid) + '/?api_key=3aa85a32d444184830f32a6d51b564a5a9397d41&format=json&field_list=guid,genres'

		response = session.get(req)
		filename = 'guids/genre_' + str(i)
		print(i, gid)
		with open(filename, 'w', encoding='utf-8') as outfile:
			json.dump(json.JSONDecoder().decode(response.content.decode("utf-8")), outfile, indent=4, separators=(',', ': '))


if __name__ == '__main__':
	#spark = SparkSession.builder.appName('join data').getOrCreate()
	#spark.sparkContext.setLogLevel('WARN')
	load_genre()
