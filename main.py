def generate_json(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()
        json = "{\n\t\"slides\": [\n"
        adding_text = False
        for i, line in enumerate(lines):
            if line == '' or line == '\n':
                if adding_text:
                    json += f']\n\t\t}}\n,'
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


import sys
import http.server
import socketserver

PORT = 8000

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

handler_object = MyHttpRequestHandler


def main():
    if len(sys.argv) < 2:
        print("Make sure to specify which file you want to present from.")
        return
    file_name = sys.argv[1]

    json = generate_json(file_name)
    with open("slides.json", 'w') as f:
        f.write(json)

    with socketserver.TCPServer(("", PORT), handler_object) as httpd:
        print("Server started at http://localhost:" + str(PORT))
        httpd.serve_forever()
    

if __name__ == '__main__':
    main()