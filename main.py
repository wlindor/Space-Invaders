import pygame
import random
import math

from pygame import mixer
# Initializing pygame
pygame.init()

# Creating the dimensions of the screen
screen = pygame.display.set_mode((910, 516))

# Background
background = pygame.image.load('space.jpg')

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)


# Player
playerImg = pygame.image.load('player.png')
playerX = 450
playerY = 475
playerX_position = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_position = []
enemyY_position = []
number_of_enemies = 6
for i in range(number_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(70, 850))
    enemyY.append(random.randint(75, 125))
    enemyX_position.append(3.25)
    enemyY_position.append(10)

# Weapon

# Ready: Bullet is not visible on the screen
# Fire: The bullet is moving
weaponimg = pygame.image.load('bullet.png')
weaponX = 0
weaponY = 475
weaponX_position = 0
weaponY_position = 10
weapon_state = "ready"

# Score
score_points = 0
font = pygame.font.Font('freesansbold.ttf', 34)
textX = 10
textY = 10

# Game over Text

game_over_font = pygame.font.Font('freesansbold.ttf', 64)




def show_score(x, y):
    score = font.render("Score : " + str(score_points), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    game_over_text = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (450, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fireWeapon(x, y):
    global weapon_state
    weapon_state = "fire"
    screen.blit(weaponimg, (x, y))


def collision(enemyX, enemyY, weaponX, weaponY):
    distance = math.sqrt((math.pow(enemyX - weaponX, 2)) + (math.pow(enemyY - weaponY, 2)))
    if distance < 27:
        return True
    return False


# Game Loop
running = True
while running:
    # Colors for screen based off of Red, Green, Blue
    # Limit is 255
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_position += 5
            if event.key == pygame.K_LEFT:
                playerX_position -= 5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                playerX_position = 0
            if event.key == pygame.K_LEFT:
                playerX_position = 0
            if event.key == pygame.K_SPACE:
                if weapon_state == 'ready':
                    # sound from mixer
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    weaponX = playerX
                    fireWeapon(weaponX, weaponY)

    playerX += playerX_position

    if playerX <= 0:
        playerX = 0
    elif playerX >= 878:
        playerX = 878

    # Enemy movement
    for i in range(number_of_enemies):
        # Game over
        if enemyY[i] > 880:
            for j in range(number_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_position[i]

        if enemyX[i] <= 0:
            enemyX_position[i] = 3.25
            enemyY[i] += 20
        elif enemyX[i] >= 878:
            enemyY[i] += 20
            enemyX_position[i] = -3.25
        # Collision
        isCollision = collision(enemyX[i], enemyY[i], weaponX, weaponY)
        if isCollision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            weaponY = 475
            weapon_state = "ready"
            score_points += 100
            enemyX[i] = random.randint(40, 875)
            enemyY[i] = random.randint(33, 125)
        enemy(enemyX[i], enemyY[i], i)
    # Weapon movement
    if weaponY <= 0:
        weaponY = 475
        weapon_state = "ready"
    if weapon_state == "fire":
        fireWeapon(weaponX, weaponY)
        weaponY -= weaponY_position

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
