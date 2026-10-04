import sys
import pygame
import random

from inhabited import Village, Town
from caravan import Caravan

#pygame initialisation, screen ize and clock
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Simple Market Map")
clock = pygame.time.Clock()

#create a village for test purposes
my_village = Village(currency = 0, population = 10)

#location of first village
village_x, village_y = random.randint(50, 750), random.randint(50, 550)

#define colour
background_color = (30,30,30) #RGB = Dark Grey
village_color = (0, 255,0) #RGB Bright Green

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background_color) #color in field
    pygame.draw.circle(screen, village_color, (village_x,village_y), 8)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
