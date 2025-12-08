# generate_site.py
# 
# Purpose: 
# This script automatically generates a simple, static HTML webpage using Python.
# It defines a function to create a clean, monochrome-styled HTML file from a given content string.
# When run directly, it produces a sample webpage titled "my_site_python.html".
#
# Features:
# - Minimal design using inline CSS (monospace font, black text on white background)
# - Responsive viewport meta tag for mobile compatibility
# - User-friendly success message after file creation
#
# How to use:
# Run this script with Python: `python generate_site.py`
# Output: A file named "my_site_python.html" will be created in the same directory.

import os  # (Note: imported but not currently used—can be removed if unnecessary)

def generate_html(content: str, filename: str = "index.html") -> None:
    """
    Generates a complete HTML file with embedded CSS styling.
    
    Parameters:
        content (str): The HTML content to insert into the <body> tag.
        filename (str): The name of the output HTML file (default: "index.html").
    """
    # Define the full HTML structure as an f-string, inserting user-provided content
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Simple Site</title>
    <style>
        body {{
            font-family: monospace;
            background: #ffffff;
            color: #000000;
            margin: 40px;
            line-height: 1.6;
        }}
        h1 {{
            border-bottom: 1px solid #ccc;
            padding-bottom: 10px;
        }}
    </style>
</head>
<body>
    {content}
</body>
</html>"""
    
    # Write the complete HTML string to a file with UTF-8 encoding
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_template)
    
    # Notify the user that the file was successfully created
    print(f"✅ HTML file '{filename}' generated successfully.")


def main():
    """Main function: defines sample content and calls the HTML generator."""
    # Sample content to display on the webpage
    welcome_msg = "<h1>Hello from Python!</h1><p>This site was generated using Sunny's clean and minimal Python style.</p>"
    
    # Generate the HTML file with the sample content and a custom filename
    generate_html(welcome_msg, "my_site_python.html")


# Entry point: run main() only when the script is executed directly (not imported)
if __name__ == "__main__":
    main()