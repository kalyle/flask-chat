from flask_socketio import Namespace, join_room, leave_room, emit, rooms
from app.utils.reids import cache
from app.extensions.init_ext import socketio
from app.models.friend_chat_record import FriendChatRecordModel
from app.models.group_chat_record import GroupChatRecordModel
from app.models.friend import FriendModel
from app.models.group_chat import GroupChatModel
from app.utils.before_request import socket_auth, g, socket_user, verify

import datetime


class NotifyNamespace(Namespace):
    # 当socket.io添加了auth参数，将把该参数指传递给connect event
    # https://github.com/miguelgrinberg/Flask-SocketIO/issues/1555
    def on_connect(self, token):
        setattr(socketio.server, 'token', token)
        is_auth = verify(token)
        if not is_auth:
            raise ConnectionRefusedError('authorized fail!')

        self.join_in()
        cache.set_add("global_online_users", g.user["id"])
        # 访问量
        # 总访问量
        cache.str_incr("visit_count")

        # 当日访问量
        today = datetime.date.today().isoformat()
        cache.str_incr(f"{today}_visit_count", 60 * 60 * 24 * 7)

        print("rooms", rooms())
        return True

    def on_disconnect(self):
        self.leave_out()
        cache.set_rem("global_online_users", socket_user["id"])
        cache.hash_del("user_info", socket_user["id"])

    @socket_auth
    def join_in(self):
        join_room(socket_user["id"])
        friend_online = []
        for friend in socket_user["friends"]:
            join_room(NotifyNamespace.get_name(socket_user["id"], friend["id"]))
            # 通知在线的朋友，你已上线（设置为需要上线通知，特别关心）,获取好友在线情况
            if cache.set_ismember("global_online_users", friend["id"]):
                friend_online.append(friend["id"])
                NotifyNamespace.online_mark(
                    to=friend["id"], online=1, user=socket_user["id"]
                )
                # if friend.setting.online_notice:
                #     emit("friend_online_notice", user, to=friend["id"])

        for group in socket_user["groups"]:
            join_room(group.id)
            NotifyNamespace.online_mark(to=group.name, online=1, user=socket_user["id"])
            cache.set_add(f"{group.name}_member_online", socket_user["id"])
        emit("friend_online", friend_online)

    @socket_auth
    def leave_out(self):
        leave_room(socket_user["id"])
        for friend in socket_user["friends"]:
            leave_room(NotifyNamespace.get_name(socket_user["id"], friend["id"]))
            NotifyNamespace.online_mark(
                to=friend["id"], online=0, user=socket_user["id"]
            )
        for group in socket_user["groups"]:
            leave_room(group.id)
            NotifyNamespace.online_mark(to=group.name, online=0, user=socket_user["id"])
            cache.set_rem(f"{group.name}_member_online", socket_user["id"])

    @staticmethod
    def get_name(user_id: int, friend_id: int):
        return (
            str(user_id) + "&" + str(friend_id)
            if user_id < friend_id
            else str(friend_id) + "&" + str(user_id)
        )

    @staticmethod
    def online_mark(to, online: int, user: int):
        # 0--->outline    1--->online
        emit("online_mark", {"online": online, "user": user}, to=to)


class ChatNamespace(Namespace):
    def on_connect(self, u):
        return True

    def on_disconnect(self):
        return True

    def on_msg_read(self, data):
        # 消息已读
        chat_id = data["chat_id"]
        chat_type = data["chat_type"]
        if chat_type == "friend":
            FriendChatRecordModel.query.filter(id=chat_id, read=False).update(
                {"read": True}
            )
            friend = FriendModel.find_by_id(chat_id)
            room = NotifyNamespace.get_name(socket_user["id"], friend.friend_id)
        else:
            GroupChatRecordModel.query.filter(id=chat_id, read=False).update(
                {"read": True}
            )
            group = GroupChatModel.find_by_id(chat_id)
            room = group.name

        emit("msgRead", 200, to=room)

    def on_friend_chat(self, msg):
        # chat_record = FriendChatSchema().load(msg)
        # id = chat_record.save_to_db()
        # result = FriendChatSchema().dump(FriendChatRecordModel.find_by_id(id))
        # emit(
        #     "friendChat",
        #     result,
        #     to=NotifyNamespace.get_name(msg["receiver"], msg["sender"]),
        # )
        # return True if result else False
        emit(
            "friendChat",
            msg,
            to=NotifyNamespace.get_name(msg["receiver"], msg["sender"]),
        )
        return True

    def on_group_chat(self):
        pass

    def on_group_welcome(self, data):
        # 新人进群
        msg = f'欢迎{data["user"]}进群'
        content = data["applyNote"]
        emit("groupWelcome", data, to=data["group_id"])

    def on_group_enter(self, group_name):
        # 推送组内用户列表
        # 统计每个群聊在线人员(首次进入房间)
        group_online_num = cache.set_members(f"{group_name}")
        emit("group_online", group_online_num)
