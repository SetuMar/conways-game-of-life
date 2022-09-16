import pygame
import sys
import random

import menu

screen_size = [1000, 800]
pygame.init()

colors = {"alive":(255, 255, 255), "dead":(0, 0, 0), "grid":(75, 75, 75),}

display = pygame.display.set_mode((screen_size))
clock = pygame.time.Clock()

def grid(color, grid_space):
    for dimension in range(0, screen_size[0]//grid_space):
        pygame.draw.line(display, color, (0, dimension * grid_space), (screen_size[0], dimension * grid_space))
        pygame.draw.line(display, color, (dimension * grid_space, 0), (dimension * grid_space, screen_size[0]))

grid_size = 10

is_placed = True
game_started = False

all_blocks_clear = True

class Block:
    def __init__(self, position, size, state):
        self.image = pygame.Surface(size)
        self.image.fill(state)

        self.state = state

        self.rect = self.image.get_rect()
        self.rect.topleft = position

        self.alive_count = 0

        if self.state == colors['alive']:
            self.alive_count = 2
        
    def draw_mode(self):
        mouse_input = pygame.mouse.get_pressed()
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if mouse_input[0]:
                self.state = colors['alive']
                self.alive_count = 2
            
            elif mouse_input[2]:
                self.state = colors['dead']
            
    def update_state(self):
        if self.alive_count < 2 and self.state == colors['alive'] or self.alive_count > 3 and self.state == colors['alive']:
            self.state = colors['dead']

        if self.alive_count == 3 and self.state == colors['dead']:
            self.state = colors['alive']
    
    def clear(self):
        self.state = colors['dead']
        self.alive_count = 0
    
    def draw(self, display):
        self.image.fill(self.state)
        display.blit(self.image, self.rect.topleft)

blocks = {}

for y in range(int(screen_size[1]/grid_size)):
    for x in range(int(screen_size[0]/grid_size)):
        blocks.update({(x, y):Block(pygame.math.Vector2(x * grid_size, y * grid_size), pygame.math.Vector2(grid_size, grid_size), colors['dead'])})

possible_indeces = blocks.keys()

main_menu = menu.StartMenu(pygame.math.Vector2(screen_size[0]/2, screen_size[0]/2), screen_size)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_e]:
        game_started = True

    for block_index, block in blocks.items():
        block.draw(display)

        if game_started:
            block.alive_count = 0
            check_indeces = []

            for y_b in range(-1, 2):
                for x_b in range(-1, 2):
                    temp_ci = (block_index[0] + x_b, + block_index[1] + y_b)
                    if temp_ci in possible_indeces and (x_b, y_b) != (0, 0):
                        check_indeces.append(temp_ci)
            
            for index in check_indeces:
                if blocks[index].state == colors["alive"]:
                    block.alive_count += 1
    
    alive_count = list(filter(lambda b: b.state == colors['alive'], blocks.values()))

    for block_index, block in blocks.items():
        if keys[pygame.K_r] or (game_started and len(alive_count) == 0):
            block.clear()
            game_started = False
        
        block.update_state()
        block.draw_mode()

    grid(colors["grid"], grid_size)

    main_menu.draw_container(display)

    pygame.display.update()
    clock.tick(60)