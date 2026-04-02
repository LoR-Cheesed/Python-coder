import pygame
import math

class MovingEntity(pygame.sprite.Sprite):
    def __init__(self, start_edge, screen_width, screen_height):
        super().__init__()
        # Create a surface and get its rectangle
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0)) # Red color
        self.rect = self.image.get_rect()

        # Set initial position based on the specified edge
        if start_edge == 'top':
            self.rect.center = (screen_width // 2, 0)
        elif start_edge == 'left':
            self.rect.center = (0, screen_height // 2)
        # ... additional edge logic ...

        # Target position (center)
        self.target = (screen_width // 2, screen_height // 2)
        self.speed = 3
        self.moving = True

    def update(self):
        """Update the entity's position towards the center."""
        if self.moving:
            # Calculate direction vector
            dx = self.target[0] - self.rect.centerx
            dy = self.target[1] - self.rect.centery
            distance = math.sqrt(dx**2 + dy**2)

            if distance > self.speed:
                # Move towards the center
                self.rect.centerx += int(dx / distance * self.speed)
                self.rect.centery += int(dy / distance * self.speed)
            else:
                self.rect.center = self.target
                self.moving = False
