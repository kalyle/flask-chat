from app.extensions.init_ext import minio_client


class MinioUtil(object):
    def get_object(object_name: str):
        try:
            object = minio_client.get_object(object_name)
            return object
        except Exception as e:
            print(e)
