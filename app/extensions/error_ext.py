from werkzeug.exceptions import HTTPException
import traceback


def handle_exception(error):
    print("error_ext catch error:", error)
    # if isinstance(error, APIException):  # 手动触发的异常
    #     pass
    # elif isinstance(e, HTTPException):  # 代码异常
    #     # return APIException(e.code, e.description, None)
    #     pass
    # else:
    #     pass
