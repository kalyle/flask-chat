from flask_socketio import (
    Namespace,
    ConnectionRefusedError,
    join_room,
    leave_room,
    emit,
)
from flask_login import current_user

from app.extensions.login_ext import User
from app.schemas.chat import FriendChatSchema, GroupChatSchema
from app.models.chat import FriendChatRecordModel, GroupChatRecordModel
from utils.socketio import authenticated_only


class NotifyNamespace(Namespace):
    # methodview decorator
    decorators = {"login_required": authenticated_only}

    def on_connect(self):
        if not current_user.is_authenticated:
            raise ConnectionRefusedError('unauthorized!')
        else:
            self.join_in()

    @staticmethod
    def join_in():
        user = User.request_user
        for friend in user.friends:
            join_room(NotifyNamespace.get_name(user.id, friend.id))
            # 通知在线的朋友，你已上线（设置为需要上线通知，特别关心）
            if friend.id in redis_data and friend.setting.online_notice:
                emit("online_notice", friend, to=friend.id)
        for group in user.groups:
            join_room(group.id)
        NotifyNamespace.online_mark(1)

    @staticmethod
    def leave_out():
        user = User.request_user
        for friend in user.friends:
            leave_room(friend.id)
        for group in user.groups:
            leave_room(group.id)

        NotifyNamespace.online_mark(0)

    @staticmethod
    def online_mark(status: int):
        # data --->  {"online": 0},0--->outline,1--->online
        emit("onlineMark", {"online": status})

    @staticmethod
    def get_name(user_id, friend_id):
        return (
            str(user_id) + "&" + str(friend_id)
            if user_id < friend_id
            else str(friend_id) + "&" + str(user_id)
        )

    def on_disconnect(self):
        self.leave_out()


class ChatNamespace(Namespace):
    def on_friend_chat(self, msg):
        chat_record = FriendChatSchema().load(msg)
        id = chat_record.save_to_db()
        result = FriendChatSchema().dump(FriendChatRecordModel.find_by_id(id))
        emit(
            "friendChat",
            result,
            to=ChatNamespace.get_name(msg["receiver", msg["sender"]]),
        )

    def on_group_chat(self):
        pass
