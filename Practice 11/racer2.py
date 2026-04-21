import pygame, sys
from pygame.locals import *
import random, time

# Initializing Pygame
pygame.init()

# Setting up FPS (Frames Per Second) to control game speed
FPS = 60
FramePerSec = pygame.time.Clock()

# Creating color tuples (R, G, B)
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5        # Initial falling speed of enemies and coins
SCORE = 0        # Tracks how many enemies have been dodged
COIN_SCORE = 0   # Tracks the total value of collected coins

# Task: Variable for Speed Increase Logic
N_COINS_THRESHOLD = 10      # Speed increases every 10 coin points
previous_speed_level = 0    # Tracks the current speed tier to prevent infinite acceleration

# Setting up Fonts for text display
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Create a white screen window
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Racer")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        # Create a red rectangle to represent the enemy
        self.image = pygame.Surface((40, 70))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        # Spawn the enemy at a random X coordinate at the very top of the screen
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        global SCORE
        # Move the enemy downwards by the current global SPEED
        self.rect.move_ip(0, SPEED)
        # If the enemy goes off the bottom of the screen
        if (self.rect.top > SCREEN_HEIGHT):
            SCORE += 1 # Increase dodge score
            # Reset enemy to the top at a new random X coordinate
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        # Create a blue rectangle to represent the player car
        self.image = pygame.Surface((40, 70))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        # Position the player near the bottom center of the screen
        self.rect.center = (160, 520)
       
    def move(self):
        # Fetch the current keys being pressed by the user
        pressed_keys = pygame.key.get_pressed()
        
        # Move left if the Left Arrow is pressed and the car is not touching the left border
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
                  
        # Move right if the Right Arrow is pressed and the car is not touching the right border
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Initialize the coin by calling the reset method
        self.reset()

    def move(self):
        # Move the coin downwards by the global SPEED
        self.rect.move_ip(0, SPEED)
        # If coin goes off screen, reset its position and weight
        if (self.rect.top > SCREEN_HEIGHT):
            self.reset()

    def reset(self):
        # Task: Randomly generating coins with different weights on the road
        self.weight = random.choice([1, 3, 5])
        self.image = pygame.Surface((20, 20))
        
        # Change the coin color based on its weight to give visual feedback to the player
        if self.weight == 1:
            self.image.fill(YELLOW)
        elif self.weight == 3:
            self.image.fill(ORANGE)
        else:
            self.image.fill(PURPLE)
            
        self.rect = self.image.get_rect()
        # Place the coin at the top of the screen at a random X coordinate
        self.rect.top = 0
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Setting up individual Sprites        
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Creating Sprite Groups for collision detection and rendering
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Game Loop
while True:
    # Cycles through all events occurring (like closing the window)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen every frame
    DISPLAYSURF.fill(WHITE)
    
    # Displaying Scores (Enemies Dodged)
    scores = font_small.render("Score: " + str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
    
    # Displaying the number/value of collected coins in the top right corner
    coin_text = font_small.render("Coins: " + str(COIN_SCORE), True, BLACK)
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 120, 10))

    # Moves and Re-draws all Sprites (Player, Enemy, Coin)
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Task: Detecting collision with coins
    # Using spritecollide to get a list of all coins currently touching the player
    collided_coins = pygame.sprite.spritecollide(P1, coins, False)
    for coin in collided_coins:
        # Add the specific weight of the coin to the score
        COIN_SCORE += coin.weight
        # Reposition the coin once collected
        coin.reset()

        # Task: Increase the speed of Enemy when the player earns N coins
        # Calculate current level based on total coin score
        current_speed_level = COIN_SCORE // N_COINS_THRESHOLD
        
        # If we have reached a new threshold tier, increase global speed
        if current_speed_level > previous_speed_level:
            SPEED += 1.0  # Increase speed
            previous_speed_level = current_speed_level # Update tracker so it only happens once per tier

    # Detecting collision between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
          # Play crash sound if a mixer is initialized
          if pygame.mixer.get_init():
              try:
                  pygame.mixer.Sound('crash.wav').play()
              except:
                  pass # Silently fail if crash.wav is missing
                  
          time.sleep(0.5)
                    
          # Show Game Over screen
          DISPLAYSURF.fill(RED)
          DISPLAYSURF.blit(game_over, (30,250))
          pygame.display.update()
          
          # Remove all sprites from the game
          for entity in all_sprites:
                entity.kill() 
                
          # Wait 2 seconds before closing the application
          time.sleep(2)
          pygame.quit()
          sys.exit()        
        
    # Refresh the display to show the updated frame
    pygame.display.update()
    
    # Tick the clock to ensure the game runs at exactly 60 FPS
    FramePerSec.tick(FPS)