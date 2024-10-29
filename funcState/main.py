from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from infoPage import InfoPage, FontManager
from progressPage import ProgressPage
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label

## 두 페이지 구현을 위한 임시 페이지 ##
class MainMenu(BoxLayout):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        self.screen_manager = screen_manager  # ScreenManager 인스턴스를 저장

        # 정보 페이지 버튼
        info_button = Button(text='info', size_hint=(1, 0.2))
        info_button.bind(on_press=self.open_info_page)
        self.add_widget(info_button)  # self.main_layout가 아닌 self에 추가

        # 진행도 페이지 버튼
        progress_button = Button(text='progress', size_hint=(1, 0.2))
        progress_button.bind(on_press=self.open_progress_page)
        self.add_widget(progress_button)  # self.main_layout가 아닌 self에 추가

    def open_info_page(self, instance):
        self.screen_manager.current = 'info'  # 'info' 화면으로 전환

    def open_progress_page(self, instance):
        self.screen_manager.current = 'progress'  # 'progress' 화면으로 전환


class MainApp(App):
    def build(self):
        FontManager.register_fonts()  # 폰트 등록

        # ScreenManager 설정
        self.screen_manager = ScreenManager()

        # 메인 메뉴 화면
        main_menu = MainMenu(screen_manager=self.screen_manager)
        main_screen = Screen(name='main')
        main_screen.add_widget(main_menu)
        self.screen_manager.add_widget(main_screen)

        # 정보 페이지 화면
        info_page = InfoPage(self.screen_manager)  # ScreenManager를 InfoPage에 전달
        info_screen = Screen(name='info')
        info_screen.add_widget(info_page)
        self.screen_manager.add_widget(info_screen)

        # 진행도 페이지 화면
        progress_page = ProgressPage(self.screen_manager)  # ProgressPage의 생성자에 ScreenManager 전달이 필요할 경우 추가
        progress_screen = Screen(name='progress')
        progress_screen.add_widget(progress_page)
        self.screen_manager.add_widget(progress_screen)

        return self.screen_manager


if __name__ == '__main__':
    MainApp().run()  # 애플리케이션 실행
