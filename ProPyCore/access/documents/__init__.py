from .files import Files
from .folders import Folders
from .document_index import DocumentIndex


class Documents:
    def __init__(self, access_token, server_url):
        self.files = Files(access_token, server_url)
        self.folders = Folders(access_token, server_url)
        self.documents = DocumentIndex(access_token, server_url)
