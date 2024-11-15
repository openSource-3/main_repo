from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.properties import StringProperty


class EndingScreen(Screen):
    image_source = StringProperty('public/image/ending_screen/background.jpg')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.full_text_lines = []
        self.displayed_text = ""
        self.current_index = 0

    def show_ending(self, game_result):
        if game_result == 'BAD':
            self.image_source = 'public/image/ending_screen/bad-ending.jpg'
            ending_text_file = './public/script/bad-ending.txt'
        elif game_result == 'NORMAL':
            self.image_source = 'public/image/ending_screen/normal-ending.jpg'
            ending_text_file = './public/script/normal-ending.txt'
        elif game_result == 'GOOD':
            self.image_source = 'public/image/ending_screen/good-ending.jpg'
            ending_text_file = './public/script/good-ending.txt'
        elif game_result == 'HIDDEN':
            self.image_source = 'public/image/ending_screen/hidden-ending.jpeg'
            ending_text_file = './public/script/hidden-ending.txt'

        with open(ending_text_file, "r", encoding='utf-8') as file:
            self.full_text_lines = file.readlines()

        self.displayed_text = ""
        self.current_index = 0
        Clock.schedule_interval(self.update_text, 1)

    def update_text(self, dt):
        if self.current_index < len(self.full_text_lines):
            self.displayed_text += self.full_text_lines[self.current_index]
            self.ids.ending_label.text = self.displayed_text
            self.current_index += 1
        else:
            Clock.unschedule(self.update_text)
            self.add_go_to_main_button()

    def add_go_to_main_button(self):
        btn = Button(
            on_press=self.go_back_to_main_menu,
            size_hint=(None, None),
            size=(100, 100),
            background_normal='public/image/ending_screen/graduation_cap.png',
            background_down='public/image/ending_screen/graduation_cap.png',
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.ids.ending_button_box.add_widget(btn)

    def go_back_to_main_menu(self, instance):
        self.manager.current = 'mainmenu'