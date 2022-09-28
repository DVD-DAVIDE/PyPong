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
BALL_VELOVITY_X = -5
BALL_VELOVITY_Y = 2.5
BALL_ACCELERATION_X = 0.5
BALL_ACCELERATION_Y = 0.5
FRAMERATE = 60

# Draw main scenario
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
gameover = pygame.image.load("data/gameover.jpg")

# Define classes

class Ball:
    RADIUS = 20

    def __init__(self, x, y, vx, vy, ax = 0, ay = 0):
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
        global BG_COLOR, BALL_COLOR, BORDER, HEIGHT, running, paddle, screen, gameover, drawWalls
        self.show(BG_COLOR)
        ## Check Collisions
        # Left Wall
        if self.x - self.RADIUS <= BORDER:
            self.vx = -self.vx
            self.ax = -self.ax
        # Right Wall / End Game
        if self.x + self.RADIUS >= WIDTH:
            screen.blit(gameover, ORIGIN)
            pygame.display.update()
            pygame.mouse.set_visible(True)
            while True:
                e = pygame.event.wait()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    screen.fill((0,0,0))
                    drawWalls()
                    break
                if e.type == pygame.QUIT:
                    running = False
                    break
            pygame.mouse.set_visible(False)
            self.vx = -self.vx
            self.ax = -self.ax
            
        # Top Wall
        if self.y - self.RADIUS <= BORDER:
            self.vy = -self.vy
            self.ay = -self.ay
        # Bottom Wall
        if self.y + self.RADIUS >= HEIGHT-BORDER:
            self.vy = -self.vy
        # Paddle
        if self.x + self.RADIUS >= paddle.x and self.y >= paddle.y and self.y <= paddle.y + paddle.HEIGHT:
            self.vx = -self.vx
            self.ay = -self.ay
        ## Movement
        self.x = self.x + self.vx
        self.y = self.y + self.vy
        self.vx = self.vx + self.ax
        self.vy = self.vy + self.ay
        self.show(BALL_COLOR)
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


# Create Objects
ball = Ball(WIDTH-2*Ball.RADIUS-Paddle.WIDTH, HEIGHT/2, BALL_VELOVITY_X, BALL_VELOVITY_Y)
ball.show(BALL_COLOR)

paddle = Paddle(WIDTH-Paddle.WIDTH-Paddle.OFFSET_LEFT, (HEIGHT-Paddle.HEIGHT)/2)
paddle.show(PADDLE_COLOR)

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
    ball.update()
    paddle.update()
    pygame.display.flip()
    clock.tick(FRAMERATE)

pygame.quit()