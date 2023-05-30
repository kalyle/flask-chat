from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy


# class SQLAlchemy(_SQLAlchemy):
#     # 可以进行数据库的优化
#     def __enter__(self):
#         pass
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         pass


db = _SQLAlchemy()


