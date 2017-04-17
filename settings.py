import os

# Environment setup
from auth import RolesAuth

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
HOST = '0.0.0.0'
PORT = 5000 if 'PORT' not in os.environ else int(os.environ.get('PORT'))

# MongoDB
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
# MONGO_USERNAME = 'admin'
# MONGO_PASSWORD = '123456'
MONGO_DBNAME = 'plantpano'

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']
PUBLIC_METHODS = ['GET']
PUBLIC_ITEM_METHODS = ['GET']

PAGINATION_DEFAULT = 15

CACHE_CONTROL = 'max-age=20'
CACHE_EXPIRES = 20

# Resources on API
users = {
    'item_title': 'users',
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'username'
    },
    'schema': {
        'username': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 128,
            'required': True,
            'unique': True,
        },
        'password': {
            'type': 'string',
            'required': True,
        },
        'roles': {
            'type': 'list',
            'allowed': ['user', 'superuser', 'admin'],
            'required': True,
        },
        'token': {
            'type': 'string',
            'required': True,
        },

    },
    'cache_control': '',
    'cache_expires': 0,
    'resource_methods': ['GET', 'POST', 'DELETE'],

    # Only allow superusers and admins.
    'allowed_roles': ['superuser', 'admin'],
    'authentication': RolesAuth,
    'extra_response_fields': ['token'],

    'public_methods': ['POST'],
    'public_item_methods': ['POST'],
}
images = {
    'item_title': 'uploaded_images',
    'schema': {
        'name': {
            'type': 'string',
            'required': True,
        },
        'image': {
            'type': 'media',
            'required': True,
        },
        'result': {
            'type': 'list',
        },
        'user': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'users',
                'field': '_id',
                'embeddable': True,
            }
        },
        'is_pub': {
            'type': 'boolean',
        },
        'like': {
            'type': 'integer',
        },
        'review': {
            'type': 'integer',
        },
        'comment': {
            'type': 'list',
        }
    },
    'resource_methods': ['GET', 'POST'],
    'extra_response_fields': ['result'],
    'datasource': {
        'projection': {
            'result': 0,
        }
    }
}
comments = {
    'item_title': 'comments',
    'schema': {
        'content': {
            'type': 'string',
        },
        'user': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'users',
                'field': '_id',
                'embeddable': True,
            }
        },
    }
}
articles = {
    'item_title': 'articles',
    'schema': {
        'title': {
            'type': 'string',
            'required': True,
        },
        'author': {
            'type': 'string',
        },
        'view': {
            'type': 'integer',
        },
        'detail_link': {
            'type': 'string',
        }
    }
}
articles_detail = {
    'item_title': 'articles_detail',
    'schema': {

    }
}

# disable default behaviour
RETURN_MEDIA_AS_BASE64_STRING = False

# return media as URL instead
RETURN_MEDIA_AS_URL = True

DOMAIN = {
    'users': users,
    'images': images,
}

# Upload
UPLOAD_FOLDER = os.path.join(WORKING_DIR, 'uploads')
ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'tiff', 'bmp']

# TensorFlow
TF_NUM_CLASSES = 5
TF_NUM_TOP_CLASSES = 5
TF_DATA_FOLDER = os.path.join(WORKING_DIR, 'data')

# Response codes and messages
CODE_CLASSIFY_SUCCESS = 0
MESSAGE_CLASSIFY_SUCCESS = 'success'
