# pygame.Rect(x, y, width, height): used to describe position and area of rectangular
# x, y, left, top, bottom, right, centerx, centery, size, width, height
# for ex: hero_rect.x = 100

import pygame
hero_rect = pygame.Rect(100, 500, 120, 125)
print("Here start position %d %d" % (hero_rect.x, hero_rect.y))
print("Here start size %d %d" % (hero_rect.width, hero_rect.height))
print("%d %d" % hero_rect.size)
