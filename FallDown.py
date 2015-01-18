"""Author: Peter ChenBin Xu
Description: This is a game program that is single player. The game begins with a ball. The ball is controlled by arrow keys and will accelerate to the left or right depending on what direction you pressed. There will be platforms that will rise up and you must make the ball fall through the gaps so you won't touch the top of the screen. The game will get more difficult as you survive longer.
Date: May 28, 2013"""

# IMPORT AND INITIALIZE
import pygame, FallSprites, random
pygame.init()
pygame.mixer.init()

def make_platform(row,colour):
    """This function creates a giant platform using many platform sprites. It takes row and colour as parameters and returns a list of sprites."""
    
    #Display
    screen = pygame.display.set_mode((640, 480))
    
    #Creates the empty lists and variables
    platforms = []
    space = []
    col = 0
    gaps = random.randint(1,3)
    
    #Creates a list made up of 1s and 0s
    for number in range(10-gaps):
        space.append(1)
    for number in range(gaps):
        space.append(0)
        
    #Randomize the list to make it unique
    random.shuffle(space)
    
    #Make a platform for the 1s in the space list while a gap for the 0s
    for number in space:
        if number == 1:
            platforms.append(FallSprites.Platform(screen, row,col, colour ))
            col += 64
        elif number == 0:
            col += 64 
            
    return platforms  

def menu():
    """This is the screen that gives the user instructions on how to play the game.It receives no parameters. The function will return a boolean variable."""
    
    #Display
    screen = pygame.display.set_mode((640, 480))
    
    #Entities-Creating the background, fonts, labels respectively
    background = pygame.Surface((640,480))
    background = background.convert()
    background.fill((255, 255, 255))
    
    Font1 = pygame.font.SysFont("Arial", 60)
    Font2 = pygame.font.SysFont("TimesNewRoman", 20)
    
    title = Font1.render("Instructions", 1, (0, 0, 255))
    instructions1 = Font2.render("Welcome to Fall Down!", 1, (0,255,0))
    instructions2 = Font2.render("Move the ball by constantly tapping the LEFT and RIGHT arrow keys.", 1, (255,165,0))
    instructions3 = Font2.render("The goal of the game is to keep FALLING!", 1, (255,255,0))
    instructions4 = Font2.render("The game will get harder as you survive longer!", 1, (255,0,0))
    start = Font1. render("Press SPACE to start!", 1, (238,130,238))
    
    #Action
    #Assign
    clock = pygame.time.Clock()
    keepGoing = True
    
    #Loop
    while keepGoing:
        
        #Timer
        clock.tick(30)
        
        #Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                else: 
                    return False 
                
        #Refresh display
        screen.blit(background, (0,0))
        screen.blit(title, (190, 20))
        screen.blit(instructions1,(220,110))
        screen.blit(instructions2,(50,160))
        screen.blit(instructions3,(150,210))
        screen.blit(instructions4,(120,260))
        screen.blit(start, (80, 400))
        
        pygame.display.flip()
        
    #Exit the game window
    pygame.quit()
    
def main():
    """This is the mainline logic of our falldown game. """
    
    #Display
    pygame.display.set_caption("~Fall Down~")
    
    menu()
    game()

        
