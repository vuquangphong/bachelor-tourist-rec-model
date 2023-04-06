import pandas as pd
from flask import jsonify
from attr_rec import *


att_df = pd.read_json('../data/attraction/attractions.json', orient='records')


def get_city_options():
    options_city = list(att_df.groupby('city').size().reset_index().sort_values([0], ascending=True).city.values)
    return jsonify(options_city)


def get_attraction_categories():
    category_df = att_df.groupby('category').size().reset_index().sort_values([0],ascending=False)[:20]
    categories = list(category_df.category.values)
    return jsonify(categories)


# data_req is a dict
def get_att_rec(data_req):
    # get data from request
    cat_rating = data_req.get('cat_rating')
    city = data_req.get('city')
    bottom_budget = data_req.get('bottom_budget')
    top_budget = data_req.get('top_budget')
    number_of_days = data_req.get('number_of_days')
    user_name = data_req.get('user_name')

    filename, user, rbm_att = get_recc(att_df, cat_rating)
    filtered = filter_df(filename, user, low=bottom_budget, high=top_budget, city=city, att_df=att_df) 

    final = dict()
    final['timeofday'] = []
    final['image'] = []
    final['name'] = []
    final['location'] = []
    final['avg_price'] = []
    final['rating'] = []
    final['category'] = []

    for i in range(1, number_of_days+1):
        for j in range(2):
            final['timeofday'].append('Morning')
        for j in range(2):
            final['timeofday'].append('Evening')

    for i in range(len(final['timeofday'])): 
        if i%4 == 0: 
            final = top_recc(filtered, final)
        else:
            final = find_closest(filtered, final['location'][-1], final['timeofday'][i], final)
    
    res = convert_final_output(number_of_days, final)
    return jsonify(res)


"""
Util function
"""
def convert_final_output(num_days, final):
    res = [] # containing final output

    for day_index in range(num_days):
        current_day = []
        
        for i in range(4):
            place = dict()
            place['name'] = final['name'][day_index*4+i]
            # place['image'] = final['image'][day_index*4+i]
            place['image'] = 'none'
            place['category'] = final['category'][day_index*4+i]
            place['location'] = final['location'][day_index*4+i]
            place['avg_price'] = final['avg_price'][day_index*4+i].item()
            place['rating'] = final['rating'][day_index*4+i]
            current_day.append(place)

        res.append(current_day)
    
    return res
