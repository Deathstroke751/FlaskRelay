from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify(message="Flask Relay Program is working!"), 200


@app.route('/relay')
def relay():
    link = request.args.get('link')
    if not link:
        return jsonify(error="Link parameter is missing"), 400

    try:
        response = requests.get(link)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify(error=str(e)), 500

    content_type = response.headers.get('Content-Type', '')
    if 'application/json' in content_type:
        return jsonify(response.json())
    else:
        return response.text


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)