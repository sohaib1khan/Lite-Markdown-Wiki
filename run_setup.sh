#!/bin/bash

# Set variables
PROJECT_DIR=$(pwd)                  # Get the current working directory
REQUIREMENTS_FILE="requirements.txt" # Name of the requirements file
HOST="127.0.0.1"                    # Host address for the Flask server
PORT="5008"                         # Port where Flask will run

# Create a virtual environment if it doesn't exist
if [ ! -d "$PROJECT_DIR/venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install the required libraries (Flask and markdown)
echo "Installing Flask and markdown..."
pip install Flask markdown

# Run the Flask application in the background
echo "Launching Flask server..."
FLASK_APP=app.py flask run --host=$HOST --port=$PORT &
FLASK_PID=$! # Capture the process ID of the Flask server

# Display the access URL and process ID
echo "The Flask server is running!"
echo "You can access the website at: http://$HOST:$PORT"
echo "To stop the server, use the following command:"
echo "kill $FLASK_PID"

# Wait for the Flask process to exit (optional if you want the script to keep running)
wait $FLASK_PID
