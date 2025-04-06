from news import get_news_headlines

if __name__ == "__main__":
    headlines = get_news_headlines()
    print("경제 헤드라인 뉴스:")
    for i, headline in enumerate(headlines, 1):
        print(f"{i}. {headline}")
















