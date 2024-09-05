import pygame
import numpy as np
pygame.init()

WIDTH, HEIGHT = 1000, 1000
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

G = 6.6743e-11 # Gravitational Const
TIMESTEP = 3600 * 24 # seconds per day

class Sun:
    def __init__(self, x, y, radius, mass, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

class Satellite:
    def __init__(self, x, y, radius, mass, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []

        self.v_x = 0
        self.v_y = 0

        self.a_x = self.a_y = 0

    def update_coors(self, sun):
        # calculate force of gravity based on Sun
        r_squared = (self.x - sun.x) ** 2 + (self.y - sun.y) ** 2 # calculate r^2
        self.distance_from_sun = np.sqrt(r_squared)
        force = -G * (sun.mass * self.mass) / r_squared # calculate gravitational force  

        theta = np.arctan2(self.y - HEIGHT // 2, self.x - WIDTH // 2) # calculate theta

        force_x = force * np.cos(theta) # calculate x comp. of force vector
        force_y = force * np.sin(theta) # calculate y comp. of force vector

        a_x = force_x / self.mass # calculate x comp. of acceleration vector
        a_y = force_y / self.mass # calculate y comp. of acceleration vector

        self.a_x = a_x
        self.a_y = a_y

        self.v_x = self.v_x + a_x * TIMESTEP # update x comp. of velocity vector
        self.v_y = self.v_y + a_y * TIMESTEP # update y comp. of velocity vector

        self.orbit.append((self.x, self.y))
        self.x = self.x + self.v_x * TIMESTEP # update x coor. of position
        self.y = self.y + self.v_y * TIMESTEP # update y coor. of position

    def draw(self, window):
        # draw orbit
        if len(self.orbit) >= 2: 
            scaled_points = []
            for point_x, point_y in self.orbit:
                scaled_points.append((point_x, point_y))

            pygame.draw.lines(window, self.color, False, scaled_points, 2)

        # draw satellite
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

        # show acceleration vector
        a_x = self.a_x * 5e12 + self.x
        a_y = self.a_y * 5e12 + self.y
        pygame.draw.polygon(window, RED, [(self.x, self.y), (a_x, self.y)], width=2) # a_x vector
        pygame.draw.polygon(window, BLUE, [(self.x, self.y), (self.x, a_y)], width=2) # a_y vector
        pygame.draw.polygon(window, WHITE, [(self.x, self.y), (a_x, a_y)], width=2) # acceleration vector

        # show velocity vector
        # v_x = self.v_x * 1e6 + self.x
        # v_y = self.v_y * 1e6 + self.y
        # pygame.draw.polygon(window, RED, [(self.x, self.y), (v_x, self.y)], width=2) # v_x vector
        # pygame.draw.polygon(window, BLUE, [(self.x, self.y), (self.x, v_y)], width=2) # v_y vector
        # pygame.draw.polygon(window, WHITE, [(self.x, self.y), (v_x, v_y)], width=2) # tangent velocity vector

def main():
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Satellite Simulation")

    running = True
    clock = pygame.time.Clock()

    sun = Sun(WIDTH // 2, HEIGHT // 2, 50, 5e4, YELLOW)

    satellite = None
    satellite_init = False
    velocity_init = False

    while running:
        clock.tick(60)
        window.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if velocity_init:
                    satellite = None
                    satellite_init = False
                    velocity_init = False
                if not satellite_init:
                    satellite = Satellite(mouse_x, mouse_y, 10, 10, GREEN)
                    satellite_init = True
                    velocity_init = False
                else:
                    satellite.v_x = (mouse_x - satellite.x) / (TIMESTEP * 5e1)
                    satellite.v_y = (mouse_y - satellite.y) / (TIMESTEP * 5e1)
                    velocity_init = True

        # pygame.draw.circle(window, YELLOW, (SUN_X, SUN_Y), SUN_RADIUS) # sun
        sun.draw(window)

        # collision detection
        if satellite_init:
            collision_range = sun.radius + satellite.radius
            if abs(sun.x - satellite.x) <= collision_range and abs(sun.y - satellite.y) <= collision_range: # collision detected
                satellite = None
                satellite_init = False
                velocity_init = False

        if velocity_init:
            satellite.update_coors(sun)
        if satellite_init:
            if not velocity_init:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                pygame.draw.polygon(window, WHITE, [(satellite.x, satellite.y), (mouse_x, mouse_y)], width=2)
            satellite.draw(window)
            

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()