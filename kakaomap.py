import requests


class KakaoMap:
    def __init__(self, key):
        self.key = key

    def geocode(self, addr):
        url = 'https://dapi.kakao.com/v2/local/search/address.json'
        headers = {"Authorization": f"KakaoAK {self.key}"}
        params = {'query': addr}

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            result = response.json()
            if result['documents']:
                address_info = result['documents'][0]['address']
                return float(address_info['y']), float(address_info['x'])  # 위도, 경도
            else:
                return None, None
        else:
            return None, None
