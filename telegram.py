import telepot

import Data

TOKEN = '7346972907:AAHjOjI87ifl9PyNCVzpkWjl13kFzbuGAe8'
MAX_MSG_LENGTH = 300
bot = telepot.Bot(TOKEN)


def send(msg):
    bot.sendMessage(7472852890, msg)

def handle(msg):
    print('handle msg')
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        send('난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')

    if text.startswith('지역') and len(args) > 1:
        if args[1] in Data.chargeInfos:
            for info in Data.chargeInfos[args[1]]:
                response = '주소: ' + info['stnAddr'] + '\n'
                response += '장소: ' + info['stnPlace'] + '\n'
                response += '급속 충전기: ' + str(info['rapidCnt']) + '\n'
                response += '완속 충전기: ' + str(info['slowCnt']) + '\n'
                send(response)
        else:
            send('경기도엔 그런 지역이 없습니다.')
    else:
        send(chat_id, '모르는 명령어입니다.\n지역 [시/군] 명령을 입력하세요.')