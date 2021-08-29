import pygame
import random

pygame.font.init()

WIDTH = 1300
HEIGHT = 650
FPS = 75
last_tick = 0

GREEN = (125, 255, 10)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

font = pygame.font.SysFont("comicsans", 50)
font_over = pygame.font.SysFont("comicsans", 100)

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

genrate_evt = pygame.USEREVENT + 1
genrate = pygame.event.Event(genrate_evt)

bird_image = pygame.transform.scale(pygame.image.load("bird_folder/bird.png"), (80, 40))
background = pygame.transform.scale(pygame.image.load("bird_folder/bird_background.png"), (WIDTH, HEIGHT))


def obsticals():
    upper_rect = pygame.Rect(WIDTH, 0, 100, random.randint(150, 350))
    upper_square = pygame.Rect(upper_rect.x - 6, (upper_rect.y + upper_rect.height) + 1, upper_rect.width + 12, 22)
    distance = random.randint(200, 250)
    lower_square = pygame.Rect(upper_square.x, upper_square.y + distance, upper_square.width, 22)
    lower_rect = pygame.Rect(upper_rect.x, lower_square.y + lower_square.height + 1, upper_rect.width,
                             HEIGHT - lower_square.y - lower_square.height)
    return [upper_rect, upper_square, lower_rect, lower_square]


def draw(ob_list, bird, score):
    WINDOW.fill(BLACK)
    WINDOW.blit(background, (0, 0))
    WINDOW.blit(bird_image, (bird.x, bird.y))
    for item in ob_list:
        for ob in item:
            pygame.draw.rect(WINDOW, GREEN, ob)
    text = font.render("score: " + str(score), True, RED)
    WINDOW.blit(text, (WIDTH // 2 - text.get_width() // 2, 10))
    pygame.display.update()


def clock_count(now):
    global last_tick
    if now - last_tick >= 900:
        last_tick = now
        pygame.event.post(genrate)


def move(ob_list, score, bird):
    for item in ob_list:
        for ob in item:
            ob.x -= 5
        if (item[1].x + item[1].width) - 1 == bird.x:
            score += 1
        if item[1].x + item[1].width <= 0:
            ob_list.remove(item)
    return score


def drop(bird):
    bird.y += 2


def game_over():
    over = font_over.render("Game Over", True, RED)
    WINDOW.blit(over, (WIDTH // 2 - over.get_width() // 2, HEIGHT // 2))
    pygame.display.update()
    pygame.time.delay(5000)
    main()


def collide(bird, ob_list):
    for item in ob_list:
        for ob in item:
            if bird.colliderect(ob):
                game_over()
    if bird.y >= HEIGHT or bird.y <= 0:
        game_over()


def main():
    run = True
    obs_list = []
    bird_rect = pygame.Rect(300, 250, bird_image.get_width(), bird_image.get_height())
    score = 0
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == genrate_evt:
                obs_list.append(obsticals())
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    bird_rect.y -= 60
        score = move(obs_list, score, bird_rect)
        draw(obs_list, bird_rect, score)
        drop(bird_rect)
        collide(bird_rect, obs_list)
        clock_count(pygame.time.get_ticks())
    pygame.quit()


if __name__ == '__main__':
    main()
