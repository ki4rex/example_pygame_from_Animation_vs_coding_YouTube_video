import pygame
import math

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()


square_pos = pygame.Rect(1920, 920, 50, 50)
circle_pos = pygame.Vector2(1500, 500)
circle_spd = pygame.Vector2()
circle_rad = 20
circle_acc = 0.1  # Adjusted for better movement behavior
circle_spd_mul = 0.99
bounce_str = 1.5

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Square movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        square_pos.y -= 20
    if keys[pygame.K_DOWN]:
        square_pos.y += 20
    if keys[pygame.K_LEFT]:
        square_pos.x -= 20
    if keys[pygame.K_RIGHT]:
        square_pos.x += 20

    # Track the red square (instead of mouse position)
    direction = pygame.Vector2(square_pos.centerx - circle_pos.x, square_pos.centery - circle_pos.y)
    distance = direction.length()

    if distance != 0:  # Avoid division by zero
        direction.normalize_ip()  # Normalize to get a unit vector
        circle_spd += direction * circle_acc  # Apply acceleration towards the square

    circle_spd *= circle_spd_mul  # Dampen the speed

    # Collision detection between circle and square
    if circle_pos.x - circle_rad < square_pos.right and circle_pos.x + circle_rad > square_pos.left and \
            circle_pos.y - circle_rad < square_pos.bottom and circle_pos.y + circle_rad > square_pos.top:
        # Circle is colliding with the square, so bounce it
        normal = pygame.Vector2(circle_pos.x - square_pos.centerx, circle_pos.y - square_pos.centery)
        normal_length = normal.length()
        if normal_length != 0:
            normal.normalize_ip()
        circle_spd.reflect_ip(normal)  # Reflect the speed based on the collision normal
        circle_pos = pygame.Vector2(square_pos.centerx + normal.x * (circle_rad + 1),
                                    square_pos.centery + normal.y * (circle_rad + 1))  # Push circle away from square

    # Circle bounds checking
    if circle_pos[0] < 0:
        circle_pos.update(circle_rad, circle_pos[1])
        circle_spd.update(-circle_spd[0] * bounce_str, circle_spd[1])
    elif circle_pos[0] > screen.get_width() - circle_rad:
        circle_pos.update(screen.get_width() - circle_rad, circle_pos[1])
        circle_spd.update(-circle_spd[0] * bounce_str, circle_spd[1])
    elif circle_pos[1] < circle_rad:
        circle_pos.update(circle_pos[0], circle_rad)
        circle_spd.update(circle_spd[0], -circle_spd[1] * bounce_str)
    elif circle_pos[1] > screen.get_height() - circle_rad:
        circle_pos.update(circle_pos[0], screen.get_height() - circle_rad)
        circle_spd.update(circle_spd[0], -circle_spd[1] * bounce_str)

    circle_pos += circle_spd  # Update circle position

    # Drawing
    screen.fill("black")
    pygame.draw.circle(screen, "blue", circle_pos, circle_rad)
    pygame.draw.rect(screen, "red", square_pos)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
