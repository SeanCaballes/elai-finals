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
    user_query = request.form.get('query', '').strip().lower()  # Get the user's query and convert to lowercase
    if not user_query:
        return jsonify({'text': "Please enter a valid query."})  # Check for empty query

    relevant_text = []

    # Check if the extracted text folder exists
    if os.path.exists(EXTRACTED_TEXT_FOLDER):
        for filename in os.listdir(EXTRACTED_TEXT_FOLDER):
            if filename.endswith('.txt'):
                with open(os.path.join(EXTRACTED_TEXT_FOLDER, filename), 'r', encoding='utf-8') as file:
                    text = file.read().lower()  # Read the file and convert the extracted text to lowercase

                    # Print the text and user query for debugging
                    print(f"Searching in file: {filename}")
                    print(f"User Query: {user_query}")
                    print(f"Extracted Text: {text[:200]}...")  # Print the first 200 characters for debugging

                    # Use regular expression to find any part of the text that matches the query
                    match = re.search(r'\b' + re.escape(user_query) + r'\b', text)
                    if match:
                        start_idx = match.start()
                        end_idx = match.end()
                        context = text[max(0, start_idx - 50):min(len(text), end_idx + 150)]  # 50 chars before, 150 after
                        relevant_text.append(context.strip())

    if relevant_text:
        return jsonify({'text': '\n\n'.join(relevant_text)})
    else:
        return jsonify({'text': "Sorry, I couldn't find anything related to your query."})

if __name__ == '__main__':
    app.run(debug=True)
