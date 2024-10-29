""" infoPage.py """

import os  # 운영체제 관련 기능을 사용하기 위해 필요
from kivy.core.text import LabelBase  # Kivy에서 커스텀 폰트를 등록하는 모듈
from kivy.uix.boxlayout import BoxLayout  # 수직 또는 수평으로 위젯을 정렬하기 위한 레이아웃
from kivy.uix.label import Label  # 텍스트를 출력하는 UI 위젯
from kivy.uix.button import Button  # 버튼을 생성하는 UI 위젯

# 1. 폰트 등록을 처리하는 클래스
class FontManager:
    """커스텀 폰트 등록을 위한 클래스."""

    @staticmethod  # 인스턴스 생성 없이 직접 호출 가능한 메서드 정의
    def register_fonts():
        """H2GPRM 폰트를 등록합니다."""
        # 현재 파일 경로 기준으로 폰트 파일 경로를 생성
        font_path = os.path.join(os.path.dirname(__file__), 'H2GPRM.ttf')
        # 'H2GPRM' 이름으로 폰트를 등록
        LabelBase.register(name='H2GPRM', fn_regular=font_path)

# 2. 사용자 정보와 능력치를 관리하는 클래스
class UserInfo:
    """사용자 정보를 저장하고 관리하는 클래스."""

    def __init__(self):
        """사용자 기본 정보를 초기화합니다."""
        self.userName = "이름"
        self.userState = "한밭대학교 5학년 2학기 재학 중이다."  # 사용자의 이름 또는 상태 정보
        self.userTrait = "처음 선택한 특성에 관한 문구"  # 사용자 특성에 대한 설명

        # 사용자의 능력치를 튜플 형식으로 저장 (이름, 레벨, 설명)
        self.abilities = [
            ("속도", 2, "능력치에 대한 설명"),
            ("지능", 2, "아니면 능력치 습득 힌트를 적어도 되겠어요"),
            ("창의", 1, "소소한 말을 써도 되겠네요"),
            ("행운", 3, "아무튼 내용이 들어갈 자리입니다"),
            ("체력", 2, "참고하세요  (>ㅂ0)/ ")
        ]

    def get_info(self):
        """사용자 이름과 특성을 포맷팅된 문자열로 반환합니다."""
        return f"{self.userName}\n{self.userState}\n\n\" {self.userTrait} \""  # 이름과 특성을 포함한 정보 반환

# 3. UI를 구성하는 클래스
class InfoPage(BoxLayout):
    """사용자 정보와 능력치를 출력하는 UI 페이지를 구성하는 클래스."""

    def __init__(self, screen_manager, **kwargs):
        """InfoPage 초기화 메서드."""
        super().__init__(**kwargs)  # 부모 클래스(BoxLayout)의 초기화 호출
        self.orientation = 'vertical'  # 수직 정렬 설정
        self.padding = [10, 10]  # 내부 여백 설정
        self.spacing = 10  # 위젯 간의 간격 설정
        self.screen_manager = screen_manager  # 전달된 ScreenManager 저장

        # UserInfo 클래스의 인스턴스 생성
        user_info = UserInfo()

        # 레이아웃에 UI 위젯 추가
        self.add_widget(Label(text='', size_hint_y=None, height=10))  # 한 칸 띄우기

        # 정보 제목 출력
        self.add_widget(Label(
            text='__정보__', font_size='24sp', bold=True,
            size_hint_y=None, height=40, font_name='H2GPRM',  # 커스텀 폰트 적용
            size_hint_x=None, width=160))

        self.add_widget(Label(text='', size_hint_y=None, height=10))  # 한 칸 띄우기

        # 사용자 정보 출력
        self.add_widget(Label(
            text=user_info.get_info(), font_size='18sp',  # 사용자 정보 텍스트
            size_hint_y=None, height=100, font_name='H2GPRM',  # 커스텀 폰트 적용
            text_size=(490, None), size_hint_x=0.5))

        self.add_widget(Label(text='\n', size_hint_y=None, height=20))  # 두 칸 띄우기

        # 능력치 제목 출력
        self.add_widget(Label(
            text='__능력치__', font_size='24sp', bold=True,
            size_hint_y=None, height=40, font_name='H2GPRM',
            size_hint_x=None, width=200))
        self.add_widget(Label(text='', size_hint_y=None, height=20))  # 여백 추가

        # 각 능력치 정보를 반복문을 통해 출력
        for name, level, desc in user_info.abilities:
            # 능력치 텍스트 형식 지정
            formatted_text = f'  {name.ljust(1)} : Lv {str(level).ljust(1)} : "{desc}"'
            ability_label = Label(
                text=formatted_text, font_size='18sp',
                size_hint_y=None, height=30,  # 높이 조정
                font_name='H2GPRM',  # 커스텀 폰트 적용
                text_size=(800, None))  # 텍스트 크기 지정
            ability_label.bind(size=ability_label.setter('text_size'))  # 위젯 크기와 텍스트 크기 연동
            self.add_widget(ability_label)  # 레이아웃에 능력치 추가

        self.add_widget(Label(text='', size_hint_y=None, height=20))  # 여백 추가

        # 돌아가기 버튼 생성 및 추가
        self.add_widget(self.create_back_button())

    def create_back_button(self):
        """돌아가기 버튼 생성."""
        back_button = Button(
            text='> 돌아간다', size_hint=(None, 1), width=200,  # 버튼 크기 설정
            font_name='H2GPRM', font_size=24,  # 커스텀 폰트 및 크기 적용
            background_color=(0, 0, 0, 1),  # 검정 배경색
            color=(1, 1, 1, 1)  # 흰색 텍스트 색상
        )
        back_button.bind(on_press=self.on_button_clicked)  # 버튼 클릭 이벤트 바인딩
        return back_button  # 버튼 반환

    def on_button_clicked(self, instance):
        """돌아가기 버튼 클릭 시 호출되는 메서드."""
        self.screen_manager.current = 'main'  # main이라는 페이지로 이동
