from user_agents import parse


def platform(request):
    user_agent = request.headers.get('User-Agent')
    conn_type = request.headers.get('Connection')
    # 记录登录设备类型：电脑，手机：mac,and 4G\5G
    ua = parse(user_agent)
    ua = request.headers.get('User-Agent')
    if 'android' in ua or 'Linux' in ua:
        return 'android'
    elif 'iphone' in ua:
        return 'iphone'
    else:
        return "computer"
