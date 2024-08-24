document.addEventListener('DOMContentLoaded', function () {
    // Dark/Light mode toggle
    const toggleSwitch = document.getElementById("darkModeToggle");  // Get the toggle switch for dark/light mode

    toggleSwitch.addEventListener('change', function () {
        if (this.checked) {
            // Switch to dark mode
            document.body.classList.add("dark-mode");
            document.body.classList.remove("light-mode");
            updateEditorMode(true);  // Update the editor to dark mode styling
        } else {
            // Switch to light mode
            document.body.classList.add("light-mode");
            document.body.classList.remove("dark-mode");
            updateEditorMode(false);  // Update the editor to light mode styling
        }
    });

    // Function to update the editor style based on the current theme (dark/light mode)
    function updateEditorMode(isDarkMode) {
        const editorEl = document.querySelector('.toastui-editor');  // Get the editor element
        const toolbar = document.querySelector('.toastui-editor-toolbar');  // Get the toolbar element
        if (isDarkMode) {
            // Apply dark mode styles
            editorEl.style.backgroundColor = '#2e2e2e';  // Dark background
            editorEl.style.color = '#ffffff';  // Light text
            toolbar.style.backgroundColor = '#444444';  // Dark toolbar background
        } else {
            // Apply light mode styles
            editorEl.style.backgroundColor = '#ffffff';  // Light background
            editorEl.style.color = '#000000';  // Dark text
            toolbar.style.backgroundColor = '#f4f4f4';  // Light toolbar background
        }
    }

    let currentPage = 1;  // Track the current page number for article pagination
    const articleList = document.getElementById("articleList");  // Get the article list element
    const loadMoreButton = document.getElementById("loadMoreButton");  // Get the "Load More" button
    const searchButton = document.getElementById("searchButton");  // Get the search button element
    const searchQuery = document.getElementById("searchQuery");  // Get the search query input

    // Initialize the Toast UI Editor with image upload handling
    const editor = new toastui.Editor({
        el: document.querySelector('#editor'),  // Set the editor container element
        height: '500px',  // Set the height of the editor
        initialEditType: 'markdown',  // Set the initial content type to markdown
        previewStyle: 'vertical',  // Display the preview vertically
        hooks: {
            addImageBlobHook: (blob, callback) => {
                // Handle image uploads
                const formData = new FormData();
                formData.append("file", blob);  // Attach the image as form data

                // Send the image to the server
                fetch("/upload", {
                    method: "POST",
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.url) {
                        // Insert the image URL into the editor
                        callback(data.url, 'image');
                    } else {
                        alert("Failed to upload image.");  // Alert if upload fails
                    }
                })
                .catch(err => {
                    console.error("Error:", err);  // Log any errors
                });

                return false;
            }
        }
    });

    // Update editor mode when the page loads based on the current theme
    const isDarkModeOnLoad = document.body.classList.contains('dark-mode');  // Check if dark mode is enabled
    updateEditorMode(isDarkModeOnLoad);  // Update the editor style

    // Save article when the "Save Article" button is clicked
    document.getElementById("saveButton").addEventListener("click", function() {
        const content = editor.getMarkdown();  // Get the markdown content from the editor
        const title = document.getElementById("articleTitle").value;  // Get the article title from input

        if (!title || !content) {  // Check if both title and content are provided
            alert("Please provide a title and content for the article.");
            return;
        }

        // Send the article title and content to the server for saving
        fetch("/save-article", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"  // Set the request content type to JSON
            },
            body: JSON.stringify({ title: title, content: content })  // Send the data as JSON
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Article saved successfully!");  // Alert on successful save
            } else {
                alert("Failed to save the article.");  // Alert on failure
            }
        })
        .catch(err => {
            console.error("Error:", err);  // Log any errors
        });
    });

    // Function to load and display articles in the list with fuzzy search
    function loadArticles(query = "") {
        fetch(`/list-articles?page=${currentPage}&query=${query}`)  // Fetch articles for the current page and query
            .then(response => response.json())
            .then(data => {
                data.articles.forEach(article => {
                    const li = document.createElement("li");  // Create a list item for each article
                    const articleTitle = article.replace('.md', '');  // Remove .md extension from the filename

                    // Create a clickable link for viewing the article, and buttons for editing and deleting
                    li.innerHTML = `
                        <a href="/view-article?name=${article}" target="_blank">${articleTitle}</a>
                        <button onclick="editArticle('${article}')">Edit</button>
                        <button onclick="deleteArticle('${article}')">Delete</button>
                    `;
                    articleList.appendChild(li);  // Add the article to the list
                });

                if (!data.has_more) {  // If no more articles are available, hide the "Load More" button
                    loadMoreButton.style.display = "none";
                }
            })
            .catch(err => {
                console.error("Error:", err);  // Log any errors
            });
    }

    // Load the first set of articles when the page loads
    loadArticles();

    // Load more articles when the "Load More" button is clicked
    loadMoreButton.addEventListener("click", function() {
        currentPage++;  // Increment the page number
        loadArticles();  // Load the next set of articles
    });

    // Perform search when the "Search" button is clicked
    searchButton.addEventListener("click", function() {
        const query = searchQuery.value.trim();  // Get the search query
        if (query) {
            currentPage = 1;  // Reset the page number
            articleList.innerHTML = "";  // Clear the current article list
            loadArticles(query);  // Load articles based on the search query
        }
    });

    // Function to open an article in a new tab
    window.openNewTab = function(article) {
        window.open(`/view-article?name=${article}`, '_blank');  // Open the article in a new browser tab
    };

    // Function to edit an article
    window.editArticle = function(article) {
        fetch(`/get-article?name=${article}`)  // Fetch the article content from the server
            .then(response => response.text())
            .then(content => {
                // Load the article content into the editor for editing
                editor.setMarkdown(content);
                document.getElementById("articleTitle").value = article.replace('.md', '');  // Set the article title in the input
            })
            .catch(err => {
                console.error("Error fetching article content:", err);  // Log any errors
            });
    };

    // Function to delete an article
    window.deleteArticle = function(article) {
        if (confirm("Are you sure you want to delete this article?")) {  // Confirm before deleting
            fetch(`/delete-article?name=${article}`, {
                method: "DELETE"  // Send a DELETE request to the server
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("Article deleted successfully!");  // Alert on successful deletion
                    // Reload the article list
                    articleList.innerHTML = '';  // Clear the current list
                    currentPage = 1;  // Reset the current page
                    loadArticles();  // Reload the articles
                } else {
                    alert("Failed to delete the article.");  // Alert on failure
                }
            })
            .catch(err => {
                console.error("Error deleting article:", err);  // Log any errors
            });
        }
    };
});
