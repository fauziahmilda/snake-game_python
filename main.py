import pygame
from pygame.locals import *  # import certain global variable
import time

SIZE = 30


class Apple:
    def __init__(self, surface):
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = surface
        self.x, self.y = SIZE*3, SIZE*3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()


class Snake:
    def __init__(self, surface, length):
        self.length = length
        self.parent_screen = surface
        # method loading the image, block or snake
        self.block = pygame.image.load("resources/block2.jpg").convert()
        self.x, self.y = [SIZE]*length, [SIZE]*length
        self.direction = 'down'

    def draw(self):
        self.parent_screen.fill((174, 153, 148))  # clear the screen
        for i in range(self.length):  # to add snake body
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.update()

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

        # initialize a window on screen for display
        self.surface = pygame.display.set_mode((500, 500))  # background
        # put the screen
        self.snake = Snake(self.surface, 6)
        # draw the snake
        self.snake.draw()
        # put the apple and draw it
        self.apple = Apple(self.surface)
        self.apple.draw()

    def play(self):
        self.snake.walk()  # snake will keeping moving on and on, without press key
        self.apple.draw()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

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

            self.play()

            time.sleep(0.3)


# main routine in python
if __name__ == "__main__":
    game = Game()
    game.run()
