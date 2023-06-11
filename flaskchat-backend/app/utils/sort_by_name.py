import pypinyin


# 定义一个函数，用于按照名字拼音首字母分组
def group_by_pinyin(names):
    groups = {}
    for name in names:
        # 获取名字的拼音首字母
        first_letter = pypinyin.lazy_pinyin(name)[0][0].upper()
        # 将名字添加到对应的分组中
        if first_letter in groups:
            groups[first_letter].append(name)
        else:
            groups[first_letter] = [name]
    sort_data = sorted(groups.items(), key=lambda dic: dic[0])
    return sort_data


# 测试代码
names = ['张三', '李四', '王五', '赵六']
groups = group_by_pinyin(names)
print(groups)
