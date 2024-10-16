# importing modules needed for the program
import pygame
from tkinter import Tk, messagebox
from Basket import basket
from Egg import egg
from Chicken import chicken
import random

Tk().withdraw()

startgame = False

# initializing the surface
pygame.init()
pygame.display.set_caption('Egg Catcher')
pygame.mouse.set_visible(False)
surface = pygame.display.set_mode((500, 750))

pygame.mixer.init()
pygame.mixer.music.load('GetawayCar.wav')
pygame.mixer.music.set_volume(0.3)

eggcatchsound = pygame.mixer.Sound('drop.wav')
eggbreaksound = pygame.mixer.Sound('splash.wav')

# basket will move if you hold down on the key
pygame.key.set_repeat(20)

# setting up the four chickens
c1 = chicken()
c1.set_location((50, 100))
c2 = chicken()
c2.set_location((160, 100))
c3 = chicken()
c3.set_location((270, 100))
c4 = chicken()
c4.set_location((380, 100))

# randomly deciding the speed at which the eggs will fall at
eggspeed = 2

# placing the eggs in a list to randomly choose which of them will be falling from the chicken
chicken_locations = ((50 + c1.get_width() // 2 - 20, 130), (160 + c2.get_width() // 2 - 20, 130), (270 + c3.get_width() // 2 - 20, 130), (380 + c4.get_width() // 2 - 20, 130))

egglist = []

# setting up the basket
b = basket()
b.set_x(surface.get_width() // 2)
b.set_y(550)

# setting the inital score, level and health that would either go up or down
score, level, health = 0, 0, 150

start_font = pygame.font.Font("neuropol.ttf", 24)
game_font = pygame.font.Font("neuropol.ttf", 18)

# setting up the words written on the surface - how to start, the score, level and health
start_output = start_font.render("HIT SPACE TO START", True, pygame.Color("#1c2e18"))
score_output = game_font.render("{:<10s}{:<5d}".format("SCORE:", score), True, pygame.Color("green"))
level_output = game_font.render("{:<10s}{:<5d}".format("LEVEL:", level), True, pygame.Color("green"))
health_output = game_font.render("HEALTH", True, pygame.Color("green"))

# loading the background
imgBackground = pygame.image.load('images/bg_bamboo.png')

# Timer for egg falling
eggfall = 20
pygame.time.set_timer(pygame.USEREVENT, 0)

# sets the screen for the game - if running is false the game is over
running = True
while running == True:
    for event in pygame.event.get():
        # if the user presses the exit button
        if event.type == pygame.QUIT:
            pygame.mixer.music.pause()
            # confirms if the user wants to quit
            choice = messagebox.askyesno('Exit', 'Are you sure you want to exit?')
            # if the choice is yes the portal and messagebox will close
            if choice == True:
                pygame.time.set_timer(pygame.USEREVENT, 0)
                running = False
            else:
                pygame.mixer.music.unpause()

        # What to do if the health level reaces 0
        if health <= 0:
            # startgame = False   
            # stop the game timer and music then ask if the user wants to play again      
            pygame.time.set_timer(pygame.USEREVENT, 0)   
            pygame.mixer.music.stop()
            replay = messagebox.askyesno('Egg Catcher', 'GAME OVER \nYou finished with ' + str(score) + ' points.\nWould you like to play again?')
            # if the user doesn't want to play again the potal will close
            if replay == False:
                running = False
            # if the user wants to play again the variables will be reset
            else:
                startgame = False
                score, level, health = 0, 0, 150
                running = True
                newegg = 3500
                egglist = []

        if startgame == True:
            # this will be producing eggs at the random chicken locations
            if event.type == pygame.USEREVENT + 1:
                anegg = egg()
                anegg.set_location(chicken_locations[random.randint(0, 3)])
                # this will randomly set the speed of the eggs falling (chnages the ypixels)
                anegg.set_yspeed(random.randint(2, 4))
                # egg gets added to an on going list so that it can be removed when needed
                egglist.append(anegg)
                
        # what to do when the space key is presssed to start the game
        if event.type == pygame.KEYDOWN:
            if startgame == False:
                if event.key == pygame.K_SPACE:
                    # the game will begin
                    startgame = True 
                    # the music will play
                    pygame.mixer.music.play(-1)
                    # the eggs will start to fall every few seconds as set by the variable newegg
                    newegg = 3500
                    pygame.time.set_timer(pygame.USEREVENT, eggfall)
                    pygame.time.set_timer(pygame.USEREVENT + 1, newegg)
            elif startgame == True:
                # keys to move the basket - the d or right key will move the basket right
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    b.movex(5)
                    # ensures the basket remains on the screen
                    if b.get_x() + b.get_width() > surface.get_width():
                        b.set_x(surface.get_width() - b.get_width())
                # the k or left key will move the basket left
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    b.movex(-5)
                    # ensures the basket remains on the screen
                    if b.get_x() < 0:
                        b.set_x(0)
        
        if startgame == True:            
            if event.type == pygame.USEREVENT:
                # takes egg from egglist and moves it
                for x in egglist:
                    x.move()

                    # checks to see if the egg and basket collide
                    if x.get_rectangle().colliderect(b.get_rectangle()) == True:
                        pygame.time.set_timer(pygame.USEREVENT, 0)
                        # if they collide the sound effect will play
                        eggcatchsound.play()
                        # the score will increase by 10 if the egg is catched
                        score += 10
                        # the egg will be removed from the list and will be regenerated with the anegg variable above
                        egglist.remove(x)

                        # what to do if the score reaches every 100th interval
                        if score > 1:
                            # if the score is divisible by 100 the level will increase by 1 each time 
                            if score % 100 == 0:
                                level += 1
                                # the speed of the new egg producing will be faster
                                newegg -= 500
                                # if the speed of eggs producing equals 500 that speed will remain constant
                                if newegg <= 500:
                                    newegg = 500

                    else:
                        # if the egg reaches the ground it will crack
                        if x.get_y() > 550 and x.get_cracked() == False:
                            x.cracked()
                            # the egg cracking sound will play
                            eggbreaksound.play()
                            # health will decrease by 15
                            health -= 15
                        else:
                            # when egg raches the bottom the speed will slow down
                            eggfall = 100
                            pygame.time.set_timer(pygame.USEREVENT, eggfall)

                    # the egg will disaper once reaching the y position of 570     
                    if x.get_y() >= 570:
                        egglist.remove(x)

    # outputting the background
    surface.blit(imgBackground, (0, 0))
    
    # outputting the chosen egg
    if startgame == True:
        for x in egglist:
            surface.blit(x.get_image(), x.get_location())
        # what to do when the egg reaches 550(the ground of the picture)

    # outputting the basket
    surface.blit(b.get_image(), b.get_location())

    # if the game hasnt begun yet the starting output is there
    if startgame == False:
        surface.blit(start_output, (surface.get_width() // 2 - start_output.get_width() // 2, surface.get_height() // 2))

    # inputting the score, level and health output
    score_output = game_font.render("{:<10s}{:<5d}".format("SCORE:", score), True, pygame.Color("green"))
    surface.blit(score_output, (20, surface.get_height() - 130))
    level_output = game_font.render("{:<10s}{:<5d}".format("LEVEL:", level), True, pygame.Color("green"))
    surface.blit(level_output, (surface.get_width() - level_output.get_width(), surface.get_height() - 130))
    surface.blit(health_output, (surface.get_width() // 2 - health_output.get_width() // 2, surface.get_height() - 80))

    # output for the health which is a rectangle that decreases in width when health goes down
    pygame.draw.rect(surface, pygame.Color('#009600'), (surface.get_width() // 2 - 150 // 2, surface.get_height() - 50, 150, 20), 0)
    pygame.draw.rect(surface, pygame.Color('green'), (surface.get_width() // 2 - 150 // 2, surface.get_height() - 50, health, 20), 0)

    # outputting the chickens
    surface.blit(c1.get_image(), c1.get_location())
    surface.blit(c2.get_image(), c2.get_location())
    surface.blit(c3.get_image(), c3.get_location())
    surface.blit(c4.get_image(), c4.get_location())

    pygame.display.update()


    # game restarting