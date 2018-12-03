import boto3, botocore
from app.config import S3_KEY, S3_SECRET, S3_BUCKET, S3_LOCATION
import os
from dotenv import load_dotenv
import braintree
from authlib.flask.client import OAuth
import app.config

s3 = boto3.client(
   "s3",
   aws_access_key_id=S3_KEY,
   aws_secret_access_key=S3_SECRET
)

def upload_file_to_s3(file, bucket_name, acl="public-read"):
    try:
        s3.upload_fileobj(file, bucket_name, file.filename, ExtraArgs={
            "ACL": acl,
            "ContentType": file.content_type
        }
        )
    except Exception as e:
        print("Something Happened: ", e)
        return e

    return "{}{}".format(S3_LOCATION, file.filename)

def allowed_images(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ['jpg', 'png', 'jpeg']


gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        environment=os.environ.get('BT_ENVIRONMENT'),
        merchant_id=os.environ.get('BT_MERCHANT_ID'),
        public_key=os.environ.get('BT_PUBLIC_KEY'),
        private_key=os.environ.get('BT_PRIVATE_KEY')
    )
)

def generate_client_token():
    return gateway.client_token.generate()

def transact(options):
    return gateway.transaction.sale(options)

def find_transaction(id):
    return gateway.transaction.find(id)


# config = eval(os.environ['APP_SETTINGS'])

oauth = OAuth()

oauth.register('google',
    client_id=os.environ.get('GOOGLE_CLIENT_ID'),
    client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={
        'scope': 'https://www.googleapis.com/auth/userinfo.email',
        'token_endpoint_auth_method': 'client_secret_basic',
        'token_placement': 'header',
        'prompt': 'consent'
    }
)

# def save_request_token(token):
#     save_request_token_to_someplace(current_user, token)

# def fetch_request_token():
#     return get_request_token_from_someplace(current_user)
