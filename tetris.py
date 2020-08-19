"""Game of tetris"""
import pygame

class Block:
    """basic class for blocks in tetris"""
    def __init__(self, width, height):
        """__init__ basic constructor with"""
        self.width = width
        self.height = height
        self.pos_x = START_X
        self.pos_y = START_Y
        self.col_d = False
        self.col_l = False
        self.col_r = False
    def collision(self, block):
        """__colision checks whether or not one block colides with another"""
        if self.pos_x == block.pos_x and self.pos_y+self.height == block.pos_y:
            self.col_d = True
        if self.pos_x == block.pos_x+block.width and self.pos_y == block.pos_y:
            self.col_l = True
        if self.pos_x == block.pos_x-self.width and self.pos_y == block.pos_y:
            self.col_r = True
    def rotate(self):
        """rotate to be implemented"""
        pass

def restart(new_block, old_blocks):
    """Restarts the game"""
    new_block.pos_x = START_X
    new_block.pos_y = START_Y
    old_blocks.clear()
    return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
def boundary(active, objects):
    """Calculates boundary for the drop"""
    limit = SIZE[1]
    for obj in objects:
        if active.pos_x == obj.pos_x:
            limit = min(limit, obj.pos_y)
    active.pos_y = limit-active.height
    active.col_d = True
def draw(screen, active, objects):
    """Draws our game"""
    screen.fill(COLOUR)
    pygame.draw.rect(screen, (0, 0, 255), (80, 220, 200, 20))
    for obj in objects:
        pygame.draw.rect(screen, (0, 255, 0), (obj.pos_x, obj.pos_y, obj.width, obj.height))
    pygame.draw.rect(screen, (255, 0, 0), (active.pos_x, active.pos_y, active.width, active.height))
def collision(active, objects):
    """calculates multiple collisions"""
    for obj in objects:
        active.collision(obj)
def row_delete(active, objects, state):
    """deletes a filled row"""
    for i in range(10):
        if state[i] == 10:
            temp = []
            for obj in objects:
                if obj.pos_y > SIZE[1]-active.height-i*20:
                    temp.append(obj)
                else:
                    if obj.pos_y < SIZE[1]-active.height-i*20:
                        obj.pos_y += 20
                        temp.append(obj)
            objects = temp
            for j in range(9-i):
                state[i+j] = state[i+j+1]
            state[9] = 0
    return objects

#Important game constants:

RUN = True
SIZE = (320, 240)
COLOUR = (0, 0, 0)

SCREEN = pygame.display.set_mode(SIZE)

START_X = SIZE[0]//2
START_Y = -20

OBJECTS = []
CURRENT_STATE = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
ACTIVE = Block(20, 20)

pygame.init()

while RUN:

    pygame.time.delay(100)
    KEYS = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
    if not ACTIVE.col_d:
        ACTIVE.pos_y = min(ACTIVE.pos_y+20, SIZE[1]-ACTIVE.height)
        collision(ACTIVE, OBJECTS)
    if not ACTIVE.col_d and ACTIVE.pos_y < SIZE[1]-ACTIVE.height:
        if not ACTIVE.col_l and KEYS[pygame.K_LEFT]:
            ACTIVE.pos_x = max(ACTIVE.pos_x-20, 80)
        if not ACTIVE.col_r and KEYS[pygame.K_RIGHT]:
            ACTIVE.pos_x = min(ACTIVE.pos_x+20, 260)
        if KEYS[pygame.K_UP]:
            boundary(ACTIVE, OBJECTS)
        if KEYS[pygame.K_DOWN]:
            ACTIVE.pos_y = min(ACTIVE.pos_y+20, SIZE[1]-ACTIVE.height)
    else:
        OBJECTS.append(ACTIVE)
        CURRENT_STATE[(SIZE[1]-ACTIVE.height-ACTIVE.pos_y)//20] += 1
        ACTIVE = Block(20, 20)
        print(CURRENT_STATE)
        print(len(OBJECTS))
        OBJECTS = row_delete(ACTIVE, OBJECTS, CURRENT_STATE)
    if KEYS[pygame.K_SPACE]:
        CURRENT_STATE = restart(ACTIVE, OBJECTS)
    collision(ACTIVE, OBJECTS)

    draw(SCREEN, ACTIVE, OBJECTS)

    if CURRENT_STATE[9] != 0:
        print("restart")
        CURRENT_STATE = restart(ACTIVE, OBJECTS)
    pygame.display.update()
