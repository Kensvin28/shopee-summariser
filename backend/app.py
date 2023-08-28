from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from scrape import get_overall_rating
from scrape import scrape
from preprocess_eng import clean
from feature_extractor_pyabsa import perform_aste_inference
# from example_response import example
import time

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
@cross_origin()
def summarise():
    time_start = time.perf_counter()

    # get JSON data from request body
    request_json = request.json
    URL = request_json['data']
    # scrape data from shopee
    print("Scraping...")
    dataframe = scrape(URL)
    if(dataframe is None):
        return jsonify({'error': "Invalid URL or Server Error"})
    # clean scraping result
    print("Cleaning...")
    cleaned_df = clean(dataframe)

    # perform aspect extraction
    result = perform_aste_inference(cleaned_df)

    # get overall rating
    rating, total = get_overall_rating(cleaned_df)
    
    response_data = {
        'overall_rating': rating,
        'total_reviews': int(total),
        **result
    }

    # example response data for development
    # time.sleep(7)
    # response_data = example

    print("Sending data...")
    time_elapsed = (time.perf_counter() - time_start)
    print("Total processing time: %3.1f secs" % time_elapsed)
    return jsonify(response_data)