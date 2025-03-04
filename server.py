from http.server import HTTPServer
from RequestHandler import RequestHandler, status
import json
from views import User

banner = r"""
                                                       _
 ___  ___ _ ____   _____ _ __   _ __ _   _ _ __  _ __ (_)_ __   __ _
/ __|/ _ \ '__\ \ / / _ \ '__| | '__| | | | '_ \| '_ \| | '_ \ / _` |
\__ \  __/ |   \ V /  __/ |    | |  | |_| | | | | | | | | | | | (_| |_ _ _
|___/\___|_|    \_/ \___|_|    |_|   \__,_|_| |_|_| |_|_|_| |_|\__, (_|_|_)
                                                               |___/
"""


class RareApi(RequestHandler):
   def do_GET(self):
        """Handle Get requests from client"""
 
        
   def do_POST(self):
        """Handle POST requests from client"""

   def do_PUT(self):
        """Handle PUT requests from client"""


   def do_DELETE(self):
        """Handle DELETE requests from client"""




def main():
    host = ""
    port = 8088
    HTTPServer((host, port), RareApi).serve_forever()


if __name__ == "__main__":
    print(banner)
    main()
