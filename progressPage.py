import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.text import LabelBase
from kivy.graphics import Color, Rectangle

# 폰트 등록
font_path = os.path.join(os.path.dirname(__file__), 'H2GPRM.ttf')
LabelBase.register(name='H2GPRM', fn_regular=font_path)

font_path_malgun = os.path.join(os.path.dirname(__file__), 'malgunbd.ttf')
LabelBase.register(name='Malgun Gothic', fn_regular=font_path_malgun)

class ProgressPageCompo:
    def __init__(self, app_instance):
        """GameProgressApp 인스턴스를 받아 콜백 연결"""
        self.app = app_instance  # App 인스턴스 저장
        self.progress_bar = ProgressBar(max=100, value=50)
        self.progress_label = Label(text='50%', size_hint=(1, 0.2), font_name='H2GPRM')
        self.days_left_labels = [
            Label(text='중간고사까지 n일 남았다.', size_hint=(1, 0.1), font_name='H2GPRM'),
            Label(text='팀 프로젝트까지 n일 남았다.', size_hint=(1, 0.1), font_name='H2GPRM'),
            Label(text='기말고사까지 n일 남았다.', size_hint=(1, 0.1), font_name='H2GPRM')
        ]
        self.back_button = self.create_back_button()
        self.title_label = Label(text='_ _ _ _ _ _ ╭(`• •´)╮ _ _ _ _ _ _', font_name='Malgun Gothic')

    def create_back_button(self):
        """중앙 하단 버튼 생성"""
        back_button = Button(
            text='> 돌아간다',
            size_hint=(0.4, 0.1),  # 버튼 크기
            pos_hint={'center_x': 0.5, 'y': 0.05},  # 중앙 하단 배치
            font_name='H2GPRM',
            font_size=24,  # 폰트 크기 확대
            background_color=(0, 0, 0, 1),  # 버튼 배경 검정
            color=(1, 1, 1, 1)  # 글씨 색 흰색
        )
        # GameProgressApp의 on_back_clicked와 연결
        back_button.bind(on_press=self.app.on_back_clicked)
        return back_button

class ProgressPageBackground:
    def __init__(self, layout):
        self.layout = layout
        self.layout.bind(size=self.update_rect, pos=self.update_rect)
        with self.layout.canvas.before:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)

    def update_rect(self, *args):
        self.rect.size = self.layout.size
        self.rect.pos = self.layout.pos

class GameProgressApp(App):
    def build(self):
        layout = FloatLayout(size=(400, 600))  # 최상위 레이아웃
        ProgressPageBackground(layout)

        # ProgressPageCompo 인스턴스 생성 (self 전달)
        progress_compo = ProgressPageCompo(self)

        # 중앙에 표시될 진행 상태 박스
        progress_box = BoxLayout(
            orientation='vertical',
            size_hint=(0.8, 0.4),
            pos_hint={'center_x': 0.5, 'center_y': 0.6},  # 화면 중앙 상단 쪽 배치
            padding=[10, 10, 10, 10],
            spacing=10
        )

        # 진행 상태 컴포넌트 추가
        progress_box.add_widget(progress_compo.title_label)
        progress_box.add_widget(progress_compo.progress_bar)
        progress_box.add_widget(progress_compo.progress_label)
        for label in progress_compo.days_left_labels:
            progress_box.add_widget(label)

        # 레이아웃에 위젯 추가
        layout.add_widget(progress_box)
        layout.add_widget(progress_compo.back_button)  # 중앙 하단에 버튼 추가

        return layout

    def on_back_clicked(self, instance):
        """돌아가기 버튼 클릭 시 실행되는 메서드"""
        print("돌아가기 버튼이 클릭되었습니다.")

if __name__ == '__main__':
    GameProgressApp().run()
