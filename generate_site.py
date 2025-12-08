#!/usr/bin/env python3

class HtmlBuilder:
    def __init__(self):
        self.content = []

    def add_title(self, title):
        self.content.append(f"<h1>{title}</h1>")
        return self

    def add_paragraph(self, paragraph):
        self.content.append(f"<p>{paragraph}</p>")
        return self

    def build(self):
        return "".join(self.content)


def generate_monochrome_html(body_content):
    return f"""<!DOCTYPE html>
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
    {body_content}
</body>
</html>
"""


def write_to_file(html, filename):
    try:
        with open(filename, 'w') as writer:
            writer.write(html)
        print(f"✅ HTML file '{filename}' generated successfully.")
    except IOError as e:
        print(f"❌ Error writing file: {e}")


def main():
    builder = HtmlBuilder()
    builder.add_title("Hello from Java!") \
           .add_paragraph("This site was generated using a verbose, object-oriented Java style with nested classes and builders.")

    full_html = generate_monochrome_html(builder.build())
    write_to_file(full_html, "my_site_java.html")


if __name__ == "__main__":
    main()