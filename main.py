from math import floor

import numpy as np
import pygame
from attrs import define
from pygame import surfarray

map_width = 24
map_height = 24
texture_width = 64
texture_height = 64
screen_width = 640
screen_height = 480


@define(frozen=True, slots=False)
class World:
    MAP: np.ndarray = np.array(
        [
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 7, 7, 7, 7, 7, 7, 7, 7],
            [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 7],
            [4, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7],
            [4, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7],
            [4, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 7],
            [4, 0, 4, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 7, 7, 0, 7, 7, 7, 7, 7],
            [4, 0, 5, 0, 0, 0, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 7, 0, 0, 0, 7, 7, 7, 1],
            [4, 0, 6, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 7, 0, 0, 0, 0, 0, 0, 8],
            [4, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 1],
            [4, 0, 8, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 7, 0, 0, 0, 0, 0, 0, 8],
            [4, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 7, 0, 0, 0, 7, 7, 7, 1],
            [4, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 0, 5, 5, 5, 5, 7, 7, 7, 7, 7, 7, 7, 1],
            [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
            [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
            [6, 6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
            [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 6, 0, 6, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3],
            [4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 6, 0, 6, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2],
            [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 2, 0, 0, 5, 0, 0, 2, 0, 0, 0, 2],
            [4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 6, 0, 6, 2, 0, 0, 0, 0, 0, 2, 2, 0, 2, 2],
            [4, 0, 6, 0, 6, 0, 0, 0, 0, 4, 6, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 2],
            [4, 0, 0, 5, 0, 0, 0, 0, 0, 4, 6, 0, 6, 2, 0, 0, 0, 0, 0, 2, 2, 0, 2, 2],
            [4, 0, 6, 0, 6, 0, 0, 0, 0, 4, 6, 0, 6, 2, 0, 0, 5, 0, 0, 2, 0, 0, 0, 2],
            [4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 6, 0, 6, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3],
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

# pixel array
array = np.zeros((screen_width, screen_height, 3), np.int32)

textures = np.zeros((8, texture_width * texture_height), np.float32)

for x in range(texture_width):
    for y in range(texture_height):
        xor_color = (x * 256 // texture_width) ^ (y * 256 // texture_height)
        ycolor = y * 256 // texture_height
        xycolor = y * 128 // texture_height + x * 128 // texture_width
        textures[0][texture_width * y + x] = (
            65536 * 254 * (x != y and x != texture_width - y)
        )
        textures[1][texture_width * y + x] = xycolor + 256 * xycolor + 65536 * xycolor
        textures[2][texture_width * y + x] = 256 * xycolor + 65536 * xycolor
        textures[3][texture_width * y + x] = (
            xor_color + 256 * xor_color + 65536 * xor_color
        )
        textures[4][texture_width * y + x] = 256 * xor_color
        textures[5][texture_width * y + x] = 65536 * 192 * (x % 16 != 0 and y % 16 != 0)
        textures[6][texture_width * y + x] = 65536 * ycolor
        textures[7][texture_width * y + x] = 128 + 256 * 128 + 65536 * 128


# initialize player
player = Player(
    pos=np.array([22.0, 11.5]), dirn=np.array([-1.0, 0.0]), cam=np.array([0.0, 0.66])
)

# variables
move_speed = (1 / 60) * 5.0
rot_speed = (1 / 60) * 3.0

# game loop
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        next_pos = player.pos + (player.dirn * move_speed)
        next_map_pos = np.floor(next_pos).astype(int)
        if world.MAP[next_map_pos[0], int(player.pos[1])] == False:
            player.pos[0] = next_pos[0]
        if world.MAP[int(player.pos[0]), next_map_pos[1]] == False:
            player.pos[1] = next_pos[1]

    if keys[pygame.K_DOWN]:
        next_pos = player.pos - (player.dirn * move_speed)
        next_map_pos = np.floor(next_pos).astype(int)
        if world.MAP[next_map_pos[0], int(player.pos[1])] == False:
            player.pos[0] = next_pos[0]
        if world.MAP[int(player.pos[0]), next_map_pos[1]] == False:
            player.pos[1] = next_pos[1]

    if keys[pygame.K_RIGHT]:
        old_dir = player.dirn.copy()
        old_cam = player.cam.copy()

        rot_mat = np.array(
            [
                [np.cos(-rot_speed), -np.sin(-rot_speed)],
                [np.sin(-rot_speed), +np.cos(-rot_speed)],
            ]
        )

        player.dirn = rot_mat @ old_dir
        player.cam = rot_mat @ old_cam

    if keys[pygame.K_LEFT]:
        old_dir = player.dirn.copy()
        old_cam = player.cam.copy()

        rot_mat = np.array(
            [
                [np.cos(rot_speed), -np.sin(rot_speed)],
                [np.sin(rot_speed), +np.cos(rot_speed)],
            ]
        )

        player.dirn = rot_mat @ old_dir
        player.cam = rot_mat @ old_cam

    #    print(player)

    for w in range(screen_width):

        # 1. Get ray direction
        x = float(w)
        camera_x = ((2 * x) / screen_width) - 1
        ray_dir = player.dirn + player.cam * camera_x

        # 2. Setup DDA

        # which box we're in on the map
        map_pos = np.floor(player.pos).astype(int)

        # length of ray from one x or y side to next x or y side
        ray_len = 1  # np.linalg.norm(ray_dir)
        delta_dist_x = np.inf if ray_dir[0] == 0 else np.abs(ray_len / ray_dir[0])
        delta_dist_y = np.inf if ray_dir[1] == 0 else np.abs(ray_len / ray_dir[1])

        # direction to take step in
        step_x = 0
        step_y = 0

        # get initial step and side distance values
        if ray_dir[0] < 0:
            step_x = -1
            side_dist_x = (player.pos[0] - map_pos[0]) * delta_dist_x
        else:
            step_x = 1
            side_dist_x = (map_pos[0] + 1.0 - player.pos[0]) * delta_dist_x

        if ray_dir[1] < 0:
            step_y = -1
            side_dist_y = (player.pos[1] - map_pos[1]) * delta_dist_y
        else:
            step_y = 1
            side_dist_y = (map_pos[1] + 1.0 - player.pos[1]) * delta_dist_y

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
        perp_wall_dist = max(perp_wall_dist, 1e-6)

        # 4. Get line to draw
        line_height = screen_height // perp_wall_dist

        draw_start = (-line_height // 2) + (screen_height // 2)
        if draw_start < 0:
            draw_start = 0

        draw_end = (line_height // 2) + (screen_height // 2)
        if draw_end >= screen_height:
            draw_end = screen_height - 1

        # texture stuff
        val = world.MAP[map_pos[0], map_pos[1]]

        tex_num = val - 1

        wall_x = 0
        if side == 0:
            wall_x = player.pos[1] + perp_wall_dist * ray_dir[1]
        else:
            wall_x = player.pos[0] + perp_wall_dist * ray_dir[0]

        wall_x -= floor(wall_x)

        tex_x = int(wall_x * texture_width)
        if side == 0 and ray_dir[0] > 0:
            tex_x = texture_width - tex_x - 1
        if side == 1 and ray_dir[1] < 0:
            tex_x = texture_width - tex_x - 1

        step = 1.0 * texture_height / line_height
        tex_pos = (draw_start - screen_height / 2 + line_height / 2) * step
        for y in range(int(draw_start), int(draw_end)):
            tex_y = int(tex_pos) & (texture_height - 1)
            tex_pos += step
            packed = int(textures[tex_num][texture_width * tex_y + tex_x])
            color = (
                (packed >> 16) & 0xFF,
                (packed >> 8) & 0xFF,
                packed & 0xFF,
            )
            if side == 1:
                color = tuple(c // 2 for c in color)
            array[w, y, :] = color
        # if val == 0:
        #    color = (255, 255, 255)
        # elif val == 1:
        #    color = (255, 0, 0)
        # elif val == 2:
        #    color = (0, 255, 0)
        # elif val == 3:
        #    color = (0, 0, 255)
        # elif val == 4:
        #    color = (255, 0, 255)
        # elif val == 5:
        #    color = (255, 255, 0)
        # if side == 0:
        #    color = tuple(x // 2 for x in color)
        ## print(x, int(draw_start), draw_end)
        ## print(type(x), type(draw_start), tdype(draw_end))
    # array[w, int(draw_start) : int(draw_end), :] = color

    surfarray.blit_array(screen, array)
    pygame.display.flip()
    array.fill(0)
    clock.tick(60)

pygame.quit()
