from flask import jsonify
import pyspark
from pyspark.sql import SQLContext
from hotel_rec import *
import json
import constants as const


sc = pyspark.SparkContext(appName='hotel_service')
spark = SQLContext(sc)

hotel_df = spark.read.json(const.DIR_DATA_HOTEL)
hotel_amenity_df = spark.read.json(const.DIR_DATA_HOTEL_AMENITIES)

hotel_df.createOrReplaceTempView('hotel_df')
hotel_amenity_df.createOrReplaceTempView('hotel_amenity_df')


def get_hotel_amenities():
    temp_amenity_df  = spark.sql("SELECT amenities, COUNT(amenities) AS tot_count FROM hotel_amenity_df GROUP BY amenities ORDER BY tot_count DESC")
    top_amenities = [x[0] for x in temp_amenity_df.head(21) if x[0] != '']
    return jsonify(top_amenities)


def get_hotel_rec(data_req):
    # get data from request
    amenities_pref = data_req.get('amenities_pref')
    city = data_req.get('city')
    number_of_days = data_req.get('number_of_days')
    user_name = data_req.get('user_name')

    usrid_s2, model = get_model_hotel(amenities_pref)

    final_hotels = get_final_output(city, usrid_s2, model)

    res = [] # containing final output

    for i in range(len(final_hotels.get('name'))):
        hotel = dict()
        
        hotel['name'] = final_hotels.get('name')[i]
        hotel['price'] = round(final_hotels.get('price')[i], 2)
        hotel['rating'] = final_hotels.get('rating')[i]
        hotel['experience'] = final_hotels.get('experience')[i]
        hotel['location'] = final_hotels.get('location')[i]
        hotel['address'] = final_hotels.get('address')[i]

        res.append(hotel)

    return jsonify(res)


"""
Util functions
"""
def get_model_hotel(amenities_pref):
    temp_json_amenities = []
    for amenity in amenities_pref:
        temp_json_amenities.append({'amenities_pref': amenity})

    with open('temp_amenities_pref.json', 'w') as f:
        json.dump(temp_json_amenities, f)

    amenities_pref_df = spark.read.json('temp_amenities_pref.json')

    usr_rating = amenities_rating(spark, amenities_pref_df, hotel_amenity_df)
    rank, error, errors, usrid_s2, model = model_train(spark, usr_rating)
    return usrid_s2, model


def get_final_output(city, usrid_s2, model): 
    u_tempdf = get_hotel_recc(spark, usrid_s2, model)
    final_hotel_df = hotel_df.join(u_tempdf, "id").withColumn("address",functions.lower(functions.col("address")))
    user_location = city.lower()
    hotel_sugg = final_hotel_df.where(final_hotel_df.address.contains(user_location))
    recc = hotel_sugg.dropna().toPandas()

    final = dict()
    final['address'] = recc[:5]['address'].values.tolist()
    final['amenities'] = recc[:5]['amenities'].values.T.tolist()
    final['experience'] = recc[:5]['hotel_experience'].values.tolist()
    final['name'] = recc[:5]['hotel_name'].values.tolist()
    final['rating'] = recc[:5]['hotel_rating'].values.tolist()
    final['location'] = [i[1:-1] for i in recc[:5]['location'].values.tolist()]
    final['price'] = recc[:5]['price'].values.tolist()
    final['image'] = [get_image(i) for i in recc[:5]['hotel_name'].values.tolist()]

    return final
