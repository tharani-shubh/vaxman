import pygame
import random
import time
from pygame.display import update


screen = pygame.display.set_mode([500, 500])

black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)
red = (255,0,0)
purple = (255,0,255)
yellow = (255,255,0)



class Wall(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self,x,y,width,height, color):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
  
        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
  
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x

def setupRoomOne(all_sprites_list):
    # Make the walls. (x_pos, y_pos, width, height)
    wall_list=pygame.sprite.RenderPlain()
     
    # This is a list of walls. Each is in the form [x, y, width, height]
    walls = [ [0,0,6,600],
              [0,0,600,6],
              [0,600,606,6],
              [600,0,6,606],
              [300,0,6,66],
              [60,60,186,6],
              [360,60,186,6],
              [60,120,66,6],
              [60,120,6,126],
              [180,120,246,6],
              [300,120,6,66],
              [480,120,66,6],
              [540,120,6,126],
              [180,180,63,6],
              [120,180,6,126],
              [360,180,63,6],
              [480,180,6,126],
              [180,240,6,126],
              [180,360,246,6],
              [420,240,6,126],
              [240,240,42,6],
              [324,240,42,6],
              [240,240,6,66],
              [240,300,126,6],
              [360,240,6,66],
              [0,300,66,6],
              [540,300,66,6],
              [60,360,66,6],
              [60,360,6,186],
              [480,360,66,6],
              [540,360,6,186],
              [120,420,366,6],
              [120,420,6,66],
              [480,420,6,66],
              [180,480,246,6],
              [300,480,6,66],
              [120,540,126,6],
              [360,540,126,6]
            ]
     
    # Loop through the list. Create the wall, add it to the list
    for item in walls:
        wall=Wall(item[0],item[1],item[2],item[3],blue)
        wall_list.add(wall)
        all_sprites_list.add(wall)
         
    # return our new list
    return wall_list

class Block(pygame.sprite.Sprite):
     
    # Constructor. Pass in the color of the block, 
    # and its x and y position
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(white)
        self.image.set_colorkey(white)
        pygame.draw.ellipse(self.image,color,[0,0,width,height])
 
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values 
        # of rect.x and rect.y
        self.rect = self.image.get_rect() 

pygame.init()

# Create an 606x606 sized screen
screen = pygame.display.set_mode([606, 606])

# Set the title of the window
pygame.display.set_caption('Pacman')

# Create a surface we can draw on
background = pygame.Surface(screen.get_size())

# Used for converting color maps and such
background = background.convert()
  
# Fill the screen with a black background
background.fill(black)

#Initalizig the icon
manimg = pygame.image.load('man.png')

pygame.display.set_icon(manimg)

x_man = 303-16
y_man = (7*60)+19
y_virus1 = (3*60)+19
y_virus2 = (1*60)+19
x_bact1 = 16
x_bact2 = 606-16-32


clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 24)

start_time = time.perf_counter_ns()

class Player(pygame.sprite.Sprite):
    change_x=0
    change_y=0
  
    # Constructor function
    def __init__(self,x,y, filename):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
   
        # Set height, width
        self.image = pygame.image.load(filename).convert()
  
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        
    
    # Change the speed of the player
    def changespeed(self,x,y):
        self.change_x=x
        self.change_y=y
          
    # Find a new position for the player
    def update(self,walls):
        # Get the old position, in case we need to go back to it
        
        old_x=self.rect.left
        new_x=old_x+self.change_x
        
        self.rect.left = new_x
        
        old_y=self.rect.top
        new_y=old_y+self.change_y
        

        # Did this update cause us to hit a wall?
        x_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_collide:
            # Whoops, hit a wall. Go back to the old position
            self.rect.left=old_x
            
        else:

            self.rect.top = new_y

            # Did this update cause us to hit a wall?
            y_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_collide:
                # Whoops, hit a wall. Go back to the old position
                self.rect.top=old_y
                

