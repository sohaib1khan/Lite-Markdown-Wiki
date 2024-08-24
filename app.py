from flask import Flask, render_template, request, jsonify  # Import necessary modules from Flask
import os  # Import os module to handle file paths and directories
import markdown  # Import markdown module to convert markdown to HTML
from flask import send_from_directory  # Import function to serve files from a directory
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

app = Flask(__name__)  # Initialize the Flask web application

# Configure the folder paths to store uploaded images and articles
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')  # Path for uploaded images
ARTICLE_FOLDER = os.path.join(os.getcwd(), 'articles')  # Path for articles
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # Add upload folder path to app configuration
app.config['ARTICLE_FOLDER'] = ARTICLE_FOLDER  # Add article folder path to app configuration

# Ensure that the upload and article folders exist; if not, create them
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(ARTICLE_FOLDER):
    os.makedirs(ARTICLE_FOLDER)

# Route to serve the homepage
@app.route('/')
def index():
    return render_template('index.html')  # Renders the index.html page when the user visits the root URL

# Route to handle image uploads
@app.route('/upload', methods=['POST'])  # This route only accepts POST requests (file uploads)
def upload_file():
    if 'file' not in request.files:  # Check if the 'file' part is present in the request
        return jsonify({"error": "No file part"}), 400  # Return error if no file is provided

    file = request.files['file']  # Get the uploaded file

    if file.filename == '':  # Check if a file was selected
        return jsonify({"error": "No selected file"}), 400  # Return error if no file is selected

    if file:
        # Save the uploaded file
        filename = file.filename  # Get the file name
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # Define the file path
        file.save(filepath)  # Save the file to the upload folder

        # Return the URL of the uploaded file as a response
        return jsonify({"url": f"/uploads/{filename}"})

# Route to serve uploaded images to the user
@app.route('/uploads/<filename>')  # This route handles requests for uploaded files
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)  # Serve the file from the upload directory

# Route to save articles (create or update)
@app.route('/save-article', methods=['POST'])
def save_article():
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        return jsonify({"error": "Invalid data"}), 400

    filename = f"{title.replace(' ', '_')}.md"  # Ensure .md extension
    filepath = os.path.join(app.config['ARTICLE_FOLDER'], filename)

    # Save the article content to a file with UTF-8 encoding
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route to edit an existing article
@app.route('/edit-article', methods=['PUT'])  # This route only accepts PUT requests (used for updating data)
def edit_article():
    article_name = request.args.get('name')  # Get the name of the article to edit
    data = request.get_json()  # Get the JSON data from the request
    content = data.get("content")  # Extract the new content of the article

    if not content:  # Check if content is provided
        return jsonify({"error": "Invalid data"}), 400  # Return error if no content is provided

    article_path = os.path.join(app.config['ARTICLE_FOLDER'], article_name)  # Define the path for the article

    if not os.path.exists(article_path):  # Check if the article exists
        return jsonify({"error": "Article not found"}), 404  # Return error if the article is not found

    # Update the article content
    with open(article_path, 'w') as f:  # Open the article in write mode
        f.write(content)  # Write the updated content

    return jsonify({"success": True})  # Return success response

# Route to delete an article
@app.route('/delete-article', methods=['DELETE'])  # This route only accepts DELETE requests (used for deleting data)
def delete_article():
    article_name = request.args.get('name')  # Get the name of the article to delete
    article_path = os.path.join(app.config['ARTICLE_FOLDER'], article_name)  # Define the path for the article

    if not os.path.exists(article_path):  # Check if the article exists
        return jsonify({"error": "Article not found"}), 404  # Return error if the article is not found

    # Delete the article
    os.remove(article_path)  # Remove the article file

    return jsonify({"success": True})  # Return success response

# Route to get article content (for viewing or editing)
@app.route('/get-article', methods=['GET'])  # This route accepts GET requests
def get_article():
    article_name = request.args.get('name')  # Get the name of the article
    article_path = os.path.join(app.config['ARTICLE_FOLDER'], article_name)  # Define the path for the article

    if not os.path.exists(article_path):  # Check if the article exists
        return jsonify({"error": "Article not found"}), 404  # Return error if the article is not found

    # Read and return the article content
    with open(article_path, 'r') as f:  # Open the article in read mode
        article_content = f.read()  # Read the content of the article

    return article_content  # Return the article content as the response


# Route to list articles with fuzzy search
@app.route('/list-articles', methods=['GET'])
def list_articles():
    page = int(request.args.get('page', 1))
    per_page = 5
    search_query = request.args.get('query', '').strip()  # Get search query if provided

    # Get all article filenames in the articles folder
    article_files = sorted(os.listdir(app.config['ARTICLE_FOLDER']))

    # If a search query is provided, perform fuzzy search
    if search_query:
        # Perform fuzzy matching of the query against article filenames
        matching_articles = process.extract(search_query, article_files, limit=len(article_files))
        # Filter out articles with a score below a certain threshold (e.g., 60)
        matching_articles = [article for article, score in matching_articles if score > 60]
    else:
        # If no search query, just paginate the articles
        matching_articles = article_files

    # Paginate the articles
    start = (page - 1) * per_page
    end = start + per_page
    paginated_articles = matching_articles[start:end]

    return jsonify({
        "articles": paginated_articles,
        "has_more": end < len(matching_articles)  # Indicate if there are more articles
    })

# Route to view an article's content in HTML format
@app.route('/view-article', methods=['GET'])  # This route accepts GET requests
def view_article():
    article_name = request.args.get('name')  # Get the name of the article
    article_path = os.path.join(app.config['ARTICLE_FOLDER'], article_name)  # Define the path for the article

    if not os.path.exists(article_path):  # Check if the article exists
        return "Article not found", 404  # Return error if the article is not found

    # Read the article content
    with open(article_path, 'r') as f:  # Open the article in read mode
        article_content = f.read()  # Read the content of the article

    # Convert the Markdown content to HTML
    html_content = markdown.markdown(article_content)

    # Return an HTML page with the article content
    return f"""
    <html>
    <head>
        <title>{article_name.replace('.md', '')}</title>
    </head>
    <body>
        <div>
            {html_content}
        </div>
    </body>
    </html>
    """

# Entry point for running the Flask application
if __name__ == '__main__':
    app.run(debug=True, port=5008)  # Run the app in debug mode on port specified
