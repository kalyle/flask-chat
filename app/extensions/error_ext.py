from werkzeug.exceptions import HTTPException
import traceback
import logging
from app.extensions.init_ext import mail

logger = logging.getLogger(__name__)


class DBException(Exception):
    ...


class APIException(Exception):
    ...


def handle_exception(error):
    traceback.format_exc()
    print("error_ext catch error:", error)
    if isinstance(error, APIException):  # 手动触发的异常
        logger.error(f"[接口异常]-[{error}]")
    elif isinstance(error, HTTPException):  # 代码异常
        # return APIException(e.code, e.description, None)
        if error.code >= 500:
            # 发送邮件
            pass
        # 其余记录log
        logger.error(f"[HTTP异常]-[{error}]")
    elif isinstance(error, DBException):  # db异常
        logger.error(f"[DB异常]-[{error}]")
