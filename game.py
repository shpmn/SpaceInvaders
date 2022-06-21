# Simple version of Space Invaders
# Authors: Lech Horosiewicz-Wróbel, Adam Byczynski
# Date: 18.06.2022

# TODO: SCORE POD GAMEOVER

import pygame
import random

pygame.init()
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
screen_width, screen_height = 800, 600
SCREEN = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Colony Defender")
TOP_SCREEN_BORDER = 0
LEFT_SCREEN_BORDER = 0
RIGHT_SCREEN_BORDER = 736


class MainScreen:
    starting_image = pygame.image.load("data/starting_menu.png")
    press_to_start_font = pygame.font.Font('freesansbold.ttf', 32)

    @staticmethod
    def show_mainscreen():
        SCREEN.blit(MainScreen.starting_image, (0, 0))

    @staticmethod
    def draw_press_to_start():
        press_to_start_text = MainScreen.press_to_start_font.render("Press SPACE to start", True, WHITE_COLOR)
        SCREEN.blit(press_to_start_text, (235, 500))


class Background:
    background_image = pygame.image.load("data/background.png").convert_alpha()

    @staticmethod
    def show_background():
        SCREEN.blit(Background.background_image, (0, 0))


class Enemy:
    alien_images = ['data/alien_1.png', 'data/alien_2.png', 'data/alien_3.png',
                    'data/alien_4.png', 'data/alien_5.png', 'data/alien_6.png']
    enemies = []
    x_base_acceleration = 0.05
    score_progression_factor = 0

    x_base_velocity = random.choice((random.uniform(-0.25, -0.1), random.uniform(0.1, 0.25)))
    y_base_velocity = random.randint(30, 60)

    def __init__(self):
        Enemy.enemies.append(self)
        self.x = random.randint(LEFT_SCREEN_BORDER, RIGHT_SCREEN_BORDER)
        self.y = random.randint(TOP_SCREEN_BORDER, TOP_SCREEN_BORDER + 64)
        self.x_velocity = 0
        self.y_velocity = self.y_base_velocity
        self.calculate_x_velocity()
        self.invader_image = pygame.image.load(random.choice(self.alien_images))
        self.x_hitbox = (self.x, self.x + 64)
        self.y_hitbox = (self.y, self.y + 64)

    def play(self):
        self.draw_on_screen()
        self.move()

    def calculate_x_velocity(self):
        if self.x_velocity >= 0:
            self.x_velocity += self.x_base_velocity + Enemy.x_base_acceleration * Enemy.score_progression_factor
        else:
            self.x_velocity -= self.x_base_velocity + Enemy.x_base_acceleration * Enemy.score_progression_factor

    def update_hitbox(self):
        self.x_hitbox = (self.x, self.x + 64)
        self.y_hitbox = (self.y, self.y + 64)

    def draw_on_screen(self):
        SCREEN.blit(self.invader_image, (self.x, self.y))

    def move(self):
        self.x += self.x_velocity
        if self.x >= RIGHT_SCREEN_BORDER or self.x <= LEFT_SCREEN_BORDER:
            self.x_velocity *= -1
            self.y += self.y_velocity
        self.update_hitbox()

    def accelerate(self):
        if self.x_velocity >= 0:
            self.x_velocity += self.x_base_acceleration
        else:
            self.x_velocity -= self.x_base_acceleration

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
        self.x_velocity = 0
        self.default_player_x_change = 0.4
        self.alive = True

    def play(self):
        self.draw_on_screen()
        self.move()

    def draw_on_screen(self):
        SCREEN.blit(self.player_image, (self.x - 16, self.y + 10))

    def move(self):
        self.x += self.x_velocity
        if self.x <= self.left_screen_border:
            self.x = self.left_screen_border
        elif self.x >= self.right_screen_border:
            self.x = self.right_screen_border


class Bullet:
    def __init__(self, player_x, player_y):
        self.bullet_image = pygame.image.load('data/bullet.png')
        gun_position_adjustment_x = 10
        gun_position_adjustment_y = -20
        self.x = player_x + gun_position_adjustment_x
        self.y = player_y + gun_position_adjustment_y
        self.x_velocity = 0
        self.y_velocity = 1.7
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
        if self.state == "fire":
            self.draw_on_screen()
            self.y -= self.y_velocity

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
        self.score_factor = 0

    def draw_on_screen(self):
        score = self.font.render("Points: " + str(self.value), True, WHITE_COLOR)
        SCREEN.blit(score, (self.x, self.y))

    def apply_progression_factor(self):
        new_score_factor = self.value // self.gap_for_enemy_acceleration
        if self.score_factor != new_score_factor:
            self.score_factor = new_score_factor
            return True
        else:
            return False

    def calculate_progression_factor(self):
        return self.value // self.gap_for_enemy_acceleration


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

    @staticmethod
    def quit_game():
        quit()


def main_screen():
    running = True
    while running:
        MainScreen.show_mainscreen()
        MainScreen.draw_press_to_start()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Utilities.quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Utilities.quit_game()
                if event.key == pygame.K_SPACE:
                    running = False


def game():
    player = Player()
    starting_enemies = 3
    enemies = [Enemy() for _ in range(starting_enemies)]
    bullets = []
    score = Score()

    def adjust_number_of_enemies():
        progression_factor = score.calculate_progression_factor()
        total_enemies = starting_enemies + progression_factor
        if len(enemies) != total_enemies:
            for _ in range(total_enemies - len(enemies)):
                enemies.append(Enemy())

    running = True
    while running:
        Background.show_background()
        score.draw_on_screen()
        Enemy.score_progression_factor = score.calculate_progression_factor()

        if player.alive:
            player.play()
        else:
            enemies.clear()
            Utilities.game_over()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Utilities.quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_LEFT:
                    player.x_velocity = -player.default_player_x_change
                if event.key == pygame.K_RIGHT:
                    player.x_velocity = player.default_player_x_change
                if event.key == pygame.K_SPACE:
                    if not bullets:
                        new_bullet = Bullet(player.x, player.y)
                        bullets.append(new_bullet)
            if event.type == pygame.KEYUP:
                player.x_velocity = 0

        for bullet in bullets:
            bullet.play()
            if bullet.is_out_of_bounds():
                bullets.remove(bullet)

        adjust_number_of_enemies()

        for enemy in enemies:
            enemy.play()
            if score.apply_progression_factor():
                for e in enemies:
                    e.accelerate()
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


def main():
    while True:
        main_screen()
        game()


if __name__ == '__main__':
     main()