from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
import random

# Размеры экрана (под мобильные устройства)
Window.size = (300, 500)

class SnakeGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.snake = [(100, 100)]
        self.direction = (10, 0)
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
        self.start_game()

    def spawn_food(self):
        return (random.randint(0, 29)*10, random.randint(0, 49)*10)

    def start_game(self):
        Clock.schedule_interval(self.update, 0.1)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.on_keyboard_down)
        self._keyboard = None

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        key = keycode[1]
        if key == 'left' and self.direction != (10, 0):
            self.direction = (-10, 0)
        elif key == 'right' and self.direction != (-10, 0):
            self.direction = (10, 0)
        elif key == 'up' and self.direction != (0, -10):
            self.direction = (0, 10)
        elif key == 'down' and self.direction != (0, 10):
            self.direction = (0, -10)
        return True

    def update(self, dt):
        if self.game_over:
            return

        new_head = (self.snake[0][0] + self.direction[0], 
                    self.snake[0][1] + self.direction[1])

        # Проверка столкновений
        if (new_head in self.snake or 
            new_head[0] < 0 or new_head[0] >= 300 or 
            new_head[1] < 0 or new_head[1] >= 500):
            self.game_over = True
            self.add_widget(Label(text='Game Over! Score: {}'.format(self.score),
                             pos=(50, 250), font_size=30))
            return

        self.snake.insert(0, new_head)

        # Съедание еды
        if new_head == self.food:
            self.score += 1
            self.food = self.spawn_food()
        else:
            self.snake.pop()

        self.canvas.clear()
        with self.canvas:
            Color(1, 0, 0)
            Rectangle(pos=self.food, size=(10, 10))
            Color(0, 1, 0)
            for pos in self.snake:
                Rectangle(pos=pos, size=(10, 10))

class SnakeApp(App):
    def build(self):
        game = SnakeGame()
        return game

if __name__ == '__main__':
    SnakeApp().run()
