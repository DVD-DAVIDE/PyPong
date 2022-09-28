import os
import string
import pygame

# Variables
ORIGIN = (0,0)
WIDTH = 1200
HEIGHT = 600
BORDER = 20
BG_COLOR = pygame.Color("black")
WALL_COLOR = pygame.Color("green")
BALL_COLOR = pygame.Color("white")
PADDLE_COLOR = pygame.Color("red")
BALL_VELOCITY_X = -5.0
BALL_VELOCITY_Y = 2.5
BALL_ACCELERATION_X = -0.0005
BALL_ACCELERATION_Y = 0.0005
FRAMERATE = 60

# Draw main scenario
pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Consolas", 30)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
gameover = pygame.image.load(os.path.join("data", "gameover.jpg"))
score = 0
try:
    with open(os.path.join("data", "highscore.txt")) as f:
        high_score = int(f.read())
except:
    high_score = 0
# Define classes

class Ball:
    RADIUS = 20

    def __init__(self, x, y, vx, vy, ax = 0.0, ay = 0.0):
        self.origin = (x, y)
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay

    def show(self, color):
        global screen
        pygame.draw.circle(screen, color, (self.x, self.y), self.RADIUS)

    def update(self):
        global BG_COLOR, BALL_COLOR, BORDER, HEIGHT, running, paddle, scoreboard, screen, gameover, score, drawWalls
        self.show(BG_COLOR)
        ## Check Collisions
        # Left Wall
        if self.x - self.RADIUS <= BORDER:
            self.vx = -self.vx
            self.ax = -self.ax
        # Right Wall / End Game
        if self.x + self.RADIUS >= WIDTH:
            screen.blit(gameover, ORIGIN)
            scoreboard.update((255,0,0), (0,255,0))
            pygame.display.flip()
            pygame.mouse.set_visible(True)
            while True:
                e = pygame.event.wait()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    screen.fill((0,0,0))
                    pygame.display.flip()
                    self.show((0,0,0))
                    self.reset(self.origin)
                    break
                if e.type == pygame.QUIT:
                    running = False
                    break
            pygame.mouse.set_visible(False)
            score = 0
        # Top Wall
        if self.y - self.RADIUS <= BORDER:
            self.vy = -self.vy
            self.ay = -self.ay
        # Bottom Wall
        if self.y + self.RADIUS >= HEIGHT-BORDER:
            self.vy = -self.vy
            self.ay = -self.ay
        # Paddle
        if self.x + self.RADIUS >= paddle.x and self.y >= paddle.y and self.y <= paddle.y + paddle.HEIGHT:
            self.vx = -self.vx
            self.ax = -self.ax
            score = score + 1


        ## Movement
        self.x = self.x + self.vx
        self.y = self.y + self.vy
        self.vx = self.vx + self.ax
        self.vy = self.vy + self.ay
        self.show(BALL_COLOR)

    def reset(self, pos):
        global BALL_VELOCITY_X, BALL_VELOCITY_Y
        (self.x, self.y) = pos
        self.vx = BALL_VELOCITY_X
        self.vy = BALL_VELOCITY_Y

class Paddle:
    WIDTH = 20
    HEIGHT = 80
    OFFSET_LEFT = 10

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def show(self, color):
        global screen
        pygame.draw.rect(screen, color, pygame.Rect((self.x, self.y),(self.WIDTH, self.HEIGHT)))
    
    def update(self):
        global BG_COLOR, PADDLE_COLOR, BORDER, HEIGHT
        self.show(BG_COLOR)
        (_, my) = pygame.mouse.get_pos()
        y = my - self.HEIGHT/2
        if y < BORDER:
            y = BORDER
        elif y + self.HEIGHT > HEIGHT - BORDER:
            y = HEIGHT - BORDER - self.HEIGHT
        else:
            self.y = y
        self.show(PADDLE_COLOR)

class Score:
    def __init__(self, x, y, score = 0, high_score = 0) -> None:
        self.x = x
        self.y = y
        self.score = score
        self.high_score = high_score
    
    def show(self, color = (252,186,3)):
        global screen, font
        screen.blit(font.render("Score: " + str(self.score) + " - Best: " + str(self.high_score), False, color), (self.x, self.y))
    
    def update(self, bg_color = (0,0,0), fg_color = (252,186,3)):
        self.show(bg_color)
        global score, high_score
        self.score = score
        self.high_score = max([self.score, self.high_score])
        high_score = self.high_score
        self.show(fg_color)

# Create Objects
ball = Ball(WIDTH-2*Ball.RADIUS-Paddle.WIDTH, int(HEIGHT/2), BALL_VELOCITY_X, BALL_VELOCITY_Y, BALL_ACCELERATION_X, BALL_ACCELERATION_Y)
ball.show(BALL_COLOR)

paddle = Paddle(WIDTH-Paddle.WIDTH-Paddle.OFFSET_LEFT, (HEIGHT-Paddle.HEIGHT)/2)
paddle.show(PADDLE_COLOR)

scoreboard = Score(20,20,high_score=high_score)
scoreboard.show()

# Draw three walls
def drawWalls():
    pygame.draw.rect(screen, WALL_COLOR, pygame.Rect(ORIGIN, (WIDTH, BORDER)))
    pygame.draw.rect(screen, WALL_COLOR, pygame.Rect(ORIGIN, (BORDER, HEIGHT)))
    pygame.draw.rect(screen, WALL_COLOR, pygame.Rect((0,HEIGHT-BORDER), (WIDTH, BORDER)))

# Set mouse invisible
pygame.mouse.set_visible(False)
drawWalls()

clock = pygame.time.Clock()
running = True
while running:
    e = pygame.event.poll()
    if e.type == pygame.QUIT:
        running = False
    drawWalls()
    ball.update()
    paddle.update()
    scoreboard.update()
    pygame.display.flip()
    clock.tick(FRAMERATE)

with open(os.path.join("data", "highscore.txt"), "w") as f:
    f.write(str(high_score))
pygame.quit()