import random
import string

import gridfs
from flask.globals import current_app

from classifier import clf


def add_token(users):
    pool = string.ascii_letters + string.digits
    for user in users:
        user["token"] = ''.join(random.sample(pool, 32))


def gen_classification_result(documents):
    for document in documents:
        image_object = document.get('image')
        fs = gridfs.GridFS(current_app.data.driver.db)
        image_data = fs.get(image_object)
        result = clf.classify_image(image_data.read())
        document['result'] = result
