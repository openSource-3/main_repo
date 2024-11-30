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
        print("Current working directory:", os.getcwd())
        print("Does 'main_menu.kv' exist?", os.path.exists("main_menu.kv"))
        sm = ScreenManager()

        Builder.load_file(self.get_resource_path('main_menu.kv'))
        Builder.load_file(self.get_resource_path('ending_screen.kv'))

        sm.add_widget(MainMenu(name='mainmenu'))  # 스크린에 추가 스크린을 상속받은 클래스만 바로 추가 가능

        game_screen = GameScreen(screen_manager=sm, name='gamescreen')  # 해당 스크린에 스크린 매니저 전달
        sm.add_widget(game_screen)  # 스크린에 추가

        sm.add_widget(EndingScreen(name='endingscreen'))

        # 정보 페이지 화면 추가
        info_screen = Screen(name='info')  # info란 이름의 스크린 래핑
        # 박스 레이아웃인 InfoPage의 스크린 역할을 함
        info_page = InfoPage(screen_manager=sm)
        # InfoPage 클래스에 스크린 매니저 전달
        info_screen.add_widget(info_page)
        # 임시 래핑한 info스크린에 InfoPage위젯 부여(InfoPage는 박스레이아웃이다)
        sm.add_widget(info_screen)
        # 해당 스크린을 스크린 매니저에 추가

        # 진행도 페이지 화면 추가
        progress_screen = Screen(name='progress')
        progress_page = ProgressPage(screen_manager=sm)
        progress_screen.add_widget(progress_page)
        sm.add_widget(progress_screen)

        return sm

    def start_game(self):
        self.root.current = 'gamescreen'

    def game_ending(self, game_result):
        ending_screen = self.root.get_screen('endingscreen')
        ending_screen.show_screen(game_result)
        self.root.current = 'endingscreen'

    def quit_game(self):
        self.stop()

    def get_resource_path(self, filename):
        """리소스 경로를 반환하는 함수"""
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, filename)
        return filename


if __name__ == '__main__':
    MyGameApp().run()