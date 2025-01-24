import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dark Humor Ping Pong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Ball properties
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, 20, 20)
ball_speed_x = 6 * random.choice((1, -1))
ball_speed_y = 6 * random.choice((1, -1))

# Paddle properties
paddle_width, paddle_height = 20, 100
player = pygame.Rect(20, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
ai = pygame.Rect(WIDTH - 40, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
player_speed = 0
ai_speed = 6

# Scores
player_score = 0
ai_score = 0

# Sarcastic comments to display
current_comment = ""
comment_timer = 0
ball_comment = ""
ball_comment_timer = 0
miss_comment = ""
miss_comment_timer = 0

# Player-specific comments
def get_player_comment():
    comments = [
        "Really? That's your best shot?",
        "My grandma could play better!",
        "Ouch, that hurt... not!",
        "Try harder, I dare you!",
        "Pathetic, just like Monday mornings.",
        "Missed it? Typical.",
        "Are you even trying?",
        "This is embarrassing for both of us.",
        "You hit it! I'm shocked!",
        "Keep this up, and you might win in 2075."
    ]
    return random.choice(comments)

# AI-specific comments
def get_ai_comment():
    comments = [
        "Was that supposed to scare me?",
        "Hah, too easy!",
        "Your skills are... amusing.",
        "Even a robot can do better than this!",
        "I'm not even trying, and I'm winning!",
        "You call that a hit?",
        "I eat balls like this for breakfast.",
        "Why don't you just give up?",
        "Next time, aim for the sky!",
        "Oops, did that hurt your pride?"
    ]
    return random.choice(comments)

# Miss-specific comments
def get_miss_comment(for_ai):
    if for_ai:
        comments = [
            "Missed it? Even I feel bad for you!",
            "Wow, that was tragic!",
            "Keep trying, maybe one day you'll learn!",
            "Did your sensors glitch, or are you just bad?",
            "That was embarrassing... for a machine!"
        ]
    else:
        comments = [
            "Haha, missed it again!",
            "You couldn't hit water if you fell out of a boat!",
            "Stick to something easier, like checkers!",
            "That was almost good... almost!",
            "Oops, better luck next time!"
        ]
    return random.choice(comments)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_speed = -6
            if event.key == pygame.K_DOWN:
                player_speed = 6
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                player_speed = 0

    # Move player
    player.y += player_speed
    player.y = max(0, min(HEIGHT - paddle_height, player.y))

    # Move AI paddle
    if ai.top < ball.y:
        ai.y += ai_speed
    if ai.bottom > ball.y:
        ai.y -= ai_speed
    ai.y = max(0, min(HEIGHT - paddle_height, ai.y))

    # Move ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with top and bottom
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Ball collision with paddles
    if ball.colliderect(player):
        ball_speed_x *= -1
        ball_comment = get_ai_comment()
        ball_comment_timer = pygame.time.get_ticks()
    if ball.colliderect(ai):
        ball_speed_x *= -1
        current_comment = get_player_comment()
        comment_timer = pygame.time.get_ticks()

    # Ball goes out of bounds
    if ball.left <= 0:
        ai_score += 1
        miss_comment = get_miss_comment(for_ai=False)
        miss_comment_timer = pygame.time.get_ticks()
        ball.x, ball.y = WIDTH // 2, HEIGHT // 2
        ball_speed_x *= random.choice((1, -1))
        ball_speed_y *= random.choice((1, -1))
    if ball.right >= WIDTH:
        player_score += 1
        miss_comment = get_miss_comment(for_ai=True)
        miss_comment_timer = pygame.time.get_ticks()
        ball.x, ball.y = WIDTH // 2, HEIGHT // 2
        ball_speed_x *= random.choice((1, -1))
        ball_speed_y *= random.choice((1, -1))

    # Drawing everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, player)
    pygame.draw.rect(screen, RED, ai)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # Scores
    player_text = font.render(f"Player: {player_score}", True, WHITE)
    ai_text = font.render(f"AI: {ai_score}", True, WHITE)
    screen.blit(player_text, (20, 20))
    screen.blit(ai_text, (WIDTH - 120, 20))

    # Display sarcastic comment for AI within its area when player hits
    if ball_comment and pygame.time.get_ticks() - ball_comment_timer < 2000:  # Show for 2 seconds
        ball_comment_text = small_font.render(ball_comment, True, WHITE)
        screen.blit(ball_comment_text, (ai.left - 150, ai.y + paddle_height // 2 - 10))

    # Display sarcastic comment for player within their area when AI hits
    if current_comment and pygame.time.get_ticks() - comment_timer < 2000:  # Show for 2 seconds
        comment_text = small_font.render(current_comment, True, WHITE)
        screen.blit(comment_text, (player.right + 10, player.y + paddle_height // 2 - 10))

    # Display sarcastic comment when either misses
    if miss_comment and pygame.time.get_ticks() - miss_comment_timer < 2000:  # Show for 2 seconds
        if ball.left <= 0:  # Player missed
            miss_comment_text = small_font.render(miss_comment, True, WHITE)
            screen.blit(miss_comment_text, (player.right + 10, player.y + paddle_height // 2 - 10))
        elif ball.right >= WIDTH:  # AI missed
            miss_comment_text = small_font.render(miss_comment, True, WHITE)
            screen.blit(miss_comment_text, (ai.left - 150, ai.y + paddle_height // 2 - 10))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
