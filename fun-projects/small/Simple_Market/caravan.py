import math
import pygame
class Caravan:
    def __init__(self, start_x, start_y, target_node, goods_count, payout_per_unit):
        self.x = float(start_x)
        self.y = float(start_y)
        self.home_node = None  # We will link the parent village here when spawning
        self.target_node = target_node  # The Town object we are traveling to

        self.goods = goods_count
        self.payout_per_unit = payout_per_unit
        self.held_currency = 0.0

        self.speed = 3.0  # Pixels per frame
        self.state = "DELIVERING"  # Can be "DELIVERING", "RETURNING", or "ARRIVED_HOME"
        self.color = (200, 150, 50)  # Orange/Brown color for the caravan dot

    def update(self):
        """Moves the caravan toward its current target depending on its state."""
        # Determine current target coordinates
        if self.state == "DELIVERING":
            target_x, target_y = self.target_node.x, self.target_node.y
        elif self.state == "RETURNING":
            target_x, target_y = self.home_node.x, self.home_node.y
        else:
            return

        # Calculate distance to target
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance <= self.speed:
            # We reached the target destination!
            self.x, self.y = target_x, target_y
            self.handle_arrival()
        else:
            # Move smoothly along the line towards target
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

    def handle_arrival(self):
        if self.state == "DELIVERING":
            # 1. Swap goods for money at the town
            self.held_currency = self.goods * self.payout_per_unit
            self.target_node.inventory += self.goods
            self.target_node.currency -= self.held_currency
            self.goods = 0

            # 2. Turn around and head home
            self.state = "RETURNING"

        elif self.state == "RETURNING":
            # 1. Give money to home village
            self.home_node.currency += self.held_currency
            self.held_currency = 0

            # 2. Mark as finished so main loop can delete it
            self.state = "ARRIVED_HOME"

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 5)
