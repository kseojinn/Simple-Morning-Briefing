# weather.py
import requests
import json
import datetime

def get_weather_data(nx=60, ny=127):  # 서울 기준 좌표
    today = datetime.datetime.now().strftime("%Y%m%d")
    base_time = "0500"  # 05시 발표 자료
    
    # 디코딩된 키를 사용 (정상 작동 확인됨)
    decoded_key = "7PjattrxPKa0He1GbJAlAAFpR/txSIyaIRwuCwEgQZCxRyh42Y3LYWWn0vrh7rovkK753c8cOqnqOeGQly/SqQ=="
    
    try:
        # API 요청
        url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
        params = {
            'serviceKey': decoded_key,
            'pageNo': '1',
            'numOfRows': '300',
            'dataType': 'JSON',
            'base_date': today,
            'base_time': base_time,
            'nx': nx,
            'ny': ny
        }
        
        response = requests.get(url, params=params)
        print(f"응답 상태 코드: {response.status_code}")
        
        if response.status_code == 200:
            try:
                weather_data = json.loads(response.text)
                
                # 응답 결과 코드 확인
                result_code = weather_data['response']['header']['resultCode']
                if result_code == '00':  # 정상 서비스
                    print("API 호출 성공")
                    # 데이터 파싱 및 반환
                    return extract_weather_data(weather_data)
                else:
                    print(f"API 오류 응답: {result_code}")
            except json.JSONDecodeError:
                print("JSON 파싱 오류")
        
        # 실패 시 더미 데이터 반환
        return {
            'sky': '맑음',
            'temp_min': '18',
            'temp_max': '28',
            'rain': '없음',
            'rain_prob': '10',
            'pm10_grade': '나쁨',
            'pm25_grade': '보통'
        }
    
    except Exception as e:
        print(f"날씨 정보 가져오기 실패: {e}")
        # 오류 발생시 기본 데이터 반환
        return {
            'sky': '맑음',
            'temp_min': '18',
            'temp_max': '28',
            'rain': '없음',
            'rain_prob': '10',
            'pm10_grade': '나쁨',
            'pm25_grade': '보통'
        }

def extract_weather_data(data):
    # 응답 데이터에서 필요한 날씨 정보 추출
    try:
        items = data['response']['body']['items']['item']
        result = {
            'sky': '정보 없음',
            'temp_min': '0',
            'temp_max': '0',
            'rain': '없음',
            'rain_prob': '0',
            'pm10_grade': '보통',  # 미세먼지 정보는 별도 API 필요
            'pm25_grade': '보통'   # 기본값 설정
        }
        
        for item in items:
            # 하늘 상태 (SKY) - 맑음(1), 구름많음(3), 흐림(4)
            if item['category'] == 'SKY' and item['fcstTime'] == '0900':
                sky_code = int(item['fcstValue'])
                if sky_code == 1:
                    result['sky'] = '맑음'
                elif sky_code == 3:
                    result['sky'] = '구름많음'
                elif sky_code == 4:
                    result['sky'] = '흐림'
            
            # 최저기온 (TMN)
            elif item['category'] == 'TMN':
                result['temp_min'] = item['fcstValue']
                
            # 최고기온 (TMX)
            elif item['category'] == 'TMX':
                result['temp_max'] = item['fcstValue']
                
            # 강수형태 (PTY) - 없음(0), 비(1), 비/눈(2), 눈(3), 소나기(4)
            elif item['category'] == 'PTY' and item['fcstTime'] in ['0900', '1200', '1500', '1800']:
                if item['fcstValue'] != '0':  # 비/눈 소식 있음
                    result['rain'] = '예상'
                    
            # 강수확률 (POP)
            elif item['category'] == 'POP' and item['fcstTime'] in ['0900', '1200', '1500', '1800']:
                pop = int(item['fcstValue'])
                if pop > int(result.get('rain_prob', '0')):  # 최대 강수확률 저장
                    result['rain_prob'] = item['fcstValue']
        
        # 실제 데이터 확인을 위한 출력
        print(f"추출된 날씨 정보: {result}")
        
        return result
    except Exception as e:
        print(f"날씨 데이터 처리 오류: {e}")
        return {
            'sky': '맑음',
            'temp_min': '18',
            'temp_max': '28',
            'rain': '없음',
            'rain_prob': '10',
            'pm10_grade': '나쁨',
            'pm25_grade': '보통'
        }

# 테스트 코드
if __name__ == "__main__":
    weather_info = get_weather_data()
    print("날씨 정보:", weather_info)
    
    # 미세먼지 단계에 따른 마스크 권고 메시지 테스트
    if weather_info.get('pm10_grade') in ['나쁨', '매우나쁨'] or weather_info.get('pm25_grade') in ['나쁨', '매우나쁨']:
        print("미세먼지가 나쁨 수준 이상입니다. 외출 시 마스크 착용을 권장합니다.")
