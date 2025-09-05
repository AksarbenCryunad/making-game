import random

BOARD_WIDTH = 800
BOARD_HEIGHT = 800
NUM_GRID = 4
GRID_SIZE = BOARD_WIDTH // NUM_GRID
TILE_MARGIN = 3

BG_COLOR = (187, 173, 160)
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}
DEFAULT_COLOR = TILE_COLORS[0]

def rotate(is_cw, board_map):
    new_map = None

    if is_cw:
        # CW
        new_map = [list(row) for row in zip(*board_map[::-1])]
    else:
        # CCW
        new_map = [list(row) for row in zip(*board_map)][::-1]
    return new_map

def merge_row(row):
    new_row = []
    skip_merge = False

    for i in range(NUM_GRID):
        if skip_merge is True:
            skip_merge = False
            continue
        if row[i] == 0:
            continue
        elif i + 1 < len(row) and row[i] == row[i + 1]:
            new_row.append(row[i]*2)
            skip_merge = True
        elif i < len(row):
            new_row.append(row[i])
    while len(new_row) < NUM_GRID:
        new_row.append(0)
    return new_row

def push_and_merge(rotate_times, board_map):
    rotated_map = board_map
    # Rotate cw90 * rotate_times
    for _ in range(rotate_times):
        rotated_map = rotate(True, rotated_map)
    # Merge row
    new_board = []
    for row in rotated_map:
        new_row = merge_row(row)
        new_board.append(new_row)
    # Rotate ccw90 * rotate_times
    for _ in range(rotate_times):
        new_board = rotate(False, new_board)
    return new_board

def draw_cell(screen, row, column, font, value):
    rect = pygame.Rect(column * GRID_SIZE + TILE_MARGIN, 
                    row * GRID_SIZE + TILE_MARGIN, 
                    GRID_SIZE - TILE_MARGIN * 2, 
                    GRID_SIZE - TILE_MARGIN * 2)
    color = TILE_COLORS.get(value, DEFAULT_COLOR) # TILE_COLOR[value]가 보통이지만 get을 쓰면 디폴트 설정가능
    pygame.draw.rect(screen, color, rect)

    # Display number
    if value != 0:
        text_area = font.render(str(value), True, (0, 0, 0))
        cell_x = rect.centerx - (text_area.get_width() // 2)
        cell_y = rect.centery - (text_area.get_height() // 2)
        screen.blit(text_area, (cell_x, cell_y))

def render_board(screen, board_map, font):
    screen.fill(BG_COLOR)

    for row in range(NUM_GRID):
        for column in range(NUM_GRID):
            draw_cell(screen, row, column, font, board_map[row][column])

def spawn_tile(board_map):
    empty_cells = [(r, c) for r in range(NUM_GRID)
                   for c in range(NUM_GRID)
                   if board_map[r][c] == 0]
    if empty_cells:
        new_value = random.choices([2, 4], weights=[0.9, 0.1])[0]
        spawn_r, spawn_c = random.choice(empty_cells)
        board_map[spawn_r][spawn_c] = new_value
        return True
    # No empty cells left.
    return False

if __name__ == "__main__":
    # Example file showing a circle moving on screen
    import pygame

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
    pygame.display.set_caption("2048 games")
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.SysFont("Arial", 50, bold=True)
    board_map = [[0 for _ in range(NUM_GRID)] for _ in range(NUM_GRID)]

    spawn_tile(board_map)

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                rotate_times = -1
                match event.key:
                    case pygame.K_LEFT:
                        rotate_times = 0
                    case pygame.K_RIGHT:
                        rotate_times = 2
                    case pygame.K_UP:
                        rotate_times = 3
                    case pygame.K_DOWN:
                        rotate_times = 1
                    case _:
                        pass
                if rotate_times != -1:
                    board_map = push_and_merge(rotate_times, board_map)
                    spawn_tile(board_map)

        # fill the screen with a color to wipe away anything from last frame
        # screen.fill(BG_COLOR)

        # RENDER YOUR GAME HERE
        render_board(screen, board_map, font)

       
        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pygame.quit()