import os
from kivy.core.text import LabelBase
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line


# 1. 폰트 등록을 처리하는 클래스
class FontManager:
    @staticmethod
    def register_fonts():
        """H2GPRM 폰트를 등록합니다."""
        font_path = os.path.join(os.path.dirname(__file__), 'H2GPRM.ttf')
        LabelBase.register(name='H2GPRM', fn_regular=font_path)


# 2. 사용자 정보와 능력치를 관리하는 클래스
class UserInfo:
    """사용자 정보를 저장하는 클래스."""

    def __init__(self):
        # 사용자 기본 정보
        self.name = "한밭대학교 5학년 2학기 재학 중이다."
        self.trait = "처음 선택한 특성에 관한 문구"
        self.abilities = [
            ("속도", 2, "능력치에 대한 설명"),
            ("지능", 2, "아니면 능력치 습득 힌트를 적어도 되겠어요"),
            ("창의", 1, "소소한 말을 써도 되겠네요"),
            ("행운", 3, "아무튼 내용이 들어갈 자리입니다"),
            ("체력", 2, "참고하세요  (>ㅂ0)/ ")
        ]

    def get_info(self):
        """사용자의 이름과 특성 문구를 반환합니다."""
        return f"' 이름 '\n{self.name}\n\n\" {self.trait} \""


# 3. UI를 구성하는 클래스
class InfoPage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [10, 10]
        self.spacing = 10

        # UserInfo 인스턴스 생성
        user_info = UserInfo()

        # 정보 출력
        self.add_widget(Label(text='', size_hint_y=None, height=10))  # 한 칸 내림
        self.add_widget(Label(text='__정보__', font_size='24sp', bold=True,
                              size_hint_y=None, height=40, font_name='H2GPRM',
                              halign='left', valign='middle', size_hint_x=None, width=160))

        # 사용자 정보 출력: 한 칸 띄우기 위해 height를 조정
        self.add_widget(Label(text='', size_hint_y=None, height=10))  # 한 칸 내림
        self.add_widget(Label(text=user_info.get_info(), font_size='18sp',
                              size_hint_y=None, height=100, font_name='H2GPRM',
                              halign='left', valign='middle', text_size=(490, None),
                              size_hint_x=0.5))  # 왼쪽으로 이동

        # '__능력치__' 전 여백 추가 (두 칸 띄우기 위해)
        self.add_widget(Label(text='\n', size_hint_y=None, height=20))  # 두 칸 띄우기

        # 능력치 출력
        self.add_widget(Label(text='__능력치__', font_size='24sp', bold=True,
                              size_hint_y=None, height=40, font_name='H2GPRM',
                              halign='left', valign='middle', size_hint_x=None, width=200))
        self.add_widget(Label(text='', size_hint_y=None, height=20))

        # 능력치 정보 출력 (정렬 적용)
        for name, level, desc in user_info.abilities:
            formatted_text = f'  {name.ljust(1)} : Lv {str(level).ljust(1)} : "{desc}"'
            ability_label = Label(text=formatted_text,
                                  font_size='18sp',
                                  size_hint_y=None, height=30,  # 높이를 줄여서 간격 줄임
                                  font_name='H2GPRM',
                                  halign='left', valign='middle',
                                  text_size=(800, None))  # text_size 추가
            ability_label.bind(size=ability_label.setter('text_size'))  # 텍스트 크기 자동 조정
            self.add_widget(ability_label)

        # 능력치와 구분선 사이 여백 추가 (20 높이)
        self.add_widget(Label(text='', size_hint_y=None, height=20))  # 여백 추가

        # 구분선 추가 (길이 15)
        self.add_widget(self.create_separator(height=15))  # 구분선 추가

        # 돌아가기 버튼 추가
        self.add_widget(self.create_back_button())

    def create_back_button(self):
        """돌아가기 버튼 생성."""
        back_button = Button(
            text='> 돌아간다', size_hint=(None, 1), width=200,  # 크기 조정 및 더 왼쪽으로 이동
            font_name='H2GPRM', font_size=24,
            background_color=(0, 0, 0, 1),  # 검정 배경
            color=(1, 1, 1, 1)  # 흰색 텍스트
        )
        back_button.bind(on_press=self.on_button_clicked)
        return back_button

    def create_separator(self, height=15):
        """구분선 위젯을 생성합니다."""
        separator = Widget(size_hint_y=None, height=height, size_hint_x=1)
        with separator.canvas:
            Color(1, 1, 1, 1)  # 흰색
            Line(points=[0, 0, 800, 0], width=2)  # 두께 2의 흰색 선
        return separator

    @staticmethod
    def on_button_clicked(instance):
        """돌아가기 버튼 클릭 이벤트."""
        print('돌아가기 버튼 클릭')


# 폰트 등록 호출 (UI 위젯 생성 전에)
FontManager.register_fonts()
