import time

import numpy as np
import pygame
from attrs import define

map_width = 24
map_height = 24
screen_width = 640
screen_height = 480


@define(frozen=True, slots=False)
class World:
    MAP: np.ndarray = np.array(
        [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 3, 0, 3, 0, 3, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 2, 2, 0, 2, 2, 0, 0, 0, 0, 3, 0, 3, 0, 3, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 4, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 4, 0, 0, 0, 0, 5, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 4, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 4, 0, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]
    )


world = World()


@define(slots=False)
class Player:
    pos: np.ndarray
    dirn: np.ndarray
    cam: np.ndarray


pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

# initialize player
player = Player(pos=np.array([22, 12]), dirn=np.array([-1, 0]), cam=np.array([0, 0.66]))

# game loop
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for x in range(screen_width):

        # 1. Get ray direction
        camera_x = ((2 * x) / map_width) - 1
        ray_dir = player.dirn + player.cam * camera_x

        # 2. Setup DDA

        # which box we're in on the map
        map_pos = np.round(player.pos).astype(int)

        # length of ray from one x or y side to next x or y side
        delta_dist_x = np.inf if player.dirn[0] == 0 else np.abs(1 / player.dirn[0])
        delta_dist_y = np.inf if player.dirn[1] == 0 else np.abs(1 / player.dirn[1])

        # direction to take step in
        step_x = 0
        step_y = 0

        # get initial step and side distance values
        if player.dirn[0] < 0:
            step_x = -1
            side_dist_x = (player.pos[0] - map_pos[0]) * delta_dist_x
        else:
            step_x = 1
            side_dist_x = (player.pos[0] - map_pos[0] + 1.0) * delta_dist_x

        if player.dirn[1] < 0:
            step_y = -1
            side_dist_x = (player.pos[1] - map_pos[1]) * delta_dist_y
        else:
            step_y = 1
            side_dist_y = (player.pos[1] - map_pos[1] + 1.0) * delta_dist_y

        # 3. Perform DDA
        no_hit = True
        side = 0  # hit x or y side first?
        while no_hit:
            if side_dist_x < side_dist_y:
                side_dist_x += delta_dist_x
                map_pos[0] += step_x
                side = 0
            else:
                side_dist_y += delta_dist_y
                map_pos[1] += step_y
                side = 1
            if world.MAP[map_pos[0], map_pos[1]] > 0:
                # print("Hit!")
                no_hit = False

        if side == 0:
            perp_wall_dist = side_dist_x - delta_dist_x
        else:
            perp_wall_dist = side_dist_y - delta_dist_y

        # 4. Get line to draw
        line_height = screen_height // perp_wall_dist

        draw_start = (-line_height // 2) + (screen_height // 2)
        if draw_start < 0:
            draw_start = 0

        draw_end = (line_height // 2) + (screen_height // 2)
        if draw_start >= screen_height:
            draw_end = screen_height - 1

    screen.fill("purple")

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
