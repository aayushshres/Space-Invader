import pygame
import random
import math
from pygame import mixer


pygame.init()
screen = pygame.display.set_mode((800, 600))

#Background
background = pygame.image.load("Images/background.jpg")

#Sound
mixer.music.load("Sound/background.wav")
mixer.music.play(-1)

#Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('Images/logo.png')
pygame.display.set_icon(icon)

#Player
playerImg = pygame.image.load('Images/spaceship.png')
#Player Coordinates
playerX = 370
playerY = 480
#Player Movements
playerX_change = 0

# Enemy
enemyImg = []
#Enemy Coordinates
enemyX = []
enemyY = []
#Enemy Movements
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('Images/ufo.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

#Bullet
bulletImg = pygame.image.load('Images/bullet.png')
#Bullet Coordinates
bulletX = 0
bulletY = 480
#Bullet Movements
bulletX_change = 0
bulletY_change = 10
bullet_state = False

#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

#Score Function
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

#Game-over Function
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

#Player Function
def player(x, y):
    screen.blit(playerImg, (x, y))

#Enemy Function
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

#Bullet Function
def fire_bullet(x, y):
    global bullet_state
    bullet_state = True
    screen.blit(bulletImg, (x + 16, y + 10))

#Collision Function
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


#Main Game Loop
running = True
while running:

    screen.fill((0, 0, 0)) #RGB
    #Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():

        #Quit Program
        if event.type == pygame.QUIT:
            running = False

        #Keyboard Binding
        if event.type == pygame.KEYDOWN:
            #Move Left
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            #Move Right
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            #Fire Bullet
            if event.key == pygame.K_SPACE:
                if bullet_state is False:
                    bulletSound = mixer.Sound("Sound/laser.wav")
                    bulletSound.play()

                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


    #Setting Player Boundry
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    #Enemy Movement
    for i in range(num_of_enemies):

        #Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]

        #Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("Sound/explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = False
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    #Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = False

    if bullet_state is True:
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()