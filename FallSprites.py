"""Author: Peter ChenBin Xu
Description: This is the module for the game "Fall Down". There are five sprites in this module. 
Date: May 8, 2013"""
import pygame, math, random

class Background(pygame.sprite.Sprite):
    """This is the sprite for my background image, so there is no image "bleed" on the normal background.(This will always be updated)"""
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("background.jpg")
        self.image = pygame.transform.scale(self.image,(640,480))
        self.image = self.image.convert()
        self.rect = self.image.get_rect()

class Platform(pygame.sprite.Sprite):
    """This class defines a platform sprite for our game. The purpose of this sprite is to interact with the ball sprite to allow the player to lose."""
    def __init__(self, screen,row, col, colour):
        """This method sets the image and reft attributes for the playform and initialized the instance variables."""
        
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Define the image attributes for the platforms 
        self.image = pygame.Surface((64, 10))
        self.image = self.image.convert()
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        
        #Controls the virtical direction of the platform and sets instance variable to keep track of the screen
        self.__dy = 2
        self.__screen = screen 
        
        self.rect.topleft = (col,row)
        
    def update(self):
        self.rect.top -=self.__dy
        if self.rect.top <= 0:
            self = self.kill         

    def get_x(self):
        self.rect.top = self.rect.top
        return self.rect.top
    
class Ball(pygame.sprite.Sprite):
    """This class defines a ball sprite for our game. The purpose of this sprite is to interact with the ball sprite to allow the player to lose."""
    
    def __init__(self, screen):
        '''This initializer takes a screen surface as a parameter, initializes
        the image and rect attributes, and x,y direction of the ball.'''
        
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        # Set the image and rect attributes for the Ball
        self.image = pygame.Surface((20,20))
        self.image.fill((0,0,0))
        self.image.set_colorkey((0,0,0))
        pygame.draw.circle(self.image, (0, 0, 255), (10, 10), 10, 0)
        
        self.image.set_colorkey((0,0,0))
        self.image = self.image.convert()
        
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width()/2,screen.get_height()/2)
 
        # Instance variables to keep track of the screen surface
        self.__screen = screen
        # and set the initial x and y vector for the ball.
        self.__dx = 0
        self.__dy = 10
        #These instance variables help track acceleration
        self.__dx_change = 0
        self.__max_speed = 10
        
    def update(self):
        
        #Updates the ball to move
        self.rect.bottom += self.__dy
        self.rect.left += self.__dx
        
        #updates rate of acceleration
        self.__dx += self.__dx_change
        
        #This makes sure the player doesn't go beyond the screen - bottom, right, and left
        if self.rect.bottom >480:
            self.rect.bottom = 480
        if self.rect.right > 640:
            self.rect.right = 640        
        if self.rect.left <0:
            self.rect.left = 0
                       
        #limits how fast it can go
        if self.__dx >= self.__max_speed:
            self.__dx = self.__max_speed
        elif self.__dx <= -self.__max_speed:
            self.__dx = -self.__max_speed
        
        #slows the ball down when no button is pressed
        if self.__dx != 0:
            self.__dx = self.__dx * 0.98
               
    def caught(self, speed, rect):
        """This is called when it is on top of a platform"""
        self.rect.bottom = rect+1
        self.__dy = -2
        
    def free(self):
        """This is called when it is below a platform"""
        self.__dy = 10
        
    def accel(self, direction):
        """This function changes the rate of acceleration depending on what button is pressed."""
        
        if direction==1:
            self.__dx_change = 2
        elif direction ==2:
            self.__dx_change -= 2
        elif direction == 0:
            if self.__dx_change > 0:
                self.__dx_change -= 2
            if self.__dx_change < 0:
                self.__dx_change += 2
                
    def lose_agility(self):
        """This functions reduced the max speed the ball can go"""
        
        self.__max_speed *=0.82
        
            
class Endzone(pygame.sprite.Sprite):
    """This is a class that is made for detecting when the ball hits the top of the screen"""
    
    def __init__(self, screen, position):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = pygame.Surface((self.screen.get_width(), 1))
        self.image = self.image.convert()
        self.image.fill((0,0,0))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.bottom = position
    
class Distraction(pygame.sprite.Sprite):
    """This class is sprites are there to distract the user"""
    
    def __init__(self, screen, position):
        pygame.sprite.Sprite.__init__(self)
        self.__screen = screen
        self.image = pygame.image.load("Paddle.png")
        self.image = pygame.transform.scale(self.image, (170,10))
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(1,640),position)
        self.__dy = 3
        self.__dx = 1
        
    def update(self):
        # Check if we have reached the left or right end of the screen.
        # If not, then keep moving the ball in the same x direction.
        self.rect.top -=self.__dy
        
        if ((self.rect.left > 0) and (self.__dx < 0)) or\
           ((self.rect.right < self.__screen.get_width()) and (self.__dx > 0)):
            self.rect.left += self.__dx
        # If yes, then reverse the x direction. 
        else:
            self.__dx = -self.__dx
             
        # Check if we have reached the top or bottom of the court.
        # If not, then keep moving the ball in the same y direction.
        if ((self.rect.top > 0) and (self.__dy > 0)) or\
           ((self.rect.bottom < self.__screen.get_height()) and (self.__dy < 0)):
            self= self.kill
            
class ScoreKeeper(pygame.sprite.Sprite):
    '''This class defines a label sprite to display the score.'''
    
    def __init__(self):
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        # Load our custom font, and initialize the starting score.
        self.__font = pygame.font.Font("Hawaii_Killer.ttf", 20)
        self.__score = 0
     
    def update(self):
        '''This method will be called automatically to display 
        the current score at the top of the game window.'''
        
        message = "Score: %d" % (self.__score)
        self.image = self.__font.render(message, 1, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (50, 20)
        
    def update_score(self):
        """This method adds to the score every time it is called"""
        
        self.__score += 0.7
        
    def return_score(self):
        """This method returns the score"""
        
        return self.__score