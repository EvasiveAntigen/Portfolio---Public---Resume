import sys
import pygame
import random

from inhabited import Village, Town, City
from pioneer import Pioneer
from caravan import Caravan

# Pygame initialisation, screen size and clock
pygame.init()
pygame.font.init()  # Initialize font module for tooltips
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Simple Market Map")
clock = pygame.time.Clock()

# Font setup for tooltips
ui_font = pygame.font.SysFont("Arial", 12)

# Colors
background_color = (30, 30, 30)   # RGB = Dark Grey
village_color = (0, 255, 0)       # RGB = Bright Green
town_color = (70, 130, 180)       # RGB = Steel Blue
city_color = (220, 20, 60)        # RGB = Crimson Red
pioneer_color = (255, 105, 180)   # Hot Pink
tooltip_bg = (10, 10, 10)         # Near Black for tooltip background
tooltip_border = (180, 180, 180)  # Light Grey border

# Lists for existing settlements, caravans, and pioneers
settlements = [Village(x=400, y=300, currency=100, population=10)]
caravans = []
pioneers = []

tick_counter = 0  # Used to slow down production/consumption to once per second
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    tick_counter += 1
    city_exists = any(isinstance(s, City) for s in settlements)

    # 1. SETTLEMENT LOGIC
    for i in range(len(settlements)):
        s = settlements[i]

        # Production and consumption every second
        if tick_counter % 60 == 0:
            if not isinstance(s, City):
                s.produce_good()
                s.consumption()

        if isinstance(s, Village):
            # Send caravan to nearest Town or City if stock is ready
            if s.inventory >= 20:
                markets = [m for m in settlements if isinstance(m, (Town, City))]
                if markets:
                    target_market = min(markets, key=lambda m: (m.x - s.x)**2 + (m.y - s.y)**2)
                    goods = 20.0
                    s.inventory -= goods

                    c = Caravan(s.x, s.y, target_market, goods, target_market.payout_per_unit)
                    c.home_node = s
                    caravans.append(c)

        elif isinstance(s, Town):
            if tick_counter % 60 == 0:
                pioneer_target = s.expansion(settlements)
                if pioneer_target:
                    pioneers.append(Pioneer(s.x, s.y, pioneer_target[0], pioneer_target[1]))

        # Settlement promotion check
        settlements[i] = s.check_promote(current_city_exists=city_exists)

    # 2. PIONEER UPDATES
    for pioneer in pioneers[:]:
        pioneer.update()
        if pioneer.state == "ARRIVED":
            new_village = Village(x=pioneer.x, y=pioneer.y, currency=50.0, population=50)
            settlements.append(new_village)
            pioneers.remove(pioneer)
            print(f"New Village founded at ({int(pioneer.x)}, {int(pioneer.y)})!")

    # 3. CARAVAN UPDATES
    for caravan in caravans[:]:
        caravan.update()
        if caravan.state == "ARRIVED_HOME":
            caravans.remove(caravan)

    # 4. RENDERING
    screen.fill(background_color)

    # Draw Settlements
    hovered_settlement = None
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for s in settlements:
        if isinstance(s, City):
            color, radius = city_color, 14
        elif isinstance(s, Town):
            color, radius = town_color, 10
        else:
            color, radius = village_color, 6

        # Draw settlement circle
        pygame.draw.circle(screen, color, (int(s.x), int(s.y)), radius)

        # Check mouse hover within radius
        dist_sq = (mouse_x - s.x) ** 2 + (mouse_y - s.y) ** 2
        if dist_sq <= radius ** 2:
            hovered_settlement = s

    # Draw Pioneers
    for pioneer in pioneers:
        pioneer.draw(screen)

    # Draw Caravans
    for caravan in caravans:
        pygame.draw.circle(screen, caravan.color, (int(caravan.x), int(caravan.y)), 5)

    # 5. DRAW TOOLTIP OVERLAY
    if hovered_settlement:
        settlement_type = hovered_settlement.__class__.__name__
        text_lines = [
            f"Type: {settlement_type}",
            f"Pop: {hovered_settlement.population}",
            f"Gold: {int(hovered_settlement.currency)}",
            f"Inv: {int(hovered_settlement.inventory)}"
        ]

        # Add good_type if it's a village
        if hasattr(hovered_settlement, "good_type"):
            text_lines.append(f"Good: {hovered_settlement.good_type}")

        # Render surfaces and calculate bounding box size
        rendered_lines = [ui_font.render(line, True, (255, 255, 255)) for line in text_lines]
        box_width = max(line.get_width() for line in rendered_lines) + 12
        box_height = sum(line.get_height() for line in rendered_lines) + 10

        # Position box near cursor with screen boundary safety
        box_x = min(mouse_x + 15, 800 - box_width - 5)
        box_y = min(mouse_y + 15, 600 - box_height - 5)

        # Draw Tooltip Background & Border
        pygame.draw.rect(screen, tooltip_bg, (box_x, box_y, box_width, box_height))
        pygame.draw.rect(screen, tooltip_border, (box_x, box_y, box_width, box_height), 1)

        # Render Text Lines
        y_offset = box_y + 5
        for surface in rendered_lines:
            screen.blit(surface, (box_x + 6, y_offset))
            y_offset += surface.get_height()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
