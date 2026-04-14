import pygame
import sys
from datetime import datetime
from clock import ClockHand

def main():
    # 1. Initialization
    pygame.init()
    WIDTH, HEIGHT = 600, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mickey's System Clock")
    clock = pygame.time.Clock()

    center = (WIDTH // 2, HEIGHT // 2)

    # 2. Load Hands
    # Using the same image but scaling them differently to distinguish right (minutes) and left (seconds)
    try:
        minute_hand = ClockHand(r"C:\Users\cooln\OneDrive\Рабочий стол\PracticePP2\Practice 9\mickeys_clock\images\hand_image.jpg", center, scale_size=(150, 300))
        second_hand = ClockHand(r"C:\Users\cooln\OneDrive\Рабочий стол\PracticePP2\Practice 9\mickeys_clock\images\hand_image.jpg", center, scale_size=(100, 250))
    except FileNotFoundError:
        print("Error: Could not find 'images/hand_image.jpg'. Please ensure the image is in the correct folder.")
        sys.exit()

    # 3. Main Loop
    running = True
    while running:
        # Handle events (like closing the window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fetch real-time system clock
        current_time = datetime.now()
        
        # Update hands based on current minutes and seconds
        minute_hand.update(current_time.minute)
        second_hand.update(current_time.second)

        # 4. Rendering
        screen.fill((255, 255, 255)) # White background
        
        # Draw a simple clock face outline and center pin
        pygame.draw.circle(screen, (200, 200, 200), center, 280, 5) 
        
        # Draw the hands (Minutes first so seconds draw on top)
        minute_hand.draw(screen)
        second_hand.draw(screen)
        
        # Draw the center pin on top of the hands
        pygame.draw.circle(screen, (0, 0, 0), center, 12)

        # Update the display
        pygame.display.flip()
        
        # Limit the frame rate (60 FPS is standard and easily handles a 1-second update interval)
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()