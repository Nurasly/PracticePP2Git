import pygame
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pygame Paint Plus - Advanced Shapes")
    clock = pygame.time.Clock()
    
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    screen.fill(WHITE)
    
    # State variables
    drawing = False
    last_pos = None
    start_pos = None
    # Tools: brush, eraser, rect, circle, square, right_tri, eq_tri, rhombus
    current_tool = 'brush' 
    current_color = BLACK
    brush_size = 5

    canvas = screen.copy()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b: current_tool = 'brush'
                if event.key == pygame.K_e: current_tool = 'eraser'
                if event.key == pygame.K_r: current_tool = 'rect'
                if event.key == pygame.K_c: current_tool = 'circle'
                # --- NEW SHAPE TOOLS ---
                if event.key == pygame.K_s: current_tool = 'square'
                if event.key == pygame.K_t: current_tool = 'right_tri'
                if event.key == pygame.K_i: current_tool = 'eq_tri'
                if event.key == pygame.K_h: current_tool = 'rhombus'

                if event.key == pygame.K_1: current_color = BLACK
                if event.key == pygame.K_2: current_color = RED
                if event.key == pygame.K_3: current_color = GREEN
                if event.key == pygame.K_4: current_color = BLUE

            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                start_pos = event.pos
                last_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False
                canvas.blit(screen, (0, 0))

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    mouse_pos = event.pos
                    if current_tool == 'brush':
                        pygame.draw.line(canvas, current_color, last_pos, mouse_pos, brush_size)
                        last_pos = mouse_pos
                    elif current_tool == 'eraser':
                        pygame.draw.line(canvas, WHITE, last_pos, mouse_pos, 20)
                        last_pos = mouse_pos

        screen.blit(canvas, (0, 0)) 

        if drawing:
            mouse_pos = pygame.mouse.get_pos()
            dx = mouse_pos[0] - start_pos[0]
            dy = mouse_pos[1] - start_pos[1]

            if current_tool == 'rect':
                rect = pygame.Rect(start_pos, (dx, dy))
                rect.normalize()
                pygame.draw.rect(screen, current_color, rect, 2)
                
            elif current_tool == 'circle':
                radius = int((dx**2 + dy**2)**0.5)
                pygame.draw.circle(screen, current_color, start_pos, radius, 2)

            # --- 1. DRAW SQUARE ---
            elif current_tool == 'square':
                # To keep it a square, we use the larger of the two distances for side length
                side = max(abs(dx), abs(dy))
                s_x = start_pos[0] if dx > 0 else start_pos[0] - side
                s_y = start_pos[1] if dy > 0 else start_pos[1] - side
                pygame.draw.rect(screen, current_color, (s_x, s_y, side, side), 2)

            # --- 2. DRAW RIGHT TRIANGLE ---
            elif current_tool == 'right_tri':
                points = [start_pos, (start_pos[0], mouse_pos[1]), mouse_pos]
                pygame.draw.polygon(screen, current_color, points, 2)

            # --- 3. DRAW EQUILATERAL TRIANGLE ---
            elif current_tool == 'eq_tri':
                # height = sqrt(3)/2 * side
                side = dx 
                height = (math.sqrt(3) / 2) * side
                points = [
                    (start_pos[0], start_pos[1]), # Top vertex
                    (start_pos[0] - side/2, start_pos[1] + height), # Bottom Left
                    (start_pos[0] + side/2, start_pos[1] + height)  # Bottom Right
                ]
                pygame.draw.polygon(screen, current_color, points, 2)

            # --- 4. DRAW RHOMBUS ---
            elif current_tool == 'rhombus':
                # A diamond shape centered around the drag vector
                points = [
                    (start_pos[0], start_pos[1] + dy), # Top
                    (start_pos[0] + dx, start_pos[1]), # Right
                    (start_pos[0], start_pos[1] - dy), # Bottom
                    (start_pos[0] - dx, start_pos[1])  # Left
                ]
                pygame.draw.polygon(screen, current_color, points, 2)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()