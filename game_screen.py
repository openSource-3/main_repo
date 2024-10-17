from kivy.app import App
from kivy.uix.screenmanager import Screen

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self):
        self.ids.go_to_ending.bind(on_press=self.end_game)

    def end_game(self, instance):
        app = App.get_running_app()
        app.game_ending('BAD')