def game():
    """This is the game loop of the program. It accepts no parameters and returns nothing."""
    
    #Display
    screen = pygame.display.set_mode((640, 480))
    
    # ENTITIES
    Font = pygame.font.SysFont("Arial", 60)
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    
    #This loads and plays the music in the background
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play(-1)
    
    #These are effects sounds
    win_sound = pygame.mixer.Sound("win.wav")
    win_sound.set_volume(0.7)
    
  
    
    #Two sprite groups are made for platforms and distractions
    platformGroup = pygame.sprite.Group()
    distractionGroup = pygame.sprite.Group()
    
    #Sprites for: Background, Ball, Endzone, and Scorekeeper
    game_background = FallSprites.Background()
    ball = FallSprites.Ball(screen)
    endzone = FallSprites.Endzone(screen, 0)
    scorekeeper = FallSprites.ScoreKeeper()    
    
    #An ordered update group is made 
    allSprites = pygame.sprite.OrderedUpdates(game_background,platformGroup, ball, endzone,scorekeeper,distractionGroup)
    
    # ASSIGN-key variables/lists
    level = 0
    timer = 0
    final_score = 0
    clock = pygame.time.Clock()
    keepGoing = True
    distraction_numbers=[1]
    colour = [(0,0,225),(0,225,0),(255,165,0),(255,255,0),(255,0,0),(238,130,238)]
 
    # Hide the mouse pointer
    pygame.mouse.set_visible(False)
 
    # LOOP
    while keepGoing:
        #TIME
        clock.tick(30)
        
        #Event handling
        
        #Increase the score by a fixed rate every "tick" and records it
        scorekeeper.update_score()
        final_score = scorekeeper.return_score()
        
        #This keeps track of how long the game has gone on in milliseconds and resets every 1000 milliseconds.
        timer += clock.get_time()
        if timer > 1000:
            timer=0
            
            #A giant platform is created and allSprites is redefined
            platformGroup.add(make_platform(480,colour[level]))
            allSprites = pygame.sprite.OrderedUpdates(game_background,platformGroup, ball, endzone,scorekeeper,distractionGroup)
    
        #This creates a distraction when the numbers in the list match the random number, allSprites are redefined
        for number in distraction_numbers:
            if number == random.randint(1, 500):
                distractionGroup.add(FallSprites.Distraction(screen,480))
                allSprites = pygame.sprite.OrderedUpdates(game_background,platformGroup, ball, endzone,scorekeeper,distractionGroup)
        
        #Every time the player gets 500 points, the diffuculty will increase
        if scorekeeper.return_score() >= 500*level:
            level += 1 
            
            #Having more numbers in the distraction_numbers list will increase chances of distractions appearing
            distraction_numbers.append((len(distraction_numbers)+1))
            
            ball.lose_agility()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            #Move the ball left and right depending on arrow keys
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    ball.accel(1)
                elif event.key == pygame.K_LEFT:
                    ball.accel(2)
                #This makes controling the ball smoother by altering direction when key is lift up
            elif event.type ==pygame.KEYUP: 
                    ball.accel(0)
                
        #When the ball hits a playform it will move up with the same speed as the platform
        if pygame.sprite.spritecollide(ball, platformGroup, False):
            for platform_hit in pygame.sprite.spritecollide(ball, platformGroup,False):    
                
                #Uses the height of the platform to get position and prevent "merging together" 
                ball.caught(2, platform_hit.get_x())
        else: 
            #Ball falls when not in contact with platform
            ball.free()
            
        #When the ball touches the endzone at the top of the screen the game ends and his final score will be displayed
        if ball.rect.colliderect(endzone.rect):
            keepGoing = False
            
        
        # REFRESH SCREEN
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)       
        pygame.display.flip()
    
    # Unhide the mouse pointer
    pygame.mouse.set_visible(True)
 
    # Display the score
    win_sound.play()
    end_screen(final_score)
    pygame.time.delay(1500)
    pygame.quit()
    

def end_screen(score):
    """This is the screen that gives the user instructions on how to play the game.It accepts score as a parameter. The function will return nothing."""
    
    #Display
    screen = pygame.display.set_mode((640, 480))
    
    #Entities- Creating the background, fonts, labels respectively
    background = pygame.Surface((640,480))
    background = background.convert()
    background.fill((255, 255, 255))
    
    score= score
    
    Font = pygame.font.SysFont("TimesNewRoman", 20)
    
    final_score = Font.render("Final Score:%i" %score , 1, (0, 0, 255))
    
    #Action
    #Assign
    clock = pygame.time.Clock()
    keepGoing = True
    
    #Loop
    while keepGoing:
        
        #Timer
        clock.tick(30)
        
        #Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                
        #Refresh display
        screen.blit(background, (0,0))
        screen.blit(final_score, (250, 20))
        
        pygame.display.flip()
        
    #Close the game window
    pygame.time.delay(2000)
    pygame.quit()
    
main()
    