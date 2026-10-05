import math
import pygame


class Pioneer:

  def __init__(self, start_x, start_y, target_x, target_y):
    self.x = float(start_x)
    self.y = float(start_y)
    self.target_x = float(target_x)
    self.target_y = float(target_y)

    self.speed = 2.0
    self.color = (255, 105, 180)  # Hot Pink
    self.state = "MOVING"

  def update(self):
    # Guard clause: stop updating if already arrived
    if self.state == "ARRIVED":
      return

    dx = self.target_x - self.x
    dy = self.target_y - self.y
    distance = math.hypot(dx, dy)

    if distance <= self.speed:
      self.x = self.target_x
      self.y = self.target_y
      self.state = "ARRIVED"
    else:
      self.x += (dx / distance) * self.speed
      self.y += (dy / distance) * self.speed

  def draw(self, surface):
    pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 4)
