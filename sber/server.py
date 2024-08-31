from flask import Flask, request
from werkzeug.exceptions import BadRequest
from sber import calc
import traceback
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    json_present = request.is_json
    if not json_present:
        return "Application required json to be passed", 400
    try:
        data = request.json
        result = calc.calculate_percents(data)
    except BadRequest:
        return 'Json format is not valid', 400
    except ValueError as e:
        return str(e), 400
    except Exception:
        app.logger.error(traceback.format_exc())
        return 'Internal server error', 500
    return result


@app.errorhandler(404)
def wrong_route(error):
    return "No such endpoint", 404
