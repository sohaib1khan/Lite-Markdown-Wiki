# Lite Markdown Wiki

## Description
Lite Markdown Wiki is a simple Flask-based web application that allows users to create, edit, delete, and view markdown articles. It also supports file uploads and provides a fuzzy search to list articles. The app uses the **Toast UI Editor** for a rich markdown editing experience, and offers both dark and light modes for user preference.

## Project Structure
```
├── app.py # The main Flask application script
├── articles # Directory where markdown articles are stored
├── README.md # This README file
├── requirements.txt # Python dependencies for the project
├── run_setup.sh # Shell script to set up the virtual environment and run the Flask app
├── static # Directory for static assets (CSS, JS)
│ ├── app.js # JavaScript for frontend logic
│ └── styles.css # CSS for styling the web app
├── templates # HTML templates
│ └── index.html # Main HTML file for the editor interface
└── uploads # Directory where uploaded images are stored
```
## Features
- Create, edit, view, and delete markdown articles.
- Fuzzy search for listing and finding articles.
- Upload and embed images in markdown articles.
- Dark and light mode toggle.
- Pagination support for articles listing.
- Easy to set up with a single shell script.

## Setup and Installation

1. Clone the repository:

   ```bash
   git clone repo
   cd Lite_Markdown_Wiki


2. Run the setup script to create a virtual environment, install dependencies, and launch the Flask server:
```
./run_setup.sh
```
The app will run on http://127.0.0.1:5008.

3. Access the app via the browser at http://127.0.0.1:5008.

- ## API Endpoints
    
    - `/` - Renders the homepage with the markdown editor.
    - `/upload` - Handles image file uploads.
    - `/save-article` - Saves new markdown articles.
    - `/edit-article` - Updates existing articles.
    - `/delete-article` - Deletes articles.
    - `/get-article` - Retrieves content for a specific article.
    - `/list-articles` - Lists articles with optional fuzzy search.
    - `/view-article` - Displays a specific article in HTML format.
    
    ## Requirements
    
    - Python 3.6 or higher
    - Flask
    - Toast UI Editor for markdown editing
    - [FuzzyWuzzy](https://github.com/seatgeek/fuzzywuzzy) for fuzzy search
    
    You can find all required Python libraries in the `requirements.txt` file. Install them using:
    

## Demo
