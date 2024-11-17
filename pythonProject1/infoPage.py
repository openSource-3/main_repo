import os
from kivy.core.text import LabelBase
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class FontManager:
    """커스텀 폰트 등록을 위한 클래스."""

    @staticmethod
    def register_fonts():
        """H2GPRM 폰트를 등록합니다."""
        font_path = os.path.join(os.path.dirname(__file__), 'H2GPRM.ttf')
        LabelBase.register(name='H2GPRM', fn_regular=font_path)


class InfoPage(BoxLayout):
    """사용자 정보와 능력치를 출력하는 UI 페이지를 구성하는 클래스."""
    def __init__(self, screen_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager

        self.orientation = 'vertical'
        self.padding = [10, 10]
        self.spacing = 10
        self.userName = "김한밭"
        self.userState = "한밭대학교 5학년 2학기 재학 중이다."
        self.userTrait = "처음 선택한 특성에 관한 문구"

        from game_screen import GameScreen

        # GameScreen에서 능력치 불러오기
        GameScreen.add_listener(self.on_stat_update)  # 리스너 추가
        self.ability_stat = GameScreen.ability_stat  # 초기 능력치 불러오기

        self.setup_ui()

    def on_stat_update(self, stat):
        """GameScreen에서 능력치 업데이트가 발생했을 때 호출되는 메서드."""
        self.update_ability_stat(stat)

    def update_ability_stat(self, stat):
        """전달받은 stat 배열을 사용해 UI 업데이트."""
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
        return f"{self.userName}\n{self.userState}\n\n\" {self.userTrait} \""

    def setup_ui(self):
        """UI를 구성하고 초기화합니다."""
        self.add_widget(Label(text='', size_hint_y=None, height=10))  # 한 칸 띄우기
        self.add_widget(Label(
            text='__정보__', font_size='24sp', bold=True,
            size_hint_y=None, height=40, font_name='H2GPRM',
            size_hint_x=None, width=160
        ))
        self.add_widget(Label(text='', size_hint_y=None, height=10))  # 한 칸 띄우기
        self.add_widget(Label(
            text=self.get_info(), font_size='18sp',
            size_hint_y=None, height=100, font_name='H2GPRM',
            text_size=(490, None), size_hint_x=0.5
        ))
        self.add_widget(Label(text='\n', size_hint_y=None, height=20))  # 두 칸 띄우기

        self.add_widget(Label(
            text='__능력치__', font_size='24sp', bold=True,
            size_hint_y=None, height=40, font_name='H2GPRM',
            size_hint_x=None, width=200
        ))
        self.add_widget(Label(text='', size_hint_y=None, height=20))  # 여백 추가

        for name, level in self.ability_stat.items():
            description = self.get_ability_description(name)
            if description != "설명이 없습니다.":
                print(f"Name: {name}, Level: {level}")

                formatted_text = f'  {name} : Lv {level} : "{description}"'
                ability_label = Label(
                    text=formatted_text, font_size='18sp',
                    size_hint_y=None, height=30,
                    font_name='H2GPRM',
                    text_size=(800, None)
                )
                ability_label.bind(size=ability_label.setter('text_size'))
                self.add_widget(ability_label)

        self.add_widget(Label(text='', size_hint_y=None, height=20))  # 여백 추가
        self.add_widget(self.create_back_button())

    def get_ability_description(self, name):
        """각 능력치의 설명을 반환합니다."""
        descriptions = {
            "컴퓨터기술": "컴퓨터를 다루는 능력",
            "체력": "육체적인 힘과 건강",
            "운": "행운과 기회",
            "지능": "논리적 사고 및 문제 해결 능력",
            "타자": "빠르게 정확히 타자치는 능력",
            "속독": "문서를 빠르게 읽는 능력",
            "창의력": "창의적 사고와 발상"
        }
        return descriptions.get(name, "설명이 없습니다.")

    def create_back_button(self):
        """돌아가기 버튼 생성."""
        back_button = Button(
            text='> 돌아간다', size_hint=(None, 1), width=200,
            font_name='H2GPRM', font_size=24,
            background_color=(0, 0, 0, 1),
            color=(1, 1, 1, 1)
        )
        back_button.bind(on_press=self.on_button_clicked)
        return back_button

    def on_button_clicked(self, instance):
        """돌아가기 버튼 클릭 시 호출되는 메서드."""
        self.screen_manager.current = 'gamescreen'