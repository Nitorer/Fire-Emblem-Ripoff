import pygame
from Sprites import *
from config import *
from assets import load_images# type: ignore
from collections import deque
import random
import math
import time
import json
import os 

class Node:
    def __init__(self, x, y, walkable = True):
        self.x = x
        self.y = y
        self.walkable = walkable
        self.parent = None
        self.g = 0 # Cost from start to node
        self.h = 0 #Heuristic cost to goal
        self.f = 0 # Total Cost to goal
        pass
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((960, 640))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("gba-fe-dialogue.ttf", 40)
        self.running = True
        self.playing = True
        self.reachable_tiles = []
        self.current_path = []

        self.mov_surface = pygame.Surface((960, 640), pygame.SRCALPHA)


        #Images
        self.images = load_images("Assets")
        self.BACKGROUND = self.images["Plains"]
        self.MovTile = self.images["MovTile"]
        self.AtkTile = self.images["AtkTile"]
        self.LynFaceL = self.images["LynFaceL"]

        
        # Game state
        self.Sx, self.Sy = 5, 5
        self.Lx, self.Ly = 0, 0
        self.PrevLx, self.PrevLy = None, None
        self.CharKey, self.SelectedUnit = None, None
        self.Over, self.attacking = False, False
        self.Mov = 5

    def new(self):
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.selector = Selector(self, self.Sx, self.Sy, self.images["Selector"])
        self.lyn = Lyn(self, PositionDict["Lyn"][0], PositionDict["Lyn"][1], self.images["Lyn"])
        self.brigand = Brigand(self, PositionDict["Brig"][0], PositionDict["Brig"][1], self.images["Brigand"])
        
    def generate_grid(self):
        self.grid = []
        for y in range(10):
            row = []
            for x in range(15):
                walkable = not self.IsTileOccupied(x, y, self.CharKey)
                row.append(Node(x, y, walkable))
            self.grid.append(row)
    
     
    def get_reachable_nodes(self, start_x, start_y, move_range):
        visited = set()
        queue = deque([(start_x, start_y, 0)])
        reachable = []

        while queue:
            x, y, dist = queue.popleft()
            if (x, y) in visited or dist > move_range:
                continue

            visited.add((x, y))
            reachable.append((x, y))

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 15 and 0 <= ny < 10:
                    if not self.IsTileOccupied(nx, ny, self.CharKey):
                        queue.append((nx, ny, dist + 1))
        
        return reachable
    
    def astar_path(self, start, goal):
        self.generate_grid()  # Regenerate with latest walkability

        open_set = []
        closed_set = set()

        start_node = self.grid[start[1]][start[0]]
        goal_node = self.grid[goal[1]][goal[0]]

        for row in self.grid:
            for node in row:
                node.g = node.h = node.f = 0
                node.parent = None

        open_set.append(start_node)

        while open_set:
            current = min(open_set, key=lambda n: n.f)

            if (current.x, current.y) == (goal_node.x, goal_node.y):
                path = []
                while current:
                    path.append((current.x, current.y))
                    current = current.parent
                return path[::-1]

            open_set.remove(current)
            closed_set.add((current.x, current.y))

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = current.x + dx, current.y + dy
                if not (0 <= nx < 15 and 0 <= ny < 10):
                    continue

                neighbor = self.grid[ny][nx]

                if self.IsTileOccupied(nx, ny, self.CharKey) and (nx, ny) != (goal_node.x, goal_node.y):
                    continue

                if (neighbor.x, neighbor.y) in closed_set:
                    continue

                tentative_g = current.g + 1

                if neighbor not in open_set:
                    open_set.append(neighbor)
                elif tentative_g >= neighbor.g:
                    continue

                neighbor.g = tentative_g
                neighbor.h = abs(neighbor.x - goal_node.x) + abs(neighbor.y - goal_node.y)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.parent = current

        return []  # No path found     
                
    def GetCharPosKey(self, x, y):
        value = next((i for i in PositionDict if PositionDict[i][:2] == [x, y]), None)
        print(value)
        return value

    def AssignCharVar(self):
        self.CharKey = self.GetCharPosKey(self.Sx, self.Sy)
        if self.CharKey:
            self.SelectedUnit = self.CharKey
            self.Lx = PositionDict[self.CharKey][0]
            self.Ly = PositionDict[self.CharKey][1]
            print(self.Lx, self.Ly)

    def MovLeft(self):
        self.Sx -= 1

    def MovRight(self):
        self.Sx += 1

    def MovUp(self):
        self.Sy -= 1

    def MovDown(self):
        self.Sy += 1

    def DrawMovDistance(self):
        self.mov_surface.fill((0, 0, 0, 0))
        self.reachable_tiles = self.get_reachable_nodes(self.Lx, self.Ly, self.Mov)
        for x, y in self.reachable_tiles:
            self.mov_surface.blit(self.MovTile, (x * TILESIZE, y * TILESIZE))
            
    def DrawAtkDistance(self):
        self.AtkRange = 1
        self.mov_surface.fill((0, 0, 0, 0))
        self.reachable_tiles = self.get_reachable_nodes(self.Lx, self.Ly, self.AtkRange)
        for x, y in self.reachable_tiles:
            self.mov_surface.blit(self.AtkTile, (x * TILESIZE, y * TILESIZE))

    def draw_menu(self): 
        selected = 0
        MenuOn = True
        while MenuOn:
            self.mov_surface.fill((0, 0, 0, 0))
            rect_x = 100
            rect_y = 100
            rect_width = 200
            rect_height = len(options) * 70
            rectangle = pygame.Rect(rect_x, rect_y, rect_width, rect_height)

            self.menurect = pygame.draw.rect(self.screen, MENU_BLUE, rectangle)
            for i, text in enumerate(options):
                color = BLUE if i == selected else WHITE
                label = self.font.render(text, True, color)
                self.screen.blit(label, (120, 120 + i * TILESIZE))

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    MenuOn = False
                    self.playing = False
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        print(f"Selected option: {options[selected]}")
                        MenuOn = False
                        return options[selected]
                        #Wait = Normal method rn
                        #Item = Open the stat menu for rn
                        #Attack should search if there is a unit in range, if there isnt then wait for right now 
                        
                        
                    elif event.key == pygame.K_ESCAPE:
                        MenuOn = False

    def ClearSurface(self):
        self.mov_surface.fill((0, 0, 0, 0))

    def IsTileOccupied(self, x, y, ignore_key=None):
        for key, value in PositionDict.items():
            if key != ignore_key and value[0] == x and value[1] == y:
                return True
        return False

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False

            if event.type == pygame.KEYDOWN:
                
                if self.Over and (self.Sx, self.Sy) in self.reachable_tiles:
                    self.current_path = self.astar_path((self.PrevLx, self.PrevLy), (self.Sx, self.Sy))
                    
                if event.key == pygame.K_LEFT:
                    if self.Over and (self.Sx - 1, self.Sy) in self.reachable_tiles:
                        self.MovLeft()
                    elif not self.Over and not self.attacking:
                        self.MovLeft()
                    elif self.attacking and (self.Sx - 1, self.Sy) in self.reachable_tiles:
                        self.MovLeft()

                elif event.key == pygame.K_RIGHT:
                    if self.Over and (self.Sx + 1, self.Sy) in self.reachable_tiles:
                        self.MovRight()
                    elif not self.Over and not self.attacking:
                        self.MovRight()
                    elif self.attacking and (self.Sx + 1, self.Sy) in self.reachable_tiles:
                        self.MovRight()

                elif event.key == pygame.K_UP:
                    if self.Over and (self.Sx, self.Sy - 1) in self.reachable_tiles:
                        self.MovUp()
                    elif not self.Over and not self.attacking:
                        self.MovUp()
                    elif self.attacking and (self.Sx, self.Sy - 1) in self.reachable_tiles:
                        self.MovUp()    

                elif event.key == pygame.K_DOWN:
                    if self.Over and (self.Sx, self.Sy + 1) in self.reachable_tiles:
                        self.MovDown()
                    elif not self.Over and not self.attacking:
                        self.MovDown()
                    elif self.attacking and (self.Sx, self.Sy + 1) in self.reachable_tiles:
                        self.MovDown()

                elif event.key == pygame.K_a:
                    print(self.current_path, self.Sx)
                    self.CharKey = self.GetCharPosKey(self.Sx, self.Sy)
                    if self.CharKey != None :
                        self.AssignCharVar()
                        self.Over = True
                        self.DrawMovDistance()
                        self.PrevLx = self.Lx
                        self.PrevLy = self.Ly
                    else:
                        self.mov_surface.fill((0, 0, 0, 0))
                        if (self.Sx, self.Sy) in self.reachable_tiles and self.current_path:
                            for x, y in self.current_path:
                                PositionDict[self.SelectedUnit][0] = x
                                PositionDict[self.SelectedUnit][1] = y
                                self.Sx, self.Sy = x, y
                                self.Lx, self.Ly = x, y
                                # Optional: delay here for animation
                            
                            
                            self.current_path = []
                            self.reachable_tiles = []
                            
                            
                        menu_result = self.draw_menu()
                        self.ClearSurface    
                        if menu_result == "Item":
                            self.StatScreen()
                            
                        elif menu_result == "Attack":
                            self.attacking = True
                            self.DrawAtkDistance()

                        elif menu_result == "Wait":
                            self.SelectedUnit = None
                            self.Over = False
                            self.ClearSurface()                                
                            

                elif event.key == pygame.K_s:
                    self.ClearSurface()
                    self.CharKey = self.GetCharPosKey(self.Sx, self.Sy)
                    if self.CharKey:
                        PositionDict[self.CharKey][0] = self.PrevLx
                        PositionDict[self.CharKey][1] = self.PrevLy
                        self.Over = False

                elif event.key == pygame.K_q:
                    self.draw_menu()

                elif event.key == pygame.K_w:
                    print(PositionDict)

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        surface.blit(textobj, (x, y))

    def StatScreen(self):
        statposX, statposY = 405, 105
        running = True
        while running:
            self.screen.fill((0, 211, 0))
            pygame.draw.rect(self.screen, (255, 255, 0), pygame.Rect(395, 95, 530, 410))
            pygame.draw.rect(self.screen, (96, 76, 225), pygame.Rect(400, 100, 520, 400))
            self.draw_text('Character Screen', self.font, (139, 0, 0), self.screen, 500, 20)

            with open("Stats.json", "r") as f:
                statsDict = json.load(f)

            for stat, value in statsDict["Lyn"]["char_stats"].items():
                self.draw_text(f"{stat}: {value}", self.font, (0, 0, 0), self.screen, statposX, statposY)
                statposY += 70
                if statposY >= 480:
                    statposY = 105
                    statposX = 625

            statposX, statposY = 405, 105
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                    self.draw_menu()

            self.screen.blit(self.LynFaceL, (30, 10))
            pygame.display.update()

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.blit(self.BACKGROUND, (0, 0))
        self.screen.blit(self.mov_surface, (0, 0))
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        for x, y in self.current_path:
            pygame.draw.rect(self.screen, (50, 150, 255), (x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE), 3)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
            self.new()
        self.running = False


# Main loop
g = Game()
g.new()
images = load_images("Assets")
while g.running:
    g.main()
pygame.quit()
