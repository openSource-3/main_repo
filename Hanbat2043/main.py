import kivy
from kivy.config import Config
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from main_menu import MainMenu
from game_screen import GameScreen
from ending_screen import EndingScreen
from infoPage import InfoPage, FontManager
from progressPage import ProgressPage
import os
import sys


class MyGameApp(App):
    def build(self):
        self.title = "Hanbat2043__v.1.0.0"
        # 5. 텍스트 파일: 현재 디렉터리 및 파일 존재 여부 확인
        print("Current working directory:", os.getcwd())
        print("Does 'main_menu.kv' exist?", os.path.exists("main_menu.kv"))
        sm = ScreenManager()

        # 9. 객체 참조, 가변성, 재활용: get_resource_path로 리소스 경로 재활용
        Builder.load_file(self.get_resource_path('main_menu.kv'))
        Builder.load_file(self.get_resource_path('ending_screen.kv'))

        sm.add_widget(MainMenu(name='mainmenu'))  # 스크린에 추가 스크린을 상속받은 클래스만 바로 추가 가능

        game_screen = GameScreen(screen_manager=sm, name='gamescreen')  # 해당 스크린에 스크린 매니저 전달
        sm.add_widget(game_screen)  # 스크린에 추가

        sm.add_widget(EndingScreen(name='endingscreen'))

        # 정보 페이지 화면 추가
        info_screen = Screen(name='info')  # info란 이름의 스크린 래핑
        # 7. 리팩토링: InfoPage를 별도로 정의하고 이를 래핑한 구조로 스크린 추가
        info_page = InfoPage(screen_manager=sm)
        # InfoPage 클래스에 스크린 매니저 전달
        info_screen.add_widget(info_page)
        # 임시 래핑한 info스크린에 InfoPage위젯 부여
        sm.add_widget(info_screen)

        # 진행도 페이지 화면 추가
        progress_screen = Screen(name='progress')
        progress_page = ProgressPage(screen_manager=sm)
        progress_screen.add_widget(progress_page)
        sm.add_widget(progress_screen)

        return sm

    def start_game(self):
        # 6. First-class Functions (일급 함수): 메서드를 이벤트로 연결
        self.root.current = 'gamescreen'

    def game_ending(self, game_result):
        # 9. 객체 참조, 가변성, 재활용: 스크린 매니저에서 객체를 재활용
        ending_screen = self.root.get_screen('endingscreen')
        ending_screen.show_screen(game_result)
        self.root.current = 'endingscreen'

    def quit_game(self):
        # 6. First-class Functions (일급 함수): App 종료 메서드를 직접 호출
        self.stop()

    def get_resource_path(self, filename):
        """리소스 경로를 반환하는 함수"""
        # 5. 텍스트 파일: 리소스 경로를 읽어오기 위한 텍스트 파일 경로 결정
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, filename)
        return filename


if __name__ == '__main__':
    # 1. 특별 메서드: __name__ == '__main__' 확인 후 실행
    MyGameApp().run()