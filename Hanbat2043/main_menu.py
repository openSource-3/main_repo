from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
import os
import sys


class MainMenu(Screen):
    dynamic_font_path = StringProperty('')  # 동적 폰트 경로
    background_image_path = StringProperty('')  # 동적 배경 이미지 경로

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 동적 경로 설정
        self.dynamic_font_path = self.get_resource_path('NanumGothic.ttf')
        self.background_image_path = self.get_resource_path('public/image/main_screen/background.png')

    def get_resource_path(self, filename):
        """리소스 경로를 반환하는 함수"""
        if hasattr(sys, '_MEIPASS'):  # PyInstaller 빌드 환경
            return os.path.join(sys._MEIPASS, filename)
        return os.path.abspath(filename)  # 개발 환경
