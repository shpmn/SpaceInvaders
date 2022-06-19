# Simple version of Space Invaders
# Authors: Lech Horosiewicz-Wróbel, Adam Byczynski
# Date: 18.06.2022

# TODO: SCORE POD GAMEOVER
# TODO: dodac predkosc przeciwnikow sie zwieksza wraz z punktami
# TODO: prędkosc X
# TODO: menu główne

import pygame
import random

pygame.init()
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
screen_width, screen_height = 800, 600
SCREEN = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Colony Defender")
LEFT_SCREEN_BORDER = 0
RIGHT_SCREEN_BORDER = 735


class InitialSetup:
    background_image = pygame.image.load("data/background.png").convert_alpha()

    @staticmethod
    def show_background():
        SCREEN.blit(InitialSetup.background_image, (0, 0))


class Enemy:
    alien_images = ['data/alien_1.png', 'data/alien_2.png', 'data/alien_3.png',
                    'data/alien_4.png', 'data/alien_5.png', 'data/alien_6.png']

    base_x_accelaration = 0.1

    def __init__(self):
        self.x = random.randint(64, 737)
        self.y = random.randint(20, 80)
        self.x_change = random.uniform(0.1, 0.4)
        self.y_change = random.randint(30, 60)
        self.invader_image = pygame.image.load(random.choice(self.alien_images))
        self.x_hitbox = (self.x, self.x + 64)
        self.y_hitbox = (self.y, self.y + 64)

    def play(self):
        self.draw_on_screen()
        self.move()
        self.update_hitbox()

    def update_hitbox(self):
        self.x_hitbox = (self.x, self.x + 64)
        self.y_hitbox = (self.y, self.y + 64)

    def draw_on_screen(self):
        SCREEN.blit(self.invader_image, (self.x, self.y))

    def move(self):
        self.x += self.x_change
        if self.x >= RIGHT_SCREEN_BORDER or self.x <= LEFT_SCREEN_BORDER:
            self.x_change *= -1
            self.y += self.y_change
            # self.x_change += self.x_accelaration

    def win_by_touch(self, player_x):
        if self.y >= 450:
            if abs(player_x - self.x) < 10:
                return True


class Player:
    player_starting_position_x = 370
    player_starting_position_y = 523

    left_screen_border = 16
    right_screen_border = 750

    def __init__(self):
        self.player_image = pygame.image.load('data/character.png')
        self.x = self.player_starting_position_x
        self.y = self.player_starting_position_y
        self.x_change = 0
        self.default_player_x_change = 0.4
        self.alive = True

    def play(self):
        self.draw_on_screen()
        self.move()

    def draw_on_screen(self):
        SCREEN.blit(self.player_image, (self.x - 16, self.y + 10))

    def move(self):

        self.x += self.x_change
        if self.x <= self.left_screen_border:
            self.x = self.left_screen_border
        elif self.x >= self.right_screen_border:
            self.x = self.right_screen_border


class Bullet:
    def __init__(self, player_x, player_y):
        self.bullet_image = pygame.image.load('data/bullet.png')
        gun_position_adjustment = 10
        self.x = player_x + gun_position_adjustment
        self.y = player_y
        self.x_change = 0
        self.y_change = 1.7
        self.state = "inactive"

    def play(self):
        self.draw_on_screen()
        self.move()

    def draw_on_screen(self):
        SCREEN.blit(self.bullet_image, (self.x, self.y))
        self.state = "fire"

    def move(self):
        if self.y <= 0:
            self.y = 560
        if self.state is "fire":
            self.draw_on_screen()
            self.y -= self.y_change

    def is_out_of_bounds(self):
        if self.y < 0 or self.y > 600:
            return True
        else:
            return False


class Score:
    gap_for_new_enemy = 5
    gap_for_enemy_acceleration = 10

    def __init__(self):
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.value = 0
        self.x, self.y = 5, 5

    def draw_on_screen(self):
        score = self.font.render("Points: " + str(self.value), True, WHITE_COLOR)
        SCREEN.blit(score, (self.x, self.y))


class Utilities:
    game_over_font = pygame.font.Font('freesansbold.ttf', 64)

    @staticmethod
    def is_collision(bullet_x, bullet_y, enemy_hitbox_x, enemy_hitbox_y):
        if enemy_hitbox_x[0] <= bullet_x <= enemy_hitbox_x[1] and enemy_hitbox_y[0] <= bullet_y <= enemy_hitbox_y[1]:
            return True
        else:
            return False

    @staticmethod
    def game_over():
        game_over_text = Utilities.game_over_font.render("GAME OVER", True, WHITE_COLOR)
        SCREEN.blit(game_over_text, (190, 250))


def main():
    player = Player()

    starting_enemies = 5
    enemies = [Enemy() for _ in range(starting_enemies)]

    bullets = []
    score = Score()

    def adjust_number_of_enemies():
        new_enemies = score.value // score.gap_for_new_enemy
        total_enemies = starting_enemies + new_enemies
        if len(enemies) != total_enemies:
            for _ in range(total_enemies - len(enemies)):
                enemies.append(Enemy())

    # def adjust_enemies_velocity(_enemy):
    #     acceleration_factor = score.value // score.gap_for_enemy_acceleration
    #     velocity_adjustment = acceleration_factor * _enemy.base_x_accelaration
    #     new_velocity = _enemy.x_change + velocity_adjustment
    #     print(velocity_adjustment)
    #     if _enemy.x_change != new_velocity:
    #         _enemy.x_change += velocity_adjustment

    # game running loop
    running = True
    while running:
        InitialSetup.show_background()
        score.draw_on_screen()

        if player.alive:
            player.play()
        else:
            enemies.clear()
            Utilities.game_over()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.x_change = -player.default_player_x_change
                if event.key == pygame.K_RIGHT:
                    player.x_change = player.default_player_x_change
                if event.key == pygame.K_SPACE:
                    if not bullets:
                        new_bullet = Bullet(player.x, player.y)
                        bullets.append(new_bullet)
            if event.type == pygame.KEYUP:
                player.x_change = 0

        for bullet in bullets:
            bullet.play()
            if bullet.is_out_of_bounds():
                bullets.remove(bullet)

        adjust_number_of_enemies()

        for enemy in enemies:
            # adjust_enemies_velocity(enemy)
            enemy.play()
            if enemy.win_by_touch(player.x):
                player.alive = False
                break

            for bullet in bullets:
                is_collision = Utilities.is_collision(bullet.x, bullet.y, enemy.x_hitbox, enemy.y_hitbox)
                if is_collision:
                    enemies.remove(enemy)
                    score.value += 1
                    bullets.remove(bullet)
                    new_enemy = Enemy()
                    enemies.append(new_enemy)


        pygame.display.update()


if __name__ == '__main__':
     main()



