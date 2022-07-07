import json

class MockRequest():
    def __init__(self, status_code, content=[]):
        self.status_code = status_code
        if isinstance(content, (list, tuple, dict)):
            self.data = content
        else:
            self.data = json.dumps(content)

    def get(self, url, headers):
        return self
    
    def json(self):
        return self.data