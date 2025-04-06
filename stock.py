# stock.py
import requests
from bs4 import BeautifulSoup

def get_stock_info():
    # 원하는 해외 주식 심볼과 기업명
    stocks = {
        'AAPL': '애플',
        'TSLA': '테슬라',
        'NVDA': '엔비디아',
        'MSFT': '마이크로소프트',
        'META': '메타',
        'GOOGL': '구글'
    }
    
    stock_data = {}
    
    try:
        for symbol, name in stocks.items():
            # 네이버 금융 해외 주식 페이지
            url = f"https://m.stock.naver.com/worldstock/stock/{symbol}.O/total"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36'
            }
            
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 모바일 버전 페이지에서 변동률 찾기 (CSS 선택자는 페이지 구조에 따라 조정 필요)
                change_element = soup.select_one('.stock_price .gap_rate')
                
                if change_element:
                    change_rate = change_element.text.strip()
                    
                    # 주가 정보 추출
                    price_element = soup.select_one('.stock_price .price')
                    price = price_element.text.strip() if price_element else "정보 없음"
                    
                    stock_data[name] = {
                        'price': price,
                        'change_rate': change_rate
                    }
                else:
                    # 다른 선택자 시도
                    alt_change_element = soup.select_one('[class*="rate"]')
                    if alt_change_element:
                        change_rate = alt_change_element.text.strip()
                        stock_data[name] = {
                            'price': '정보 없음',
                            'change_rate': change_rate
                        }
                    else:
                        # 정보를 찾지 못한 경우
                        stock_data[name] = {
                            'price': '정보 없음',
                            'change_rate': '0.00%'
                        }
                
            except Exception as e:
                print(f"{name} 정보 가져오기 실패: {e}")
                
                # 첫 번째 시도 실패시 다른 URL 시도
                try:
                    backup_url = f"https://finance.naver.com/world/sise.naver?symbol={symbol}"
                    backup_response = requests.get(backup_url, headers={'User-Agent': 'Mozilla/5.0'})
                    backup_soup = BeautifulSoup(backup_response.text, 'html.parser')
                    
                    backup_change = backup_soup.select_one('.no_up, .no_down')
                    if backup_change:
                        stock_data[name] = {
                            'price': '정보 없음', 
                            'change_rate': backup_change.text.strip()
                        }
                    else:
                        stock_data[name] = {
                            'price': '정보 없음',
                            'change_rate': '0.00%'
                        }
                except:
                    stock_data[name] = {
                        'price': '정보 없음',
                        'change_rate': f"{name}의 등락률 정보 없음"
                    }
        
        return stock_data
    
    except Exception as e:
        print(f"주식 정보 처리 중 오류: {e}")
        # 오류 발생시 기본 데이터 반환
        return {
            '애플': {'price': '정보 없음', 'change_rate': '0%'},
            '테슬라': {'price': '정보 없음', 'change_rate': '0%'},
            '엔비디아': {'price': '정보 없음', 'change_rate': '0%'},
            '마이크로소프트': {'price': '정보 없음', 'change_rate': '0%'},
            '메타': {'price': '정보 없음', 'change_rate': '0%'},
            '구글': {'price': '정보 없음', 'change_rate': '0%'}
        }

# 테스트 코드
if __name__ == "__main__":
    stock_info = get_stock_info()
    print("주요 기업 주가 정보:")
    for company, info in stock_info.items():
        print(f"{company}: {info['price']} ({info['change_rate']})")
