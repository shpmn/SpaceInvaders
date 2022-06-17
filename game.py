import pygame
import random
import math

# initializing pygame
pygame.init()

# creating screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# caption and icon
pygame.display.set_caption("Space Invaders")

# Score
score_val = 0
scoreX = 5
scoreY = 5
font = pygame.font.Font('freesansbold.ttf', 20)

# Game Over
game_over_font = pygame.font.Font('freesansbold.ttf', 64)


class Invader:
    def __init__(self):
        self.invader_X = random.randint(64, 737)
        self.invader_Y = random.randint(450, 550)
        self.invader_Xchange = 0.2
        self.invader_Ychange = 30



def show_score(x, y):
    score = font.render("Points: " + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (190, 250))


playerImage = pygame.image.load('data/spaceship.png')
player_X = 370
player_Y = 523
player_Xchange = 0
default_player_Xchange = 0.4

# Invader
invaderImage = []
invader_X = []
invader_Y = []
invader_Xchange = []
invader_Ychange = []
no_of_invaders = 6
alien_images = ['data/alien_blue.png', 'data/alien_gray.png', 'data/alien_green.png',
                'data/alien_white.png', 'data/alien_yellow.png', 'data/alien_red.png']

for num in range(no_of_invaders):
    # invaderImage.append(pygame.image.load(random.choice(alien_images)))
    invader_X.append(random.randint(64, 737))
    invader_Y.append(random.randint(450, 550))
    invader_Xchange.append(0.2)
    invader_Ychange.append(30)

# Bullet
# rest - bullet is not moving
# fire - bullet is moving
bulletImage = pygame.image.load('data/bullet.png')
bullet_X = 0
bullet_Y = 100
bullet_Xchange = 0
bullet_Ychange = 2
bullet_state = "rest"


# Collision Concept
def isCollision(x1, x2, y1, y2):
    distance = math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2)))
    if distance <= 50:
        return True
    else:
        return False


def player(x, y):
    screen.blit(playerImage, (x - 16, y + 10))


def invader(x, y):
    invader_image = pygame.image.load(random.choice(alien_images))
    screen.blit(invader_image, (x, y))


def bullet(x, y):
    global bullet_state
    screen.blit(bulletImage, (x, y))
    bullet_state = "fire"


# game loop

running = True
while running:

    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Controling the player movement from the arrow keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_Xchange = -default_player_Xchange
            if event.key == pygame.K_RIGHT:
                player_Xchange = default_player_Xchange
            if event.key == pygame.K_SPACE:
                if bullet_state is "rest":
                    bullet_X = player_X + random.randint(-30, 10)
                    bullet(bullet_X, bullet_Y)
        if event.type == pygame.KEYUP:
            player_Xchange = 0

    # adding the change in the player position
    player_X += player_Xchange
    for i in range(no_of_invaders):
        invader_X[i] += invader_Xchange[i]

    # bullet movement
    if bullet_Y <= 0:
        bullet_Y = 600
        bullet_state = "rest"
    if bullet_state is "fire":
        bullet(bullet_X, bullet_Y)
        bullet_Y -= bullet_Ychange

    # movement of the invader
    for i in range(no_of_invaders):
        if invader_Y[i] >= 450:
            if abs(player_X - invader_X[i]) < 80:
                for j in range(no_of_invaders):
                    invader_Y[j] = 200
                game_over()
                break

        if invader_X[i] >= 735 or invader_X[i] <= 0:
            invader_Xchange[i] *= -1
            invader_Y[i] += invader_Ychange[i]

        # Collision
        collision = isCollision(bullet_X, invader_X[i], bullet_Y, invader_Y[i])
        if collision:
            score_val += 1
            bullet_Y = 600
            bullet_state = "rest"
            invader_X[i] = random.randint(64, 736)
            invader_Y[i] = random.randint(30, 200)
            invader_Xchange[i] *= -1

        invader(invader_X[i], invader_Y[i])

    # restricting the spaceship so that it doesn't go out of screen
    left_screen_border = 16
    right_screen_border = 750
    if player_X <= left_screen_border:
        player_X = left_screen_border
    elif player_X >= right_screen_border:
        player_X = right_screen_border

    player(player_X, player_Y)
    show_score(scoreX, scoreY)
    pygame.display.update()
 