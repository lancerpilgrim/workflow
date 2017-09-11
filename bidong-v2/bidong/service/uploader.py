from qiniu import Auth, BucketManager, put_file

import settings


class QiniuService:

    def __init__(self):
        self.access_key = settings.qiniu['access_key']
        self.secret_key = settings.qiniu['secret_key']
        self.auth = Auth(self.access_key, self.secret_key)
        self.bucket = settings.qiniu['bucket']

    def gen_upload_token(self, bucket=None, key=None, expired=1800):
        if bucket is None:
            bucket = self.bucket

        token = self.auth.upload_token(bucket, key, expired)
        return token

    def delete(self, key, bucket=None):
        if bucket is None:
            bucket = self.bucket

        bucket_manager = BucketManager(self.auth)
        rv, resp = bucket_manager.delete(bucket, key)
        return rv, resp

    def put(self, token, key, localfile):
        return put_file(token, key, localfile)
