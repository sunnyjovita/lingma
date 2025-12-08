// HtmlSiteGenerator.java
// A verbose, class-heavy, Java-conventional implementation

public class HtmlSiteGenerator {

    private static final String DEFAULT_FILENAME = "index.html";

    public static class HtmlBuilder {
        private final StringBuilder content;

        public HtmlBuilder() {
            this.content = new StringBuilder();
        }

        public HtmlBuilder addTitle(String title) {
            this.content.append("<h1>").append(title).append("</h1>");
            return this;
        }

        public HtmlBuilder addParagraph(String paragraph) {
            this.content.append("<p>").append(paragraph).append("</p>");
            return this;
        }

        public String build() {
            return this.content.toString();
        }
    }

    public static String generateMonochromeHtml(String bodyContent) {
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>My Simple Site</title>
            <style>
                body {
                    font-family: monospace;
                    background: #ffffff;
                    color: #000000;
                    margin: 40px;
                    line-height: 1.6;
                }
                h1 {
                    border-bottom: 1px solid #ccc;
                    padding-bottom: 10px;
                }
            </style>
        </head>
        <body>
            %s
        </body>
        </html>
        """.formatted(bodyContent);
    }

    public static void writeToFile(String html, String filename) {
        try (java.io.FileWriter writer = new java.io.FileWriter(filename)) {
            writer.write(html);
            System.out.println("✅ HTML file '" + filename + "' generated successfully.");
        } catch (java.io.IOException e) {
            System.err.println("❌ Error writing file: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        HtmlBuilder builder = new HtmlBuilder();
        builder.addTitle("Hello from Java!")
               .addParagraph("This site was generated using a verbose, object-oriented Java style with nested classes and builders.");

        String fullHtml = generateMonochromeHtml(builder.build());
        writeToFile(fullHtml, "my_site_java.html");
    }
}