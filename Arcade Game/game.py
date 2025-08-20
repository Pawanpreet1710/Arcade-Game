import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arcade Game")


# Vibrant Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 64, 64)
BLUE = (64, 128, 255)
GREEN = (64, 255, 128)
YELLOW = (255, 255, 64)
PURPLE = (192, 64, 255)
ORANGE = (255, 128, 0)
CYAN = (64, 255, 255)
PINK = (255, 64, 192)
GRAY = (220, 220, 220)

BG_GRADIENTS = [((255, 255, 200), (255, 200, 255)), ((200, 255, 255), (255, 220, 200)), ((220, 255, 200), (200, 220, 255))]
OBSTACLE_COLORS = [RED, ORANGE, YELLOW, PURPLE, CYAN, PINK, GREEN]
PLAYER_COLOR = BLUE
BUTTON_COLOR = GREEN
BUTTON_TEXT_COLOR = BLACK


font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 28)

class Button:
    def __init__(self, text, x, y, w, h, color=BUTTON_COLOR, text_color=BUTTON_TEXT_COLOR, font=small_font, is_back=False):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.text_color = text_color
        self.font = font
        self.is_back = is_back
    def draw(self, surface):
        if self.is_back:
            # Draw circular button
            center = (self.rect.x + self.rect.w//2, self.rect.y + self.rect.h//2)
            radius = self.rect.w//2
            pygame.draw.circle(surface, ORANGE, center, radius)
            pygame.draw.circle(surface, PURPLE, center, radius, 4)
            # Draw left arrow
            arrow_color = WHITE
            arrow_start = (center[0]+8, center[1])
            arrow_points = [
                (center[0]+8, center[1]),
                (center[0]-6, center[1]-10),
                (center[0]-6, center[1]+10)
            ]
            pygame.draw.polygon(surface, arrow_color, arrow_points)
        else:
            pygame.draw.rect(surface, self.color, self.rect, border_radius=12)
            pygame.draw.rect(surface, PURPLE, self.rect, 3, border_radius=12)
            draw_text(self.text, self.font, self.text_color, surface, self.rect.x+18, self.rect.y+10)
    def is_clicked(self, pos):
        if self.is_back:
            center = (self.rect.x + self.rect.w//2, self.rect.y + self.rect.h//2)
            radius = self.rect.w//2
            dx = pos[0] - center[0]
            dy = pos[1] - center[1]
            return dx*dx + dy*dy <= radius*radius
        return self.rect.collidepoint(pos)

def draw_text(text, font, color, surface, x, y):
    txt = font.render(text, True, color)
    surface.blit(txt, (x, y))

    pass

    pass

    pass

def user_exists(username):
    if not os.path.exists("users.txt"):
        return False
    with open("users.txt", "r") as f:
        for line in f:
            if line.strip().startswith(f"{username}:"):
                return True
    return False

def add_user(username, password):
    with open("users.txt", "a") as f:
        f.write(f"{username}:{password}\n")

def check_user(username, password):
    if not os.path.exists("users.txt"):
        return False
    with open("users.txt", "r") as f:
        for line in f:
            if line.strip() == f"{username}:{password}":
                return True
    return False

def select_difficulty():
    easy_btn = Button("Easy", WIDTH//2-80, 120, 160, 40)
    medium_btn = Button("Medium", WIDTH//2-80, 180, 160, 40)
    hard_btn = Button("Hard", WIDTH//2-80, 240, 160, 40)
    back_btn = Button("", 20, 20, 36, 36, is_back=True)
    bg1, bg2 = BG_GRADIENTS[0]
    while True:
        for y in range(HEIGHT):
            r = int(bg1[0] + (bg2[0] - bg1[0]) * y / HEIGHT)
            g = int(bg1[1] + (bg2[1] - bg1[1]) * y / HEIGHT)
            b = int(bg1[2] + (bg2[2] - bg1[2]) * y / HEIGHT)
            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))
        draw_text("Select Difficulty", font, PURPLE, screen, WIDTH//2-110, 40)
        easy_btn.draw(screen)
        medium_btn.draw(screen)
        hard_btn.draw(screen)
        back_btn.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_btn.is_clicked(event.pos):
                    return 'easy'
                elif medium_btn.is_clicked(event.pos):
                    return 'medium'
                elif hard_btn.is_clicked(event.pos):
                    return 'hard'
                elif back_btn.is_clicked(event.pos):
                    return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'easy'
                elif event.key == pygame.K_2:
                    return 'medium'
                elif event.key == pygame.K_3:
                    return 'hard'
        pygame.display.flip()

def home_page(username):
    start_btn = Button("Start Game", WIDTH//2-80, 180, 160, 40)
    quit_btn = Button("Quit", WIDTH//2-80, 240, 160, 40)
    active = True
    bg1, bg2 = BG_GRADIENTS[2]
    while active:
        for y in range(HEIGHT):
            r = int(bg1[0] + (bg2[0] - bg1[0]) * y / HEIGHT)
            g = int(bg1[1] + (bg2[1] - bg1[1]) * y / HEIGHT)
            b = int(bg1[2] + (bg2[2] - bg1[2]) * y / HEIGHT)
            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))
        draw_text(f"Welcome, {username}!", font, PURPLE, screen, WIDTH//2-100, 80)
        start_btn.draw(screen)
        quit_btn.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.is_clicked(event.pos):
                    difficulty = select_difficulty()
                    return difficulty
                elif quit_btn.is_clicked(event.pos):
                    pygame.quit()
                    exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    difficulty = select_difficulty()
                    return difficulty
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()
        pygame.display.flip()

def save_score(username, score, is_guest=False):
    if is_guest:
        return
    # Get difficulty from global or pass as argument
    global current_difficulty
    scores_file = "scores.txt"
    with open(scores_file, "a") as f:
        f.write(f"{username}:{current_difficulty}: {score}\n")

def show_game_over(username, score, is_guest=False):
    save_score(username, score, is_guest)
    global current_difficulty
    # Calculate high score for Player and current difficulty
    high_score = score
    if not is_guest and os.path.exists("scores.txt"):
        with open("scores.txt", "r") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
            # Only scores for this user and difficulty
            user_scores = [int(l.split(": ")[1]) for l in lines if l.startswith(f"{username}:{current_difficulty}:") and ": " in l]
            if user_scores:
                high_score = max(user_scores)
    restart_btn = Button("Restart", WIDTH//2-80, 200, 160, 40)
    quit_btn = Button("Quit", WIDTH//2-80, 260, 160, 40)
    back_btn = Button("", 20, 20, 36, 36, is_back=True)
    active = True
    bg1, bg2 = BG_GRADIENTS[1]
    while active:
        for y in range(HEIGHT):
            r = int(bg1[0] + (bg2[0] - bg1[0]) * y / HEIGHT)
            g = int(bg1[1] + (bg2[1] - bg1[1]) * y / HEIGHT)
            b = int(bg1[2] + (bg2[2] - bg1[2]) * y / HEIGHT)
            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))
        draw_text("Game Over!", font, RED, screen, WIDTH//2-80, 80)
        draw_text(f"Score: {score}", font, PURPLE, screen, WIDTH//2-60, 140)
        draw_text(f"High Score: {high_score}", font, ORANGE, screen, WIDTH//2-80, 180)
        restart_btn.draw(screen)
        quit_btn.draw(screen)
        back_btn.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_btn.is_clicked(event.pos):
                    active = False
                    return True
                elif quit_btn.is_clicked(event.pos):
                    pygame.quit()
                    exit()
                elif back_btn.is_clicked(event.pos):
                    return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    active = False
                    return True
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()
        pygame.display.flip()
    return False

def game_loop(username, difficulty):
    player_size = 50
    player_x = WIDTH // 2 - player_size // 2
    player_y = HEIGHT - player_size - 10
    player_speed = 5
    obstacle_size = 50
    # Difficulty settings
    if difficulty == 'easy':
        obstacle_speed = 4
        obstacle_count = 2
    elif difficulty == 'medium':
        obstacle_speed = 6
        obstacle_count = 3
    else:
        obstacle_speed = 8
        obstacle_count = 5
    obstacles = []
    for _ in range(obstacle_count):
        x = random.randint(0, WIDTH - obstacle_size)
        y = random.randint(-300, -obstacle_size)
        obstacles.append([x, y])
    score = 0
    clock = pygame.time.Clock()
    running = True
    bg1, bg2 = BG_GRADIENTS[random.randint(0,2)]
    while running:
        for y in range(HEIGHT):
            r = int(bg1[0] + (bg2[0] - bg1[0]) * y / HEIGHT)
            g = int(bg1[1] + (bg2[1] - bg1[1]) * y / HEIGHT)
            b = int(bg1[2] + (bg2[2] - bg1[2]) * y / HEIGHT)
            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
            player_x += player_speed
        # Move obstacles
        for i in range(obstacle_count):
            obstacles[i][1] += obstacle_speed
            if obstacles[i][1] > HEIGHT:
                obstacles[i][1] = random.randint(-300, -obstacle_size)
                obstacles[i][0] = random.randint(0, WIDTH - obstacle_size)
                score += 1
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        hit = False
        for idx, (ox, oy) in enumerate(obstacles):
            obstacle_rect = pygame.Rect(ox, oy, obstacle_size, obstacle_size)
            color = OBSTACLE_COLORS[idx % len(OBSTACLE_COLORS)]
            if player_rect.colliderect(obstacle_rect):
                hit = True
            pygame.draw.rect(screen, color, obstacle_rect, border_radius=8)
        if hit:
            running = False
        # Draw player as triangle
        triangle_points = [
            (player_x + player_size // 2, player_y),  # Top
            (player_x, player_y + player_size),        # Bottom left
            (player_x + player_size, player_y + player_size)  # Bottom right
        ]
        pygame.draw.polygon(screen, PLAYER_COLOR, triangle_points)
        score_text = font.render(f"Score: {score}", True, PURPLE)
        screen.blit(score_text, (10, 10))
        pygame.display.flip()
        clock.tick(60)
    return score

def main():
    username = "Player"
    global current_difficulty
    while True:
        difficulty = None
        while difficulty is None:
            difficulty = home_page(username)
        current_difficulty = difficulty
        score = game_loop(username, difficulty)
        restart = None
        while restart is None:
            restart = show_game_over(username, score, False)
            if restart is False:
                break
        if not restart:
            break
    pygame.quit()
    print(f"Game Over! Final Score: {score}")

if __name__ == "__main__":
    main()
