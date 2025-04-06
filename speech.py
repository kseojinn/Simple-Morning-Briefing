# speech.py
import os
import subprocess
import tempfile
from gtts import gTTS
import time

def speak_text(text):
    try:
        print("텍스트를 음성으로 변환 중...")
        # gTTS를 사용하여 음성 생성 (Google TTS)
        tts = gTTS(text=text, lang='ko')
        
        # 임시 파일로 저장
        output_file = "temp_speech.mp3"
        tts.save(output_file)
        
        # 블루투스 스피커로 재생
        print("블루투스 스피커로 음성 재생 중...")
        
        # mpg321으로 재생 (MP3 플레이어)
        subprocess.run(["mpg321", output_file], check=True)
        
        print("음성 재생 완료")
        
        # 임시 파일 삭제
        os.remove(output_file)
        
    except Exception as e:
        print(f"음성 변환 또는 재생 오류: {e}")
        
        # 오류 발생 시 대체 방법으로 시도
        try:
            print("다른 방법으로 재생 시도...")
            subprocess.run(["aplay", "-D", "bluealsa:DEV=68:68:01:BF:CE:9A", output_file], check=True)
        except Exception as e2:
            print(f"대체 방법도 실패: {e2}")
            print("텍스트로 대체합니다:")
            print(text)

# 테스트 코드
if __name__ == "__main__":
    test_text = "안녕하세요, 블루투스 스피커 테스트입니다. 소리가 잘 들리나요?"
    speak_text(test_text)
