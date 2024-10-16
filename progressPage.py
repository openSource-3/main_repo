import os
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.core.text import LabelBase
from kivy.graphics import Color, Rectangle, Line
from kivy.core.window import Window

# 폰트 등록 클래스
class FontManager:
    @staticmethod
    def register_fonts():
        font_path_h2gprm = os.path.join(os.path.dirname(__file__), 'H2GPRM.ttf')
        LabelBase.register(name='H2GPRM', fn_regular=font_path_h2gprm)

        font_path_malgun = os.path.join(os.path.dirname(__file__), 'malgunbd.ttf')
        LabelBase.register(name='Malgun Gothic', fn_regular=font_path_malgun)

class ProgressPageCompo:
    def __init__(self, layout):
        self.layout = layout
        self.progress_value = 50
        self.days_left = {'mid_exam': 3, 'project': 5, 'final_exam': 7}
        self.progress_bar = []

        self.days_left_labels = [
            self.create_days_left_label('중간고사', 'mid_exam'),
            self.create_days_left_label('팀 프로젝트', 'project'),
            self.create_days_left_label('기말고사', 'final_exam')
        ]
        self.back_button = self.create_back_button()
        self.title_image_path = os.path.join(os.path.dirname(__file__), 'progress_icon.png')

        # 창 크기 변경 시 진행 바 위치 업데이트
        self.layout.bind(size=self.update_progress_rect)

    def create_days_left_label(self, event_name, event_key):
        days_left_text = f"{event_name}까지 {self.days_left[event_key]}일 남았다."
        return Label(text=days_left_text, size_hint=(1, None), height=30, font_name='H2GPRM')

    def create_back_button(self):
        back_button = Button(
            text='> 돌아가기',
            size_hint=(0.4, 0.1),
            pos_hint={'center_x': 0.5, 'y': 0.05},
            font_name='H2GPRM',
            font_size=24,
            background_color=(0, 0, 0, 1),
            color=(1, 1, 1, 1)
        )
        back_button.bind(on_press=self.on_button_clicked)
        return back_button

    def draw_progress_rect(self):
        """진행 바를 생성하고 중앙에 배치."""
        self.rect_width = 600
        self.rect_height = 45

        with self.layout.canvas:
            # 테두리
            Color(1, 1, 1)
            self.progress_bar.append(
                Line(rectangle=(0, 0, self.rect_width, self.rect_height), width=9)
            )

            # 검정 배경
            Color(0, 0, 0)
            self.progress_bar.append(
                Rectangle(pos=(0, 0), size=(self.rect_width, self.rect_height))
            )

            # 진행 바
            Color(1, 1, 1)
            progress_width = (self.progress_value / 100) * self.rect_width
            self.progress_bar.append(
                Rectangle(pos=(0, 0), size=(progress_width, self.rect_height))
            )

        # 초기 위치 업데이트
        self.update_progress_rect()

    def update_progress_rect(self, *args):
        """진행 바 위치를 창 중앙에 고정."""
        x_pos = (Window.width - self.rect_width) / 2
        y_pos = (Window.height - self.rect_height) / 2

        # 저장된 직사각형의 위치 업데이트
        self.progress_bar[0].rectangle = (x_pos, y_pos, self.rect_width, self.rect_height)
        self.progress_bar[1].pos = (x_pos, y_pos)
        self.progress_bar[2].pos = (x_pos, y_pos)

    @staticmethod
    def on_button_clicked(instance):
        print('돌아가기 버튼 클릭')

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

def ProgressPage():
    """진행도 페이지의 위젯을 반환하는 함수."""
    layout = FloatLayout(size=(400, 600))
    ProgressPageBackground(layout)

    # ProgressPageCompo 생성 및 초기화
    progress_compo = ProgressPageCompo(layout)

    # 이미지 상단에서 조금 내린 위치에 배치
    if os.path.exists(progress_compo.title_image_path):
        title_image = Image(
            source=progress_compo.title_image_path,
            size_hint=(1, None),
            height=100,
            pos_hint={'top': 0.68}  # 이미지 위치를 약간 하단으로 조정
        )
        layout.add_widget(title_image)
    else:
        layout.add_widget(Label(
            text='이미지를 찾을 수 없습니다.',
            font_name='Malgun Gothic',
            size_hint=(1, None),
            height=150,
            pos_hint={'top': 0.85}
        ))

    # 텍스트와 버튼 배치
    text_layout = BoxLayout(
        orientation='vertical',
        size_hint=(1, 0.4),
        pos_hint={'x': 0, 'y': 0},
        padding=[10, 10, 10, 10],
        spacing=10
    )

    for label in progress_compo.days_left_labels:
        text_layout.add_widget(label)

    text_layout.add_widget(progress_compo.back_button)

    # 레이아웃 조합
    layout.add_widget(text_layout)

    # 진행 바 그리기 및 중앙 고정
    progress_compo.draw_progress_rect()

    return layout
