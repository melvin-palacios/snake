import pygame
import random
import time
import os
import json

pygame.init()
pygame.display.set_caption('Snake')
H = 21
W = 21
CELL_SIZE = 36
BG = (255, 255, 255)
clock = pygame.time.Clock()
score = 0
count = 0
screen = pygame.display.set_mode((W * CELL_SIZE, H * CELL_SIZE))
last_move = time.time()
speed = 0.14
apple = pygame.image.load('img/apple.png')
apple = pygame.transform.scale(apple, (CELL_SIZE, CELL_SIZE))
field = [[0] * W for i in range(H)]

if not os.path.exists('score.json'):
    with open('score.json', 'w+') as f:
        mel_score = W * H
        f.write('{"name": "Mel", "score": ' + str(mel_score) + '}\n')
        f.write('{"name": "Max" , "score": 0}\n')



class Snake:
    def __init__(self, x, y, last_direction, direction):
        self.x = x
        self.y = y
        self.snake = [(self.y, self.x)]
        self.last_dir = last_direction
        self.dir = direction
        self.CELL_SIZE = CELL_SIZE
        self.W = W
        self.H = H
        self.length = 2
        self.score = score
        self.snake_init()
        self.pom_x, self.pom_y = 0, 0
        self.get_apple()

    def get_apple(self):
        for i in range(self.W):
            for j in range(self.H):
                if field[j][i] == 4:
                    field[j][i] = 0
        x = random.randint(0, self.W - 1)
        y = random.randint(0, self.H - 1)
        cor = (y, x)
        if not cor in self.snake:
            field[y][x] = 4
            self.pom_x, self.pom_y = x, y

    def draw(self):
        self.draw_field()
        self.draw_snake()
        self.draw_apple()
        self.draw_score()

    def draw_score(self):
        font = pygame.font.Font(None, 50)
        text = font.render('Score: ' + str(self.score), True, (0, 0, 0))
        screen.blit(text, (580, 20))

    def draw_apple(self):
        for i in range(self.W):
            for j in range(self.H):
                if field[j][i] == 4:
                    screen.blit(apple, (i * self.CELL_SIZE, j * self.CELL_SIZE))

    def snake_init(self):
        a = 1
        for i in range(self.length):
            self.snake.append((self.y, self.x + a))
            a += 1
        self.y, self.x = self.snake[-1]
        return self.snake

    def draw_snake(self):
        for i in range(self.length):
            for y, x in self.snake:
                pygame.draw.rect(screen, (15, 115, 191), (x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))

    def draw_field(self):
        a = 1
        for i in range(W):
            for j in range(H):
                if a % 2 == 0:
                    pygame.draw.rect(screen, (42, 170, 3), (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                else:
                    pygame.draw.rect(screen, (127, 255, 0), (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                a += 1

    def snake_field(self):
        for i in range(self.W):
            for j in range(self.H):
                field[j][i] = 0
        for y, x in self.snake:
            if self.snake == self.snake[-1]:
                field[y][x] = 2
            field[y][x] = 1

    def move(self):
        if self.dir == 'RIGHT':
            if self.x + 1 == self.pom_x and self.y == self.pom_y:
                self.score += 1
                self.get_apple()
                self.snake.append((self.y, self.x + 1))
            else:
                self.snake.append((self.y, self.x + 1))
                self.snake.pop(0)
            self.x += 1
        elif self.dir == 'LEFT':
            if self.x - 1 == self.pom_x and self.y == self.pom_y:
                self.score += 1
                self.get_apple()
                self.snake.append((self.y, self.x - 1))
            else:
                self.snake.append((self.y, self.x - 1))
                self.snake.pop(0)
            self.x -= 1
        elif self.dir == 'UP':
            if self.x == self.pom_x and self.y - 1 == self.pom_y:
                self.score += 1
                self.get_apple()
                self.snake.append((self.y - 1, self.x))
            else:
                self.snake.append((self.y - 1, self.x))
                self.snake.pop(0)
            self.y -= 1
        elif self.dir == 'DOWN':
            if self.x == self.pom_x and self.y + 1 == self.pom_y:
                self.score += 1
                self.get_apple()
                self.snake.append((self.y + 1, self.x))
            else:
                self.snake.append((self.y + 1, self.x))
                self.snake.pop(0)
            self.y += 1

    def check_coli(self):
        head = self.snake[-1]
        body = self.snake[:-1]
        if head in body:
            return True
        else:
            return False

    def check_wall(self):
        if self.x < 0 or self.x > self.W - 1 or self.y < 0 or self.y > self.H - 1:
            return True
        else:
            return False

def game_over():
    pygame.display.set_caption('Snake - Game Over')
    font = pygame.font.Font(None, 70)
    font_medium = pygame.font.Font(None, 50)
    text_game = font.render('GAME OVER', True, (219, 39, 39))
    text_score = font_medium.render(f'Your score: {game.score}', True, (255, 255, 255))
    text_save = font_medium.render('SAVE', True, (255, 255, 255))
    rect_save = pygame.Rect(240, 430, 95, 30)
    text_exit = font_medium.render('EXIT', True, (255, 255, 255))
    rect_exit = pygame.Rect(450, 430, 90, 30)
    while True:
        screen.fill((0, 0, 0))
        screen.blit(text_game, (240, 220))
        screen.blit(text_score, (280, 300))
        screen.blit(text_save, (240, 430))
        screen.blit(text_exit, (450, 430))
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_save.collidepoint(mouse):
                    save()
                    game.snake = [(5, 8), (5, 9), (5, 10)]
                    game.length = 3
                    game.x, game.y = game.snake[-1]
                    game.dir = 'RIGHT'
                    game.score = 0
                    return
                elif rect_exit.collidepoint(mouse):
                    pygame.quit()
        pygame.display.flip()

def save():
    pygame.display.set_caption('Snake - Save')
    name = ''
    font = pygame.font.Font(None, 70)
    font_medium = pygame.font.Font(None, 50)
    text_save = font.render('Enter your name', True, (255, 255, 255))
    text_name = font_medium.render(str(name), True, (255, 255, 255))
    text_saved = font_medium.render('SCORE SAVED !', True, (59, 255, 21))
    text_error = font_medium.render('ERROR !', True, (255, 0, 0))
    text_enter = font_medium.render('Press Enter to save', True, (255, 255, 255))
    while True:
        screen.fill((0, 0, 0))
        mouse = pygame.mouse.get_pos()
        text_name = font_medium.render(str(name), True, (255, 255, 255))
        screen.blit(text_save, (190, 190))
        screen.blit(text_name, (330, 300))
        screen.blit(text_enter, (230, 390))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    screen.fill((0, 0, 0))
                    if save_score(name, game.score):
                        screen.blit(text_saved, (250, 300))
                        pygame.display.flip()
                        time.sleep(1)
                        game_init()
                    else:
                        screen.blit(text_error, (250, 300))
                        pygame.display.flip()
                        time.sleep(1)
                        save()
                    return
                else:
                    name += event.unicode
        pygame.display.flip()


def save_score(name, score):
    if name == '':
        name = 'Unknown'
    try:
        with open('score.json', 'a') as f:
            f.write('{"name": "' + str(name) + '" , "score": ' + str(score) + '}\n')
            return True
    except:
        return False

def game_init():
    screen.fill((0, 0, 0))
    bg = pygame.image.load('img/bg.jpg').convert_alpha()
    bg = pygame.transform.scale(bg, (W * CELL_SIZE + 200, H * CELL_SIZE))
    pygame.display.set_caption('Snake - Menu')
    font_title = pygame.font.Font(None, 130)
    font = pygame.font.Font(None, 70)
    font_medium = pygame.font.Font(None, 50)
    text_title = font_title.render('SNAKE', True, (255, 255, 255))
    text_start = font.render('START', True, (255, 255, 255))
    text_score = font_medium.render('SCOREBOARD', True, (255, 255, 255))
    text_exit = font_medium.render('EXIT', True, (255, 255, 255))
    rect_start = pygame.Rect(290, 340, 158, 50)
    rect_score = pygame.Rect(250, 420, 248, 33)
    rect_exit = pygame.Rect(330, 620, 87, 30)
    while True:
        screen.blit(bg, (-170, 0))
        screen.blit(text_title, (220, 140))
        screen.blit(text_start, (290, 340))
        screen.blit(text_score, (250, 420))
        screen.blit(text_exit, (330, 620))
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_start.collidepoint(mouse):
                    return
                elif rect_score.collidepoint(mouse):
                    scoreboard()
                elif rect_exit.collidepoint(mouse):
                    pygame.quit()
        pygame.display.flip()


def scoreboard():
    screen.fill((0, 0, 0))
    pygame.display.set_caption('Snake - Scoreboard')
    font = pygame.font.Font(None, 70)
    font_medium = pygame.font.Font(None, 50)
    text_score = font.render('SCOREBOARD', True, (255, 255, 255))
    player_score = []
    player_score_end = []
    with open('score.json', 'r') as f:
        for line in f:
            player_score.append(line.strip())
    for i in range(0, len(player_score)):
        data = player_score[i]
        data = json.loads(data)
        name = data['name']
        score = data['score']
        name_score = f'{name} - {score}'
        player_score_end.append(name_score)
    text_return = font_medium.render('RETURN', True, (255, 255, 255))
    rect_return = pygame.Rect(330, 620, 120, 30)


    while True:
        screen.fill((150, 179, 3))
        screen.blit(text_score, (210, 140))
        for i in range(0, len(player_score_end)):
            text_scoreboard = font.render(player_score_end[i], True, (255, 255, 255))
            screen.blit(text_scoreboard, (290, 250 + i * 50))
        screen.blit(text_return, (300, 620))

        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_return.collidepoint(mouse):
                    game_init()
                    return
        pygame.display.flip()


game = Snake(5, 10, 'RIGHT', 'RIGHT')
game_init()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if count < 1:
                if event.key == pygame.K_LEFT:
                    if game.dir != 'RIGHT':
                        game.dir = 'LEFT'
                elif event.key == pygame.K_RIGHT:
                    if game.dir != 'LEFT':
                        game.dir = 'RIGHT'
                elif event.key == pygame.K_UP:
                    if game.dir != 'DOWN':
                        game.dir = 'UP'
                elif event.key == pygame.K_DOWN:
                    if game.dir != 'UP':
                        game.dir = 'DOWN'
                count += 1
    if time.time() - last_move > speed:
        last_move = time.time()
        game.move()
        count = 0
    if game.check_coli():
        game_over()
    if game.check_wall():
        game_over()
    game.draw()
    pygame.display.flip()
    clock.tick(60)
