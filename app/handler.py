import base64
import json
import re

from Crypto.Cipher import AES
from tornado.web import RequestHandler


class Controller(RequestHandler):

    PATH = None

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

    @classmethod
    def register(cls, application):
        application.add_handlers(".*$", [(cls.PATH, cls)])

    def set_default_headers(self):
        self.set_header('Content-Type', 'text/plain')

    def session(self):
        base = self.get_cookie('PYC_ELEARN')
        content = base64.b64decode(re.sub('%\w{2}$', '===', base))
        content = content.decode('utf-8')
        detail = json.loads(content)
        AES.key_size = 16
        iv = base64.b64decode(detail['iv'])
        key = "9kUdngvdFXDOxGnAjuc6jY9zvS9itsu5"
        crypt = AES.new(key=key, IV=iv, mode=AES.MODE_CBC)

        content = base64.b64decode(detail['value'])
        content = crypt.decrypt(content)

        content = content.decode('utf-8')
        content = re.sub('\";.*$', '', content)
        session_id = re.sub('^.*\"', '', content)

        return session_id

    def db(self, engine='mysql'):
        return self.application.db[engine]


class JsonController(Controller):
    def prepare(self):
        # Incorporate request JSON into arguments dictionary.
        if self.request.body:
            try:
                json_data = json.loads(self.request.body)
                self.request.arguments.update(json_data)
            except ValueError:
                message = 'Unable to parse JSON.'
                self.send_error(400, message=message)

    def set_default_headers(self):
        self.set_header('Content-Type', 'text/JSON')

    def write_error(self, status_code, **kwargs):
        if 'message' not in kwargs:
            if status_code == 405:
                kwargs['message'] = 'Invalid HTTP method.'
            else:
                kwargs['message'] = 'Unknown error.'

        self.write_json(kwargs)

    def write_json(self, content):
        output = json.dumps(content)
        self.write(output)