class Virus(pygame.sprite.Sprite):

    def __init__(self,x,y, filename):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
   
        # Set height, width
        self.image = pygame.image.load(filename).convert()
        self.path = filename
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.change_x = 0
        self.change_y = 0
    
    def update(self,walls):
        self.check()

        old_x = self.rect.left
        old_y = self.rect.top

        self.rect.left = old_x + self.change_x
        if(pygame.sprite.spritecollide(self, walls, False)):
            self.rect.left = old_x
            self.changeY(walls)
        else:
            self.rect.top = old_y + self.change_y
            if(pygame.sprite.spritecollide(self, walls, False)):
                self.rect.top = old_y
                self.changeX(walls)


    def check(self):
        if(self.change_x != 0 or self.change_y != 0):
            return
        self.change()

    def change(self):
        x_or_y = random.randrange(0,2)
        if x_or_y == 0:
            self.change_x = random.randrange(-1,2,2)
        else:
            self.change_y = random.randrange(-1,2,2)

    def changeY(self,walls):
        self.change_x = 0
        cond = random.randrange(0,2)
        if cond == 0:
            change1 = -1
            change2 = 1
            old_y = self.rect.top
            self.rect.top = old_y + change1
            self.change_y = change1
            if(pygame.sprite.spritecollide(self, walls, False)):
                self.rect.top = old_y + change2
                self.change_y = change2
                if(pygame.sprite.spritecollide(self, walls, False)):
                    self.rect.top = old_y
                    self.change_y = 0
                    self.changeX(walls)
        else:
            change1 = 1
            change2 = -1
            old_y = self.rect.top
            self.rect.top = old_y + change1
            self.change_y = change1
            if(pygame.sprite.spritecollide(self, walls, False)):
                self.rect.top = old_y + change2
                self.change_y = change2
                if(pygame.sprite.spritecollide(self, walls, False)):
                    self.rect.top = old_y
                    self.change_y = 0
                    self.changeX(walls)

    def changeX(self,walls):
        self.change_y = 0
        cond = random.randrange(0,2)
        if cond == 0:
            change1 = -1
            change2 = 1
            old_x = self.rect.left
            self.rect.left = old_x + change1
            self.change_x = change1
            if(pygame.sprite.spritecollide(self, walls, False)):
                self.rect.left = old_x + change2
                self.change_x = change2
                if(pygame.sprite.spritecollide(self, walls, False)):
                    self.rect.left = old_x
                    self.change_x = 0
                    self.changeY(walls)
        else:
            change1 = 1
            change2 = -1
            old_x = self.rect.left
            self.rect.left = old_x + change1
            self.change_x = change1
            if(pygame.sprite.spritecollide(self, walls, False)):
                self.rect.left = old_x + change2
                self.change_x = change2
                if(pygame.sprite.spritecollide(self, walls, False)):
                    self.rect.left = old_x
                    self.change_x = 0
                    self.changeY(walls)

    def replicate(self):
        new_virus = Virus(self.rect.left,self.rect.top,self.path)
        return new_virus

