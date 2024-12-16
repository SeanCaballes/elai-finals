from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

GEMINI_API_KEY = 'AIzaSyD382Lp17CtEnJzZUlMix5sczcb6waqVcI'
GEMINI_API_URL = 'https://api.gemini.com/v1/query'  # Replace with the correct Gemini API endpoint

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_relevant_text', methods=['POST'])
def get_relevant_text():
    user_query = request.form.get('query', '').strip().lower()
    if not user_query or len(user_query) > 100:  # Validate query
        return jsonify({'status': 'error', 'text': "Please enter a valid and concise query."})

    headers = {
        'Authorization': f'Bearer {GEMINI_API_KEY}',  # Add your Gemini API key in the Authorization header
    }

    data = {
        'query': user_query,  # The query sent to the Gemini API
    }

    # Make POST request to Gemini API
    response = requests.post(GEMINI_API_URL, headers=headers, json=data)

    # Debugging: Print status code and response content
    print(f"API Response Status Code: {response.status_code}")
    print(f"API Response Content: {response.text}")

    if response.status_code == 200:
        try:
            response_data = response.json()
            if 'text' in response_data:
                bot_response = response_data['text']
                return jsonify({'status': 'success', 'results': [bot_response]})
            else:
                return jsonify({'status': 'success', 'text': "Sorry, I couldn't find anything related to your query."})
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            return jsonify({'status': 'error', 'text': "Error parsing the response from Gemini API."})
    else:
        return jsonify({'status': 'error', 'text': f"Error contacting Gemini API: {response.text}"})


if __name__ == '__main__':
    app.run(debug=True)
