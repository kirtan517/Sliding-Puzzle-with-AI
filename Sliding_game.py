import pygame
import math
import os
import time

pygame.init()

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# Independent Variables
OFFSET = 20
SPACE_BETWEEN_BLOCK = 5
NUM_BLOCKS_X = 5         #number_of_blocks_X
NUM_BLOCKS_Y = 5         # number_of_blocks_Y
BLOCK_SIZE = 150        # block_size
FONT_SIZE=70

# Dependent Variables        
WIDTH = BLOCK_SIZE*NUM_BLOCKS_X+(NUM_BLOCKS_X-1)*SPACE_BETWEEN_BLOCK+OFFSET*2
HEIGHT = BLOCK_SIZE*NUM_BLOCKS_Y+(NUM_BLOCKS_Y-1)*SPACE_BETWEEN_BLOCK+OFFSET*2

# Backgrounds 
win = pygame.display.set_mode((WIDTH, HEIGHT))

BACKGROUND_DIR = os.path.join("Images", "Background_1.jpeg")
BLOCK_DIR = os.path.join("Images", "Block_red.jpeg")

BACKGROUND_IMAGE=pygame.image.load(BACKGROUND_DIR)
# BACKGROUND_RESIZED=pygame.transform.scale(BACKGROUND_IMAGE,(WIDTH,HEIGHT))
BACKGROUND_RESIZED = pygame.Surface((WIDTH, HEIGHT))
BACKGROUND_RESIZED.fill(GREY)


BLOCK_IMAGE = pygame.image.load(BLOCK_DIR)
# BLOCK_RESIZED = pygame.transform.scale(BLOCK_IMAGE, (BLOCK_SIZE, BLOCK_SIZE))
BLOCK_RESIZED = pygame.Surface((BLOCK_SIZE,BLOCK_SIZE))
BLOCK_RESIZED.fill(WHITE)

BLOCK_CORDS=BLOCK_RESIZED.get_rect()

win.blit(BACKGROUND_RESIZED, (0, 0))
surface = pygame.Surface((WIDTH-2*OFFSET, HEIGHT-2*OFFSET))
surface.fill(BLACK)
font = pygame.font.SysFont('Sans', FONT_SIZE)




class block():

    def __init__(self,x,y,digit,invisible):
        self.x=x
        self.y=y
        self.digit=digit
        self.invisible=invisible
        self.image_draw=self.x - BLOCK_SIZE/(2),self.y - BLOCK_SIZE/(2)

    def draw(self,win):
        if not self.invisible:
            img = font.render(str(self.digit), True, BLACK)
            c=img.get_width()
            d=img.get_height()
            win.blit(BLOCK_RESIZED,(self.image_draw[0],self.image_draw[1]))
            win.blit(img, (self.x-c//2,self.y-d//2))

    def width(self):
        return BLOCK_RESIZED.get_width()

    def height(self):
        return BLOCK_RESIZED.get_height()

    def update(self,xpos,ypos):
        self.x=xpos
        self.y=ypos
        self.image_draw = self.x - BLOCK_SIZE/(2), self.y - BLOCK_SIZE/(2)

    

cords=[(x,y) for y in range(OFFSET+BLOCK_CORDS.center[1],HEIGHT-OFFSET,SPACE_BETWEEN_BLOCK+BLOCK_SIZE) 
             for x in range(OFFSET+BLOCK_CORDS.center[0],WIDTH-OFFSET,SPACE_BETWEEN_BLOCK+BLOCK_SIZE)]

blocks=[]
centers_x={}
centers_y={}
current_dic={}

for i in range(len(cords)-1):
    blocks.append(block(cords[i][0],cords[i][1],i,False))
    current_dic[(blocks[i].x,blocks[i].y)]=blocks[i]
    if (blocks[i].x-blocks[i].width()//2,blocks[i].x+blocks[i].width()//2) in centers_x:
        centers_x[(blocks[i].x-blocks[i].width()//2, blocks[i].x+blocks[i].width()//2)].append(i)
    else:
        centers_x[(blocks[i].x-blocks[i].width()//2, blocks[i].x+blocks[i].width()//2)]=[]
        centers_x[(blocks[i].x-blocks[i].width()//2,blocks[i].x+blocks[i].width()//2)].append(i)

    if (blocks[i].y-blocks[i].height()//2, blocks[i].y+blocks[i].height()//2) in centers_y:
        centers_y[(blocks[i].y-blocks[i].height()//2,blocks[i].y+blocks[i].height()//2)].append(i)
    else:
        centers_y[(blocks[i].y-blocks[i].height()//2,blocks[i].y+blocks[i].height()//2)] = []
        centers_y[(blocks[i].y-blocks[i].height()//2,blocks[i].y+blocks[i].height()//2)].append(i)

blocks.append(block(cords[-1][0], cords[-1][1], len(cords)-1, True))


def draw(win):
    win.blit(surface,(OFFSET,OFFSET))
    for i in blocks:
        i.draw(win)
    pygame.display.update()

def get_position(xpos,ypos):
    l=[]
    x=0
    y=0
    for i in centers_x:
        if xpos>=i[0] and xpos<i[1]:
            l=centers_x[i]
            x = (i[0]+i[1])//2
    for i in centers_y:
        if ypos>=i[0] and ypos<i[1]:
            for j in l:
                if j in centers_y[i]:
                    y = (i[0]+i[1])//2
                    return x,y

def Available_moves(blocks,Available):
    for i in blocks:
        if i.invisible:
            invisible = i
            Available=[(i.x+BLOCK_SIZE+SPACE_BETWEEN_BLOCK, i.y),
                        (i.x-BLOCK_SIZE-SPACE_BETWEEN_BLOCK, i.y),
                        (i.x,i.y+BLOCK_SIZE+SPACE_BETWEEN_BLOCK),
                        (i.x, i.y-BLOCK_SIZE-SPACE_BETWEEN_BLOCK)]
            for j in Available:
                if not (j[0]<WIDTH-OFFSET and j[0]>OFFSET and j[1]<HEIGHT-OFFSET and j[1]>OFFSET):
                    Available.remove(j)
            
    return Available,invisible

def move(win,to_be_moved,invisible):
    while  to_be_moved.x - invisible.x > 0:
       to_be_moved.update(to_be_moved.x-1,to_be_moved.y)
       draw(win)

    while to_be_moved.x - invisible.x < 0:
       to_be_moved.update(to_be_moved.x+1, to_be_moved.y)
       draw(win)

    while to_be_moved.y - invisible.y > 0:
       to_be_moved.update(to_be_moved.x, to_be_moved.y-1)
       draw(win)

    while to_be_moved.y - invisible.y < 0:
       to_be_moved.update(to_be_moved.x, to_be_moved.y+1)
       draw(win)



def main():
    run=True
    Available=[]
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False

            if event.type == pygame.MOUSEBUTTONDOWN:
                xpos,ypos=pygame.mouse.get_pos()
                Available,invisible=Available_moves(blocks,Available)
                

                if get_position(xpos,ypos):
                    x, y = get_position(xpos, ypos)
                    if (x,y) in Available:
                        move(win,current_dic[(x,y)],invisible)
                        current_dic[(invisible.x,invisible.y)]=current_dic[(x,y)]
                        current_dic.pop((x,y))
                        invisible.update(x,y)



        draw(win)

if __name__ == "__main__":
    main()
    
