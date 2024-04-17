#!/opt/homebrew/bin/python3

def generate_json(file_name):
    try:
        file = open(file_name, 'r')
    except OSError as e:
        print('open() failed', e)
        quit(1)
    else:
        with file:
            lines = file.readlines()
            json = "{\n\t\"slides\": [\n"
            adding_text = False
            for i, line in enumerate(lines):
                if line == '' or line == '\n':
                    if adding_text:
                        json += f']\n\t\t}},\n'
                        adding_text = False
                    continue
                is_img = line.startswith('@')
                if is_img:
                    json += "\t\t{\n"
                    json += f'\t\t\t"type": "image",\n'
                    json += f'\t\t\t"url": "{line[1:]}"\n\t\t}}'
                    if i == len(lines) - 1:
                        json += "\n"
                    else:
                        json += ",\n"
                    adding_text = False
                else:
                    if adding_text:
                        json += f', "{line.strip()}"'
                    else:
                        json += "\t\t{\n"
                        json += f'\t\t\t"type": "text",\n'
                        json += f'\t\t\t"content": ["{line.strip()}"'
                        adding_text = True
            if adding_text:
                json += f']\n\t\t}}\n'

            json += "\t]\n}"
            return json

html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>mini-keynote</title>
    <script type="module" defer>
        // Get the body element
        const insert_here = document.getElementById('insert_here');

        // Set the initial slide index
        let slideIndex = 0;
        let slideLength = 1;
        // Function to update the slide
        function updateSlide() {
            // Clear the body content
            insert_here.innerHTML = '';
            fetch('./slides.json')
            .then(response => response.json()).then(data => data.slides)
            .then(slides => {
                const slide = slides[slideIndex % slides.length];
                slideLength = slides.length;

                if (slide.type === 'text') {
                    const p = document.createElement('p');
                    let fontmultiplier = 1;
                    if (slide.content.length == 1) {
                        insert_here.style.fontWeight = '600'
                        insert_here.style.textAlign = 'center';
                    } else {
                        insert_here.style.fontWeight = '400'
                        insert_here.style.textAlign = 'left';
                        fontmultiplier = .8;
                    }
                    p.textContent = slide.content.join('\\n');
                    p.style.fontSize = `calc(6.4vw * ${fontmultiplier})`;

                    insert_here.appendChild(p);
                } else if (slide.type === 'image') {
                    const img = document.createElement('img');
                    img.src = slide.url;
                    img.className = 'centered';
                    img.style.height = '800px';
                    insert_here.appendChild(img);
                }
            });
        }

        function invertColors() {
            if (document.body.style.backgroundColor === 'black') {
                document.body.style.backgroundColor = 'white';
                document.body.style.color = 'black';
                return;
            }
            document.body.style.backgroundColor = 'black';
            document.body.style.color = 'white';

        }

        // Function to handle key events
        function handleKeyEvents(event) {
            if (event.key === 'ArrowLeft') {
                // Decrease the slide index
                if (slideIndex !== 0) {
                    slideIndex--
                    updateSlide();
                }
            } else if (event.key === 'ArrowRight') {
                // Increase the slide index
                if (slideIndex !== slideLength - 1) {
                    slideIndex++;
                    updateSlide();
                }
            } else if (event.key === 'i') {
                invertColors();
            }
        }

        // Add event listener for keydown events
        document.addEventListener('keydown', handleKeyEvents);

        // Initial update of the slide
        updateSlide();
    </script>
    <style>
        body {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            background-color: black;
            color: white;
        }
        
        p {
            line-height: 1.4;
        }
        
        .centered {
            position: fixed; /* or absolute */
            top: 50%;
            left: 50%;
            /* bring your own prefixes */
            transform: translate(-50%, -50%);
          }
    </style>
</head>
<body style="width: 100%;">
    <div id="insert_here" class="centered"  style="white-space: pre-wrap; width: 80%">
    </div>
</body>
</html>
"""

import sys
import http.server
import socketserver
import os

PORT = 8000

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
    # This is to suppress the logging of every request to the server
    def log_message(self, format, *args):
        if self.server.logging:
            http.server.SimpleHTTPRequestHandler.log_message(self, format, *args)


handler_object = MyHttpRequestHandler

# Custom server to suppress logging
class MyServer(socketserver.TCPServer):
    allow_reuse_address = True 
    logging = False


def main():
    if len(sys.argv) < 2:
        print("Make sure to specify which file you want to present from.")
        return
    file_name = sys.argv[1]
    
    json = generate_json(file_name)
    with open("slides.json", 'w') as f:
        print('Created temporary slides.json file.')
        f.write(json)
    
    with open("index.html", 'w') as f:
        print('Created temporary index.html file.')
        f.write(html)

    with MyServer(("", PORT), handler_object) as httpd:
        print("Server started at http://localhost:" + str(PORT))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Server stopped.")
            pass
        finally:
            # Close the server
            httpd.server_close()
            os.remove("slides.json")
            os.remove("index.html")
            print("Removed temporary files.")
    

if __name__ == '__main__':
    main()
