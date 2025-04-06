# main.py
import datetime
import time
import schedule
from weather import get_weather_data
from news import get_news_headlines
from briefing import create_briefing
from speech import speak_text

def morning_briefing():
    print(f"===== {datetime.datetime.now()} 아침 브리핑 시작 =====")
    
    try:
        # 1. 날씨 정보 가져오기
        print("날씨 정보 가져오는 중...")
        weather_data = get_weather_data()
        
        # 2. 뉴스 헤드라인 가져오기
        print("뉴스 정보 가져오는 중...")
        news_headlines = get_news_headlines()
        
        # 3. 정보 요약하기
        print("브리핑 생성 중...")
        briefing_text = create_briefing(weather_data, news_headlines)
        
        # 결과 출력 (디버깅용)
        print("\n===== 브리핑 내용 =====")
        print(briefing_text)
        print("=====================\n")
        
        # 4. 음성으로 브리핑 읽어주기
        print("음성 변환 중...")
        speak_text(briefing_text)
        
        print("브리핑 완료!")
        
    except Exception as e:
        print(f"브리핑 생성 중 오류 발생: {e}")

# 스케줄 설정 (매일 아침 7시 실행)
schedule.every().day.at("07:00").do(morning_briefing)

# 프로그램 시작 메시지
print("라즈베리파이 아침 브리핑 서비스 시작됨")
print("매일 아침 7시에 자동 실행됩니다")
print("또는 'python main.py now'로 즉시 실행할 수 있습니다")

# 테스트용 즉시 실행 (인자로 'now'가 전달된 경우)
import sys
if len(sys.argv) > 1 and sys.argv[1] == 'now':
    morning_briefing()

# 무한 루프로 스케줄러 실행
while True:
    schedule.run_pending()
    time.sleep(1)
