import spam

cities = {'가평군': ['가평군'], '고양시': ['고양시 덕양구', '고양시 일산동구', '고양시 일산서구'],
          '과천시': ['과천시'], '광명시': ['광명시'], '광주시': ['광주시'], '구리시': ['구리시'],
          '군포시': ['군포시'], '김포시': ['김포시'], '남양주시': ['남양주시'], '동두천시': ['동두천시'],
          '부천시': ['부천시'], '성남시': ['성남시 분당구', '성남시 수정구', '성남시 중원구'],
          '수원시': ['수원시 권선구', '수원시 영통구', '수원시 장안구', '수원시 팔달구'],
          '시흥시': ['시흥시'], '안산시': ['안산시 단원구', '안산시 상록구'], '안성시': ['안성시'],
          '안양시': ['안양시 동안구', '안양시 만안구'], '양주시': ['양주시'], '양평군': ['양평군'],
          '여주시': ['여주시'], '연천군': ['연천군'], '오산시': ['오산시'],
          '용인시': ['용인시 기흥구', '용인시 수지구', '용인시 처인구'], '의왕시': ['의왕시'],
          '의정부시': ['의정부시'], '이천시': ['이천시'], '파주시': ['파주시'], '평택시': ['평택시'],
          '포천시': ['포천시'], '하남시': ['하남시'], '화성시': ['화성시']}

chargeInfos = None

bookmarkCities = []

with open('API키', 'rb') as file:
    key = file.read().decode('utf-8')
    key = spam.decrypt(key)

with open('카카오키', 'rb') as file:
    kakaokey = file.read().decode('utf-8')
    kakaokey = spam.decrypt(kakaokey)

with open('텔레그램토큰', 'rb') as file:
    teleToken = file.read().decode('utf-8')
    teleToken = spam.decrypt(teleToken)

with open('메일비번', 'rb') as file:
    password = file.read().decode('utf-8')
    password = spam.decrypt(password)

print('데이터 실행')