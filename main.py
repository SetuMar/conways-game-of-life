import pygame
import sys
import random

screen_size = [800, 800]
pygame.init()

colors = {"alive":(255, 255, 255), "dead":(0, 0, 0), "grid":(75, 75, 75),}

display = pygame.display.set_mode((screen_size))
clock = pygame.time.Clock()

def grid(color, grid_space):
    for dimension in range(0, screen_size[0]//grid_space):
        pygame.draw.line(display, color, (0, dimension * grid_space), (screen_size[0], dimension * grid_space))
        pygame.draw.line(display, color, (dimension * grid_space, 0), (dimension * grid_space, screen_size[0]))

grid_size = 10

class Block:
    def __init__(self, position, size, state):
        self.image = pygame.Surface(size)
        self.image.fill(state)

        self.state = state

        self.rect = self.image.get_rect()
        self.rect.topleft = position

        self.alive_count = 0
    
    def update_state(self):
        if self.alive_count < 2 and self.state == colors['alive'] or self.alive_count > 3 and self.state == colors['alive']:
            self.state = colors['dead']

        if self.alive_count == 3 and self.state == colors['dead']:
            self.state = colors['alive']
    
    def draw(self, display):
        self.image.fill(self.state)
        display.blit(self.image, self.rect.topleft)

blocks = {}

for y in range(int(screen_size[1]/grid_size)):
    for x in range(int(screen_size[0]/grid_size)):
        blocks.update({(x, y):Block(pygame.math.Vector2(x * grid_size, y * grid_size), pygame.math.Vector2(grid_size, grid_size), colors[random.choice(['alive', 'dead'])])})

possible_indeces = blocks.keys()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for block_index, block in blocks.items():
        block.alive_count = 0
        block.draw(display)

        check_indeces = []

        for y_b in range(-1, 2):
            for x_b in range(-1, 2):
                temp_ci = (block_index[0] + x_b, + block_index[1] + y_b)
                if temp_ci in possible_indeces and (x_b, y_b) != (0, 0):
                    check_indeces.append(temp_ci)
        
        for index in check_indeces:
            if blocks[index].state == colors["alive"]:
                block.alive_count += 1
    
    for block_index, block in blocks.items():
        block.update_state()

    grid(colors["grid"], grid_size)

    pygame.display.update()
    clock.tick(60)