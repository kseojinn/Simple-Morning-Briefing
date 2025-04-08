# news.py
import urllib.request
import urllib.parse
import json

def get_news_headlines():
    # 네이버 개발자 센터에서 발급받은 API 키 입력
    client_id = ""
    client_secret = ""
    
    # 경제 뉴스 검색 (display=5는 5개 결과 요청)
    query = urllib.parse.quote("경제")
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=5&sort=sim"
    
    try:
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        
        if rescode == 200:
            # 응답 받아서 파싱
            response_body = response.read()
            news_data = json.loads(response_body.decode('utf-8'))
            
            # HTML 태그 및 불필요한 문자 제거하여 제목만 추출
            headlines = []
            for item in news_data['items']:
                title = item['title']
                # HTML 태그 제거
                title = title.replace('<b>', '').replace('</b>', '')
                title = title.replace('&quot;', '"').replace('&apos;', "'")
                title = title.replace('&lt;', '<').replace('&gt;', '>')
                title = title.replace('&amp;', '&')
                headlines.append(title)
            
            return headlines
        else:
            print(f"네이버 API 오류 코드: {rescode}")
            return ["경제 뉴스를 가져오는데 실패했습니다."] * 5
            
    except Exception as e:
        print(f"뉴스 가져오기 실패: {e}")
        # 오류 발생시 더미 데이터 반환
        return ["경제 뉴스 1", "경제 뉴스 2", "경제 뉴스 3", "경제 뉴스 4", "경제 뉴스 5"]

# 테스트 코드
if __name__ == "__main__":
    headlines = get_news_headlines()
    print("경제 헤드라인 뉴스:")
    for i, headline in enumerate(headlines, 1):
        print(f"{i}. {headline}")
