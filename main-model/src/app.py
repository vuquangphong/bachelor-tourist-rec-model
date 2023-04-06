from flask import Flask, request
from flask_cors import CORS
from attraction_service import get_city_options, get_attraction_categories, get_att_rec
from hotel_service import get_hotel_amenities, get_hotel_rec


app = Flask(__name__)
CORS(app) # unblocked CORS policy


"""
Route of Attractions
"""
@app.route('/api/attractions/cities', methods=['GET'])
def get_cities():
    return get_city_options()


@app.route('/api/attractions/categories', methods=['GET'])
def get_categories():
    return get_attraction_categories()


@app.route('/api/attractions', methods=['POST'])
def get_final_output():
    data_req = request.get_json()
    return get_att_rec(data_req)




"""
Route of Hotels
"""
@app.route('/api/hotels/amenities', methods=['GET'])
def get_amenities():
    return get_hotel_amenities()


@app.route('/api/hotels', methods=['POST'])
def get_hotels():
    data_req = request.get_json()
    return get_hotel_rec(data_req)


if __name__ == '__main__':
    app.run(debug=True)
