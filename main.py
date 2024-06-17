from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Perfect Tense API configuration
PERFECT_TENSE_APP_KEY = 'your_app_key_here'
USER_API_KEY = 'user_api_key_here'
PERFECT_TENSE_API_URL = 'https://api.perfecttense.com'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/check_text', methods=['POST'])
def check_text():
    data = request.get_json()

    if 'text' not in data:
        return jsonify({"error": "Missing 'text' field"}), 400

    text_to_check = data['text']

    # Prepare the payload for the Perfect Tense API
    payload = {
        'text': text_to_check,
        'app_key': PERFECT_TENSE_APP_KEY,
        'api_key': USER_API_KEY,
        'check_spell': True  # Enable spell checking
    }

    # Send a request to the Perfect Tense API
    response = requests.post(PERFECT_TENSE_API_URL, json=payload)

    if response.status_code == 200:
        result = response.json()
        corrected_text = result.get('corrected', text_to_check)
        spell_checked_text = result.get('spell_checked', corrected_text)
        return jsonify({"result": spell_checked_text})
    else:
        return jsonify({"error": "Failed to check text"}), response.status_code


if __name__ == '__main__':
    app.run(debug=True)