def startGame():

    global x_man
    global y_man
    global start_time


    all_sprites_list = pygame.sprite.RenderPlain()
    man_collide = pygame.sprite.RenderPlain()
    block_list = pygame.sprite.RenderPlain()
    virus_list = pygame.sprite.RenderPlain()
    wall_list = setupRoomOne(all_sprites_list)

    man = Player(x_man,y_man,'man.png')
    all_sprites_list.add(man)
    man_collide.add(man)

    virus1 = Virus(x_man,y_virus1,'virus.png')
    virus2 = Virus(x_man,y_virus2,'virus.png')

    bact1 = Virus(x_bact1,y_virus1,'bacteria.png')
    bact2 = Virus(x_bact2,y_virus2,'bacteria.png')
    
    viruses = []
    viruses.append(virus1)
    viruses.append(virus2)
    viruses.append(bact1)
    viruses.append(bact2)
    
    virus_list.add(virus1)
    virus_list.add(virus2)
    virus_list.add(bact1)
    virus_list.add(bact2)

    all_sprites_list.add(virus1)
    all_sprites_list.add(virus2)
    all_sprites_list.add(bact1)
    all_sprites_list.add(bact2)


    for row in range(19):
      for column in range(19):
          if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
              continue
          else:
            block = Block(yellow, 4, 4)

            # Set a random location for the block
            block.rect.x = (30*column+6)+26
            block.rect.y = (30*row+6)+26

            b_collide = pygame.sprite.spritecollide(block, wall_list, False)
            p_collide = pygame.sprite.spritecollide(block, man_collide, False)
            if b_collide:
              continue
            elif p_collide:
              continue
            else:
              # Add the block to the list of objects
              block_list.add(block)
              all_sprites_list.add(block)

    score = 0
    total = len(block_list)
        
    done=False
    while done == False:
      # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done=True
            if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_LEFT:
                  man.changespeed(-1,0)
              if event.key == pygame.K_RIGHT:
                  man.changespeed(1,0)
              if event.key == pygame.K_UP:
                  man.changespeed(0,-1)
              if event.key == pygame.K_DOWN:
                  man.changespeed(0,1)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    man.changespeed(0,0)
                if event.key == pygame.K_RIGHT:
                    man.changespeed(0,0)
                if event.key == pygame.K_UP:
                    man.changespeed(0,0)
                if event.key == pygame.K_DOWN:
                    man.changespeed(0,0)

        blocks_hit_list = pygame.sprite.spritecollide(man, block_list, True)
       
        # Check the list of collisions.
        if len(blocks_hit_list) > 0:
            score +=len(blocks_hit_list)

        screen.fill(black)
        
        wall_list.draw(screen)
        man.update(wall_list)
        
        for virus in virus_list:
            virus.update(wall_list)
        
        curr_time = time.perf_counter_ns()
        if((curr_time-start_time)>=30000000000):
            start_time = time.perf_counter_ns()
            n = len (virus_list)
            for virus in virus_list:
                new_virus = virus.replicate()
                #viruses.append(new_virus)
                virus_list.add(new_virus)
                all_sprites_list.add(new_virus)
                if n*2 == len(virus_list):
                    break

        pygame.sprite.spritecollide(man, virus_list, True)        
        
        
        all_sprites_list.draw(screen)
        text=font.render("Score: "+str(score)+"/"+str(total), True, red)
        screen.blit(text, [10, 10])

        pygame.display.flip()
        clock.tick(210)

        if score == total:
            doNext("Congratulations, you won!",145,all_sprites_list,block_list,virus_list,man_collide,wall_list)
            return

        if len(virus_list) > 32:
            doNext("Game Over",235,all_sprites_list,block_list,virus_list,man_collide,wall_list)
            return

def doNext(message,left,all_sprites_list,block_list,virus_list,man_collide,wall_list):
  while True:
      # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          return
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            pygame.quit()
            return
          if event.key == pygame.K_RETURN:
            del all_sprites_list
            del block_list
            del virus_list
            del man_collide
            del wall_list
            
            startGame()

      #Grey background
      w = pygame.Surface((400,200))  # the size of your rect
      w.set_alpha(10)                # alpha level
      w.fill((128,128,128))           # this fills the entire surface
      screen.blit(w, (100,200))    # (0,0) are the top-left coordinates

      #Won or lost
      text1=font.render(message, True, white)
      screen.blit(text1, [left, 233])

      text2=font.render("To play again, press ENTER.", True, white)
      screen.blit(text2, [135, 303])
      text3=font.render("To quit, press ESCAPE.", True, white)
      screen.blit(text3, [165, 333])

      pygame.display.flip()

      clock.tick(210)

startGame()

pygame.quit()