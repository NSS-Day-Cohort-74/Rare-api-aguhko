from http.server import HTTPServer
from request_handler import RequestHandler, status
import json

from views import User
from views.category import Category
from views.posts import Post
from views.tag import Tag


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
        url = self.parse_url(self.path)
        if url["requested_resource"] == "tags":
            response = Tag().get_all()
            return self.response(response, status.HTTP_200_SUCCESS)

        elif url["requested_resource"] == "categories":
            response = Category().get_all()
            return self.response(response, status.HTTP_200_SUCCESS)
        elif url["requested_resource"] == "posts":
            print("Fetching posts...")
            response_body = Post().list_posts()
            return self.response(json.dumps(response_body), status.HTTP_200_SUCCESS)

    def do_POST(self):
        """Handle POST requests from client"""
        url = self.parse_url(self.path)

        content_len = int(self.headers.get("content-length", 0))
        request_body = self.rfile.read(content_len)
        request = json.loads(request_body.decode("UTF-8"))

        if url["requested_resource"] == "posts":
            Post().create_post(request)
            return self.response("", status.HTTP_201_SUCCESS_CREATED)
        elif url["requested_resource"] == "register":
            response = User().create_user(request)
            return self.response(response, status.HTTP_201_SUCCESS_CREATED)

        elif url["requested_resource"] == "login":
            response = User().login_user(request)
            if json.loads(response)["valid"] == True:
                return self.response(response, status.HTTP_200_SUCCESS)
            else:
                return self.response(response, status.HTTP_406_CLIENT_ERROR_NOT_ACCEPTABLE)

        elif url["requested_resource"] == "tags":
            response = Tag().create_tag(request)
            if response == True:
                return self.response("",status.HTTP_201_SUCCESS_CREATED)
            return self.response("", status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA)

        elif url["requested_resource"] == "categories":
            response = Category().create_category(request)
            if response == True:
                return self.response("",status.HTTP_201_SUCCESS_CREATED)
            return self.response("", status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA)

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
