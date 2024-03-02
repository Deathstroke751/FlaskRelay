from flask import Flask, jsonify, request, session
import requests

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def index():
    return jsonify(message="Flask Relay Program is working!"), 200


@app.route('/relay', methods=['GET', 'POST'])
def relay():
    link = request.args.get(
        'link') if request.method == 'GET' else request.form.get('link')
    if not link:
        return jsonify(error="Link parameter is missing"), 400

    try:
        if request.method == 'GET':
            response = requests.get(link)
        else:
            response = requests.post(link, data=request.form)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify(error=str(e)), 500

    content_type = response.headers.get('Content-Type', '')
    if 'application/json' in content_type:
        return jsonify(response.json())
    else:
        return response.text


@app.route('/relaybrpost')
def relaybr():
    link = "https://www.bitrefill.com/api/accounts/cart"
    cart_id = request.args.get('cart_id')
    slug = request.args.get('slug')
    value = request.args.get('value')
    count = request.args.get('count')
    recipient = request.args.get('recipient')

    try:
        if slug and value and count:
            sesh = requests.Session()

            cookies = {
                "cart_id": cart_id
            }

            if recipient:
                payload = {
                    "slug": slug,
                    "count": count,
                    "value": value,
                    "recipient": recipient,
                    "is_gift": False,
                    "bill_payment_id": "",
                    "bill_account_id": ""
                }
            else:
                payload = {
                    "slug": slug,
                    "count": count,
                    "value": value,
                    "is_gift": False,
                    "bill_payment_id": "",
                    "bill_account_id": ""
                }

            sesh.cookies.update(cookies)
            response = sesh.post(link, json=payload)
        else:
            return jsonify(error="Parameters missing"), 400

    except requests.exceptions.RequestException as e:
        return jsonify(error=str(e)), 500

    content_type = response.headers.get('Content-Type', '')
    if 'application/json' in content_type:
        return jsonify(response.json())
    else:
        return response.text


@app.route('/brinvoice')
def invoice():
    link = "https://www.bitrefill.com/api/accounts/invoice"
    cart_id = request.args.get('cart_id')
    email = request.args.get('email')
    method = request.args.get('method')

    try:
        if cart_id and email and method:

            headers = {
                "Content-Type": "application/json",
            }

            payload = {
                "cart_id": cart_id,
                "email": email,
                "isSubscribing": False,
                "paymentMethod": method,
                "unsealAll": False,
                "isLifiSwap": False,
                "is_batch": False,
                "is_embedded": False,
                "user_source": "web",
                "user_source_platform": "web"
            }

            response = requests.post(link, headers=headers, json=payload)
        else:
            return jsonify(error="Parameters missing"), 400

    except requests.exceptions.RequestException as e:
        return jsonify(error=str(e)), 500

    content_type = response.headers.get('Content-Type', '')
    if 'application/json' in content_type:
        return jsonify(response.json())
    else:
        return response.text


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8880, debug=True)
