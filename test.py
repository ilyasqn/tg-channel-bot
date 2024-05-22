import datetime
import time


def read_subscr(file):
    with open(file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        subsr_lst = [[line.split()[0], line.split()[-1]] for line in lines if len(line) >= 2]
        return subsr_lst

def send_end_subscr():
    while True:
        subscr_lst = read_subscr('add.txt')
        for lst in subscr_lst:
            today_day = datetime.datetime.now()
            subscr_end_date = datetime.datetime.strptime(lst[1], '%Y-%m-%d')
            if lst[1] == today_day.strftime('%Y-%m-%d'):
                print('end')
                # #kick
                # count -= 1
            elif 0 < (today_day - subscr_end_date).days < 4:
                print('Хотите продлить прописку?')
        time.sleep(86400)
        
# send_end_subscr()

def check_cheater():
    with open('add.txt') as file:
        lines = file.readlines()
        id_lst = [line.split()[0] for line in lines if len(line) > 1]
        if '864278487' not in id_lst:
             print('BAN')
check_cheater()



@dp.message(ContentType.NEW_CHAT_MEMBERS)
async def check_cheater(message: Message):
    with open('add.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        id_lst = [line[0] for line in lines]

        if message.from_user.id not in id_lst:
            await bot.ban_chat_member(CHANNEL_ID, message.from_user.id)
#
#
# def read_subscr(file):
#     with open(file, 'r', encoding='utf-8') as file:
#         lines = file.readlines()
#         subsr_lst = [[line.split()[0], line.split()[-1]] for line in lines if len(line) >= 2]
#         return subsr_lst
#
#
# def send_end_subscr():
#     while True:
#         subscr_lst = read_subscr('add.txt')
#         for lst in subscr_lst:
#             today_day = datetime.datetime.now()
#             subscr_end_date = datetime.datetime.strptime(lst[1], '%Y-%m-%d')
#             if lst[1] == today_day.strftime('%Y-%m-%d'):
#                 await bot.ban_chat_member(CHANNEL_ID, int(lst[0]))
#                 await bot.unban_chat_member(CHANNEL_ID, int(lst[0]))
#             elif 0 < (today_day - subscr_end_date).days < 4:
#                 await bot.send_message(lst[0], 'Хотите продлить подписку?')
#         time.sleep(86400)
#
#
# # send_end_subscr()