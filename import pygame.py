import pygame
import random
import sys


pygame.init()
balloons=[]


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


GREY= (128, 128, 128)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


BALLOON_RADIUS = 30
BALLOON_SPEED = 3
BALLOON_COLORS = [(255, 255, 0), (128, 128, 128), (0, 0, 255)]  


timer = 7200 
score = 0
miss_penalty = 1


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pop-The-Balloon")


def spawn_balloon():
    color = random.choice(BALLOON_COLORS)
    x = random.randint(BALLOON_RADIUS, SCREEN_WIDTH - BALLOON_RADIUS)
    y = SCREEN_HEIGHT + BALLOON_RADIUS
    return {'rect': pygame.Rect(x, y, BALLOON_RADIUS * 2, BALLOON_RADIUS * 2), 'color': color}


def decrease_timer():
    global timer
    timer -= 1

def check_balloon_popped(balloon, pos):
    return balloon['rect'].collidepoint(pos)


clock = pygame.time.Clock()
running = True
spawn_timer = 0

while running:
    screen.fill(GREY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for balloon in balloons:
                if check_balloon_popped(balloon, pos):
                    score += 2
                    balloons.remove(balloon)
                    break
            else:
                score -= miss_penalty

   
    spawn_timer += 1

    if spawn_timer % 60 == 0:
        balloons.append(spawn_balloon())

    for balloon in balloons:
        balloon['rect'].move_ip(0, -BALLOON_SPEED)

    balloons = [balloon for balloon in balloons if balloon['rect'].bottom > 0]

    for balloon in balloons:
        pygame.draw.circle(screen, balloon['color'], balloon['rect'].center, BALLOON_RADIUS)

    font = pygame.font.SysFont(None, 36)
    timer_text = font.render(f'Time: {timer // 60}:{timer % 60:0>2}', True, BLUE)
    score_text = font.render(f'Score: {score}', True, BLUE)
    screen.blit(timer_text, (10, 10))
    screen.blit(score_text, (10, 50))

    pygame.display.flip()

    decrease_timer()

    if timer <= 0:
        running = False

    clock.tick(60)

screen.fill(GREY)
game_over_text = font.render("Game Over!", True, YELLOW)
final_score_text = font.render(f"Final Score: {score}", True, BLUE)
screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
screen.blit(final_score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
pygame.display.flip()

pygame.time.delay(3000)  
pygame.quit()