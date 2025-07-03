import pygame
Sx = 5
Sy = 5
Lx = 5
Ly = 5
Bx = 0
By = 0
PrevLx = 5
PrevLy = 5
Over = False
SELECTOR_LAYER = 3
LYN_LAYER = 2
MOV_LAYER =1
TILESIZE = 64
BACKGROUND = pygame.image.load('plains.png')
MovTile = pygame.image.load('MovTile.png')
LynFaceL = pygame.image.load('LynFaceL.png')

FPS = 30
Mov = 5
MapWidth = 14
MapHeight = 9
options = ["Item", "Attack", "Wait"]
selected = 0 
#Key = Character, [X Pos, Y Pos, SelectedStatus(0 is false, 1 is true)]
PositionDict = {
	"Lyn": [5,5,False],
	"Brig": [5,2,False]
}
SelectorPos = [5,5]
SelectedDict = {
	"Lyn": 0,
	"Brig": 0,

}
#Colors
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLUE = (50, 100, 255)
BLACK = (0, 0, 0)