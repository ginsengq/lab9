import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Paint")
    
    radius = 15
    x = 0
    y = 0
    mode = 'blue'
    points = []
    drawing = False
    
    running = True  # Variable to determine if the program should continue running
    
    while running:
        
        pressed = pygame.key.get_pressed()
        
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        
        # Clear points when changing drawing mode
        clear_points = False
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                running = False  # If the window is closed, end the loop
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    running = False  # If the user presses Ctrl + W, end the loop
                if event.key == pygame.K_F4 and alt_held:
                    running = False  # If the user presses Alt + F4, end the loop
                if event.key == pygame.K_ESCAPE:
                    running = False  # If the user presses ESC, end the loop
            
                # Determine the selected mode
                if event.key == pygame.K_r:
                    mode = 'red'
                    clear_points = True
                elif event.key == pygame.K_g:
                    mode = 'green'
                    clear_points = True
                elif event.key == pygame.K_b:
                    mode = 'blue'
                    clear_points = True
                elif event.key == pygame.K_c:
                    mode = 'circle'
                    clear_points = True
                elif event.key == pygame.K_e:
                    mode = 'eraser'
                    clear_points = True
                elif event.key == pygame.K_l:
                    mode = 'rectangle'
                    clear_points = True
                elif event.key == pygame.K_s:
                    mode = 'square' # Task: Draw square
                    clear_points = True
                elif event.key == pygame.K_t:
                    mode = 'right_triangle' # Task: Draw right triangle
                    clear_points = True
                elif event.key == pygame.K_u:
                    mode = 'equilateral_triangle' # Task: Draw equilateral triangle
                    clear_points = True
                elif event.key == pygame.K_h:
                    mode = 'rhombus' # Task: Draw rhombus
                    clear_points = True
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click grows radius 
                    drawing = True
                    x, y = event.pos
                elif event.button == 3: # Right click shrinks radius
                    radius = max(1, radius - 1)
                    
                # Change drawing mode on middle mouse button click
                elif event.button == 2:
                    mode = 'circle'  # Change the mode to circle
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
            
            elif event.type == pygame.MOUSEMOTION:
                # If mouse moved and drawing is enabled, add point to list 
                if drawing:
                    position = event.pos
                    points.append(position)
                    points = points[-256:]
        
        if clear_points:
            points.clear()  # Clear points when changing mode
                
        screen.fill((0, 0, 0))
        
        # Draw all points 
        i = 0
        while i < len(points) - 1:
            drawShapeBetween(screen, i, points[i], points[i + 1], radius, mode)
            i += 1
        
        pygame.display.flip()
        
        clock.tick(60)

def drawShapeBetween(screen, index, start, end, width, mode):
    c1 = max(0, min(255, 2 * index - 256))
    c2 = max(0, min(255, 2 * index))
    
    if mode == 'blue':
        color = (c1, c1, c2)
    elif mode == 'red':
        color = (c2, c1, c1)
    elif mode == 'green':
        color = (c1, c2, c1)
    elif mode in ['circle', 'rectangle', 'square', 'right_triangle', 'equilateral_triangle', 'rhombus']:
        color = (255, 255, 255)  # White for drawing shapes
    elif mode == 'eraser':
        color = (0, 0, 0)  # Black for erasing
    
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    
    if mode == 'circle':
        pygame.draw.circle(screen, color, (start[0], start[1]), width)
    elif mode == 'rectangle':
        pygame.draw.rect(screen, color, (start[0], start[1], end[0] - start[0], end[1] - start[1]))
    elif mode == 'square': # Task: Draw square
        side_length = max(abs(dx), abs(dy))
        pygame.draw.rect(screen, color, (start[0], start[1], side_length, side_length))
    elif mode == 'right_triangle': # Task: Draw right triangle
        pygame.draw.polygon(screen, color, [(start[0], start[1]), (end[0], start[1]), (start[0], end[1])])
    elif mode == 'equilateral_triangle': # Task: Draw equilateral triangle
        height = abs(dy)
        base_half = abs(dx) // 2
        pygame.draw.polygon(screen, color, [(start[0], end[1]), (end[0], end[1]), (start[0] + base_half, start[1])])
    elif mode == 'rhombus': # Task: Draw rhombus
        pygame.draw.polygon(screen, color, [(start[0], start[1] + abs(dy) // 2), (start[0] + abs(dx) // 2, end[1]), (end[0], start[1] + abs(dy) // 2), (start[0] + abs(dx) // 2, start[1])])
    else:
        for i in range(iterations):
            progress = 1.0 * i / iterations
            aprogress = 1 - progress
            x = int(aprogress * start[0] + progress * end[0])
            y = int(aprogress * start[1] + progress * end[1])
            pygame.draw.circle(screen, color, (x, y), width)

main()

'''
'r' - red
'g' - green
'b' - blue
'c' - circle
'l' - rectangle
'e' - eraser
's' - square 
't' - right triangle
'u' - equilateral triangle
'h' - rhombus
'ESC' - exit 
'''
