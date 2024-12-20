import kivy
import random
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.anchorlayout import AnchorLayout
from kivy.clock import Clock  # Kivy의 Clock을 이용해 딜레이 처리
from typing import Tuple, Any
from kivy.uix.image import Image
from infoPage import InfoPage, FontManager
from progressPage import ProgressPage
import re
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
import sys
import os



# 기본 16:9 비율 설정 (예: 720x1280)
target_aspect_ratio = 16 / 9

class ColoredBox(Widget):
    # 1. 특별 메서드: __init__ 및 __class__method는 특별 메서드로, 객체 초기화 및 클래스 수준 작업 수행
    def __init__(self, color=(1, 0, 0, 1), **kwargs):  # 기본값은 빨간색
        super(ColoredBox, self).__init__(**kwargs)
        with self.canvas:
            Color(*color)  # 색 설정 (R, G, B, A)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        # 크기와 위치가 변할 때마다 배경을 다시 그려줍니다.
        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
class ClickableLabel(ButtonBehavior, Label):
    pass



class GameScreen(Screen):
    if hasattr(sys, '_MEIPASS'):
        fontName_Bold = os.path.join(sys._MEIPASS, 'GowunBatang-Bold.ttf')
    else:
        fontName_Bold = os.path.join(os.path.dirname(__file__), 'GowunBatang-Bold.ttf')
    if hasattr(sys, '_MEIPASS'):
        fontName_Regular = os.path.join(sys._MEIPASS, 'GowunBatang-Regular.ttf')
    else:
        fontName_Regular = os.path.join(os.path.dirname(__file__), 'GowunBatang-Regular.ttf')

    # 3. 데이터 구조체 - 딕셔너리와 집합: 딕셔너리 `ability_stat`는 게임 속 능력치 데이터를 저장하고 관리하는 데 사용
    ability_stat = {"컴퓨터기술": 0, "체력": 0, "운": 1, "허기": 0, "지능": 0, "타자": 0,
                    "속독": 0, "창의력":0, "속도" : 0, "돈": 3, "집중도": 3, "멘탈": 3,"성적": 100,  "sw" : 0, "zoom" : 0, "day" : 0, "팀인원":0, "dinner" : 0, "저녁약속" : 0, "동아리" : 0
                    ,"running" : 0, "service" : 0}
    on_choice_able = False
    start = False
    reaction_part = False
    event = False
    flag = True
    end = False
    day = 0
    choice = 0
    group_count = 0
    reaction_line = ""
    file_name = ""
    save_file_name = ""
    saved_re_position = ""
    previous_name = "mainmenu"

    listeners = []  # 변수 연결용

    def __init__(self, screen_manager=None, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.screen_manager = screen_manager  # ScreenManager 인스턴스 저장
        self.build()

    @classmethod
    def add_listener(cls, listener):
        """변경 사항을 알리기 위한 리스너를 추가합니다."""
        cls.listeners.append(listener)

    # 9. 객체 참조, 가변성, 재활용: `self.ability_stat`는 게임 내에서 상태 변경을 나타내는 가변 데이터 구조로 사용
    @classmethod
    def update_stat(cls, stat_name='day', value='0'):
        """능력치를 업데이트하고 리스너에게 변경 사항을 알립니다."""
        if stat_name in cls.ability_stat:
            cls.ability_stat[stat_name] = value
            cls.notify_listeners()  # 모든 리스너에게 변경 사항 알림
            print("리스너 변경사항 전달")

    @classmethod
    def notify_listeners(cls):
        """모든 리스너에게 능력치 변경을 알립니다."""
        for listener in cls.listeners:
            listener(cls.ability_stat)

    def get_resource_path(self, filename):
        """리소스 경로를 반환하는 함수"""
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, filename)
        return filename

    def build(self):
        print("빌드 실행")
        # 전체 레이아웃 (수직)
        self.main_layout = BoxLayout(orientation='vertical')

        # 가운데 부분의 레이아웃 (가로로 나눔)
        self.middle_layout = BoxLayout(orientation='horizontal', size_hint=(1, 6 / 7))

        # 텍스트 영역 (가로로 7/8)
        self.text_area = ClickableLabel(
            text="",
            font_size=18,
            size_hint=(7 / 8, 1),
            font_name=self.fontName_Regular,
            text_size=(720 * 7 / 8, None),
            halign='left',
            valign='top',
            markup=True,
        )

        # 텍스트 영역 배경을 하얀색으로 설정
        with self.text_area.canvas.before:
            Color(0, 0, 0, 1)  # 검은색
            self.text_bg_rect = Rectangle(size=self.text_area.size, pos=self.text_area.pos)

        # 텍스트 영역 크기 및 위치 변경 시 배경 업데이트
        self.text_area.bind(size=self.update_text_background, pos=self.update_text_background)
        self.text_area.bind(on_touch_down=self.on_click_next_text)
        # 오른쪽 레이아웃 (1/8 공간에 능력창과 진척도창 버튼 추가)
        self.right_layout = BoxLayout(orientation='vertical', size_hint=(1 / 8, 1))

        # 능력창 및 진척도창 버튼 추가
        self.ability_button = Button(text="능력창", font_name=self.fontName_Regular, size_hint=(1, 0.15))
        self.progress_button = Button(text="진척도", font_name=self.fontName_Regular, size_hint=(1, 0.15))

        self.ability_button.bind(on_press=self.open_info_page)
        self.progress_button.bind(on_press=self.open_progress_page)

        # 빈 공간을 검은색으로 설정
        self.black_space = ColoredBox(color=(0, 0, 0, 1), size_hint=(1, 0.5))

        # 오른쪽 레이아웃에 버튼과 빈 공간 추가 (버튼은 상단 정렬)
        self.right_layout.add_widget(self.ability_button)
        self.right_layout.add_widget(self.progress_button)
        self.stat_image_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.4))
        self.right_layout.add_widget(self.stat_image_layout)
        self.right_layout.add_widget(self.black_space)

        # 하단 선택지 영역 (수직으로 4개 선택지 배치)
        self.choice_layout = BoxLayout(orientation='vertical', size_hint=(1, 1 / 4))

        # 선택지 버튼들
        self.choice1 = Button(font_name=self.fontName_Bold, background_normal='', background_down='',
                              background_color=(0, 0, 0, 1))
        self.choice2 = Button(font_name=self.fontName_Bold, background_normal='', background_down='',
                              background_color=(0, 0, 0, 1))
        self.choice3 = Button(font_name=self.fontName_Bold, background_normal='', background_down='',
                              background_color=(0, 0, 0, 1))
        self.choice4 = Button(font_name=self.fontName_Bold, background_normal='', background_down='',
                              background_color=(0, 0, 0, 1))

        # 각 버튼에 이벤트 핸들러 연결
        self.choice1.bind(on_press=self.on_choice)
        self.choice2.bind(on_press=self.on_choice)
        self.choice3.bind(on_press=self.on_choice)
        self.choice4.bind(on_press=self.on_choice)

        # AnchorLayout을 사용하여 버튼을 아래쪽에 추가
        choice_anchor1 = AnchorLayout(anchor_y='bottom')
        choice_anchor1.add_widget(self.choice1)

        choice_anchor2 = AnchorLayout(anchor_y='bottom')
        choice_anchor2.add_widget(self.choice2)

        choice_anchor3 = AnchorLayout(anchor_y='bottom')
        choice_anchor3.add_widget(self.choice3)

        choice_anchor4 = AnchorLayout(anchor_y='bottom')
        choice_anchor4.add_widget(self.choice4)

        # choice_layout에 버튼들을 추가
        self.choice_layout.add_widget(choice_anchor4)
        self.choice_layout.add_widget(choice_anchor3)
        self.choice_layout.add_widget(choice_anchor2)
        self.choice_layout.add_widget(choice_anchor1)

        # 가운데 레이아웃에 텍스트 영역과 오른쪽 하얀색 공간 추가
        self.middle_layout.add_widget(self.text_area)  # 텍스트 영역 (7/8)
        self.middle_layout.add_widget(self.right_layout)  # 오른쪽 능력창, 진척도창, 검은색 공간 (1/8)

        # 메인 레이아웃에 가운데 레이아웃, 선택지 영역 순서대로 추가
        self.main_layout.add_widget(self.middle_layout)  # 가운데 레이아웃 (텍스트 + 오른쪽 버튼 및 빈 공간)
        self.main_layout.add_widget(self.choice_layout)  # 선택지 영역

        # 메인 레이아웃을 먼저 추가
        self.add_widget(self.main_layout)

        self.image_overlay = Widget()
        with self.image_overlay.canvas:
            self.image_rect = Rectangle(
                source="",  # 초기 상태에서 이미지를 비움
                size=(self.text_area.size[0], self.text_area.size[1] / 2),
                pos=(self.text_area.pos[0], self.text_area.pos[1] + self.text_area.size[1] / 2)
            )

        self.image_overlay.opacity = 0

        # 텍스트 영역과 이미지 레이아웃 크기 및 위치 동기화
        self.text_area.bind(pos=self.update_image_overlay, size=self.update_image_overlay)

        # 이미지 오버레이를 텍스트 위에 배치
        self.add_widget(self.image_overlay)

        # 윈도우 사이즈 변경 이벤트 핸들러 추가
        Window.bind(on_resize=self.adjust_layout)

        self.update_stat_images()

    def update_text_background(self, *args):
        """텍스트 영역 배경 업데이트."""
        self.text_bg_rect.size = self.text_area.size
        self.text_bg_rect.pos = self.text_area.pos

    def update_image_overlay(self, *args):
        """이미지 레이아웃 업데이트."""
        self.image_rect.pos = (self.text_area.pos[0], self.text_area.pos[1] + self.text_area.size[1] / 2)
        self.image_rect.size = (self.text_area.size[0], self.text_area.size[1] / 2)

    def reset_game(self):
        """ 게임 상태를 초기화하는 메서드 """
        self.start = True
        self.reaction_part = False
        self.flag = True
        self.is_waiting_for_click = False
        self.event = False
        self.end = False
        self.choice = 0
        self.current_line = 0
        self.day = 0
        self.group_count = 0
        self.reaction_line = ""
        self.file_name = self.get_resource_path(self.get_resource_path("./routine/start_story.txt"))
        self.save_file_name = ""
        self.saved_re_position = ""
        self.text_area.text = ""
        self.ability_stat = {"컴퓨터기술": 0, "체력": 0, "운": 1, "허기": 0, "지능": 0, "타자": 0,
                             "속독": 0, "창의력":0, "속도" : 0, "돈": 3, "집중도": 3, "멘탈": 3,"성적": 100, "sw" : 0,  "zoom" : 0, "day" : 0, "팀인원":0, "dinner" : 0, "저녁약속" : 0,"동아리" : 0
                             ,"running" : 0, "service" : 0}
        self.update_stat_images()
        self.story_lines = self.read_story_text(self.get_resource_path('./routine/start_story.txt')).splitlines()
        self.start_automatic_text()

        self.listeners = [] # 변수 연결용

    # 6. First-class Functions (일급 함수): 함수가 인자로 전달되거나 반환값으로 사용되는 사례로, 이벤트 시스템에서 콜백 함수를 사용

    def on_enter(self):
        # GameScreen에 들어왔을 때 텍스트 출력을 시작합니다.
        print("on enter 실행")
        if self.previous_name == "mainmenu":
            self.reset_game()
        else:
            print(self.previous_name)

    def open_info_page(self, instance):
        info_screen = self.screen_manager.get_screen('info')  # 'a' 화면 가져오기
        info_layout = info_screen.children[0]  # ABoxLayout 인스턴스 (Screen의 첫 번째 자식)
        info_layout.update_ability_stat(self.ability_stat)  # 점수 전달

        # a 화면으로 전환
        self.screen_manager.current = 'info'
        self.previous_name = "other"

    def open_progress_page(self, instance):
        # 'progress' 화면 가져오기
        progress_screen = self.screen_manager.get_screen('progress')
        progress_layout = progress_screen.children[0]  # ProgressPage 인스턴스

        progress_compo = progress_layout.progress_compo

        progress_compo.update_day_stat(self.day)  # update_day 메서드를 추가해 self.day 값을 반영하도록 함
        # progress 화면으로 전환
        self.screen_manager.current = 'progress'
        self.previous_name = "other"
    # 윈도우 크기가 변경될 때 비율 조정
    def adjust_layout(self, instance, width, height):
        # 현재 창의 비율 계산
        self.text_area.text_size = (width * 7 / 8-30, None)
        if width >800:
            self.text_area.font_size = 32
            self.choice1.font_size = 28
            self.choice2.font_size = 28
            self.choice3.font_size = 28
            self.choice4.font_size = 28
        else :
            self.text_area.font_size = 18
            self.choice1.font_size = 22
            self.choice2.font_size = 22
            self.choice3.font_size = 22
            self.choice4.font_size = 22

    # 7. 리팩토링: 클래스 구조로 캡슐화하고 복잡한 기능을 여러 메서드로 분리
    def update_stat_images(self):
        """ 스탯 값에 따라 이미지를 갱신하는 함수 """
        # 기존 이미지 제거
        self.stat_image_layout.clear_widgets()

        # '돈'에 해당하는 돈 이미지
        money_stat = self.ability_stat.get('돈', 0)
        money_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)
        for _ in range(money_stat):
            money_layout.add_widget(Image(source=self.get_resource_path('./public/image/icon/money.png')))  # 돈 이미지 경로 설정
        self.stat_image_layout.add_widget(money_layout)

        # '집중도'에 해당하는 세모 이미지
        focus_stat = self.ability_stat.get('집중도', 0)
        focus_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)
        for _ in range(focus_stat):
            focus_layout.add_widget(Image(source=self.get_resource_path('./public/image/icon/pen.png')))  # 연필 이미지 경로 설정
        self.stat_image_layout.add_widget(focus_layout)

        # '멘탈'에 해당하는 하트 이미지
        mental_stat = self.ability_stat.get('멘탈', 0)
        mental_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)
        for _ in range(mental_stat):
            mental_layout.add_widget(Image(source=self.get_resource_path('./public/image/icon/heart.png')))  # 하트 이미지 경로 설정
        self.stat_image_layout.add_widget(mental_layout)

    # 텍스트 파일에서 내용을 읽어오는 함수
    # 4. 데이터 구조체 - 텍스트와 바이트: 텍스트 데이터는 `read_story_text` 메서드에서 파일로부터 읽어오는 방식으로 사용
    # 5. 텍스트 파일: 텍스트 파일에서 스토리를 읽어오고 `read_story_text`에서 반환하는 방식으로 사용
    def read_story_text(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.file_name = file.name
                return file.read()
        except FileNotFoundError:
            return "스토리 파일을 찾을 수 없습니다."

    # 자동으로 텍스트를 출력하는 함수 이벤트 분기 확인
    def start_automatic_text(self, dt=None):
        if self.day % 2 == 0:
            self.ability_stat["day"] = 1
        else:
            self.ability_stat["day"] = 0
        while self.current_line < len(self.story_lines):  # 전체 내용 탐색
            line = self.story_lines[self.current_line].strip()  # 한 줄씩 입력받음

            if self.reaction_part:  # 리액션 파트에 돌입했을 경우
                # 내가 원하는 부분이 나올 때까지 탐색하는 부분
                if self.reaction_line == "# lecture":
                    num = random.randint(1, 3)
                    self.reaction_line = f"# lecture_{num+3*self.ability_stat['dinner']}"
                if line.startswith("#") and line == self.reaction_line:  # 내가 원하는 리액션 파트 진입
                    print("내가 원하는 리액션 파트 진입 성공")
                    print(self.file_name, self.current_line, line)
                    self.flag = True  # 텍스트 출력 활성화
                    self.current_line += 1  # 다음 줄 탐색
                    continue
                elif not self.flag:  # 내가 원하는 리액션 파트가 아닌 경우
                    self.current_line += 1  # 다음 줄 탐색
                    continue  # 다음 줄을 즉시 탐색
            if self.flag:
                print(self.file_name, self.current_line, line)
                if line.startswith("I"):  # 이미지 경로 처리
                    image_path = self.get_resource_path(line[1:].strip()) # 'I' 이후 경로 추출
                    print(f"이미지 경로 감지: {image_path}")
                    self.update_image_source(image_path)  # 이미지 업데이트
                    self.current_line += 1  # 다음 줄로 이동
                    self.image_overlay.opacity = 1
                    self.text_area.text = "\n\n\n\n\n"
                    Clock.schedule_once(self.start_automatic_text, 0.5)
                    return
                elif line.startswith("A"):
                    audio_path =self.get_resource_path(line[1:].strip())

                    if audio_path:  # "A" 다음 경로가 있는 경우
                        print(f"사운드 경로 감지: {audio_path}")
                        self.play_audio(audio_path)  # 사운드 재생
                    else:  # "A"만 있는 경우
                        print("사운드 페이드 아웃 요청")
                        self.fade_out_audio()  # 사운드 페이드 아웃

                    self.current_line += 1
                    continue
                # 4. 데이터 구조체 - 텍스트와 바이트: 줄 단위로 텍스트 데이터를 처리하고, 조건, 선택지, 빈 줄 등을 다룰 수 있는 구조를 구현
                elif line == "":  # 빈 줄일 경우 클릭 대기
                    print("빈줄 실행")
                    self.is_waiting_for_click = True  # True일 경우 텍스트 화면 클릭시 다음 줄 텍스트가 출력됨
                    return
                elif line.startswith("-"):  # 선택지 항목이면 버튼 텍스트로 설정하고 넘김
                    #자동으로 선택지 있는 부분을 읽음
                    self.is_waiting_for_click = False
                    self.on_choice_able = True
                    self.set_choices_from_story(self.current_line)
                    return
                # 6. First-class Functions (일급 함수): 조건문을 처리하는 함수가 인자로 전달되어 특정 부분의 동작을 결정
                elif line.startswith("#") and not self.reaction_part:  # 첫 번째 글자가 #일 때, 리액션 파트가 아닐 경우
                    self.reaction_line = line
                    while ":" in self.reaction_line and "?" in self.reaction_line:  # 조건문이 포함된 경우 파싱
                        print("조건이 포함된 리액션 파트 발견")
                        # `self.reaction_line`에서 조건문을 파싱
                        self.reaction_line = "#" + self.parse_conditional_reaction(self.reaction_line[1:])  # '#' 이후 전달
                    print("랜덤 이벤트 OR 리액션 파트 진입 성공")
                    self.load_alternate_story(self.current_line + 1,
                                              self.reaction_line)  # 세이브 텍스트 라인 설정 후 이벤트 스토리 or 리액션 파트 진입
                    return
                elif (line.startswith("#") and line != self.reaction_line) or line == "pass":
                    # 리액션 파트에 속해 있을 때, 다른 #을 썼을 경우. 혹은 pass라는 line을 썼을 경우
                    print("리액션 파트 종료")
                    self.reaction_part = False
                    self.story_lines = self.read_story_text(self.save_file_name).splitlines()  # 이전 스토리 파일 호출
                    self.current_line = self.saved_re_position + 1  # 저장된 위치로 돌아감
                    Clock.schedule_once(self.start_automatic_text, 0.5)
                    return
                else:
                    # 일반 텍스트는 출력 (한 줄씩)
                    self.text_area.text += line + "\n"
                    self.current_line += 1

                    # 다음 줄을 0.5초 후에 출력
                    Clock.schedule_once(self.start_automatic_text, 0.5)
                    return
        # 리액션 파트에서 모든 텍스트를 출력한 후 기존 파일로 복귀
        if self.reaction_part:
            print("리액션 파트 종료")
            self.story_lines = self.read_story_text(self.save_file_name).splitlines()  # 기존 텍스트 파일 호출
            self.current_line = self.saved_re_position + 1  # 저장된 위치로 돌아감
            #리액션 파트는 다른 이벤트나 시작, 메인 스토리에서도 호출 될 수 있게 다른 텍스트 위치 저장 변수를 사용함.
            self.reaction_part = False
            Clock.schedule_once(self.start_automatic_text, 0.5)
        elif self.end:
            self.previous_name = "mainmenu"
            self.end_game()
        # 7. 리팩토링: 반복적인 작업을 메서드로 분리하여 유지보수를 용이하게
        elif self.start:  # 종료 텍스트 파일이 start_story인 경우. 1회 실행
            self.story_lines = self.read_story_text(self.get_resource_path(self.get_resource_path('./routine/main_story.txt'))).splitlines()
            self.current_line = 0
            self.start = False
            self.day += 1
            self.text_area.text += f"{self.day}일차입니다.\n"
            Clock.schedule_once(self.start_automatic_text, 0.5)
        elif self.event:  # 이벤트 스토리에서 종료 됐을 시
            print("이벤트 스토리 종료 메인 스토리 위치로 돌아갑니다.")
            if self.file_name == self.get_resource_path("./event_story/i.txt"):
                self.current_line = 79
            else:
                self.current_line = self.saved_position + 1  # 저장된 위치로 돌아감
            self.story_lines = self.read_story_text(self.get_resource_path('./routine/main_story.txt')).splitlines()  # 메인 스토리 호출
            Clock.schedule_once(self.start_automatic_text, 0.5)
            self.event = False
        # 5. 텍스트 파일: 특정 조건에 따라 텍스트 파일을 읽고 처리하여 게임 흐름을 제어
        elif self.day == 4:  # 메인 스토리 루트가 5주차 진입 시 중간고사 이벤트
            self.day += 1
            self.story_lines = self.read_story_text(self.get_resource_path('./routine/middle_story.txt')).splitlines()
            self.current_line = 0
            Clock.schedule_once(self.start_automatic_text, 0.5)
        elif self.day <= 10 and self.day != 9:  # 메인 스토리 루틴 11주차까지 진행
            print("메인스토리 루트 진행")
            self.story_lines = self.read_story_text(self.get_resource_path('./routine/main_story.txt')).splitlines()
            self.current_line = 0
            self.day += 1
            self.text_area.text += f"{self.day}일차입니다.\n"
            Clock.schedule_once(self.start_automatic_text, 0.5)
        elif self.day == 9:  # 조별과제 10주차
            print("조별과제 엔딩 루트 진행")
            self.story_lines = self.read_story_text(self.get_resource_path(f"./group_task/result/{self.ability_stat['팀인원']}.txt")).splitlines()
            self.current_line = 0
            self.day += 1
            self.text_area.text += f"{self.day}일차입니다.\n"
            Clock.schedule_once(self.start_automatic_text, 0.5)
        elif self.day == 11: #12주차 기말고사 and end스토리 진입
            self.story_lines = self.read_story_text(self.get_resource_path('./routine/end_story.txt')).splitlines()
            self.current_line = 0
            self.day += 1
            Clock.schedule_once(self.start_automatic_text, 0.5)
        elif self.day == 12: #13주차
            self.load_ending_branch()

    # 1. 특별 메서드: 오버레이 이미지 업데이트를 위한 메서드
    def update_image_source(self, image_path):
        """이미지 오버레이에 새로운 이미지를 설정."""
        if self.image_rect:
            self.image_rect.source = image_path  # 이미지 경로 업데이트
            self.image_overlay.canvas.ask_update()  # 캔버스 업데이트 요청

    def play_audio(self, audio_path):
        """지정된 경로의 사운드를 재생."""
        if hasattr(self, 'sound') and self.sound:
            self.sound.stop()  # 기존에 재생 중인 사운드 정지

        self.sound = SoundLoader.load(audio_path)  # 새로운 사운드 로드
        if self.sound:
            print(f"사운드 재생 중: {audio_path}")
            self.sound.volume = 0  # 초기 볼륨 0
            self.sound.play()  # 사운드 재생

            # 사운드 길이 확인
            if self.sound.length and self.sound.length >= 5:  # 사운드 길이가 5초 이상인 경우
                print(f"사운드 길이: {self.sound.length}초, 점진적 볼륨 증가 시작")
                self.fade_in_event = Clock.schedule_interval(self.increase_volume, 0.1)  # 0.1초마다 볼륨 증가
            else:
                print(f"사운드 길이: {self.sound.length}초, 볼륨 즉시 최대")
                self.sound.volume = 1.0  # 볼륨을 즉시 최대치로 설정
        else:
            print(f"사운드 파일을 찾을 수 없습니다: {audio_path}")

    def increase_volume(self, dt):
        """볼륨을 점차적으로 증가."""
        if hasattr(self, 'sound') and self.sound:
            if self.sound.volume < 1.0:
                self.sound.volume = min(1.0, self.sound.volume + 0.05)  # 0.05씩 증가
            else:
                print("볼륨 최대치 도달")
                Clock.unschedule(self.fade_in_event)  # 볼륨 증가 중지

    def fade_out_audio(self):
        """사운드의 볼륨을 점진적으로 줄인 후 정지."""
        if hasattr(self, 'sound') and self.sound:
            self.fade_out_event = Clock.schedule_interval(self.reduce_volume, 0.1)  # 0.1초 간격으로 볼륨 감소

    def reduce_volume(self, dt):
        """사운드 볼륨을 감소시키는 함수."""
        if hasattr(self, 'sound') and self.sound:
            if self.sound.volume > 0:
                self.sound.volume = max(0, self.sound.volume - 0.05)  # 0.05씩 감소
            else:
                print("사운드 정지")
                self.sound.stop()
                self.sound = None
                Clock.unschedule(self.fade_out_event)  # 볼륨 감소 스케줄 취소

    def set_choices_from_story(self, start_index):
        choices = []
        adjustments = []

        # 선택지 라인들 (`-`로 시작하는 줄)을 추출
        while start_index < len(self.story_lines):
            line = self.story_lines[start_index].strip()

            # `-`로 시작하는 줄은 선택지로 처리
            if line.startswith("-"):
                choice_text = line[1:].strip()  # `-` 기호를 제거한 선택지 텍스트
                reaction_number = -1  # 기본값은 -1로 설정

                # `_`로 끝나는지 여부를 확인하고 필요 시 마지막 `_` 제거
                choice_has_underscore = choice_text.endswith("_")
                if choice_has_underscore:
                    choice_text = choice_text[:-1]

                # 조건문이 포함된 경우 처리
                while(True):
                    if ":" in choice_text and "?" in choice_text:
                        choice_text = self.parse_conditional_choice(choice_text)
                    else:
                        break

                # 확률값이 있는 경우 처리
                if "*" in choice_text:
                    choice_text = self.parse_luck_adjustment(choice_text)

                # 가중치 정보가 있는 경우 처리
                if "%" in choice_text or "&" in choice_text:
                    choice, adjustment = self.parse_choice_adjustment(choice_text)
                else:
                    choice, adjustment = choice_text, None

                # `[숫자]` 형태의 리액션 구분 숫자 추출
                match = re.search(r'\[(\d+)\]', choice)
                if match:
                    reaction_number = int(match.group(1))  # 숫자를 reaction_number로 설정
                    choice = re.sub(r'\[\d+\]', '', choice).strip()  # `[]` 구문 제거하여 선택지 텍스트만 남김

                # 빈 선택지는 choices에 추가하지 않음
                if choice:  # 선택지 텍스트가 빈 문자열이 아닌 경우에만 추가
                    choices.append((choice, choice_has_underscore, reaction_number))
                    adjustments.append(adjustment)
            else:
                break  # `-`로 시작하지 않으면 선택지 추출 종료

            start_index += 1

        # 최종 선택지 리스트 역순으로 저장
        choices.reverse()
        adjustments.reverse()

        # 선택지 버튼 텍스트 설정 (선택지 텍스트와 `_` 여부, reaction_number를 분리하여 사용)
        if len(choices) >= 1:
            self.choice1.text = choices[0][0]
            self.choice1.has_underscore = choices[0][1]  # `_` 여부 저장
            self.choice1.reaction_number = choices[0][2]
        if len(choices) >= 2:
            self.choice2.text = choices[1][0]
            self.choice2.has_underscore = choices[1][1]
            self.choice2.reaction_number = choices[1][2]
        if len(choices) >= 3:
            self.choice3.text = choices[2][0]
            self.choice3.has_underscore = choices[2][1]
            self.choice3.reaction_number = choices[2][2]
        if len(choices) >= 4:
            self.choice4.text = choices[3][0]
            self.choice4.has_underscore = choices[3][1]
            self.choice4.reaction_number = choices[3][2]

        # 선택지에 대응하는 능력치 조정 리스트 저장
        self.adjustments = adjustments

        # 선택지 이후의 줄을 스토리 출력 시작 위치로 설정
        self.current_line = start_index  # 선택지 이후의 첫 번째 줄로 이동

    def parse_conditional_choice(self, choice_text):
        # ':'와 '?'로 조건문을 나누기
        main_part, conditional_part = choice_text.split(":", 1)  # 분할 횟수 1 참일 때 실행 문장과 나머지로 이루어짐
        condition, else_part = conditional_part.split("?", 1)  # 분할 횟수 1 조건문과 거짓일 때 실행 문장으로 이루어짐

        # 조건문 해석
        stat_name = ''.join([char for char in condition if char.isalpha()])  # 영어 또는 한글만 출력 (변경 스탯)
        stat_value = int(''.join([char for char in condition if char.isdigit()]))  # 숫자만 출력 (변경값)
        operator = ''.join([char for char in condition if not char.isalnum()])  # 영어 또는 한글이 아닌 특수문자인 경우만 출력 (조건문부등호)

        # stat 딕셔너리에서 현재 능력치를 확인
        current_stat_value = self.ability_stat.get(stat_name, 0)  # 키가 존재하지 않을 경우 0을 반환 (0대신 None넣어도 될듯)

        # 조건 비교
        if self.evaluate_condition(current_stat_value, stat_value, operator):
            # 조건이 참이면 main_part를 선택지 텍스트로 사용하고 조정값 추출
            return main_part
        else:
            # 조건이 거짓이면 else_part를 선택지 텍스트로 사용하고 조정값 추출
            return else_part

    def parse_conditional_reaction(self, line_text):
        main_part, conditional_part = line_text.split(":", 1)  # 참일 때 실행 문장과 나머지로 분리
        condition, else_part = conditional_part.split("?", 1)  # 조건문과 거짓일 때 실행 문장으로 분리

        # 조건문 해석
        stat_name = ''.join([char for char in condition if char.isalpha()])  # 영어 또는 한글만 출력 (변경 스탯)
        stat_value = int(''.join([char for char in condition if char.isdigit()]))  # 숫자만 출력 (변경값)
        operator = ''.join([char for char in condition if not char.isalnum()])  # 특수문자만 출력 (조건문 부등호)

        # stat 딕셔너리에서 현재 능력치를 확인
        current_stat_value = self.ability_stat.get(stat_name, 0)  # 키가 존재하지 않을 경우 0 반환

        # 조건 비교
        if self.evaluate_condition(current_stat_value, stat_value, operator):
            # 조건이 참이면 main_part 반환
            return main_part
        else:
            # 조건이 거짓이면 else_part 반환
            return else_part

    # 6. First-class Functions (일급 함수): 콜백 함수와 조건문 평가를 통한 다이내믹한 게임 흐름 제어
    # 텍스트 파일의 조건문에 대한 판별 함수
    def evaluate_condition(self, current_value, target_value, operator):
        if operator == ">=":
            return current_value >= target_value
        elif operator == "<=":
            return current_value <= target_value
        elif operator == "==":
            return current_value == target_value
        elif operator == ">":
            return current_value > target_value
        elif operator == "<":
            return current_value < target_value
        return False  # 정의되지 않은 연산자일 경우 False 반환

    # 선택지 텍스트 내용과 능력치 조정 내용을 구분하는 함수
    def extract_choice_and_adjustment(self, text):
        if "%" in text or "&" in text:  # 수행 문장에 능력치 조정이 있는 지 판단
            choice, adjustment = self.parse_choice_adjustment(text)  # 있을 경우 능력치 조정
            return choice, adjustment
        else:
            return text, None  # 능력치 조정이 없는 경우 텍스트만 반환

    def parse_choice_adjustment(self, choice_text):
        """
        텍스트에서 여러 능력치 조정을 처리하는 함수
        예: %지능1&체력1 또는 &지능1%체력1 혼합 형태도 처리 가능
        """
        adjustments = []  # 여러 능력치 조정을 담을 리스트

        # 능력치 조정 전의 선택지 텍스트
        choice_part = re.split("[%&]", choice_text)[0].strip()

        # 조정치 부분만 추출하기 (%, & 기준으로 split)
        adjustment_parts = re.findall(r'[%&][가-힣A-Za-z0-9]+', choice_text)
        # %나 &로 시작하는 단어들 구분 추출 ex &지능1%속독1인경우 &나 %을 기준으로 나눠져서 ['&지능1','%속독1']이 된다.

        for part in adjustment_parts:
            sign = '+' if part[0] == '%' else '-'  # %면 +, &면 - (상황에 맞게 변경 가능)
            adjustments.append(self.extract_stat_adjustment(part[1:], sign))  # part[1:]조정 속성(&%)을 제외한 나머지 문장

        return choice_part, adjustments

    def extract_stat_adjustment(self, adjustment_text: str, operation: str) -> Tuple[str, int, str]:
        """
        주어진 능력치 조정 텍스트에서 능력치 이름과 값을 추출하고 조정 정보 반환
        """
        # 능력치 이름만 추출 (한글 또는 영어 알파벳만 사용)
        stat_name = ''.join([char for char in adjustment_text if char.isalpha()])

        # 능력치 값만 추출
        stat_value = ''.join([char for char in adjustment_text if char.isdigit()])

        # 값이 없을 경우 기본값 0 설정
        stat_value = int(stat_value) if stat_value else 0  # 문자형으로 받았으니 int형 변경

        return (stat_name, stat_value, operation)

    # 9. 객체 참조, 가변성, 재활용: 가변 데이터를 조건에 따라 변경하여 게임 상태를 관리
    def parse_luck_adjustment(self, choice_text):
        # *숫자* 형식을 찾고 파싱
        if '*' in choice_text:
            print("운 확인 요소 진입 성공")
            parts = choice_text.split('*')
            print("parts=", parts)
            luck_factor = int(parts[1])  # *숫자* 사이의 숫자
            player_luck = self.ability_stat["운"]

            # 성공 확률 계산 - 확률이 100%를 초과하지 않도록 보정
            # 예: (운 * 조정 값) / (운 * 조정 값 + 일정 보정값)
            max_luck_effect = 100  # 최대 보정값을 설정하여 확률의 상한을 제한
            success_chance = (player_luck * luck_factor) / (player_luck * luck_factor + max_luck_effect) * 100
            print("보정된 성공 확률:", success_chance)

            # 성공 여부 결정
            if random.uniform(0, 100) <= success_chance:
                return parts[0]  # 성공 시 앞쪽 텍스트 반환
            else:
                return parts[2]  # 실패 시 뒤쪽 텍스트 반환
        return choice_text  # *숫자*가 없으면 그대로 반환
    # 텍스트 영역을 클릭하면 다음 텍스트 출력 시작
    def on_click_next_text(self, *args):
        print("is_waiting_for_click : ", self.is_waiting_for_click)
        if self.is_waiting_for_click:
            self.is_waiting_for_click = False  # 클릭을 기다리는 상태를 해제
            self.text_area.text = ""  # 텍스트 영역 초기화
            if self.image_rect.source != "":
                self.image_rect.source = ""
                self.image_overlay.opacity = 0  # 이미지 레이아웃을 숨김
            self.current_line += 1
            self.start_automatic_text()

    # 1. 특별 메서드: 선택지 버튼을 클릭했을 때 호출되는 메서드
    def on_choice(self, instance):
        stat_text = ""
        if self.on_choice_able and instance.text != "":
            # 6. First-class Functions (일급 함수):  선택된 버튼의 인스턴스를 기반으로 관련 데이터를 가져와 처리
            self.select_text = instance.text
            if instance == self.choice1:
                adjustments = self.adjustments[0]  # (stat_name, stat_value, operation) 각 형태를 가진 배열
                self.choice = 0
                has_underscore = self.choice1.has_underscore  # `_` 여부 저장
            elif instance == self.choice2:
                adjustments = self.adjustments[1]
                self.choice = 1
                has_underscore = self.choice2.has_underscore
            elif instance == self.choice3:
                adjustments = self.adjustments[2]
                self.choice = 2
                has_underscore = self.choice3.has_underscore
            elif instance == self.choice4:
                adjustments = self.adjustments[3]
                self.choice = 3
                has_underscore = self.choice4.has_underscore
            else:
                adjustments = []  # 빈 리스트로 초기화
                has_underscore = False  # 기본값 False

            # 3. 데이터 구조체 - 딕셔너리와 집합: 선택지를 통해 능력치(딕셔너리) 값을 수정
            if adjustments is None:
                adjustments = []

            # 여러 능력치 조정 처리
            for adjustment in adjustments:
                if adjustment:
                    stat_name, stat_value, operation = adjustment
                    if stat_name in self.ability_stat:  # stat 딕셔너리에서 해당 능력치 확인
                        if operation == "+":
                            self.ability_stat[stat_name] += stat_value
                            if stat_name in ["돈", "집중도", "멘탈"] and self.ability_stat[stat_name] > 3:
                                # ["돈", "집중도", "멘탈"] 스탯이 최대 스탯인 3을 넘을 경우
                                self.ability_stat[stat_name] = 3  # 더해져도 최대치 3으로 설정
                            elif stat_name in list(self.ability_stat.keys())[0:12]:  # 능력치 부분은 능력치 조정 수치가 텍스트에 보임
                                stat_text += "[color=808080]|[/color] "
                                stat_text += f"[color=A5FFC9]{stat_name} {operation}{stat_value}[/color]  "
                        elif operation == "-" and self.ability_stat[stat_name] >= 1:
                            self.ability_stat[stat_name] -= stat_value
                            if stat_name in list(self.ability_stat.keys())[0:12]:
                                stat_text += "[color=808080]|[/color] "
                                stat_text += f"[color=FFA5A5]{stat_name} {operation}{stat_value}[/color]  "
                        print(f"{stat_name} 능력치가 {operation}{stat_value}만큼 조정되었습니다.")
                    else:
                        self.ability_stat[stat_name] = stat_value #주어진 능력치를 추가

            # 선택지 버튼 텍스트 초기화 (선택 후)
            self.clear_choices()
            if self.ability_stat['멘탈'] == 0 or self.ability_stat['집중도'] == 0:
                self.load_ending_branch()


            # 선택한 내용을 출력 후 이어서 출력
            self.text_area.text = ""
            self.text_area.text += f"[color=808080]{self.select_text}[/color] {stat_text}\n"

            # 선택 후 처리
            if has_underscore:
                # 선택한 텍스트가 `_`로 끝난 경우
                print("강제종료 시점", self.file_name, self.current_line)
                if self.file_name == self.get_resource_path("./reaction/reaction_a.txt") and self.current_line == 303:
                    self.current_line = 69
                else :
                    self.current_line = self.saved_position + 1  # 저장된 위치로 돌아감
                self.story_lines = self.read_story_text(self.get_resource_path('./routine/main_story.txt')).splitlines()  # 메인 스토리 호출
                self.on_choice_able = False
                self.reaction_part = False
                self.event = False  # 이벤트 스토리 판정 false
                self.start_automatic_text()
                self.update_stat_images()
            else:
                self.current_line += 1
                self.on_choice_able = False
                self.start_automatic_text()
                self.update_stat_images()
            print(self.ability_stat)
            if self.image_rect.source != "":
                self.image_rect.source = ""
                self.image_overlay.opacity = 0  # 이미지 레이아웃을 숨김

    def clear_choices(self):
        self.choice1.text = ""
        self.choice2.text = ""
        self.choice3.text = ""
        self.choice4.text = ""

    # 5. 텍스트 파일: 특정 조건에 따라 다른 스토리 파일을 불러오는 메서드
    def load_alternate_story(self, saved_position, line):
        if line == "# lecture":
            # 1~3 사이의 랜덤 정수를 생성하여 파일 이름 결정
            lecture_num = random.randint(1, 3)
            lecture_file_name = self.get_resource_path(f"./reaction/lecture.txt")

            print(f"강의 파트 파일 로드: {lecture_file_name}")

            # 강의 파트 파일 읽어들이기
            self.save_file_name = self.file_name  # 리액션 텍스트에 돌입하기 전 기존 텍스트 파일의 이름을 저장
            self.story_lines = self.read_story_text(lecture_file_name).splitlines()
            self.current_line = 0  # 강의 파트의 첫 번째 줄부터 시작
            self.saved_re_position = saved_position
            self.reaction_part = True  # 리액션 파일 진입 확인 변수
            self.flag = False  # 리액션 파일에 내가 원하는 부분이 나오기 전까지 자동 텍스트 출력 패스
            Clock.schedule_once(self.start_automatic_text, 0.5)
        elif line == "# group_task":
            if self.group_count >= 4: #5번째 부터는 조원 찾기 이벤트를 스킵한다.
                group_task_file_name = self.get_resource_path("./group_task/group_task_e.txt")
            else:
                group_task_file_name = self.get_resource_path(f"./group_task/group_task_{chr(ord('a')+self.group_count)}.txt")
            #group_task는 실행 될 때 마다 다음 파일을 읽음
            print(f"강의 파트 파일 로드: {group_task_file_name}")
            self.group_count += 1
            # 강의 파트 파일 읽어들이기
            self.save_file_name = self.file_name  # 리액션 텍스트에 돌입하기 전 기존 텍스트 파일의 이름을 저장
            self.story_lines = self.read_story_text(group_task_file_name).splitlines()
            self.current_line = 0  # 강의 파트의 첫 번째 줄부터 시작
            self.saved_position = saved_position
            self.event = True  # 이벤트와 유사한 별도의 강의 파트 => 종료 시 메인 파트로 돌아가고 리액션 기능을 사용가능함.
            Clock.schedule_once(self.start_automatic_text, 0.5)
        elif line == "#":
            # 랜덤 이벤트용 파일을 불러오기
            self.event = True
            file_name = self.get_resource_path(self.sub_event_story())
            self.story_lines = self.read_story_text(file_name).splitlines()
            if file_name == self.get_resource_path("./event_story/i.txt") and self.ability_stat["저녁약속"] == 1 and self.ability_stat["dinner"] == 1:#저녁 약속이 존재하고 지금이 저녁인 경우
                self.current_line = 15
            elif file_name == self.get_resource_path("./event_story/j-1.txt"):
                self.current_line = 60 * self.ability_stat["running"]
            elif file_name == self.get_resource_path("./event_story/j-2.txt"):
                self.current_line = 60 * self.ability_stat["service"]
            else:
                self.current_line = 0
            self.saved_position = saved_position
            Clock.schedule_once(self.start_automatic_text, 0.5)
        else:
            self.save_file_name = self.file_name  # 리액션 텍스트에 돌입하기 전 기존 텍스트 파일의 이름을 저장
            print("저장된 파일 이름", self.save_file_name)
            self.story_lines = self.read_story_text(self.get_resource_path(self.reaction_text())).splitlines()
            self.current_line = 0  # 새로운 파일의 첫 번째 줄부터 시작
            # 스토리가 끝났을 때 이전 파일로 돌아감
            self.saved_re_position = saved_position
            self.reaction_part = True  # 리액션 파일 진입 확인 변수
            self.flag = False  # 리액션 파일에 내가 원하는 부분이 나오기 전까지 자동 텍스트 출력 패스
            Clock.schedule_once(self.start_automatic_text, 0.5)

    def sub_event_story(self):
        sub_event_list = ["a.txt", "b.txt", "c.txt", "d.txt", "e.txt", "f.txt", "g.txt", "h.txt", "i.txt", "j.txt"]
        if self.ability_stat["동아리"] < 0 : #동아리 이벤트 진입 후 동아리에 들어가는 것을 거부했을 때. 동아리 이벤트를 삭제함
            sub_event_list = ["a.txt", "b.txt", "c.txt", "d.txt", "e.txt", "f.txt", "g.txt", "h.txt", "i.txt"]
        num = random.randint(0, len(sub_event_list)-1)
        print("진입확인", num)
        if self.ability_stat["dinner"] == 1 and self.ability_stat["저녁약속"] == 1:
            #현재 저녁약속이 존재하고 실제로 저녁 시간대일 때
            return "./event_story/" + "i.txt" #무조건 이벤트 i 실행
        elif num == 9 and self.ability_stat["동아리"] > 0: #동아리 이벤트에 진입하고 난 뒤, 동아리 참가했을 때 내가 참가한 동아리 이벤트를 들어감
            #동아리가 1인것은 홍보부스 - 하트비트 동아리 이벤트 2인 경우 체험부스 - 봉사활동 동아리 이벤트로 넘어감
            return "./event_story/" + f'j-{self.ability_stat["동아리"]}.txt'
        else:
            return "./event_story/" + f"{sub_event_list[num]}"

    # 7. 리팩토링: 코드의 반복성을 줄이고 재사용성을 높인 구조화된 로직
    def reaction_text(self):
        # 선택된 버튼의 reaction_number를 기준으로 텍스트 파일을 선택
        reaction_number = -1
        if self.choice == 0:
            reaction_number = self.choice1.reaction_number
        elif self.choice == 1:
            reaction_number = self.choice2.reaction_number
        elif self.choice == 2:
            reaction_number = self.choice3.reaction_number
        elif self.choice == 3:
            reaction_number = self.choice4.reaction_number

        # reaction_number에 따라 리액션 텍스트 파일 선택
        if reaction_number == -1:
            # 기본 동작 (reaction_number가 없을 때 기존 로직 실행)
            print("리액션 진입", self.choice)
            reaction_list = ["reaction_a.txt", "reaction_b.txt", "reaction_c.txt", "reaction_d.txt"]
            return "./reaction/" + reaction_list[self.choice]
        else:
            # reaction_number로 텍스트 파일 선택
            reaction_list = ["reaction_a.txt", "reaction_b.txt", "reaction_c.txt", "reaction_d.txt"]
            print("내가 정한 특수 리액션 진입", reaction_list[reaction_number])
            if 0 <= reaction_number < len(reaction_list):
                return "./reaction/" + reaction_list[reaction_number]
            else:
                print("경고: 유효하지 않은 reaction_number", reaction_number)
                return "./reaction/reaction_default.txt"  # 유효하지 않으면 기본 파일을 반환

    def load_ending_branch(self):
        print("엔딩 이벤트 실행")
        self.story_lines = self.read_story_text(self.get_resource_path(self.ending_branch_story())).splitlines()
        self.current_line = 0  # 새로운 파일의 첫 번째 줄부터 시작
        self.end = True
        Clock.schedule_once(self.start_automatic_text, 0.5)

    def ending_branch_story(self):
        if self.ability_stat['멘탈'] == 0:
            return "./ending_part/game_over_m.txt"
        elif self.ability_stat['집중도'] == 0:
            return "./ending_part/game_over_c.txt"
        elif self.ability_stat["성적"] > 90:
            return "./ending_part/hidden_end.txt"
        elif self.ability_stat["성적"] > 80:
            return "./ending_part/good_end.txt"
        elif self.ability_stat["성적"] > 70:
            return "./ending_part/normal_end.txt"
        else:
            return "./ending_part/bad_end.txt"

    def end_game(self):
        self.privious_name = "mainmenu"
        app = App.get_running_app()
        if self.ability_stat['멘탈'] == 0:
            app.game_ending('MENTAL_ZERO')
        elif self.ability_stat['집중도'] == 0:
            app.game_ending('CONCENTRATION_ZERO')
        elif self.ability_stat["성적"] > 90:
            app.game_ending('HIDDEN')
        elif self.ability_stat["성적"] > 80:
            app.game_ending('GOOD')
        elif self.ability_stat["성적"] > 70:
            app.game_ending('NORMAL')
        else:
            app.game_ending('BAD')