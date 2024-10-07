import pygame
import sys

# Initialize pygame
pygame.init()

# Define screen size
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bouncing Ball Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Define fonts
font = pygame.font.SysFont('Arial', 30)

# Game variables
ball_radius = 20
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_speed_x = 3  # Horizontal speed
ball_speed_y = 5  # Vertical speed
ball_speed_increase = 0.5
player_name = ""
score = 0

# Paddle (Board)
paddle_width = 100
paddle_height = 20
paddle_x = (SCREEN_WIDTH // 2) - (paddle_width // 2)
paddle_y = SCREEN_HEIGHT - 30
paddle_speed = 10  # Increased paddle speed for better responsiveness

# Game states
START, PLAYING, GAME_OVER = "start", "playing", "game_over"
game_state = START

# Function to display text
def display_text(text, size, color, x, y):
    font = pygame.font.SysFont('Arial', size)
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

# Start screen
def start_screen():
    screen.fill(WHITE)
    display_text("Enter Your Name:", 40, BLACK, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4)
    display_text(player_name, 40, BLACK, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3)
    display_text("Press Enter to Start", 30, BLACK, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)

# Game over screen
def game_over_screen():
    screen.fill(WHITE)
    display_text(f"Game Over, {player_name}", 40, RED, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4)
    display_text(f"Score: {score}", 40, BLACK, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3)
    display_text("Press R to Restart", 30, BLACK, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)

# Reset game state for restarting
def reset_game():
    global ball_x, ball_y, ball_speed_x, ball_speed_y, score, paddle_x, game_state
    ball_x, ball_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    ball_speed_x, ball_speed_y = 3, 5  # Reset ball speed
    score = 0
    paddle_x = (SCREEN_WIDTH // 2) - (paddle_width // 2)  # Reset paddle position
    game_state = PLAYING  # Change game state back to playing

# Main game loop
def game_loop():
    global ball_x, ball_y, ball_speed_x, ball_speed_y, score, paddle_x, game_state, player_name

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if game_state == START:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and player_name != "":
                        reset_game()  # Reset the game when starting for the first time
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode

            elif game_state == GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        reset_game()  # Reset the game when restarting

        if game_state == START:
            start_screen()

        elif game_state == PLAYING:
            # Paddle movement using continuous key press (left and right)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                paddle_x -= paddle_speed
            if keys[pygame.K_RIGHT]:
                paddle_x += paddle_speed

            # Ensure paddle stays within screen bounds
            paddle_x = max(0, min(paddle_x, SCREEN_WIDTH - paddle_width))

            # Ball movement
            ball_x += ball_speed_x
            ball_y += ball_speed_y

            # Ball collision with paddle (bounce back)
            if paddle_y <= ball_y + ball_radius <= paddle_y + paddle_height and \
                    paddle_x <= ball_x <= paddle_x + paddle_width:
                ball_speed_y = -(ball_speed_y + ball_speed_increase)
                score += 1

            # Ball collision with the left and right walls (bounce back)
            if ball_x - ball_radius <= 0 or ball_x + ball_radius >= SCREEN_WIDTH:
                ball_speed_x = -ball_speed_x  # Reverse horizontal direction

            # Ball collision with the top wall (bounce back)
            if ball_y - ball_radius <= 0:
                ball_speed_y = -ball_speed_y  # Reverse vertical direction

            # Check if ball hits the bottom (game over condition)
            if ball_y + ball_radius > SCREEN_HEIGHT:
                game_state = GAME_OVER

            # Draw ball and paddle
            pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)
            pygame.draw.rect(screen, GREEN, (paddle_x, paddle_y, paddle_width, paddle_height))

            # Display score
            display_text(f"Score: {score}", 30, BLACK, 10, 10)

        elif game_state == GAME_OVER:
            game_over_screen()

        pygame.display.update()
        pygame.time.Clock().tick(60)

# Run the game
game_loop()
