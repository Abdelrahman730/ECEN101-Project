import pygame
import random 
import math
import os


pygame.init()

File = open("Score.txt","r+")


Postive_Sound = pygame.mixer.Sound("Sound/Postive.wav")
Negaive_Sound = pygame.mixer.Sound("Sound/Negative.wav")

display_width = 600
display_height = 900
Level = 1
Score = int(File.readline())
if (Score <= 0):
    Score = 1;

gameDisplay = pygame.display.set_mode((display_width,display_height))
gameDisplay.fill((255, 255, 255))
pygame.display.set_icon(pygame.image.load('Images/Icon.png'))
pygame.display.set_caption('Flying Superman')

Image_Background = pygame.image.load("Images/Background_1.png")

Char_X = 200
Char_Y = 800
Char_Width = 100
Char_Hight = 100
Char_Speed = 5
moveLeft = False
moveRight = False
Image_Character = pygame.image.load("Images/Char_1.png")

Char_Positions = []
Position_Index = 2;
for i in range (6):
    Char_Positions.append(i*100)

Poles_List = [ 
    [None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None],      
]

About_List = [
    ["Abdelrahman Ahmed",19105768],
    ["Ahmed Dahy Ahmed",19100643],
    ["Youssef Mohamed",19100935],
    ["Khalil Ahmed",19105768],
]


class button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (255,255,255))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] >= self.x and pos[0] <= self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

    
#Main
Start_Game_Button = button( (0,35,163) , 100 , 100 , 400 , 100 ,"Start")
About_Game_Button = button( (0,35,163) , 100 , 300 , 400 , 100 ,"About")
Exit_Game_Button = button( (0,35,163) , 100 , 500 , 400 , 100 ,"Exit")
#Start
Level_Button = button( (0,35,163) , 0 , 0 , 50 , 50 ,"1")
Score_Button = button( (0,35,163) , 550 , 0 , 50 , 50 ,"0")

Current_Window = "Main"

Enable = True
running = True
while running:
    gameDisplay.fill((255, 255, 255))
    gameDisplay.blit(Image_Background, (0, 0))
    
    if Current_Window == "Main":
        Start_Game_Button.draw(gameDisplay,(0,0,0))
        About_Game_Button.draw(gameDisplay,(0,0,0))
        Exit_Game_Button.draw(gameDisplay,(0,0,0))
    elif Current_Window == "Start":
        Level_Button.text = str(Level)
        Score_Button.text = str(Score)
        
        Level_Button.draw(gameDisplay,(0,0,0))
        Score_Button.draw(gameDisplay,(0,0,0))        
        
        for i in range(6):
            if (Poles_List[i][2] > display_height):
                Enable = True
                Poles_List[i][2] = 0
                Poles_List[i][6] = random.randrange( (Level*-10),(Level*10)) # Value
                Poles_List[i][5] = (Level*10) #Speed
                if Poles_List[i][6] < 0:
                    Poles_List[i][0].text = (str(Poles_List[i][6]))
                    Poles_List[i][0].color = (200,0,0)
                else:
                    Poles_List[i][0].text = ("+"+str(Poles_List[i][6]))
                    Poles_List[i][0].color = (0,200,0)
            else:
                Poles_List[i][2] += Poles_List[i][5] # Speed
                
            Poles_List[i][0].y = Poles_List[i][2]
            
            Poles_List[i][0].draw(gameDisplay,(0,0,0))
            gameDisplay.blit(Image_Character, (Char_X, Char_Y))
            
        if (Poles_List[0][0].y >= (display_height-100)) and (Enable == True):
            
            if (Poles_List[Position_Index][6] > 0 ):
                pygame.mixer.Sound.play(Postive_Sound)
            else:
                pygame.mixer.Sound.play(Negaive_Sound)
                
            pygame.mixer.music.stop()
            
            Score += Poles_List[Position_Index][6]
            if (Score <= 0):
                Score = 1
            Enable = False     
            
        
        Level = math.ceil(Score/100)
        
        if Position_Index > 5 :
            Position_Index = 5
        elif Position_Index < 0:
            Position_Index = 0;
        else:
            Char_X = Char_Positions[Position_Index]    
            
    elif Current_Window == "About":
        TX , TY , TW , TH = (150,200,300,100)
        for i in range(4):
            font = pygame.font.SysFont('comicsans', 50)
            text = font.render(About_List[i][0]+"("+str(About_List[i][1])+")", 1, (255,255,255))
            gameDisplay.blit(text, (TX + (TW/2 - text.get_width()/2), (TY+(100*i) ) + (TH/2 - text.get_height()/2)))
                
                    
                

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if Current_Window == "Main":
                if Start_Game_Button.isOver(pos):
                    Image_Background = pygame.image.load("Images/Background_2.png")
                    
                    Current_Window = "Start"
                    for i in range(6):
                        Value = random.randrange(-10,10)
                        Pole = None
                        x,y,width,hight = (i*100,50,100,50)
                        if Value < 0:
                            Pole = button( (200,0,0),x,y,width,hight, (str(Value)) )
                        else:
                            Pole = button( (0,200,0),x,y,width,hight, ("+"+str(Value)) )
                        #                  x   y  width,hight,speed Value
                        Poles_List[i] = [Pole,x,y,width,hight,5,Value]
                        
                elif About_Game_Button.isOver(pos):
                    Current_Window = "About"
                elif Exit_Game_Button.isOver(pos):
                    running = False
                    File.close()
                    os.remove("Score.txt") 
                    File = open("Score.txt","w+")
                    File.write(str(Score))
                    File.close()
        elif event.type == pygame.MOUSEMOTION:
            Start_Game_Button.color = (0,35,163)
            About_Game_Button.color = (0,35,163)
            Exit_Game_Button.color = (0,35,163)
            if Start_Game_Button.isOver(pos):
                Start_Game_Button.color = (255,0,0)
            elif About_Game_Button.isOver(pos):
                About_Game_Button.color = (255,0,0)
            elif Exit_Game_Button.isOver(pos):
                Exit_Game_Button.color = (255,0,0)     
        elif event.type == pygame.KEYDOWN:
            if Current_Window == "Start":
                if event.key == pygame.K_LEFT: 
                    Position_Index -= 1;
                if event.key == pygame.K_RIGHT: 
                    Position_Index += 1;
                    
            if (event.key == pygame.K_ESCAPE and Current_Window != "Main"):
                Image_Background = pygame.image.load("Images/Background_1.png")
                Current_Window = "Main"
                

            
    pygame.display.update()