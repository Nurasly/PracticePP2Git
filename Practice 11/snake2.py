import pygame
import random
import time

# Initialize Pygame
pygame.init()

# --- Configuration & Constants ---
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 255) # Added color for the weighted/timed Special Food

WIDTH = 600
HEIGHT = 400
BLOCK_SIZE = 20  # Size of snake segment and food

# Initialize Display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Level Up Edition')
clock = pygame.time.Clock()

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def display_score(score, level):
    """Displays current score and level on the screen."""
    value = score_font.render(f"Score: {score}  Level: {level}", True, YELLOW)
    screen.blit(value, [10, 10])

def draw_snake(block_size, snake_list):
    """Draws each segment of the snake."""
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], block_size, block_size])

# Updated to accept an optional 'other_food' parameter so foods don't spawn on top of each other
def generate_food(snake_list, other_food=None):
    """Generates random food position that doesn't collide with the snake body or other food."""
    while True:
        food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        
        # Ensure food is not spawning inside the snake body or exactly where the other food is
        if [food_x, food_y] not in snake_list and [food_x, food_y] != other_food:
            return food_x, food_y

def game_loop():
    game_over = False
    game_close = False

    # Snake Initial Position
    x1, y1 = WIDTH / 2, HEIGHT / 2
    x1_change, y1_change = 0, 0

    snake_list = []
    length_of_snake = 1

    # Initial Stats
    score = 0
    level = 1
    speed = 10 
    
    # Standard Food variables
    food_x, food_y = generate_food(snake_list)
    
    # --- NEW: Special Food Variables ---
    special_food_active = False
    special_food_x, special_food_y = -1, -1
    special_food_timer = 0
    SPECIAL_FOOD_DURATION = 5000  # Disappears after 5000 milliseconds (5 seconds)
    SPECIAL_FOOD_WEIGHT = 3       # Gives 3 points and length instead of 1

    while not game_over:

        while game_close:
            screen.fill(BLACK)
            msg = font_style.render("Game Over! Press C-Play Again or Q-Quit", True, RED)
            screen.blit(msg, [WIDTH / 6, HEIGHT / 3])
            display_score(score, level)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = BLOCK_SIZE
                    x1_change = 0

        # --- 1. Border Collision Detection ---
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(BLACK)
        
        # --- NEW: Special Food Timer Logic ---
        # Check if special food is active and if its timer has run out
        if special_food_active:
            current_time = pygame.time.get_ticks()
            if current_time - special_food_timer > SPECIAL_FOOD_DURATION:
                special_food_active = False  # Timer expired, food disappears
            else:
                # Draw Special Food (Blue) if still active
                pygame.draw.rect(screen, BLUE, [special_food_x, special_food_y, BLOCK_SIZE, BLOCK_SIZE])

        # Draw Standard Food (Red)
        pygame.draw.rect(screen, RED, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])
        
        # Snake Movement Logic
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # --- 2. Self Collision Detection ---
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        draw_snake(BLOCK_SIZE, snake_list)
        display_score(score, level)

        pygame.display.update()

        # --- 3. Eating Standard Food ---
        if x1 == food_x and y1 == food_y:
            # Generate new standard food, making sure it doesn't spawn on top of special food
            other_pos = [special_food_x, special_food_y] if special_food_active else None
            food_x, food_y = generate_food(snake_list, other_pos)
            
            length_of_snake += 1
            score += 1
            
            # 20% chance to spawn a special food when a standard one is eaten
            if not special_food_active and random.randint(1, 5) == 1:
                special_food_active = True
                special_food_x, special_food_y = generate_food(snake_list, [food_x, food_y])
                special_food_timer = pygame.time.get_ticks() # Start the countdown timer

        # --- NEW: Eating Special Food (Weight & Disappear) ---
        if special_food_active and x1 == special_food_x and y1 == special_food_y:
            special_food_active = False # Deactivate it immediately upon eating
            length_of_snake += SPECIAL_FOOD_WEIGHT
            score += SPECIAL_FOOD_WEIGHT

        # --- NEW: Updated Leveling Up Logic ---
        # Because special food jumps the score by 3, we calculate the expected level mathematically
        # rather than using modulo (score % 3), which might get skipped.
        expected_level = (score // 3) + 1
        if expected_level > level:
            # Increase speed for every level gained
            speed += 2 * (expected_level - level)
            level = expected_level
            print(f"Level Up! Current Speed: {speed}")

        clock.tick(speed)

    pygame.quit()
    quit()

game_loop()