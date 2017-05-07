from flask import Flask, make_response, jsonify, request
import InpediaSearchService.constants
from InpediaSearchService.exceptions.InpediaException import InpediaException
import InpediaSearchService.es_helper as es_helper
from flask_cors import CORS
import time
import requests

app = Flask(__name__)
CORS(app)


@app.route(constants.API_PATH_CLIENT + constants.API_PATH_TYPE, methods=['GET'])
def search():
    """
    The endpoint to perform a search for the given client and the requested `type`
    :return:
    """
    start_time = time.perf_counter()
    token = request.args.get("token")
    if token is None or verify_token(token) is False:
        raise InpediaException(401, constants.RESPONSE_MESSAGE_UNAUTHORIZED)

    query = request.args.get("q")

    start_es= time.perf_counter()
    results = es_helper.query_es(query)
    took_es = time.perf_counter() - start_es

    res = dict()
    res['data'] = dict()
    res['data']['res'] = results

    time_taken = time.perf_counter() - start_time
    res['data']['meta'] = dict()
    res['data']['meta']['took'] = time_taken
    res['data']['meta']['es_took'] = took_es

    return make_response(jsonify(res), 200)


def verify_token(token):
    req_dict = {"token": token}
    r = requests.post('http://localhost:4000/api/jwt/check', data=req_dict)
    res = r.json()

    if 'success' in res:
        if res['success'] == "true":
            return True

    return False


@app.errorhandler(InpediaException)
def error_occurred(error):
    return make_response(error.to_json(), error.status_code)


@app.errorhandler(404)
def not_found(error):
    exception = InpediaException(404, constants.RESPONSE_MESSAGE_NOT_FOUND)
    return make_response(exception.to_json(), exception.status_code)


@app.errorhandler(400)
def bad_request(error):
    exception = InpediaException(400, constants.RESPONSE_MESSAGE_BAD_REQUEST)
    return make_response(exception.to_json(), exception.status_code)