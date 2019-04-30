from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers

import logging

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload = self.get_uploads()[0]

        logging.info("here")
        logging.info(upload.key())
        self.redirect('/?blobkey='+str(upload.key()))
