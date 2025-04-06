# briefing.py
import datetime
from transformers import pipeline

def create_briefing(weather_data, news_headlines):
    try:
        # 모델 로드
        pipe = pipeline(
            "text-generation",
            model="Bllossom/llama-3.2-Korean-Bllossom-3B",
            torch_dtype="auto",
            device_map="auto"
        )
        
        # 프롬프트 작성
        today = datetime.datetime.now().strftime("%Y년 %m월 %d일")
        weekday = ["월", "화", "수", "목", "금", "토", "일"][datetime.datetime.now().weekday()]
        
        prompt = f"""<|system|>
당신은 아침 브리핑을 위한 인공지능 비서입니다. 수집된 날씨와 뉴스 데이터를 분석하여 사용자에게 유용한 통찰과 조언이 담긴 브리핑을 제공하세요.
</s>

<|user|>
다음 데이터를 분석하여 오늘 아침 브리핑을 작성해주세요.

날씨 정보:
- 오늘 날씨: {weather_data.get('sky', '정보 없음')}
- 최저/최고 기온: {weather_data.get('temp_min', '정보 없음')}℃ / {weather_data.get('temp_max', '정보 없음')}℃
- 강수 여부: {weather_data.get('rain', '없음')}
- 강수 확률: {weather_data.get('rain_prob', '0')}%
- 미세먼지: {weather_data.get('pm10_grade', '정보 없음')}

오늘의 주요 뉴스:
{' '.join([f"- {headline}" for headline in news_headlines[:5]])}

다음 사항을 분석하여 브리핑에 포함해주세요:
1. 오늘은 {today} {weekday}요일입니다.
2. 날씨 상태에 따른 조언:
   - 비 소식이 있으면 우산을 챙기라는 조언 포함
   - 미세먼지가 나쁨 이상이면 마스크 착용 권고 포함
   - 일교차가 크면 겉옷 준비 권고 포함
3. 뉴스 중요도 분석 및 요약
4. 자연스러운 대화체로 200단어 이내 작성

상황에 맞는 실용적인 조언이 담긴 아침 브리핑을 작성해주세요.
</s>

<|assistant|>"""
        
        # 모델 실행
        result = pipe(
            prompt,
            max_new_tokens=512,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.2
        )
        
        # 응답 추출 및 정리
        generated_text = result[0]["generated_text"]
        briefing = generated_text.split("<|assistant|>")[-1].strip()
        
        return briefing
        
    except Exception as e:
        print(f"오류 발생: {e}")
        # 오류 발생시 템플릿 기반 요약으로 대체
        return create_fallback_briefing(weather_data, news_headlines)

# 백업용 템플릿 기반 요약 함수
def create_fallback_briefing(weather_data, news_headlines):
    today = datetime.datetime.now().strftime("%Y년 %m월 %d일")
    weekday = ["월", "화", "수", "목", "금", "토", "일"][datetime.datetime.now().weekday()]
    
    # 날씨 정보 포맷팅
    weather_text = f"오늘 날씨는 {weather_data.get('sky', '정보 없음')}이며, 최저기온은 {weather_data.get('temp_min', '정보 없음')}도, 최고기온은 {weather_data.get('temp_max', '정보 없음')}도입니다."
    
    if weather_data.get('rain', '') == '예상' or int(weather_data.get('rain_prob', '0')) > 30:
        weather_text += " 비 소식이 있으니 우산을 챙기세요."
    
    # 미세먼지 정보 추가 (마스크 권고 포함)
    dust_grade = weather_data.get('pm10_grade', '')
    if dust_grade in ['나쁨', '매우나쁨']:
        weather_text += f" 미세먼지는 {dust_grade} 수준입니다. 외출 시 마스크 착용을 권장합니다."
    elif 'pm10_grade' in weather_data:
        weather_text += f" 미세먼지는 {weather_data['pm10_grade']} 수준입니다."
    
    # 뉴스 정보 포맷팅
    news_text = "오늘의 주요 뉴스는 다음과 같습니다. "
    for i, headline in enumerate(news_headlines[:3], 1):
        news_text += f"{i}. {headline}. "
    
    # 전체 브리핑 조합
    briefing = f"""안녕하세요, {today} {weekday}요일 아침 브리핑입니다.

{weather_text}

{news_text}

오늘도 좋은 하루 되세요!"""
    
    return briefing

# 테스트 코드
if __name__ == "__main__":
    # 테스트를 위한 더미 데이터
    test_weather = {
        'sky': '맑음',
        'temp_min': '0',
        'temp_max': '0',
        'rain': '없음',
        'rain_prob': '0',
        'pm10_grade': '나쁨'
    }
    
    test_news = [
        "한국 경제 성장률 전망치 상향 조정",
        "글로벌 기업들 한국 투자 확대 계획 발표",
        "신규 일자리 창출 정책 효과 나타나",
        "소비자 물가 상승세 둔화",
        "에너지 분야 혁신 기술 개발에 정부 지원 확대"
    ]
    
    # 브리핑 생성 테스트
    briefing_text = create_briefing(test_weather, test_news)
    print("=== 테스트 브리핑 ===")
    print(briefing_text)
