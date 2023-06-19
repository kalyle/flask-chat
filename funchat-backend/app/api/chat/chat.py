from flask_socketio import (
    Namespace,
    ConnectionRefusedError,
    join_room,
    leave_room,
    emit,
)
from flask_login import current_user
from flask import request
from app.extensions.login_ext import User
from app.schemas.chat import FriendChatSchema, GroupChatSchema
from app.models.chat import FriendChatRecordModel, GroupChatRecordModel
from utils.socketio import authenticated_only
from app.extensions.reids import cache
import datetime


class NotifyNamespace(Namespace):
    # methodview decorator
    # decorators = {"login_required": authenticated_only}

    def on_connect(self):
        if not current_user.is_authenticated:
            raise ConnectionRefusedError('unauthorized!')
        else:
            cache.set_add("global_online_users", current_user.id)
            self.join_in()
        # 访问量
        # 总访问量
        cache.incr("visit_count")

        # 当日访问量
        today = datetime.date.today().isoformat()
        cache.str_incr(f"{today}_visit_count", 60 * 60 * 24 * 7)

        # 在线
        cache.set_add("online_users", current_user.id)

    def on_disconnect(self):
        self.leave_out()
        cache.set_rem("global_online_users", current_user.id)

    @staticmethod
    def join_in():
        user = User.request_user
        friend_online = []
        for friend in user.friends:
            join_room(NotifyNamespace.get_name(user.id, friend.id))
            # 通知在线的朋友，你已上线（设置为需要上线通知，特别关心）,获取好友在线情况
            if cache.set_ismember("global_online_users", friend.id):
                friend_online.append(friend.id)
                NotifyNamespace.online_mark(to=friend.id, status=1, user=user.id)
                if friend.setting.online_notice:
                    emit("friend_online_notice", user, to=friend.id)

        for group in user.groups:
            join_room(group.id)
            NotifyNamespace.online_mark(to=group.name, status=1, user=user.id)
            cache.set_add(f"{group.name}_member_online", user.id)
        emit("friend_online", friend_online)

    @staticmethod
    def leave_out():
        user = User.request_user
        for friend in user.friends:
            leave_room(friend.id)
            NotifyNamespace.online_mark(to=friend.id, status=0, user=user.id)
        for group in user.groups:
            leave_room(group.id)
            NotifyNamespace.online_mark(to=group.name, status=0, user=user.id)
            cache.set_rem(f"{group.name}_member_online", user.id)

    @staticmethod
    def online_mark(to, status: int, user: int):
        # data ---> 0--->outline    1--->online
        emit("online_mark", {"online": status, "user": user}, to=to)

    @staticmethod
    def get_name(user_id, friend_id):
        return (
            str(user_id) + "&" + str(friend_id)
            if user_id < friend_id
            else str(friend_id) + "&" + str(user_id)
        )

    @property
    def playform(self):
        # 记录登录设备类型：电脑，手机：mac,and
        ua = request.headers.get('User-Agent')
        if 'android' in ua or 'Linux' in ua:
            return 'android'
        elif 'iphone' in ua:
            return 'iphone'
        else:
            return "computer"


class ChatNamespace(Namespace):
    def on_friend_chat(self, msg):
        chat_record = FriendChatSchema().load(msg)
        id = chat_record.save_to_db()
        result = FriendChatSchema().dump(FriendChatRecordModel.find_by_id(id))
        emit(
            "friendChat",
            result,
            to=NotifyNamespace.get_name(msg["receiver", msg["sender"]]),
        )

    def on_group_chat(self):
        pass

    def on_group_welcome(self, data):
        # 新人进群
        msg = f'欢迎{data["user"]}进群'
        content = data["applyNote"]
        emit("groupWelcome", data, to=data["group_id"])

    def on_into_group(self, group_name):
        # 推送组内用户列表
        # 统计每个群聊在线人员(首次进入房间)
        group_online_num = cache.set_members(f"{group_name}")
        emit("group_online", group_online_num)
