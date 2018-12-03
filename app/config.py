import os

S3_BUCKET   = os.environ.get("S3_BUCKET_NAME")
S3_KEY      = os.environ.get("S3_ACCESS_KEY")
S3_SECRET   = os.environ.get("S3_SECRET_ACCESS_KEY")
S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

SECRET_KEY  = os.urandom(32)
DEBUG       = True
PORT        = 5000

BT_ENVIRONMENT = os.environ.get("BT_ENVIRONMENT")
BT_MERCHANT_ID = os.environ.get("BT_MERCHANT_ID")
BT_PUBLIC_KEY = os.environ.get("BT_PUBLIC_KEY")
BT_PRIVATE_KEY = os.environ.get("BT_PRIVATE_KEY")
APP_SECRET_KEY = os.environ.get("APP_SECRET_KEY")
