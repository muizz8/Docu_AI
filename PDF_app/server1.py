import logging
import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import work  # Import the worker module

# Initialize Flask app and CORS
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.logger.setLevel(logging.ERROR)

# Define the route for the index page
@app.route('/', methods=['GET'])
def index():
    return render_template('main.html')  # Render the index.html template

# Define the route for processing messages
@app.route('/process-message', methods=['POST'])
def process_message_route():
    user_message = request.json['userMessage']  # Extract the user's message from the request
    print('user_message', user_message)

    bot_response = work.process_prompt(user_message)  # Process the user's message using the worker module

# Return the bot's response as JSON
    return jsonify({
    "botResponse": bot_response
}), 200

# Define the route for processing documents
@app.route('/process-document', methods=['POST'])
def process_document_route():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return jsonify({
            "botResponse":"It seems there's been a hiccup with the file upload. Could you please give it another shot? If the issue persists, you might want to try using a different file."
        }), 400

    file = request.files['file']  # Extract the uploaded file from the request

    file_path = file.filename  # Define the path where the file will be saved
    file.save(file_path)  # Save the file

    work.process_document(file_path)  # Process the document using the worker module

# Return a success message as JSON
    return jsonify({
    "botResponse": "Thanks for sharing your PDF document. I've finished analyzing it, so feel free to ask me any questions about it!"
}), 200

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=8000, host='0.0.0.0')