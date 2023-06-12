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


class NotifyNamespace(Namespace):
    def on_connect(self):
        if not current_user.is_authenticated:
            raise ConnectionRefusedError('unauthorized!')

    @staticmethod
    def join_in():
        user = User.request_user
        for friend in user.friends:
            join_room(friend.id)
        for group in user.groups:
            join_room(group.id)

    @staticmethod
    def leave_out():
        user = User.request_user
        for friend in user.friends:
            leave_room(friend.id)
        for group in user.groups:
            leave_room(group.id)

    def history(self):
        # friend chat

        # group chat

        response = {}
        response["friendChat"] = []
        response["groupChat"] = []
        return response

    def on_disconnect(self):
        self.leave_out()
        emit("onlineMark", {"online": 0})  # 0--->outline,1--->online


class ChatNamespace(Namespace):
    def on_friend_chat(self):
        pass

    def on_group_chat(self):
        pass
