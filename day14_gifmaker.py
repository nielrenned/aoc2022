from PIL import Image

WALL_POINTS = set()

MIN_X = 500
MAX_X = 500
MIN_Y = 0
MAX_Y = 0

def sgn(n):
    if n > 0:  return 1
    if n == 0: return 0
    if n < 0:  return -1

def points_between_inclusive(p1, p2):
    dx = p2[0] - p1[0]
    sx = sgn(dx)
    dy = p2[1] - p1[1]
    sy = sgn(dy)
    for i in range(max(abs(dx), abs(dy))+1):
        yield (p1[0] + i*sx, p1[1] + i*sy)

def load_and_parse_input():
    global WALL_POINTS, MIN_X, MAX_X, MIN_Y, MAX_Y
    
    path = 'inputs/day14.txt'
    with open(path) as f:
        RAW_INPUT = f.read()
    
    for line in RAW_INPUT.split('\n')[:-1]:
        pairs = line.split(' -> ')
        for i in range(len(pairs)-1):
            p1 = tuple(map(int, pairs[i].split(',')))
            p2 = tuple(map(int, pairs[i+1].split(',')))
            for x,y in points_between_inclusive(p1, p2):
                WALL_POINTS.add((x,y))
                MIN_X = min(x, MIN_X)
                MAX_X = max(x, MAX_X)
                MIN_Y = min(y, MIN_Y)
                MAX_Y = max(y, MAX_Y)

def draw_frame(settled_sand_points, moving_sand_points):
    SCALE = 3
    
    X_MARGIN = 2
    Y_MARGIN = 1
    
    WIDTH  = (MAX_X - MIN_X + 1 + 2*X_MARGIN)*SCALE + SCALE
    HEIGHT = (MAX_Y - MIN_Y + 1 + 2*Y_MARGIN)*SCALE + SCALE
    
    BG_COLOR           = (64, 64, 64) # gray
    WALL_COLOR         = (0, 0, 0) # black
    SETTLED_SAND_COLOR = (255, 255, 255) # white
    MOVING_SAND_COLOR  = (255, 255, 0)
    
    im = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    
    for x, y in WALL_POINTS:
        pixel_x_start = (x - MIN_X + X_MARGIN)*SCALE
        pixel_y_start = (y - MIN_Y + Y_MARGIN)*SCALE
        for pixel_x in range(pixel_x_start, pixel_x_start + SCALE):
            for pixel_y in range(pixel_y_start, pixel_y_start+SCALE):
                im.putpixel((pixel_x, pixel_y), WALL_COLOR)
    
    for x, y in settled_sand_points:
        pixel_x_start = (x - MIN_X + X_MARGIN)*SCALE
        pixel_y_start = (y - MIN_Y + Y_MARGIN)*SCALE
        for pixel_x in range(pixel_x_start, pixel_x_start + SCALE):
            for pixel_y in range(pixel_y_start, pixel_y_start+SCALE):
                im.putpixel((pixel_x, pixel_y), SETTLED_SAND_COLOR)
    
    for x, y in moving_sand_points:
        pixel_x_start = (x - MIN_X + X_MARGIN)*SCALE
        pixel_y_start = (y - MIN_Y + Y_MARGIN)*SCALE
        for pixel_x in range(pixel_x_start, pixel_x_start + SCALE):
            for pixel_y in range(pixel_y_start, pixel_y_start+SCALE):
                im.putpixel((pixel_x, pixel_y), MOVING_SAND_COLOR)
    
    return im

def run_simulation():
    SAND_DIRECTIONS = [(0, 1), (-1, 1), (1, 1)] # order matters here!
    SAND_START = (500, 0)
    SAND_CAP = 1016 + 1
    
    images = []
    
    settled_sand = set()
    moving_sand = []
    
    ticks = 0
    dropped_sand = 0
    done_dropping = False
    
    while not (done_dropping):
        if ticks % 2 == 0 and dropped_sand < SAND_CAP:
            moving_sand.append(SAND_START)
            dropped_sand += 1
        
        still_moving = []
        for i, (x, y) in enumerate(moving_sand):
            for dx, dy in SAND_DIRECTIONS:
                next_position = (x + dx, y + dy)
                if next_position not in settled_sand and next_position not in WALL_POINTS:
                    still_moving.append(next_position)
                    break
            else:
                settled_sand.add((x,y))
                continue
            
            if y > MAX_Y:
                done_dropping = True
                break
        
        moving_sand = still_moving
        ticks += 1
        
        print(ticks)
        
        images.append(draw_frame(settled_sand, moving_sand))
    
    MS_PER_FRAME = 20 # 20ms/frame = 50fps, which is the max supported by most browsers
    FPS = 1000 // MS_PER_FRAME
    
    # Freeze frame for 2 seconds at the end
    for _ in range(2*FPS):
        images.append(draw_frame(settled_sand, set()))
    
    
    images[0].save('images/day14.gif', save_all=True, append_images=images[1:], optimize=False, duration=MS_PER_FRAME)
    
if __name__ == "__main__":
    load_and_parse_input()
    run_simulation()