from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
import os
import sys


class MainMenu(Screen):
    # 4. 데이터 구조체 - 텍스트와 바이트: 문자열 속성을 동적으로 관리하기 위한 Kivy 속성
    dynamic_font_path = StringProperty('')  # 동적 폰트 경로
    background_image_path = StringProperty('')  # 동적 배경 이미지 경로

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 7. 리팩토링: 동적 리소스 경로 설정을 메서드로 분리
        self.dynamic_font_path = self.get_resource_path('NanumGothic.ttf')
        self.background_image_path = self.get_resource_path('public/image/main_screen/background.png')

    def get_resource_path(self, filename):
        """리소스 경로를 반환하는 함수"""
        # 5. 텍스트 파일: PyInstaller와 개발 환경 모두에서 파일 경로를 정확히 설정
        if hasattr(sys, '_MEIPASS'):  # PyInstaller 빌드 환경
            return os.path.join(sys._MEIPASS, filename)
        return os.path.abspath(filename)  # 개발 환경
