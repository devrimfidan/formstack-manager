# temp_app.py
from flask import Flask

# Initialize the Flask application
app = Flask(__name__)

# Define a simple route for the root URL
@app.route('/')
def hello_world():
    """
    Returns a simple greeting message.
    """
    return 'Hello from Flask! If you see this, Flask is working correctly.'

# Run the application if this script is executed directly
if __name__ == '__main__':
    # Run in debug mode for detailed error messages
    # Use port 5000, which is the default for Flask
    app.run(debug=True, port=5000)

