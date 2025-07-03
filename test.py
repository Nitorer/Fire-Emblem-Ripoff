import pygame
from Sprites import *
from Vars import * # type: ignore
import random
import math
import time
import json
import os 


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((960, 640))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("gba-fe-dialogue.ttf", 40)
        self.running = True
        self.playing = True

        self.mov_surface = pygame.Surface((960, 640), pygame.SRCALPHA)

        # Game state
        self.Sx, self.Sy = 5, 5
        self.Lx, self.Ly = 0, 0
        self.PrevLx, self.PrevLy = None, None
        self.CharKey = None
        self.Over = False
        self.Mov = 5

    def new(self):
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.selector = Selector(self, self.Sx, self.Sy)
        self.lyn = Lyn(self, PositionDict["Lyn"][0], PositionDict["Lyn"][1])
        self.brigand = Brigand(self, PositionDict["Brig"][0], PositionDict["Brig"][1])

    def GetCharPosKey(self, x, y):
        value = next((i for i in PositionDict if PositionDict[i][:2] == [x, y]), None)
        print(value)
        return value

    def AssignCharVar(self):
        self.CharKey = self.GetCharPosKey(self.Sx, self.Sy)
        if self.CharKey:
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

    def MoveLim(self, prev_ly, prev_lx, new_lx, new_ly):
        return abs(new_lx - prev_lx) + abs(new_ly - prev_ly) <= self.Mov

    def DrawMovDistance(self):
        self.mov_surface.fill((0, 0, 0, 0))
        for x in range(15):
            for y in range(10):
                if (abs(self.Sx - x) + abs(self.Sy - y)) <= self.Mov and not self.IsTileOccupied(x, y, self.CharKey):
                    self.mov_surface.blit(MovTile, (x * 64, y * 64))

    def draw_menu(self):
        selected = 0
        running = True
        while running:
            self.screen.fill(BLACK)
            for i, text in enumerate(options):
                color = BLUE if i == selected else WHITE
                label = self.font.render(text, True, color)
                self.screen.blit(label, (250, 150 + i * 50))

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        print(f"Selected option: {options[selected]}")
                        running = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False

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
                if event.key == pygame.K_LEFT:
                    if self.Over and self.MoveLim(self.PrevLy, self.PrevLx, self.Lx - 1, self.Ly) and not self.IsTileOccupied(self.Sx - 1, self.Sy, self.CharKey):
                        self.MovLeft()
                        PositionDict[self.CharKey][0] = self.Sx
                        self.Lx = self.Sx
                    elif not self.Over:
                        self.MovLeft()

                elif event.key == pygame.K_RIGHT:
                    if self.Over and self.MoveLim(self.PrevLy, self.PrevLx, self.Lx + 1, self.Ly) and not self.IsTileOccupied(self.Sx + 1, self.Sy, self.CharKey):
                        self.MovRight()
                        PositionDict[self.CharKey][0] = self.Sx
                        self.Lx = self.Sx
                    elif not self.Over:
                        self.MovRight()

                elif event.key == pygame.K_UP:
                    if self.Over and self.MoveLim(self.PrevLy, self.PrevLx, self.Lx, self.Ly - 1) and not self.IsTileOccupied(self.Sx, self.Sy - 1, self.CharKey):
                        self.MovUp()
                        PositionDict[self.CharKey][1] = self.Sy
                        self.Ly = self.Sy
                    elif not self.Over:
                        self.MovUp()

                elif event.key == pygame.K_DOWN:
                    if self.Over and self.MoveLim(self.PrevLy, self.PrevLx, self.Lx, self.Ly + 1) and not self.IsTileOccupied(self.Sx, self.Sy + 1, self.CharKey):
                        self.MovDown()
                        PositionDict[self.CharKey][1] = self.Sy
                        self.Ly = self.Sy
                    elif not self.Over:
                        self.MovDown()

                elif event.key == pygame.K_a:
                    self.CharKey = self.GetCharPosKey(self.Sx, self.Sy)
                    if self.CharKey:
                        self.AssignCharVar()
                        self.Over = not self.Over
                        self.DrawMovDistance()
                        PositionDict[self.CharKey][2] = False
                        self.PrevLx = self.Lx
                        self.PrevLy = self.Ly
                        if self.Over == False:
                            self.ClearSurface()

                elif event.key == pygame.K_s:
                    self.ClearSurface()
                    self.CharKey = self.GetCharPosKey(self.Sx, self.Sy)
                    if self.CharKey:
                        PositionDict[self.CharKey][0] = self.PrevLx
                        PositionDict[self.CharKey][1] = self.PrevLy
                        PositionDict[self.CharKey][2] = False
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

            self.screen.blit(LynFaceL, (30, 10))
            pygame.display.update()

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.blit(BACKGROUND, (0, 0))
        self.screen.blit(self.mov_surface, (0, 0))
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
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
while g.running:
    g.main()
pygame.quit()
