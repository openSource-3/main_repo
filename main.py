from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from infoPage import InfoPage, FontManager
from progressPage import ProgressPage, FontManager

## 두 페이지 구현을 위한 임시 페이지 ##
class MainApp(App):

    def build(self):
        FontManager.register_fonts()  # 폰트 등록
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # 정보 페이지 버튼
        info_button = Button(text='info', size_hint=(1, 0.2))
        info_button.bind(on_press=self.open_info_page)
        self.main_layout.add_widget(info_button)

        # 진행도 페이지 버튼
        progress_button = Button(text='progress', size_hint=(1, 0.2))
        progress_button.bind(on_press=self.open_progress_page)
        self.main_layout.add_widget(progress_button)

        return self.main_layout

    def open_info_page(self, instance):
        """정보 페이지를 여는 메소드"""
        self.main_layout.clear_widgets()  # 현재 레이아웃의 모든 위젯 삭제
        info_page = InfoPage()  # InfoPage 인스턴스 생성
        self.main_layout.add_widget(info_page)  # InfoPage 위젯을 추가

    def open_progress_page(self, instance):
        """진행도 페이지를 여는 메소드"""
        self.main_layout.clear_widgets()  # 현재 레이아웃의 모든 위젯 삭제
        progress_page = ProgressPage()  # ProgressPageApp 인스턴스 생성
        self.main_layout.add_widget(progress_page)  # 위젯 추가


if __name__ == '__main__':
    MainApp().run()
