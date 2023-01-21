import pygame
from pygame.locals import *  # import certain global variable
import time
import random

SIZE = 30
BACKGROUND_COLOR = (174, 153, 148)


class Apple:
    def __init__(self, surface):
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = surface
        self.x, self.y = SIZE*3, SIZE*3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 14)*SIZE
        self.y = random.randint(1, 14)*SIZE


class Snake:
    def __init__(self, surface, length):
        self.length = length
        self.parent_screen = surface
        # method loading the image, block or snake
        self.block = pygame.image.load("resources/block2.jpg").convert()
        self.x, self.y = [SIZE]*length, [SIZE]*length
        self.direction = 'down'

    def draw(self):
        self.parent_screen.fill(BACKGROUND_COLOR)  # clear the screen
        for i in range(self.length):  # to add snake body
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.update()

    def increase_lenght(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_up(self):
        self.direction = 'up'
        # self.y -= 10
        # self.draw()

    def move_down(self):
        self.direction = 'down'
        # self.y += 10
        # self.draw()

    def move_left(self):
        self.direction = 'left'
        # self.x -= 10
        # self.draw()

    def move_right(self):
        self.direction = 'right'
        # self.x += 10
        # self.draw()

    def walk(self):

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # drawing the snake based on current direction
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE

        self.draw()


class Game:
    def __init__(self):
        pygame.init()  # initiate pygame
        # play bg music
        self.play_background_music()
        # initialize a window on screen for display
        self.surface = pygame.display.set_mode((500, 500))  # background
        # put the screen
        self.snake = Snake(self.surface, 1)
        # draw the snake
        self.snake.draw()
        # put the apple and draw it
        self.apple = Apple(self.surface)
        self.apple.draw()
        # initialize to put music by mixer: sound mode
        pygame.mixer.init()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 <= x2 + SIZE:
            if y1 >= y2 and y1 <= y2 + SIZE:
                return True
        return False

    def play_background_music(self):
        pygame.mixer.music.load("resources/bg.mp3")
        pygame.mixer.music.play()

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def play(self):
        self.snake.walk()  # snake will keeping moving on and on, without press key
        self.apple.draw()
        self.display_score()
        pygame.display.update()

        # snake colliding with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            # play music
            self.play_sound("ding")
            self.snake.increase_lenght()
            self.apple.move()

        # snake colliding with it self
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise "Game Over"

        # snake colliding with the border
        if not (0 <= self.snake.x[0] <= 500 and 0 <= self.snake.y[0] <= 500):
            self.play_sound("crash")
            raise "Hit the boundary, ERROR"

    def display_score(self):
        font = pygame.font.SysFont('arial', 25)
        score = font.render(
            f"Score: {self.snake.length}", True, (0, 0, 0))
        self.surface.blit(score, (400, 10))

    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 20)
        line1 = font.render(
            f"Game is Over ! Your score is {self.snake.length}", True, (0, 0, 0))
        self.surface.blit(line1, (80, 150))
        line2 = font.render(
            f"To play again press Enter. To exit press Escape!", True, (0, 0, 0))
        self.surface.blit(line2, (70, 200))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False
                        pygame.mixer.music.unpause()

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.25)


# main routine in python
if __name__ == "__main__":
    game = Game()
    game.run()
