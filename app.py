from flask import Flask, jsonify, request, session
import requests

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def index():
    return jsonify(message="Flask Relay Program is working!"), 200


@app.route('/relay', methods=['GET', 'POST'])
def relay():
    link = request.args.get('link')
    if not link:
        return jsonify(error="Link parameter is missing"), 400

    try:
        if request.method == 'GET':
            response = requests.get(link, cookies=session.get('cookies'))
        else:
            response = requests.post(
                link, data=request.form, cookies=session.get('cookies'))

        response.raise_for_status()
        # Update session cookies
        session['cookies'] = response.cookies.get_dict()
    except requests.exceptions.RequestException as e:
        return jsonify(error=str(e)), 500

    content_type = response.headers.get('Content-Type', '')
    if 'application/json' in content_type:
        return jsonify(response.json())
    else:
        return response.text


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8880, debug=True)
