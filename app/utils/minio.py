from app.extensions.init_ext import minio_client
from minio.error import MinioException
import os

DEFAULT_BUCKET = f"funchat-{os.getenv('TAG') or 'dev'}"


class Bucket(object):
    @staticmethod
    def exist_bucket():
        if not minio_client.bucket_exists(bucket_name=DEFAULT_BUCKET):
            minio_client.make_bucket(bucket_name=DEFAULT_BUCKET)

    @staticmethod
    def remove_bucket():
        try:
            minio_client.remove_bucket(bucket_name=DEFAULT_BUCKET)
        except MinioException as err:
            print(err)

    @property
    def policy():
        return minio_client.get_bucket_policy(DEFAULT_BUCKET)

    # # 获取存储桶上的通知配置
    # def bucket_notification(self):
    #     try:
    #         # 获取存储桶的通知配置。
    #         notification = minio_client.get_bucket_notification('testfiles')
    #         # 如果存储桶上没有任何通知：
    #         # notification  == {}
    #     except MinioException as err:
    #         print(err)

    # # 给存储桶设置通知配置
    # def set_bucket_notification(notification):
    #     pass

    # # 监听存储桶上的通知
    # def listen_bucket_notification(prefix, suffix, events):
    #     pass


class MinioUtil(object):
    def __new__(cls, *args, **kwargs):
        Bucket.exist_bucket(DEFAULT_BUCKET)
        super().__new__(cls, *args, **kwargs)

    @staticmethod
    def get_object(object_name: str):
        try:
            object = minio_client.get_object(
                bucket_name=DEFAULT_BUCKET, object_name=object_name
            )
            return object
        except Exception as e:
            print(e)

    @staticmethod
    def put_object(object_name: str, file, file_size):
        # 放置一个具有默认内容类型的文件
        try:
            minio_client.put_object(
                bucket_name=DEFAULT_BUCKET,
                object_name=object_name,
                data=file,
                length=file_size,
            )
        except Exception as e:
            print(e)

    @staticmethod
    def put_object_csv(object_name: str, file, file_size):
        try:
            minio_client.put_object(
                bucket_name=DEFAULT_BUCKET,
                object_name=object_name,
                data=file,
                length=file_size,
                content_type='application/csv',
            )
        except Exception as e:
            print(e)

    @staticmethod
    def remove_object(file_name: str):
        # 删除对象
        try:
            minio_client.remove_object(DEFAULT_BUCKET, file_name)
        except MinioException as err:
            print(err)

    @staticmethod
    def remove_objects(object_list):
        # 删除存储桶中的多个对象
        try:
            minio_client.remove_objects(DEFAULT_BUCKET, object_list)
        except MinioException as err:
            print(err)

    @staticmethod
    def remove_incomplete_upload(file_name: str):
        # 删除一个未完整上传的对象

        try:
            minio_client.remove_incomplete_upload(DEFAULT_BUCKET, file_name)
        except MinioException as err:
            print(err)

    @staticmethod
    def stat_object(file_name: str):
        # 获取对象的元数据
        try:
            minio_client.stat_object(DEFAULT_BUCKET, file_name)
        except MinioException as err:
            print(err)
