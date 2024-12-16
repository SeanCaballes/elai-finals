from flask import Flask, render_template, request, jsonify
import os
import re

app = Flask(__name__)

EXTRACTED_TEXT_FOLDER = 'extracted_text'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_relevant_text', methods=['POST'])
def get_relevant_text():
    user_query = request.form.get('query', '').strip().lower()
    if not user_query or len(user_query) > 100:  # Validate query
        return jsonify({'status': 'error', 'text': "Please enter a valid and concise query."})

    relevant_text = []

    if not os.path.exists(EXTRACTED_TEXT_FOLDER):
        return jsonify({'status': 'error', 'text': "No extracted text files available for search."})

    for filename in os.listdir(EXTRACTED_TEXT_FOLDER):
        if filename.endswith('.txt'):
            with open(os.path.join(EXTRACTED_TEXT_FOLDER, filename), 'r', encoding='utf-8') as file:
                text = file.read().lower()
                match = re.search(r'\b' + re.escape(user_query) + r'\b', text)
                if match:
                    start_idx = match.start()
                    end_idx = match.end()
                    context = text[max(0, start_idx - 50):min(len(text), end_idx + 150)]
                    relevant_text.append(context.strip())

    if relevant_text:
        return jsonify({'status': 'success', 'results': relevant_text})
    else:
        return jsonify({'status': 'success', 'text': "Sorry, I couldn't find anything related to your query."})

if __name__ == '__main__':
    app.run(debug=True)
