from pyspark.sql import SparkSession, functions, types
from pyspark.sql.types import StringType, LongType, IntegerType, BooleanType, FloatType, DateType
import sys
import json
import datetime as dt




def getDate(dateStr):
    date = dt.datetime.strptime(dateStr, '%Y-%m-%dT%H:%M:%SZ')
    just_date = date.date()
    jd = just_date.strftime('%Y-%m-%d')
    return jd


def main(input1):
    stream_creation_date = functions.udf(getDate)
    data_c = spark.read.json(input1)
    data_c = data_c.repartition(40)
    data_c = data_c.withColumn('last_updated_at', stream_creation_date(data_c.updated_at))
    data_c.createOrReplaceTempView('data_c')



    data_ch = data_c.select('stream_id', 'channel_id','name', 'game', 'views',
                           'followers', 'broadcaster_language',
                           'created_at', 'last_updated_at', 'mature', 'partner')\
        .where(functions.lower(data_c['game'])
                               .isin('fortnite','league of legends','call of duty: black ops 4',
                                      'overwatch', 'counter-strike: global offensive',
                                      'playerunknown\'s battlegrounds','just chatting', 'fallout 76',
                                      'tom clancy\'s rainbow six: siege',
                                      'world of warcraft','red dead redemption 2', 'destiny 2',
                                      'dota 2', 'fifa 19', 'battlefield v', 'dead by daylight',
                                      'rocket league','minecraft','grand theft auto v',
                                      'nba 2k19')).cache()

    data_ch.createOrReplaceTempView('data_ch')




#---------------see what are the most popular non-english speaking streams (by game and language)-----------------------
    yuyan = spark.sql(
        """
        SELECT broadcaster_language, COUNT(DISTINCT channel_id)  AS total_streamers, LOWER(game)
        FROM data_ch
        WHERE broadcaster_language IN ('de', 'ru', 'fr', 'es', 'en-gb', 'ko')
        AND LOWER(game) IN ('fortnite','league of legends','call of duty: black ops 4',
                                      'overwatch', 'counter-strike: global offensive')
        GROUP BY broadcaster_language, LOWER(game)
        ORDER BY  total_streamers DESC
        """
            )
    yuyan.createOrReplaceTempView('yuyan')

    print('see what are the most popular non-english speaking streams (by game and language)')
    print(yuyan.show(20))

    yuyan_output = yuyan.toJSON().collect()
    filename = 'bigdata1_' + 'yuyan'
    with open(filename, 'w') as output:
        json.dump(yuyan_output, output)
        output.close()


    yuyan_wtih_en = spark.sql(
        """
        SELECT broadcaster_language, LOWER(game), COUNT(DISTINCT channel_id)  AS total_streamers
        FROM data_ch
        WHERE broadcaster_language IN ('en', 'de', 'ru', 'fr', 'es', 'en-gb', 'ko')
        AND (LOWER(game) IN ('fortnite','league of legends','call of duty: black ops 4',
                                      'overwatch', 'counter-strike: global offensive'))
        GROUP BY broadcaster_language, LOWER(game)
        ORDER BY  total_streamers DESC
        """
            )
    print(yuyan_wtih_en.show(20))

    yuyan_wtih_en_output = yuyan_wtih_en.toJSON().collect()
    filename = 'bigdata1_' + 'yuyan_wtih_en'
    with open(filename, 'w') as output:
        json.dump(yuyan_wtih_en_output, output)
        output.close()


    yuyan_in_general_ = spark.sql(
        """
        SELECT broadcaster_language, COUNT(DISTINCT channel_id) AS total_streamers
        FROM data_ch
        GROUP BY broadcaster_language
        ORDER BY  total_streamers DESC
        """
            )

    print(yuyan_in_general_.show(20))

    yuyan_in_general_output = yuyan_in_general_.toJSON().collect()
    filename = 'bigdata_' + 'yuyan_in_general'
    with open(filename, 'w') as output:
        json.dump(yuyan_in_general_output, output)
        output.close()



#-----------------------------see what are the biggest broadcaster communities (by language)-------------------------
    yuyan_by_game = spark.sql(
        """
        SELECT broadcaster_language, game, COUNT(DISTINCT channel_id) AS total_streamer
        FROM data_ch
        GROUP BY broadcaster_language, game
        ORDER BY total_streamer DESC
        """
            )
    yuyan_by_game.createOrReplaceTempView('yuyan_by_game')

    print('see what are the biggest broadcaster communities (by language)')
    print(yuyan_by_game.show(20))

    yuyan_by_game_output = yuyan_by_game.toJSON().collect()
    filename = 'bigdata_' + 'yuyan_by_game'
    with open(filename, 'w') as output:
        json.dump(yuyan_by_game_output, output)
        output.close()


if __name__ == '__main__':
    spark = SparkSession.builder.appName('clean data').getOrCreate()
    spark.sparkContext.setLogLevel('WARN')

    input1 = sys.argv[1]

    main(input1)