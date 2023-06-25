### event name

- online_mark:用于向好友、群在线标记
- friend_online_notice:好友上线通知
- friend_online:用于登录后给自己推送好友在线列表
- group_online:用于登录后首次获取群在线人员

### redis key:s

- global_online_users:全局在线人员
- {group.nmae}\_member_online:群内在线人员
- visit_count: 总访问量
- {today}\_visit_count：当日访问量
- chat_list：首页聊天列表
