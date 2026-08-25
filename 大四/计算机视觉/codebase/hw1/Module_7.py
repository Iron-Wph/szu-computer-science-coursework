# from datetime import datetime, date, time, timedelta
#  # 获取当前日期和时间
# now = datetime.now()
# print(f"当前日期时间: {now}")
# print(f"年份: {now.year}, 月份: {now.month}, 日期: {now.day}")
# print(f"小时: {now.hour}, 分钟: {now.minute}, 秒: {now.second}")
# # 创建特定日期
# christmas = date(2024, 12, 25)
# print(f"圣诞节日期: {christmas}")
# # 创建特定时间
# lunch_time = time(12, 30, 0)
# print(f"午餐时间: {lunch_time}")
# # 日期时间计算
# one_week = timedelta(weeks=1)
# next_week = now + one_week
# print(f"一周后的时间: {next_week}")
# # 日期格式化
# formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
# print(f"格式化日期: {formatted_date}")
# # 解析字符串为日期
# date_string = "2024-08-26 15:30:00"
# parsed_date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
# print(f"解析后的日期: {parsed_date}")
# # 计算日期差
# new_year = date(2025, 1, 1)
# today = date.today()
# days_until_new_year = (new_year - today).days
# print(f"距离2025年元旦还有 {days_until_new_year} 天")
# # 工作日计算
# from datetime import timedelta, date
# def add_business_days(start_date, business_days):
#     current_date = start_date
#     added_days = 0
#     while added_days < business_days:
#         current_date += timedelta(days=1)
#         # 如果是周末（5=周六，6=周日）
#         if current_date.weekday() < 5:
#             added_days += 1
#     return current_date
# start = date(2024, 8, 26)  # 星期一
# result = add_business_days(start, 3)  # 加3个工作日
# print(f"开始日期: {start}, 加3个工作日后: {result}")

from datetime import datetime

def calculate_next_birthday():
    # 获取用户输入的生日（格式：年-月-日，年份不影响，仅用月和日）
    while True:
        birthday_input = input("请输入你的生日（格式：YYYY-MM-DD，\
            例如 2000-05-20）：").strip()
        try:
            # 解析输入为日期对象（仅提取月和日，年份用当前年占位）
            birthday = datetime.strptime(birthday_input, "%Y-%m-%d")
            birth_month = birthday.month
            birth_day = birthday.day
            break  # 输入格式正确，退出循环
        except ValueError:
            print("输入格式错误！请按照 'YYYY-MM-DD' 的格式重新输入 \
                （例如 2000-05-20）。")

    # 获取当前日期
    today = datetime.now()
    current_year = today.year
    current_month = today.month
    current_day = today.day

    # 确定下一个生日的年份（生日已过则用明年，未过则用今年）
    if (current_month > birth_month) or (current_month == birth_month \
        and current_day > birth_day):
        next_birthday_year = current_year + 1
    else:
        next_birthday_year = current_year

    # 构造下一个生日的完整日期对象
    # 处理特殊情况：2月29日生日（非闰年时自动调整为2月28日）
    try:
        next_birthday = datetime(next_birthday_year, birth_month, birth_day)
    except ValueError:
        # 仅当生日是2月29日且下一年不是闰年时触发，调整为2月28日
        next_birthday = datetime(next_birthday_year, 2, 28)

    # 计算剩余天数（用下一个生日减去当前日期，取天数差）
    days_remaining = (next_birthday - today).days

    # 获取下一个生日的星期几（weekday()返回0=周一，6=周日；
    # strftime("%A")直接返回英文星期名）
    # 如需中文星期，可建立映射关系
    weekday_map = {0: "星期一", 1: "星期二", 2: "星期三", 3: "星期四", \
        4: "星期五", 5: "星期六", 6: "星期日"}
    next_birthday_weekday = weekday_map[next_birthday.weekday()]

    # 输出结果
    print(f"\n===== 生日计算结果 =====")
    print(f"当前日期：{today.strftime('%Y年%m月%d日')}")
    print(f"下一个生日：{next_birthday.strftime('%Y年%m月%d日')}")
    print(f"距离下一个生日还有 {days_remaining} 天")
    print(f"下一个生日是 {next_birthday_weekday}")
    print("=======================")

if __name__ == "__main__":
    calculate_next_birthday()