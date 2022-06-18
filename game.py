# Simple version of Space Invaders
# Authors: Lech Horosiewicz-Wróbel, Adam Byczynski
# Date: 18.06.2022

# TODO: przeciwnicy znikają jak dotkną sciany
# TODO: pociski nie lecą xd


import pygame
import random
import math

pygame.init()
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
screen_width, screen_height = 800, 600
SCREEN = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders")


class InitialSetup:
    pass


class Enemy:
    alien_images = ['data/alien_blue.png', 'data/alien_gray.png', 'data/alien_green.png',
                    'data/alien_white.png', 'data/alien_yellow.png', 'data/alien_red.png']

    def __init__(self):
        self.X = random.randint(64, 737)
        self.Y = random.randint(20, 80)
        self.X_change = random.uniform(0.1, 0.4)
        self.Y_change = random.randint(25, 40)
        self.invader_image = pygame.image.load(random.choice(self.alien_images))

    def draw_on_screen(self):
        SCREEN.blit(self.invader_image, (self.X, self.Y))

    def move(self):
        self.X += self.X_change
        if self.X >= 735 or self.X <= 0:
            self.X_change *= -1
            self.Y += self.Y_change
            self.X_change += 0.05


class Player:
    def __init__(self):
        self.player_image = pygame.image.load('data/spaceship.png')
        self.X = 370
        self.Y = 523
        self.X_change = 0
        self.default_player_X_change = 0.4

    def draw_on_screen(self):
        SCREEN.blit(self.player_image, (self.X - 16, self.Y + 10))

    def move(self):
        left_screen_border = 16
        right_screen_border = 750
        self.X += self.X_change
        if self.X <= left_screen_border:
            self.X = left_screen_border
        elif self.X >= right_screen_border:
            self.X = right_screen_border


class Bullet:
    def __init__(self):
        self.bullet_image = pygame.image.load('data/bullet.png')
        self.X = 0
        self.Y = 100
        self.X_change = 0
        self.Y_change = 2
        self.state = "inactive"

    @staticmethod
    def is_collision(x1, x2, y1, y2):
        distance = math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2)))
        if distance <= 30:
            return True
        else:
            return False

    def draw_on_screen(self):
        SCREEN.blit(self.bullet_image, (self.X, self.Y))
        self.state = "fire"

    def move(self):
        if self.Y <= 0:
            self.Y = 560
            state = "inactive"
        if self.state is "fire":
            self.draw_on_screen()
            self.Y -= self.Y_change


class Score:
    def __init__(self):
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.value = 0
        self.X, self.Y = 5, 5

    def draw_on_screen(self):
        score = self.font.render("Points: " + str(self.value), True, WHITE_COLOR)
        SCREEN.blit(score, (self.X, self.Y))


game_over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over():
    game_over_text = game_over_font.render("GAME OVER", True, WHITE_COLOR)
    SCREEN.blit(game_over_text, (190, 250))



def main():
    player = Player()  # nie działało ruszanie statkiem bo caly czas
    # spawnował nowy w tym samym miejscu, wiec w domyslnym położeniu

    number_of_enemies = 6
    enemies = []
    for num in range(number_of_enemies):
        new_enemy = Enemy()
        enemies.append(new_enemy)

    bullet = Bullet()
    score = Score()

    running = True
    while running:

        SCREEN.fill(BLACK_COLOR)

        player.draw_on_screen()
        player.move()

        score.draw_on_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.X_change = -player.default_player_X_change
                if event.key == pygame.K_RIGHT:
                    player.X_change = player.default_player_X_change
                if event.key == pygame.K_SPACE:
                    if bullet.state is "inactive":
                        random_X_addition = random.randint(-30, 10)
                        bullet.X = player.X + random_X_addition
                        bullet.draw_on_screen()
            if event.type == pygame.KEYUP:
                player.X_change = 0

        for enemy in enemies:
            enemy.draw_on_screen()
            enemy.move()

            if enemy.Y >= 450:
                if abs(player.X - enemy.X) < 10:
                    game_over()
                    break

            collision = bullet.is_collision(bullet.X, enemy.X, bullet.Y, enemy.Y)
            if collision:
                enemies.remove(enemy)
                del enemy
                score.value += 1
                bullet.Y = 600
                state = "inactive"
                new_enemy = Enemy()
                enemies.append(new_enemy)

        pygame.display.update()


if __name__ == '__main__':
     main()



