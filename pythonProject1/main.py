import kivy
from kivy.config import Config
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from main_menu import MainMenu
from game_screen import GameScreen
from ending_screen import EndingScreen

class MyGameApp(App):
    def build(self):
        sm = ScreenManager()
        
        Builder.load_file('main_menu.kv')
        Builder.load_file('ending_screen.kv')

        sm.add_widget(MainMenu(name='mainmenu'))
        sm.add_widget(GameScreen(name='gamescreen'))
        sm.add_widget(EndingScreen(name='endingscreen'))

        return sm

    def start_game(self):
        self.root.current = 'gamescreen'

    def game_ending(self, game_result):
        ending_screen = self.root.get_screen('endingscreen')
        ending_screen.show_ending(game_result)
        self.root.current = 'endingscreen'

    def quit_game(self):
        self.stop()

if __name__ == '__main__':
    MyGameApp().run()