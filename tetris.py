import pygame
from pygame.locals import *
from tiles import *
import colors
from random import randint, seed
import math

pygame.init()

#VARS
WIDTH, HEIGHT = 400,800
SCALE = 40
WIDTHSCL = int(WIDTH / SCALE)
HEIGHTSCL = int(HEIGHT/  SCALE)

window = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

grid = [[0 for h in range(WIDTHSCL)] for w in range(HEIGHTSCL)]

SPEED_MUTLIPLICATOR = .25
LEVEL = 1
TILE_SPEED = 0.04
TileX = 4
TileY = -2
TileRotation = 0

TileID = randint(0, len(pieces) - 1)
CurrentTile = pieces[TileID][0]
CurrentName = Names[TileID + 1]

colors.SetUp(Names)

GameEnded = False
#FUNCTIONS
def GetColor(h,w):
	return (255,255,255) if grid[h][w] is 0 else colors.GetColor(Names[grid[h][w] - 1])

def GetTileColor(state):
	return (255,255,255) if state is 0 else colors.GetColor(CurrentName)


def DrawGrid():
	for h in range(HEIGHTSCL):
		for w in range(WIDTHSCL):
			pygame.draw.rect(window, GetColor(h,w), (w * SCALE, h * SCALE, SCALE - 1, SCALE - 1))

#GRID IS COMING FROM (0,0) TO (19,9)
def IsOnGrid(h,w):
	if h >= 0 and h < HEIGHTSCL and w >= 0 and w < WIDTHSCL:
		return True

	return False

def MovePiece(deltaTime):
	global TileY
	TileY += (TILE_SPEED * deltaTime + (SPEED_MUTLIPLICATOR * math.floor(LEVEL))) / SCALE

def DrawPiece():
	for w in range(4):
		for h in range(4):
			if CurrentTile[h][w] is 1:
				pygame.draw.rect(window, GetTileColor(CurrentTile[h][w]),
								((TileX + w) * SCALE,int(TileY + h) * SCALE,
								SCALE - 1, SCALE - 1))
def CanMove(direction):
	for w in range(4):
		for h in range(4):
			if CurrentTile[h][w] is 1:
				if (not IsOnGrid(int(TileY), TileX + w + direction)
					or not grid[int(TileY) + h][TileX + w + direction] is 0):
					return False
	return True

#ROTATE THE PIECE
def Rotate():
	global TileRotation, CurrentTile
	NextTile = pieces[TileID][(TileRotation + 1) % 4]
	for h in range(4):
		for w in range(4):
			if NextTile[h][w] is 1:
				if not IsOnGrid(int(TileY) + h, TileX + w):
					return False

	CurrentTile = NextTile
	TileRotation = (TileRotation + 1) % 4

#CHECK IF THE PIECE IS ON THE LAST LINE OR ON ANOTHER PIECE
def CheckEndGrid():
	for h in range(3, -1, -1):
		for w in range(4):
			if CurrentTile[h][w] is 1:
				if math.ceil(TileY) + h is 21 or (not grid[math.ceil(TileY) + h - 1][TileX + w] is 0):
					AddPieceToGrid()
					CheckLine()
					return

def AddPieceToGrid():
	global grid, TileY, TileX
	TileY -= 1
	for w in range(4):
		for h in range(4):
			if CurrentTile[h][w] is 1:
					grid[int(TileY) + h][TileX + w] = TileID + 1

	if math.floor(TileY) <= 0:
		EndGame()
	else:
		NewPiece()

#CHECK IF A LINE IS COMPLETE
def CheckLine():
	global LEVEL
	for h in range(HEIGHTSCL - 1, 0, -1):
		sum = 0

		for w in range(WIDTHSCL):
			if grid[h][w] is not 0:
				sum += 1

		if sum == 10:
			LEVEL += 0.1
			for w in range(WIDTHSCL):
				for H in range(h, 0, -1):
					grid[H][w] = grid[H - 1][w]
					grid[H - 1][w] = 0
			CheckLine()

def NewPiece():
	global CurrentTile, TileY, TileX, TileRotation, TileID, CurrentName
	seed(TileX + TileY + TileID)
	TileID = randint(0, len(pieces) - 1)
	CurrentTile = pieces[TileID][0]
	CurrentName = Names[TileID]
	TileRotation = 0
	TileX = 4
	TileY = -1

#CHECK IF THE PIECE IS HIGHER THAN THE GRID AND END THE GAME
def EndGame():
	global GameEnded
	GameEnded = True
	print("Game Finished")
	DrawGrid()

while True:
	deltaTime = clock.tick(60)
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			quit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT and CanMove(1):
				TileX += 1
			if event.key == pygame.K_LEFT and CanMove(-1):
				TileX -= 1
			if event.key == pygame.K_DOWN:
				TILE_SPEED = TILE_SPEED * 10
			if event.key == pygame.K_UP:
				Rotate()

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_DOWN:
				TILE_SPEED = TILE_SPEED / 10
	if not GameEnded:
		DrawGrid()

		MovePiece(deltaTime)
		CheckEndGrid()
		DrawPiece()

	pygame.display.update()