import os
import sys
from kivy.core.text import LabelBase
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

class FontManager:
    """커스텀 폰트 등록을 위한 클래스."""
    @staticmethod
    def register_fonts():
        """H2GPRM 폰트를 등록합니다."""
        # 5. 텍스트 파일: 폰트 파일 경로를 확인하고 등록
        if hasattr(sys, '_MEIPASS'):
            font_path = os.path.join(sys._MEIPASS, 'H2GPRM.ttf')
        else:
            font_path = os.path.join(os.path.dirname(__file__), 'H2GPRM.ttf')
        LabelBase.register(name='H2GPRM', fn_regular=font_path)



class InfoPage(FloatLayout):
    """사용자 정보와 능력치를 출력하는 UI 페이지를 구성하는 클래스."""
    def __init__(self, screen_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        self.userName = "김한밭"
        self.userState = "한밭대학교 5학년 2학기 재학 중이다."
        self.userTrait = "엔딩까지 화이팅!"

        from game_screen import GameScreen

        # GameScreen에서 능력치 불러오기
        # 1. 특별 메서드:  GameScreen의 add_listener 메서드 호출
        GameScreen.add_listener(self.on_stat_update)  # 리스너 추가
        self.ability_stat = GameScreen.ability_stat  # 초기 능력치 불러오기

        # UI 구성
        self.setup_ui()

    def on_stat_update(self, stat):
        """GameScreen에서 능력치 업데이트가 발생했을 때 호출되는 메서드."""
        self.update_ability_stat(stat)

    def update_ability_stat(self, stat):
        """전달받은 stat 배열을 사용해 UI 업데이트."""
        # 3. 데이터 구조체 - 딕셔너리와 집합: stat 딕셔너리를 활용하여 능력치 관리
        self.ability_stat = stat
        print("infoPage에서 Stat 데이터:", self.ability_stat)
        self.update_ui()  # UI 업데이트 로직

    def update_ui(self):
        """UI를 능력치 정보에 맞게 업데이트."""
        # UI 갱신 로직 추가
        self.clear_widgets()
        self.setup_ui()

    def get_info(self):
        """사용자 이름과 특성을 포맷팅된 문자열로 반환합니다."""
        # 4. 데이터 구조체 - 텍스트와 바이트: 포맷팅을 통해 문자열 생성
        return f"{self.userName}\n{self.userState}\n\n\" {self.userTrait} \""

    def setup_ui(self):
        """UI를 구성하고 초기화합니다."""
        # 텍스트 레이아웃
        text_layout = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height=400,
            pos_hint={'top': 0.9},  # top 위치를 0.9로 변경해 1cm 정도 아래로 이동
            spacing=10  # 위젯 간 간격 추가
        )

        # 정보 제목
        text_layout.add_widget(self.create_label('__정보__', font_size='24sp', height=40, bold=True, padding_y=38))

        # 사용자 정보
        text_layout.add_widget(self.create_label(self.get_info(), font_size='18sp', height=100, padding_y=38))

        # 능력치 제목
        text_layout.add_widget(self.create_label('__능력치__', font_size='24sp', height=40, bold=True, padding_y=38))

        # 3. 데이터 구조체 - 딕셔너리와 집합: 능력치 딕셔너리를 순회하며 UI를 동적으로 생성
        for name, level in self.ability_stat.items():
            description = self.get_ability_description(name)
            if description != "설명이 없습니다.":
                formatted_text = f'  {name} : Lv {level} : "{description}"'
                text_layout.add_widget(self.create_label(formatted_text, font_size='18sp', height=30, padding_y=38))

        # 텍스트 레이아웃 추가
        self.add_widget(text_layout)

        # 돌아가기 버튼
        self.add_widget(self.create_back_button())

    def create_label(self, text, font_size, height, bold=False, padding_y=0):
        """공통적으로 사용되는 Label을 생성."""
        # 3. 데이터 구조체 - 딕셔너리와 집합: 능력치 설명 딕셔너리 사용
        return Label(
            text=text,
            font_size=font_size,
            bold=bold,
            size_hint=(None, None),  # 크기를 고정
            width=800, height=height,  # 기존 높이를 유지
            font_name='H2GPRM',
            halign='left',
            valign='middle',  # 텍스트 세로 정렬 유지
            text_size=(800, None),  # 텍스트 너비 고정
            padding=(50, padding_y)  # 패딩 추가: Y축으로 아래로 이동
        )

    def get_ability_description(self, name):
        """각 능력치의 설명을 반환합니다."""
        descriptions = {
            "컴퓨터기술": "컴퓨터에 대한 기본적인 이해",
            "체력": "깔끔한 코딩도 좋지만 건강도 꼭 챙기기",
            "운": "어떨 때는 순전히 운이 모든 걸 결정한다",
            "지능": "문제 접근에 필수적인 문제 해결 능력",
            "타자": "무시할 수 없는 요소",
            "속독": "문서를 빠르게 읽고 이해하기",
            "창의력": "아이디어를 위한 말랑말랑 두뇌"
        }
        return descriptions.get(name, "설명이 없습니다.")

    def create_back_button(self):
        """돌아가기 버튼 생성."""
        back_button = Button(
            text='> 돌아간다',
            size_hint=(None, None),  # 고정 크기로 설정
            width=200, height=50,  # 버튼 크기 설정
            font_name='H2GPRM', font_size=24,
            background_color=(0, 0, 0, 1),
            color=(1, 1, 1, 1),
            pos_hint={'x': 0.05, 'y': 0.05}  # 왼쪽 아래에 위치
        )
        back_button.bind(on_press=self.on_button_clicked)
        return back_button

    def on_button_clicked(self, instance):
        """돌아가기 버튼 클릭 시 호출되는 메서드."""
        # 9. 객체 참조, 가변성, 재활용: screen_manager의 상태를 변경하여 화면을 재활용
        self.screen_manager.current = 'gamescreen'