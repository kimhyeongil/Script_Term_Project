import telepot

import Data

bot = telepot.Bot(Data.teleToken)


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
    elif text.startswith('즐찾추가') and len(args) > 2:
        place = ''
        for i in range(2, len(args)):
            place += args[i] + ' '
        place = place[:-1]
        if args[1] in Data.chargeInfos:
            for info in Data.chargeInfos[args[1]]:
                if info['stnPlace'] == place:
                    Data.bookmarkCities.append(info)
                    send('즐겨찾기에 추가했습니다.')
                    return
            send(f'{args[1]}에는 {place}가 없습니다.')
    elif text.startswith('즐찾삭제') and len(args) > 1:
        place = ''
        for i in range(1, len(args)):
            place += args[i] + ' '
        place = place[:-1]
        for index, info in enumerate(Data.bookmarkCities):
            if info['stnPlace'] == place:
                Data.bookmarkCities.pop(index)
                send('삭제했습니다.')
                return
        send(f'즐겨찾기에 {place}가 없습니다.')
    elif text.startswith('즐찾보기'):
        for info in Data.bookmarkCities:
            response = '주소: ' + info['stnAddr'] + '\n'
            response += '장소: ' + info['stnPlace'] + '\n'
            response += '급속 충전기: ' + str(info['rapidCnt']) + '\n'
            response += '완속 충전기: ' + str(info['slowCnt']) + '\n'
            send(response)
    else:
        send('모르는 명령어입니다.\n지역 [시/군], 즐찾추가 [시/군] [장소], 즐찾보기 중 한 명령을 입력하세요.')
