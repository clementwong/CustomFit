#DesignBoard.py
# Made by Clement Wong, clementw
import pygame
import random
import os 
import shelve
import math

"""

Images used in Program 
http://icons.iconarchive.com/icons/custom-icon-design/mono-general-1/128/save-icon.png
http://www.clker.com/cliparts/3/3/6/4/12074316411296807266camera%20white.svg.hi.png
https://cdn2.iconfinder.com/data/icons/windows-8-metro-style/512/open_in_browser.png
http://res.freestockphotos.biz/pictures/15/15107-illustration-of-a-red-close-button-pv.png
https://cdn2.iconfinder.com/data/icons/designers-and-developers-icon-set/32/increased_proportionally_square_button-512.png
https://cdn3.iconfinder.com/data/icons/tools-solid-icons-vol-2/72/91-512.png 

"""


class Tshirt (object): 
    def __init__(self, x, y,width, height, color = pygame.color.THECOLORS["white"]): 
        self.x =x 
        self.y=y
        self.width =width
        self.height = height 
        self.color = color

        self.space = 10
        self.borderwidth = (self.width)*47/78
        self.borderheight = (self.height)*55/67 
        self.borderx = (self.x +self.x+ self.width)/2 - self.borderwidth/2
        self.bordery = self.y+self.height*10/67
        
    def draw (self, screen):
        #rectangle outline of tshirt 
        pygame.draw.rect(screen, pygame.color.THECOLORS["black"], ((self.x-self.space),(self.y-self.space), 
                     self.width+self.space*2, self.height+self.space*2), 2)
        width = self.width
        height = self.height  
        shoulderWidth = (49/78)*width
        mShoulderWidth = 49
        mArmSpace = 20
        mHeight = 67
        mNeck = 14
        mSideLength = 42
        #neck points
        p1 = ((self.x+self.x+self.width)/2-((mNeck/mShoulderWidth)*shoulderWidth/2), self.y )
        p10 = ((self.x+self.x+self.width)/2+((mNeck/mShoulderWidth)*shoulderWidth/2), self.y )
        #leftarmpoints
        p2 = (self.x , self.y +height*10/69)
        p3 = (self.x +width*4/78, self.y +height*(27/69))

        #right arm points
        p8 = (self.x  +width*74/78, self.y +height*(27/69))
        p9 =  (self.x+self.width, self.y +height*(10/69))
        
        
        p4 = ((self.x+self.x+self.width)/2-shoulderWidth/2, self.y +height*(1-mSideLength/mHeight))
        p5 = ((self.x+self.x+self.width)/2-shoulderWidth/2, self.y +height)
        p6 = ((self.x+self.x+self.width)/2+shoulderWidth/2, self.y +height)
        p7 =  ((self.x+self.x+self.width)/2+shoulderWidth/2, self.y +height*(1-mSideLength/mHeight))
        pygame.draw.polygon(screen, self.color, (p1, p2, p3 ,p4, p5, p6,p7, p8,p9, p10) )
        #tshirt black outline
        pygame.draw.polygon(screen, pygame.color.THECOLORS["black"] , (p1, p2, p3 ,p4, p5, p6,p7, p8,p9, p10),1 )
        
    def containsPoint (self, x, y): 
        # if the person clicked on the item itself
         return (((self.x-self.space)<x<(self.x +self.width+self.space) and (self.y-self.space)<y<(self.y+self.height+self.space)))  
    #draw t-shirt borders
    def draw_tshirtBorders(self, screen): 
        color = pygame.color.THECOLORS["black"]
        pygame.draw.rect(screen, color, ((self.borderx),(self.bordery), 
                     self.borderwidth, self.borderheight), 2)
    def __repr__(self):
        return "Tshirt(%d, %d,%d,%d, %s)" % (self.borderx, self.bordery, self.borderwidth, self.borderheight, self.color)
class TshirtItem (object): 
    def __init__ (self,x, y, width,height ): 
        self.x = x 
        self.y= y
        self.width = width
        self.height = height
        self.radius = 15
    def containsPoint (self, x, y): 
        # if the person clicked on the item itself
        return (((self.x)<x<(self.x +self.width) and (self.y)<y<(self.y+self.height))) 
    def containsPoint2 (self, x,y):
        # if the person clicked on the close buttom or the resize button
        return (((self.x+self.width)<x<(self.x+self.width+self.radius*2) and (self.y+self.height)<y<(self.y+self.height+self.radius*2)) 
            or 
            ((self.x-2*self.radius*2)<x<(self.x) and (self.y-2*self.radius*2)<y<(self.y))) 


    def drawIsSelected (self,screen): 
        #outline
        
        pygame.draw.rect(screen, pygame.color.THECOLORS["black"], ((self.x-1),(self.y-1), 
                     self.width+2, self.height+2), 2)
        #red Button 
        pygame.draw.circle(screen, pygame.color.THECOLORS["red"], (round(self.x-self.radius),round(self.y-self.radius)), 
                     round(self.radius), 0)
        close = pygame.image.load("redButton.png").convert_alpha()
        close = pygame.transform.scale(close, (round(self.radius)*2 , round(self.radius)*2)) 
        screen.blit(close, (round(self.x-2*self.radius),round(self.y-2*self.radius)))
        
        #resize Button
        
        resize = pygame.image.load("resizeButton.png").convert_alpha()
        resize = pygame.transform.rotate(resize, 90)
        resize = pygame.transform.scale(resize, (round(self.radius)*2 , round(self.radius)*2)) 
        screen.blit(resize, (round(self.x+self.width),round(self.y+self.height)))
        
    def isClickClosed(self, x,y): 
        centerX = (self.x-self.radius)
        centerY = (self.y-self.radius)
        d = ((x-centerX)**2 +(y-centerY)**2)**.5
        return d<self.radius 
    def isClickResize(self, x,y): 
        centerX = (self.x+self.width+self.radius)
        centerY = (self.y+self.height+self.radius)
        d = ((x-centerX)**2 +(y-centerY)**2)**.5
        return d<=self.radius 



class Textbox(TshirtItem):
    def __init__ (self,   x,y , text = "Type Text Here",font= "timesnewroman" , textSize = 34,color = pygame.color.THECOLORS["black"] ): 
    
        self.moveSpeed = 10
        self.text = text 
        self.font = font
        self.textSize = textSize
        font = pygame.font.SysFont(self.font, round(self.textSize)) 
        self.fontColor = color
        self.inst = font.render(self.text, True, self.fontColor, None) 
        self.width = self.inst.get_width()
        self.height = self.inst.get_height()
        #features for typing in text
        self.shifted = False
        self.angle= 0 #for kinect rotation
        self. widthConversion = 0
        self.caps = False
        super().__init__(x,y, self.width, self.height)
    def draw(self,screen): 
        #updates textbox when typing
        font = pygame.font.SysFont(self.font, round(self.textSize))
        self.inst = font.render(self.text, True, self.fontColor, None) 
        self.inst = pygame.transform.rotate(self.inst, self.angle) # for kinect rotation
        self.width = self.inst.get_width()
        self.height = self.inst.get_height()
        if (self.widthConversion!=0): #in kinect
            self.inst = pygame.transform.scale (self.inst, (round(self.widthConversion*self.width), round(self.height)))
        screen.blit(self.inst, ((self.x),(self.y)))
    # update code was modified by a code found online
    def update (self, code): 
        if code == pygame.K_BACKSPACE and len(self.text)>0: self.text = self.text[:-1]
        elif code == pygame.K_SPACE: self.text+= ' '
        if pygame.key.get_mods() == 1 or pygame.key.get_mods() == 8193:
            if code == pygame.K_a: self.text += 'A'
            elif code == pygame.K_b: self.text += 'B'
            elif code == pygame.K_c: self.text += 'C'
            elif code == pygame.K_d: self.text += 'D'
            elif code == pygame.K_e: self.text += 'E'
            elif code == pygame.K_f: self.text += 'F'
            elif code == pygame.K_g: self.text += 'G'
            elif code == pygame.K_h: self.text += 'H'
            elif code == pygame.K_i: self.text += 'I'
            elif code == pygame.K_j: self.text += 'J'
            elif code == pygame.K_k: self.text += 'K'
            elif code == pygame.K_l: self.text += 'L'
            elif code == pygame.K_m: self.text += 'M'
            elif code == pygame.K_n: self.text += 'N'
            elif code == pygame.K_o: self.text += 'O'
            elif code == pygame.K_p: self.text += 'P'
            elif code == pygame.K_q: self.text += 'Q'
            elif code == pygame.K_r: self.text += 'R'
            elif code == pygame.K_s: self.text += 'S'
            elif code == pygame.K_t: self.text += 'T'
            elif code == pygame.K_u: self.text += 'U'
            elif code == pygame.K_v: self.text += 'V'
            elif code == pygame.K_w: self.text += 'W'
            elif code == pygame.K_x: self.text += 'X'
            elif code == pygame.K_y: self.text += 'Y'
            elif code == pygame.K_z: self.text += 'Z'
            elif code == pygame.K_0: self.text += ')'
            elif code == pygame.K_1: self.text += '!'
            elif code == pygame.K_2: self.text += '@'
            elif code == pygame.K_3: self.text += '#'
            elif code == pygame.K_4: self.text += '$'
            elif code == pygame.K_5: self.text += '%'
            elif code == pygame.K_6: self.text += '^'
            elif code == pygame.K_7: self.text += '&'
            elif code == pygame.K_8: self.text += '*'
            elif code == pygame.K_9: self.text += '('
            elif code == pygame.K_BACKQUOTE: self.text += '~'
            elif code == pygame.K_MINUS: self.text += '_'
            elif code == pygame.K_EQUALS: self.text += '+'
            elif code == pygame.K_LEFTBRACKET: self.text += '{'
            elif code == pygame.K_RIGHTBRACKET: self.text += '}'
            elif code == pygame.K_BACKSLASH: self.text += '|'
            elif code == pygame.K_SEMICOLON: self.text += ':'
            elif code == pygame.K_QUOTE: self.text += '"'
            elif code == pygame.K_COMMA: self.text += '<'
            elif code == pygame.K_PERIOD: self.text += '>'
            elif code == pygame.K_SLASH: self.text += '?'
        #just capslock 
        elif pygame.key.get_mods() == 8192:
            if code == pygame.K_a: self.text += 'A'
            elif code == pygame.K_b: self.text += 'B'
            elif code == pygame.K_c: self.text += 'C'
            elif code == pygame.K_d: self.text += 'D'
            elif code == pygame.K_e: self.text += 'E'
            elif code == pygame.K_f: self.text += 'F'
            elif code == pygame.K_g: self.text += 'G'
            elif code == pygame.K_h: self.text += 'H'
            elif code == pygame.K_i: self.text += 'I'
            elif code == pygame.K_j: self.text += 'J'
            elif code == pygame.K_k: self.text += 'K'
            elif code == pygame.K_l: self.text += 'L'
            elif code == pygame.K_m: self.text += 'M'
            elif code == pygame.K_n: self.text += 'N'
            elif code == pygame.K_o: self.text += 'O'
            elif code == pygame.K_p: self.text += 'P'
            elif code == pygame.K_q: self.text += 'Q'
            elif code == pygame.K_r: self.text += 'R'
            elif code == pygame.K_s: self.text += 'S'
            elif code == pygame.K_t: self.text += 'T'
            elif code == pygame.K_u: self.text += 'U'
            elif code == pygame.K_v: self.text += 'V'
            elif code == pygame.K_w: self.text += 'W'
            elif code == pygame.K_x: self.text += 'X'
            elif code == pygame.K_y: self.text += 'Y'
            elif code == pygame.K_z: self.text += 'Z'
            elif code == pygame.K_0: self.text += '0'
            elif code == pygame.K_1: self.text += '1'
            elif code == pygame.K_2: self.text += '2'
            elif code == pygame.K_3: self.text += '3'
            elif code == pygame.K_4: self.text += '4'
            elif code == pygame.K_5: self.text += '5'
            elif code == pygame.K_6: self.text += '6'
            elif code == pygame.K_7: self.text += '7'
            elif code == pygame.K_8: self.text += '8'
            elif code == pygame.K_9: self.text += '9'
            elif code == pygame.K_BACKQUOTE: self.text += '`'
            elif code == pygame.K_MINUS: self.text += '-'
            elif code == pygame.K_EQUALS: self.text += '='
            elif code == pygame.K_LEFTBRACKET: self.text += '['
            elif code == pygame.K_RIGHTBRACKET: self.text += ']'
            elif code == pygame.K_BACKSLASH : self.text += '\\'
            elif code == pygame.K_SEMICOLON: self.text += ';'
            elif code == pygame.K_QUOTE : self.text += '\''
            elif code == pygame.K_COMMA: self.text += ','
            elif code == pygame.K_PERIOD: self.text += '.'
            elif code == pygame.K_SLASH: self.text += '/'
        else:
            if code == pygame.K_a: self.text += 'a'
            elif code == pygame.K_b: self.text += 'b'
            elif code == pygame.K_c: self.text += 'c'
            elif code == pygame.K_d: self.text += 'd'
            elif code == pygame.K_e: self.text += 'e'
            elif code == pygame.K_f: self.text += 'f'
            elif code == pygame.K_g: self.text += 'g'
            elif code == pygame.K_h: self.text += 'h'
            elif code == pygame.K_i: self.text += 'i'
            elif code == pygame.K_j: self.text += 'j'
            elif code == pygame.K_k: self.text += 'k'
            elif code == pygame.K_l: self.text += 'l'
            elif code == pygame.K_m: self.text += 'm'
            elif code == pygame.K_n: self.text += 'n'
            elif code == pygame.K_o: self.text += 'o'
            elif code == pygame.K_p: self.text += 'p'
            elif code == pygame.K_q: self.text += 'q'
            elif code == pygame.K_r: self.text += 'r'
            elif code == pygame.K_s: self.text += 's'
            elif code == pygame.K_t: self.text += 't'
            elif code == pygame.K_u: self.text += 'u'
            elif code == pygame.K_v: self.text += 'v'
            elif code == pygame.K_w: self.text += 'w'
            elif code == pygame.K_x: self.text += 'x'
            elif code == pygame.K_y: self.text += 'y'
            elif code == pygame.K_z: self.text += 'z'
            elif code == pygame.K_0: self.text += '0'
            elif code == pygame.K_1: self.text += '1'
            elif code == pygame.K_2: self.text += '2'
            elif code == pygame.K_3: self.text += '3'
            elif code == pygame.K_4: self.text += '4'
            elif code == pygame.K_5: self.text += '5'
            elif code == pygame.K_6: self.text += '6'
            elif code == pygame.K_7: self.text += '7'
            elif code == pygame.K_8: self.text += '8'
            elif code == pygame.K_9: self.text += '9'
            elif code == pygame.K_BACKQUOTE: self.text += '`'
            elif code == pygame.K_MINUS: self.text += '-'
            elif code == pygame.K_EQUALS: self.text += '='
            elif code == pygame.K_LEFTBRACKET: self.text += '['
            elif code == pygame.K_RIGHTBRACKET: self.text += ']'
            elif code == pygame.K_BACKSLASH : self.text += '\\'
            elif code == pygame.K_SEMICOLON: self.text += ';'
            elif code == pygame.K_QUOTE : self.text += '\''
            elif code == pygame.K_COMMA: self.text += ','
            elif code == pygame.K_PERIOD: self.text += '.'
            elif code == pygame.K_SLASH: self.text += '/'
      
    def __repr__(self):
        return "Textbox(%d,%d,%s,%s,%d,%s)" % (self.x, self.y, self.text, self.font, self.textSize, str(self.fontColor))
    

    def rescale (self, rightCornerY):
        heightChange = self.height - rightCornerY 
        if ((rightCornerY - self.y)>0):
            heightChange = self.y+self.height - rightCornerY 
            self.textSize -=heightChange 
            font = pygame.font.SysFont(self.font, int (self.textSize))
            self.inst = font.render(self.text, True, self.fontColor, None) 
            self.width = self.inst.get_width()
            self.height = self.inst.get_height()
            
class Image (TshirtItem): 
    def __init__(self, name, x , y, width, height): 
        super().__init__(x,y, width, height)
        self.name = name
        self.image = pygame.image.load(name).convert_alpha()
        self.image = pygame.transform.scale(self.image, (round(self.width), round(self.height))) 
    def draw (self, screen):
        screen.blit(self.image, (self.x, self.y))
        
    def __repr__(self):
        return "Image(%s,%d,%d,%d,%d)" % (self.name, self.x , self.y, self.width, self.height)
    def rescale(self, rightCornerX, rightCornerY): 
        if ((rightCornerX-self.x)>0 and (rightCornerY - self.y)>0):
            self.image = pygame.image.load(self.name).convert_alpha()
            self.image = pygame.transform.scale(self.image, (round(rightCornerX-self.x), round(self.height/(self.width/(rightCornerX-self.x))))) 
        self.width = self.image.get_width()
        self.height = self.image.get_height()
class Button (object): 
    #x and y are center
    def __init__(self, x, y, width,height, color, text): 
        self.x = x 
        self.y = y 
        self.width = width
        self.height = height 
        self.color= pygame.color.THECOLORS[color]
        self.text = text
        self.textSize = 20
        font = pygame.font.SysFont("microsoftyaheitruetypemicrosoftyaheiui", round(self.textSize)) 
        self.fontColor = pygame.color.THECOLORS["black"]
        self.inst = font.render(self.text, True, self.fontColor, None)
        
    def draw(self,screen): 
        pygame.draw.rect(screen, self.color, ((self.x),(self.y), 
                     self.width, self.height), 0)
         #border
        pygame.draw.rect(screen, pygame.color.THECOLORS["black"], ((self.x),(self.y), 
                     self.width, self.height), 2)
        screen.blit(self.inst, (self.x +self.width/2-self.inst.get_width()/2, self.y+self.height/2-self.inst.get_height()/2))
    def containsPoint (self, x, y): 
        return ((self.x)<x<(self.x +self.width) and 
            (self.y)<y<(self.y+self.height))

class LoadTextButton (Button): 
    def __init__(self, x, y, width, height, color, text = "Add Text"): 
        super().__init__(x, y, width, height, color, text)
    def draw(self,screen): 
        pygame.draw.rect(screen, self.color, ((self.x),(self.y), 
                     self.width, self.height), 0)
         #border
        pygame.draw.rect(screen, pygame.color.THECOLORS["black"], ((self.x),(self.y), 
                     self.width, self.height), 2)

        icon = pygame.image.load("text.png").convert_alpha()
        icon = pygame.transform.scale(icon, (round((self.height/4)*(icon.get_width()/icon.get_height())) , round(self.height/4 )))
        screen.blit(icon, (round(self.x+self.width/2-icon.get_width()/2),round(self.y+self.height/4)))

        screen.blit(self.inst, (self.x +self.width/2-self.inst.get_width()/2, self.y+self.height/2))
class TryItOnButton(Button): 
    def __init__(self, x, y, width, height, color, text = "Try It On"): 
        super().__init__(x, y, width, height, color, text)

class ImageButton(Button): 
    def __init__(self, x, y, width, height, color, text ="Add Image"): 
        super().__init__(x, y, width, height, color, text)
    def draw(self,screen): 
        pygame.draw.rect(screen, self.color, ((self.x),(self.y), 
                     self.width, self.height), 0)
         #border
        pygame.draw.rect(screen, pygame.color.THECOLORS["black"], ((self.x),(self.y), 
                     self.width, self.height), 2)

        icon = pygame.image.load("camera.png").convert_alpha()
        icon = pygame.transform.scale(icon, (round((self.height/4)*(icon.get_width()/icon.get_height())) , round(self.height/4 )))
        screen.blit(icon, (round(self.x+self.width/2-icon.get_width()/2),round(self.y+self.height/4)))

        screen.blit(self.inst, (self.x +self.width/2-self.inst.get_width()/2, self.y+self.height/2))

    
class EditTextColorButton (Button): 
    def __init__(self, x, y, width, height, color, text = "Edit Text Color "): 
        super().__init__(x, y, width, height, color, text)
    def draw(self,screen): 
        pygame.draw.rect(screen, self.color, ((self.x),(self.y), 
                     self.width, self.height), 0)
         #border
        pygame.draw.rect(screen, pygame.color.THECOLORS["black"], ((self.x),(self.y), 
                     self.width, self.height), 2)

        icon = pygame.image.load("text.png").convert_alpha()
        icon = pygame.transform.scale(icon, (round((self.height/4)*(icon.get_width()/icon.get_height())) , round(self.height/4 )))
        screen.blit(icon, (round(self.x+self.width/2-icon.get_width()/2),round(self.y+self.height/4)))

        screen.blit(self.inst, (self.x +self.width/2-self.inst.get_width()/2, self.y+self.height/2))
class EditTextFontButton (Button): 
    def __init__(self, x, y, width, height, color, text = "Edit Text Font"): 
        super().__init__(x, y, width, height, color, text)
    def draw(self,screen): 
        pygame.draw.rect(screen, self.color, ((self.x),(self.y), 
                     self.width, self.height), 0)
         #border
        pygame.draw.rect(screen, pygame.color.THECOLORS["black"], ((self.x),(self.y), 
                     self.width, self.height), 2)

        icon = pygame.image.load("text.png").convert_alpha()
        icon = pygame.transform.scale(icon, (round((self.height/4)*(icon.get_width()/icon.get_height())) , round(self.height/4 )))
        screen.blit(icon, (round(self.x+self.width/2-icon.get_width()/2),round(self.y+self.height/4)))

        screen.blit(self.inst, (self.x +self.width/2-self.inst.get_width()/2, self.y+self.height/2))
class ColorMover (object):
    #x1 are the bounds of which the ColorMover can go 
    def __init__(self, x1, x2, y, radius, color = "black"): 
        self.startX = x1
        self.endX = x2
        self.x = x1
        self.y = y 
        self.r = radius 
        self.color = pygame.color.THECOLORS[color]
        self.isSelected = False
    def containsPoint (self, x, y): 
        return ((self.x-self.r)<x<(self.x +self.r) and 
            (self.y-self.r)<y<(self.y+self.r))
    def update (self, x):
        if (self.startX<x<self.endX):
            self. x = x 
    def draw(self, screen): 
        pygame.draw.circle(screen, self.color, (round(self.x),round(self.y)), round(self.r), 0)
    def getColorValue (self): 
        return 255* (self.x-self.startX)/(self.endX - self.startX) 

class ColorTool(object): 
    def __init__(self, x, y, width, height): 
        self.x = x 
        self.y = y 
        self.width = width 
        self.height = height 
        self.color= pygame.color.THECOLORS["black"] 
        self.startPos = self.x + (1/8)*self.width
        self. endPos = self.x +self.width*(7/8)
        self.moverLength = self.endPos - self.startPos
        self.rMover = ColorMover (self.startPos, self.endPos, self.y+self.height/4+(self.height*3/4)/4, 10)
        self.gMover = ColorMover (self.startPos, self.endPos, self.y+self.height/4+2*(self.height*3/4)/4, 10)
        self.bMover = ColorMover(self.startPos, self.endPos, self.y+self.height/4+3*(self.height*3/4)/4, 10)
    def getColor (self): 
        return (self.rMover.getColorValue(), self.gMover.getColorValue(), self.bMover.getColorValue())

    def draw (self,screen): 
        textSize = (self.height*3/4)/4
        font = pygame.font.SysFont("microsoftyaheitruetypemicrosoftyaheiui", round(textSize)) 
        r = font.render("R", True, (255,0,0) , None) 
        g = font.render("G", True, (0,255,0), None) 
        b = font.render("B", True, (0,0,255) , None) 
        #draw movers and lines
        pygame.draw.line(screen, self.color, (self.startPos, self.y+self.height/4+(self.height*3/4)/4), (self.endPos,self.y+self.height/4+(self.height*3/4)/4), 5)
        screen.blit(r, ((self.x, self.y+self.height/8+(self.height*3/4)/4)))
        pygame.draw.line(screen, self.color, (self.startPos, self.y+self.height/4+2*(self.height*3/4)/4), (self.endPos,self.y+self.height/4+2*(self.height*3/4)/4), 5)
        screen.blit(g, (self.x, self.y+self.height/8+2*(self.height*3/4)/4))
        pygame.draw.line(screen, self.color, (self.startPos, self.y+self.height/4+3*(self.height*3/4)/4), (self.endPos,self.y+self.height/4+3*(self.height*3/4)/4), 5)
        screen.blit(b, (self.x, self.y+self.height/8+3*(self.height*3/4)/4))
        self.rMover.draw(screen)
        self.gMover.draw(screen)
        self.bMover.draw(screen)
        (r,g,b) = self.getColor()
        # result color
        pygame.draw.rect(screen, (r,g,b), (self.x, self. y, self.width, self.height/4))
        pygame.draw.rect(screen, (0,0,0), (self.x, self. y, self.width, self.height/4),1)
    def isColorClicked (self,x,y): 
        return ((self.x)<x<(self.x +self.width) and (self.y)<y<(self.y+self.height/4)) 
        
class SaveButton (Button): 
    def __init__(self, x, y, width, height, color, text = "Save Current Design"): 
        super().__init__(x, y, width, height, color, text)
    def draw(self,screen): 
        pygame.draw.rect(screen, self.color, ((self.x),(self.y), 
                     self.width, self.height), 0)
         #border
        pygame.draw.rect(screen, pygame.color.THECOLORS["black"], ((self.x),(self.y), 
                     self.width, self.height), 2)

        icon = pygame.image.load("save.png").convert_alpha()
        icon = pygame.transform.scale(icon, (round((self.height/4)*(icon.get_width()/icon.get_height())) , round(self.height/4 )))
        screen.blit(icon, (round(self.x+self.width/2-icon.get_width()/2),round(self.y+self.height/4)))

        screen.blit(self.inst, (self.x +self.width/2-self.inst.get_width()/2, self.y+self.height/2))        
        

class OpenButton (Button): 
    def __init__(self, x, y, width, height, color, text = "Open Past Designs"): 
        super().__init__(x, y, width, height, color, text)
    def draw(self,screen): 
        pygame.draw.rect(screen, self.color, ((self.x),(self.y), 
                     self.width, self.height), 0)
         #border
        pygame.draw.rect(screen, pygame.color.THECOLORS["black"], ((self.x),(self.y), 
                     self.width, self.height), 2)

        icon = pygame.image.load("open.png").convert_alpha()
        icon = pygame.transform.scale(icon, (round((self.height/4)*(icon.get_width()/icon.get_height())) , round(self.height/4 )))
        screen.blit(icon, (round(self.x+self.width/2-icon.get_width()/2),round(self.y+self.height/4)))

        screen.blit(self.inst, (self.x +self.width/2-self.inst.get_width()/2, self.y+self.height/2))

class ApplyButton (Button): 
    def __init__(self, x, y, width, height, color, text = "Apply"): 
        super().__init__(x, y, width, height, color, text)

class BackButton(Button):
    def __init__(self, x, y, width, height, color, text = "Back"): 
        super().__init__(x, y, width, height, color, text)
    def draw (self, screen): 
        pygame.draw.polygon(screen, self.color, ((self.x, self.y +self.height/2), (self.x+self.width/3, self.y), 
            (self.x+self.width/3, self.y+self.height/4), (self.x+self.width,self.y+self.height/4), 
            (self.x+self.width, self.y+3*self.height/4), (self.x+self.width/3, self.y+3*self.height/4), (self.x+self.width/3, self.y+self.height)))
        pygame.draw.polygon(screen, pygame.color.THECOLORS["black"], ((self.x, self.y +self.height/2), (self.x+self.width/3, self.y), 
            (self.x+self.width/3, self.y+self.height/4), (self.x+self.width,self.y+self.height/4), 
            (self.x+self.width, self.y+3*self.height/4), (self.x+self.width/3, self.y+3*self.height/4), (self.x+self.width/3, self.y+self.height)), 1)
class Page (object): 
    def __init__(self, width, height): 
        self.width = width 
        self.height= height 
class StartPage (Page): 
    def __init__(self, width, height): 
        super().__init__(width, height)
        self.title = "CustomFit"
        self.instructions = "Design T-shirts and see how"
        self.instructions2 = "they look on you. "
        self.startButton = Button (self.width/3, 5*self.height/8, self.width/3, self.height/8, "gray", "LET'S GET STARTED")
        font = pygame.font.SysFont("microsoftyaheitruetypemicrosoftyaheiuibold", 80)
        font2 = pygame.font.SysFont("microsoftyaheitruetypemicrosoftyaheiui", 30)
        self.title= font.render(self.title, True, pygame.color.THECOLORS["black"], None)
        self.instructions = font2.render(self.instructions, True, pygame.color.THECOLORS["black"], None)
        self.instructions2 = font2.render(self.instructions2, True, pygame.color.THECOLORS["black"], None)

    def draw(self,screen): 
        pygame.draw.rect(screen, pygame.color.THECOLORS["white"], ((0),(0), 
                     self.width, self.height))
    
        screen.blit(self.title, (self.width/2-self.title.get_width()/2, self.height/4))
        screen.blit (self.instructions, (self.width/2 - self.instructions.get_width()/2, self.height/4+self.title.get_height()))
        screen.blit (self.instructions2, (self.width/2 - self.instructions2.get_width()/2, self.height/4+self.title.get_height()+self.instructions.get_height()))
        self.startButton.draw(screen)
class Arrow (object): 
    def __init__ (self, x, y,width, height): 
        self.x = x
        self.y = y 
        self.width = width 
        self.height = height 
    


class UpArrow (Arrow): 
    def __init__(self,x,y,width, height):
        super().__init__(x,y , width, height)
    def draw (self,screen): 
        pygame.draw.rect(screen, pygame.color.THECOLORS["black"], ((self.x),(self.y), 
                     self.width, self.height), 1)
        pygame.draw.polygon(screen, pygame.color.THECOLORS["gray"], ((self.x+self.width/4, self.y+3*self.height/4),(self.x+self.width/2, self.y +self.height/4), 
            (self.x + 3*self.width/4, self.y+self.height*3/4)))
class DownArrow (Arrow): 
    def __init__(self,x,y,width, height):
        super().__init__(x,y , width, height)
    def draw (self,screen): 
        pygame.draw.rect(screen, pygame.color.THECOLORS["black"], ((self.x),(self.y), 
                     self.width, self.height), 1)
        pygame.draw.polygon(screen, pygame.color.THECOLORS["gray"], ((self.x+self.width/4, self.y+self.height/4),(self.x+self.width/2, self.y +3*self.height/4), 
            (self.x + 3*self.width/4, self.y+self.height/4)))

class EditFontPage (Page): 
    def __init__ (self, width, height): 
        super().__init__(width, height)
        self.title = "Select and Click a Font"
        self.titleSize = 50
        self.fonts = pygame.font.get_fonts()
        self.fontTextboxes = []
        self.textSelectionX = self.width/8
        self.textSelectionY = self.height/8
        self.textSelectionHeight = 3*self.height/4 
        self.textSelectionWidth = 3*self.width/4 
        self.backButton = BackButton (10, 10, 50, 50, "red")
        arrowSize = 50
        self.uparrow = UpArrow (self.textSelectionX + self.textSelectionWidth-arrowSize, self.textSelectionY-5, arrowSize, arrowSize)
        self.downarrow = DownArrow(self.textSelectionX + self.textSelectionWidth-arrowSize, self.textSelectionY+self.textSelectionHeight-arrowSize+5, arrowSize, arrowSize)
        textSize = 20
        textPerPage = self.textSelectionHeight//textSize
        count =0
        self.page = 0
        self.totalpages = len(self.fonts)//textPerPage
        
        self.selectionRectangleHeight = self.textSelectionHeight - self.uparrow.height -self.downarrow.height
        for font in self.fonts:
            count +=1 
            page= count//textPerPage
            y = self.textSelectionY +(count%textPerPage)*textSize
            try:
                textbox = Textbox (self.textSelectionX,y , font,font ,  textSize)
                self.fontTextboxes.append((page, textbox))
            except: 
                pass

    def draw (self,screen):
        pygame.draw.rect(screen, pygame.color.THECOLORS["white"], ((0),(0), 
                     self.width, self.height))
        
        self.backButton.draw(screen)
        self.uparrow.draw(screen)
        self.downarrow.draw(screen)
        #scroll bar 
        length = self.downarrow.y - (self.uparrow.y+ self.uparrow.height)
        pygame.draw.rect(screen, pygame.color.THECOLORS["gray"], (self.downarrow.x,self.uparrow.y+self.uparrow.height+(self.page)*length/(self.totalpages+1), 
                     self.downarrow.width, length/(self.totalpages+1)))
        pygame.draw.rect(screen, pygame.color.THECOLORS["black"], (self.downarrow.x,self.uparrow.y+self.uparrow.height+(self.page)*length/(self.totalpages+1), 
                     self.downarrow.width, length/(self.totalpages+1)),1)
        for (page, fontTextbox) in self.fontTextboxes: 
            if self.page == page: 
                fontTextbox.draw(screen)
        font = pygame.font.SysFont("microsoftyaheitruetypemicrosoftyaheiui", self.titleSize) 
        inst = font.render(self.title, True, pygame.color.THECOLORS["black"], None) 
        width = inst.get_width()
        height = inst.get_height()
        screen.blit(inst, ((self.textSelectionX),(self.textSelectionY-height)))
        instructions = "Use Arrow Keys to Scroll Through Fonts"
        font2 =pygame.font.SysFont("microsoftyaheitruetypemicrosoftyaheiui", int(self.titleSize/2)) 
        inst2 = font2.render(instructions, True, pygame.color.THECOLORS["black"], None) 
        screen.blit(inst2, ((self.textSelectionX),( self.textSelectionY+self.textSelectionHeight+5)))
        pygame.draw.rect(screen, pygame.color.THECOLORS["black"], ((self.textSelectionX-5),( self.textSelectionY-5), 
                     self.textSelectionWidth+5,  self.textSelectionHeight+10), 4)
    def fontClicked(self,x,y): 
        for (page, textbox) in self.fontTextboxes: 
            if page == self.page and textbox.containsPoint(x,y): 
                return textbox
        return None

class EditColorPage (Page): 
    def __init__ (self, width, height, textbox=None, backgroundColor=None): 
        super().__init__(width, height)
        self.textbox = textbox
        self.textColor = None
        self.textSize = 100
        self.backgroundColor = backgroundColor
        self.colorTool = ColorTool(self.width/4,self.height/2,self.width/2, self.height/4)
        self.backButton = BackButton (10, 10, 50, 50, "red")
        self.applyButton = ApplyButton(self.width/4, 3*self.height/4, self.width/2, self.height/8,"gray")
    def draw (self,screen):
       pygame.draw.rect(screen, pygame.color.THECOLORS["white"], ((0),(0), 
                     self.width, self.height))
       self.backButton.draw(screen)
       self.applyButton.draw(screen)
       if (self.textbox!=None):
            

            font = pygame.font.SysFont(self.textbox.font, round(self.textSize)) 
            inst = font.render(self.textbox.text, True,self.textColor, None) 
            textwidth = inst.get_width()
            textheight = inst.get_height()
            
            x = self.width/2 - textwidth/2
            y= 3*self.height/8-textheight

            #rectangle for comparisoon
            instructions = "Click Color Bar to see how the text color looks with tshirt color"
            instructions2 = "Click Apply to apply text color"
            font2 =pygame.font.SysFont("microsoftyaheitruetypemicrosoftyaheiui", 20) 
            inst2 = font2.render(instructions, True, pygame.color.THECOLORS["black"], None) 
            inst3 = font2.render(instructions2, True, pygame.color.THECOLORS["black"], None) 
            screen.blit(inst2, ((self.width/2-inst2.get_width()/2,y-inst2.get_height()-inst3.get_height())))
            screen.blit(inst3, ((self.width/2-inst3.get_width()/2,y-inst3.get_height())))
            pygame.draw.rect(screen, pygame.color.THECOLORS["black"], (x-1, y-1,textwidth+2, textheight+2))
            pygame.draw.rect(screen, self.backgroundColor, (x, y, textwidth, textheight))
            
            screen.blit(inst, ((x,y)))
            self.colorTool.draw(screen)
    


#from 15-112 notes
def listFiles(path):
    if (os.path.isdir(path) == False):
        # base case:  not a folder, but a file, so return singleton list with its path
        return [path]
    else:
        # recursive case: it's a folder, return list of all paths
        files = [ ]
        for filename in os.listdir(path):
            files += listFiles(path + "/" + filename)
        return files

class ImagesPage (Page):
    #path can be modified according to what folder the user wants to access
    def __init__(self, width, height, path = "DesignT/images"): 
        super().__init__(width, height)
        self.title = "Select and Click Image"
        self.titleSize = 50 
        self.backButton = BackButton (10, 10, 50, 50, "red")
        self.imagePaths = []
        pygameImageExtensions = [".jpg", ".png", ".gif", ".bmp", ".pcx", ".tga", ".tif", ".lbm", ".pbm", ".xpm", ".jpeg"]
        for filepath in listFiles (path): 
            filename, file_extension = os.path.splitext(filepath)
            file_extension= file_extension.lower()
            if (file_extension in pygameImageExtensions):
                self.imagePaths.append(filepath)
        self.imageObjects = []
        self.startX= 10
    def draw (self, screen): 
        #blank the screen
        pygame.draw.rect(screen, pygame.color.THECOLORS["white"], ((0),(0), 
                     self.width, self.height))
        #title
        font = pygame.font.SysFont("microsoftyaheitruetypemicrosoftyaheiui", self.titleSize) 
        inst = font.render(self.title, True, pygame.color.THECOLORS["black"], None) 
        twidth = inst.get_width()
        theight = inst.get_height()
        screen.blit(inst, (120,0))
        
        self.backButton.draw(screen)
        #images
        spaceY = self.height*5/80 
        imageHeight = (self.height-spaceY*5)/4 
        spaceX = self.width*5/80 
        row= 0
        x = self.startX
        y = theight
        for imagePath in self.imagePaths: 
            image =  pygame.image.load(imagePath).convert_alpha()
            imageWidth = image.get_width()*(imageHeight/image.get_height())
            if (x+imageWidth> self.width): 
                #image out of page
                x=self.startX
                row +=1   
            imageObject = Image (imagePath, x, row*(imageHeight+spaceY) +theight, width=imageWidth , height=imageHeight)
            if (len(self.imageObjects)<len(self.imagePaths)): 
                self.imageObjects.append(imageObject)
            imageObject.draw(screen)
            x+= imageWidth +spaceX
    def imageClicked (self, x, y): 
        for image in self.imageObjects: 
            if (image.containsPoint(x,y)):
                return image
        return None
class FilesPage (Page):
    
    def __init__(self, width, height,realT): 
        super().__init__(width, height)
        self.path ="Designs"
        self.title1 = "Select and Click Design"
        self.titleSize = 50 
        self.filepaths = []

        self.realT = realT
        self.backButton = BackButton (10, 10, 50, 50, "red")
        self.startX = 20 
        try:
            for filepath in listFiles (self.path): 
                filename, file_extension = os.path.splitext(filepath)
                if (file_extension == '.txt'):
                    self.filepaths.append(filepath)
            # print (self.filepaths)
        except: 
            pass
        self.title2 = "You Have No Designs"
        font = pygame.font.SysFont("microsoftyaheitruetypemicrosoftyaheiui", self.titleSize) 
        self.inst1 = font.render(self.title1, True, pygame.color.THECOLORS["black"], None) 
        self.inst2 = font.render(self.title2, True, pygame.color.THECOLORS["black"], None) 
        self.twidth = self.inst1.get_width()
        self.theight = self.inst1.get_height()
        self.tshirtButtons = dict()
        #made so that you can reload it back to the screen
        self.tshirtObjects = dict()
        
    def draw (self, screen): 
        pygame.draw.rect(screen, pygame.color.THECOLORS["white"], ((0),(0), 
                     self.width, self.height))
        #title and backButton
        self.backButton.draw(screen)
        if (len(self.filepaths)==0): 
            screen.blit(self.inst2, (120,0))
            self.twidth = self.inst2.get_width()
            self.theight = self.inst2.get_height()
        else: 
            screen.blit(self.inst1,(120,0))
            self.twidth = self.inst1.get_width()
            self.theight = self.inst1.get_height()

        #read all the data and create tshirts, textboxes images (done in draw because of image loading reasons)
        if (len(self.tshirtButtons)<len(self.filepaths)): #prevents from multiple calls
            self.tshirtButtons = dict()
            self.tshirtObjects = dict()
            def readFile (path): 
                with open (path, "rt") as f: 
                    return f.read()
            #drawing every file by it shirt content
            spaceY = self.height*4/80 
            height = (self.height-self.theight - spaceY*5)/4
            spaceX = self.width*4/80 
            row= 0
            x = self.startX
            y = self.theight +10
            for filepath in self.filepaths: 

                tshirtInfo = readFile (filepath)
                textboxes = []
                images = []
                tshirtColor = None
                for line in tshirtInfo.splitlines():
                    if (line.startswith("textbox:")):
                        textbox = line[line.find("textbox:")+ len("textbox:"):]
                        textboxes.append(textbox)
                    elif(line.startswith ("image:")):
                        image = line[line.find("image:")+ len("image:"):]
                        images.append(image)
                    elif(line.startswith("tshirtColor:" )):
                        tshirtColor = line[line.find("tshirtColor:" )+ len("tshirtColor:" ):]
                        #need to convert string to tuple
                        color = []
                        for detail in tshirtColor.split(","):
                            detailNum=  None 
                            if (detail.startswith("(")):
                                detailNum = float(detail[1:])
                            elif(detail.endswith(")")): 
                                detailNum = float(detail[:-1])
                            else: 
                                detailNum = float(detail)
                            color.append(detailNum) 
                        tshirtColor = tuple(color)
                width = height*78/67
                #creating an tshirt button
                if (x+width> self.width): 
                    #image out of page
                    x=self.startX
                    row +=1   
                tshirtButton = Tshirt (x, row*(height+spaceY+10) +y, width, height, tshirtColor)
                self.tshirtButtons[tshirtButton] =[]
                self.tshirtObjects[tshirtButton] = []
                #adding images to tshirt Button
                for image in images: 
                    #convert String Image 
                    imageString = image
                    name = imageString[imageString.find("Image(")+ len("Image("): imageString.find(",")]
                    imageString= imageString[imageString.find(",")+1:]
                    imageX = (imageString [:imageString.find(",")])
                    imageString = imageString[imageString.find(",")+1:]
                    imageX = float(imageX)
                    imageY = (imageString [:imageString.find(",")])
                    imageString = imageString[imageString.find(",")+1:]
                    imageY = float(imageY)
                    imageWidth = (imageString [:imageString.find(",")])
                    imageString = imageString[imageString.find(",")+1:]
                    imageWidth = float(imageWidth)
                    imageHeight = (imageString [:imageString.find(")")])
                    imageHeight = float(imageHeight)  
                    self.tshirtObjects[tshirtButton].append(Image(name,imageX,imageY,imageWidth,imageHeight))
                    imageWidth = imageWidth * tshirtButton.width/self.realT.width
                    imageHeight = imageHeight *tshirtButton.height/self.realT.height

                    imageX = tshirtButton.x+ (imageX - self.realT.x) *tshirtButton.width/self.realT.width
                    imageY = tshirtButton.y+ (imageY - self.realT.y) *tshirtButton.height/self.realT.height
                    image = Image (name, imageX,imageY,imageWidth,imageHeight)
                    self.tshirtButtons[tshirtButton].append(image)
            
                for textbox in textboxes: 
                    #convert String textbox
                    textboxString = textbox
                    textboxX = float(textboxString[textboxString.find("Textbox(")+ len("Textbox("): textboxString.find(",")])
                    textboxString= textboxString[textboxString.find(",")+1:]
                    textboxY = (textboxString [:textboxString.find(",")])
                    textboxString = textboxString[textboxString.find(",")+1:]
                    textboxY = float(textboxY)
                    textboxText = (textboxString [:textboxString.find(",")])
                    textboxString = textboxString[textboxString.find(",")+1:]
                    textboxFont = (textboxString [:textboxString.find(",")])
                    textboxString = textboxString[textboxString.find(",")+1:]
                    textboxTextSize = (textboxString [:textboxString.find(",")])
                    textboxString = textboxString[textboxString.find(",")+1:]
                    textboxTextSize = float(textboxTextSize)  
                    textboxColor = textboxString[textboxString.find("("):-1]

                    color = []
                    for detail in textboxColor.split(","):
                        detailNum=  None 
                        if (detail.startswith("(")):
                            detailNum = float(detail[1:])
                        elif(detail.endswith(")")): 
                            detailNum = float(detail[:-1])
                        else: 
                            detailNum = float(detail)
                        color.append(detailNum) 
                    textboxColor = tuple(color)
                    self.tshirtObjects[tshirtButton].append(Textbox(textboxX, textboxY, textboxText, textboxFont, textboxTextSize, textboxColor))
                    textboxTextSize = textboxTextSize*tshirtButton.height/self.realT.height
                    textboxX = tshirtButton.x+ (textboxX - self.realT.x) *tshirtButton.width/self.realT.width
                    textboxY = tshirtButton.y+ (textboxY - self.realT.y) *tshirtButton.height/self.realT.height
                    textbox = Textbox(textboxX,textboxY , textboxText,textboxFont , textboxTextSize, textboxColor)
                    self.tshirtButtons[tshirtButton].append(textbox)

                x+= width +spaceX
                self.tshirtButtons[tshirtButton].append(filepath)
        #drawing every file by it shirt content
        for tshirtButton in self.tshirtButtons: 
            tshirtButton.draw(screen)
            for tshirtItem in self.tshirtButtons[tshirtButton]: 
                if ( isinstance (tshirtItem, TshirtItem)):
                    tshirtItem.draw(screen)
                elif (type(tshirtItem) == str ): 
                    filepath = tshirtItem
                    filename, file_extension = os.path.splitext(filepath)
                    name = None
                    if (filename.find("/")!=-1): 
                        name = filename[filename.find("/")+1:]
                    else: 
                        name = filename[filename.find("\\")+1:]
                    font = pygame.font.SysFont("microsoftyaheitruetypemicrosoftyaheiuilight",20) 
                    inst = font.render(name, True, pygame.color.THECOLORS["black"], None) 
                    screen.blit(inst, (tshirtButton.x,tshirtButton.y+tshirtButton.height+10))
    def fileClicked(self,x,y): 
        for tshirtButton in self.tshirtButtons: 
            if tshirtButton.containsPoint(x,y): 
                textboxes =[]
                images = []
                for item in self.tshirtObjects[tshirtButton]: 
                    if (isinstance (item,Textbox)): 
                        textboxes.append (item)
                    elif(isinstance (item,Image)): 
                        images.append(item)

                return (tshirtButton.color, textboxes, images)
        return None
    
class ErrorMessage (object): 
    def __init__(self, pwidth, pheight): 
        
        self.width = pwidth 
        self.height= pheight 
        self.title = "Designs are out of border."
        self.instructions = "Please resize into the border"
        self.okButton = Button (self.width/2-30, self.height/2, 60, 50, "gray", "ok")
    def draw(self,screen): 
        font = pygame.font.SysFont("microsoftyaheitruetypemicrosoftyaheiui",20) 
        inst = font.render(self.title, True, pygame.color.THECOLORS["black"], None) 
        inst2 = font.render(self.instructions,True, pygame.color.THECOLORS["black"], None)
        width = inst.get_width() if (inst.get_width()>=inst2.get_width()) else inst2.get_width()
        pygame.draw.rect(screen, pygame.color.THECOLORS["white"], ((self.width/2-width/2)-5,(self.height/2-(inst.get_height()+inst2.get_height()+ self.okButton.height)/2), 
                     width+10, (inst.get_height()+inst2.get_height()+ self.okButton.height)))
        pygame.draw.rect(screen, pygame.color.THECOLORS["black"], ((self.width/2-width/2)-5,(self.height/2-(inst.get_height()+inst2.get_height()+ self.okButton.height)/2), 
                     width+10, (inst.get_height()+inst2.get_height()+ self.okButton.height)), 2)
        screen.blit(inst, ((self.width/2-width/2),(self.height/2-(inst.get_height()+inst2.get_height()+ self.okButton.height)/2)))
        screen.blit(inst2, ((self.width/2-width/2),(self.height/2-(inst.get_height()+inst2.get_height()+ self.okButton.height)/2)+ inst.get_height()))
        self.okButton.draw(screen)
class SaveMessage (object): 
    def __init__(self, pwidth, pheight ): 
        
        self.width = pwidth 
        self.height= pheight 
        self.title = "This design has been saved "
        self.filename = None
        self.instructions = "as " 
        self.okButton = Button (self.width/2-30, self.height/2, 60, 50, "gray", "ok")
    def getName(self): 
        if (self.filename!=None): 
            return self.instructions+self.filename
    def draw(self,screen): 
        font = pygame.font.SysFont("microsoftyaheitruetypemicrosoftyaheiui",20) 
        inst = font.render(self.title, True, pygame.color.THECOLORS["black"], None) 
        inst2 = font.render(self.getName(),True, pygame.color.THECOLORS["black"], None)
        width = inst.get_width() if (inst.get_width()>=inst2.get_width()) else inst2.get_width()
        pygame.draw.rect(screen, pygame.color.THECOLORS["white"], ((self.width/2-width/2)-5,(self.height/2-(inst.get_height()+inst2.get_height()+ self.okButton.height)/2), 
                     width+10, (inst.get_height()+inst2.get_height()+ self.okButton.height)))
        pygame.draw.rect(screen, pygame.color.THECOLORS["black"], ((self.width/2-width/2)-5,(self.height/2-(inst.get_height()+inst2.get_height()+ self.okButton.height)/2), 
                     width+10, (inst.get_height()+inst2.get_height()+ self.okButton.height)), 2)
        screen.blit(inst, ((self.width/2-width/2),(self.height/2-(inst.get_height()+inst2.get_height()+ self.okButton.height)/2)))
        screen.blit(inst2, ((self.width/2-width/2),(self.height/2-(inst.get_height()+inst2.get_height()+ self.okButton.height)/2)+ inst.get_height()))
        self.okButton.draw(screen)


class DesignPygame(object):
    def init(self, fps = 50, title = "Custom Fit"):
        self.fps =fps
        self.title = title 
        self.bgColor = (255,255,255) #may change 
        self.color = None
    def __init__(self, textboxes = [], images = [], tshirt = None, start=True,  width = 800, height =800): 
        pygame.init()
        self.width = width
        self.height= height
        self.spaceX = self.width/60
        self.spaceY = self.height/60
        if (tshirt == None): #starting from no tshirt receiving then make a tshirt
            self.tshirt = Tshirt(self.spaceX, self.height/8+self.spaceY+10 , (self.width*(2/3)-2*self.spaceX), (self.width*(2/3)-2*self.spaceX)*67/78)
        else: 
            self.tshirt = tshirt
        #going through pages    
        self.startPage = StartPage(self.width, self.height)
        self.imagesPage  = ImagesPage(self.width, self.height)
        self.editFontPage = EditFontPage(self.width,self.height)
        self.editColorPage = EditColorPage(self.width, self.height)
        self.filesPage = FilesPage (self.width, self.height, self.tshirt)

        self.isStartPage = start
        self.isImagesPage = False
        self.isEditFontPage = False
        self.isEditColorPage = False
        self.isFilesPage =False
        self.uploadTextbox = False
        self.editTextbox = False
        self.uploadImage = False 
        self.tryItOn = False
        
        
       

        #initializing all buttons
        self.tryItOnButton = TryItOnButton (2*self.width/3, 0, self.width/3, self.height/8, "yellow")
        self.colorTool = ColorTool (self.spaceX,self.tshirt.y + self.tshirt.height+ self.spaceY+2*self.tshirt.space,
            self.tshirt.width, self.height - (self.tshirt.y+self.tshirt.height+4*self.spaceY)) 
        self.openButton = OpenButton(2*self.width/3+self.spaceX,self.tryItOnButton.y + self.tryItOnButton.height + self.spaceY, 
            self.width/3-(2*self.spaceX), 
             (1/6)*(7/8)*self.height -(self.spaceY), "gray")
        self.saveButton = SaveButton(2*self.width/3+self.spaceX,self.openButton.y + self.openButton.height + self.spaceY, 
            self.width/3-(2*self.spaceX), 
             (1/6)*(7/8)*self.height -(self.spaceY), "gray")
        self.imageButton= ImageButton (2*self.width/3+self.spaceX,self.saveButton.y +self.saveButton.height + self.spaceY, 
            self.width/3-(2*self.spaceX), 
             (1/6)*(7/8)*self.height -(self.spaceY), "gray")
        self.loadTextButton = LoadTextButton(2*self.width/3+ self.spaceX, 
            self.imageButton.y +self.imageButton.height+self.spaceY, self.width/3 -(2*self.spaceX),
             (1/6)*(7/8)*self.height -(self.spaceY), "gray")
        self.editTextFontButton = EditTextFontButton(2*self.width/3+ self.spaceX,
            (self.loadTextButton.y +self.loadTextButton.height+ self.spaceY), self.width/3-(2*self.spaceX),
             (1/6)*(7/8)*self.height -2*(self.spaceY), "gray")
        self.editTextColorButton = EditTextColorButton (2*self.width/3+ self.spaceX,
            (self.editTextFontButton.y +self.editTextFontButton.height+ self.spaceY), 
            self.width/3-(2*self.spaceX), (1/6)*(7/8)*self.height -2*(self.spaceY), "gray")
      
       
        self.isError = False
        self.errorMessage = ErrorMessage(self.width,self.height)
        self.saveMessage = SaveMessage(self.width,self.height)
        #features that go into a design of a shirt 
        #the groups will be empty since it will start out as an empty shirt
        self.textBoxes = textboxes
        self.images = images
        self.textboxSelected = None
        self.imageSelected = None
        self.itemResize= False
        self.isSaveSelected = False
        self.isOpenSelected = False
        self.drawSaveMessage=False        

        #color movers

        #going into kinect
        self.outOfBorder = False
        self.playing = True
        
    def getTshirtDesign (self): 
        return (self.textBoxes, self.images, self.tshirt)
    def mousePressed(self, x, y):

        #going through pages 

        if (self.isStartPage==True and self.startPage.startButton.containsPoint(x,y)): 
            self.isStartPage = False

        elif (self.isImagesPage == True): 
            if(self.imagesPage.imageClicked(x,y)!=None): 
                
                selectedImage = self.imagesPage.imageClicked(x,y)
                newImage = Image (selectedImage.name, self.tshirt.borderx, self.tshirt.bordery,selectedImage.width, selectedImage.height)
                
                self.images.append(newImage)
                self.imageSelected = self.images[0]
                self.isImagesPage = False
            elif(self.imagesPage.backButton.containsPoint(x,y)): 
                self.isImagesPage = False
        elif (self.isEditFontPage ==True): 
            if (self.editFontPage.backButton.containsPoint(x,y)): 
                self.isEditFontPage = not self.isEditFontPage
            if (self.editFontPage.fontClicked(x,y)!=None): 
                selectedFont = self.editFontPage.fontClicked(x,y).font
                self.textboxSelected.font = selectedFont
                self.isEditFontPage = not self.isEditFontPage
        elif (self.isEditColorPage): 
            if (self.editColorPage.colorTool.isColorClicked(x,y)): 
                self.editColorPage.textColor = self.editColorPage.colorTool.getColor()
            elif (self.editColorPage.backButton.containsPoint(x,y)): 
                self.isEditColorPage = not self.isEditColorPage
            elif (self.editColorPage.applyButton.containsPoint(x,y)): 
                self.textboxSelected.fontColor = self.editColorPage.textColor
                self.isEditColorPage = not self.isEditColorPage
            elif (self.editColorPage.colorTool.rMover.containsPoint(x,y)): 
                self.editColorPage.colorTool.rMover.isSelected = True
            elif (self.editColorPage.colorTool.gMover.containsPoint(x,y)): 
                self.editColorPage.colorTool.gMover.isSelected = True
            elif (self.editColorPage.colorTool.bMover.containsPoint(x,y)): 
                self.editColorPage.colorTool.bMover.isSelected = True
        elif (self.isFilesPage): 
            if (self.filesPage.backButton.containsPoint(x,y)): 
                self.isFilesPage = not self.isFilesPage
            if (self.filesPage.fileClicked(x,y)!=None): 
                (self.tshirt.color, self.textBoxes, self.images ) = self.filesPage.fileClicked(x,y)
                self.isFilesPage = not self.isFilesPage
        elif (self.loadTextButton. containsPoint(x,y)):
            self.uploadTextbox = True
        elif (self.imageButton.containsPoint(x,y)): 
            self.isImagesPage = True
        elif (self.tryItOnButton.containsPoint(x,y)): 
            self.tryItOn = True
        elif(self.saveButton.containsPoint(x,y)): 
            self.isSaveSelected = True
        elif(self.openButton.containsPoint(x,y)): 
            self.isOpenSelected= True
        elif(self.colorTool.isColorClicked(x,y)): 
            self.tshirt.color = self.colorTool.getColor()
        elif (self.editTextFontButton.containsPoint(x,y) and self.textboxSelected!=None): 
            self.isEditFontPage = True
        elif (self.editTextColorButton.containsPoint(x,y) and self.textboxSelected!=None): 
            self.editColorPage.textbox = self.textboxSelected
            self.editColorPage.backgroundColor= self.tshirt.color
            self.editColorPage.textColor = self.textboxSelected.fontColor
            self.isEditColorPage = True
        elif  (self.colorTool.rMover.containsPoint(x,y)): 
            self.colorTool.rMover.isSelected = True
        elif (self.colorTool.gMover.containsPoint(x,y)):
            self.colorTool.gMover.isSelected = True
        elif (self.colorTool.bMover.containsPoint(x,y)):       
            self.colorTool.bMover.isSelected = True

        #detecting if cloose or resize button is pressed 
        if (self.textboxSelected!=None):
            if self.textboxSelected.isClickClosed(x,y): 
                self.textBoxes.remove(self.textboxSelected)
                self.textboxSelected = None
            elif self.textboxSelected.isClickResize(x,y):   
                self.itemResize = True
        if (self.imageSelected!=None):
            if self.imageSelected.isClickClosed(x,y):
                self.images.remove(self.imageSelected)
                self.imageSelected = None

            elif self.imageSelected.isClickResize(x,y): 
                self.itemResize = True

        
        if (self.isError==True and self.errorMessage.okButton.containsPoint(x,y)): 
            self.isError = not self.isError
        elif (self.drawSaveMessage and self.saveMessage.okButton.containsPoint(x,y)): 
            self.drawSaveMessage=not self.drawSaveMessage

        if (self.isEditFontPage!= True and self.isEditColorPage!=True):     
        #prevent textboxes to be unselected during editing process
            for textbox in self.textBoxes: 
                
                if  textbox.containsPoint(x,y) or textbox.containsPoint2(x,y): 
                    self.textboxSelected = textbox

                    break
                else: 
                    self.textboxSelected = None
        
        for image in self.images: 
            if image.containsPoint(x,y) or image.containsPoint2(x,y): 
                self.imageSelected = image
                break
            else: 
                self.imageSelected = None
    
        
    def mouseReleased(self, x, y):
        self.itemResize= False
        self.editColorPage.colorTool.rMover.isSelected = False 
        self.editColorPage.colorTool.gMover.isSelected = False
        self.editColorPage.colorTool.bMover.isSelected =False
        self.colorTool.rMover.isSelected = False 
        self.colorTool.gMover.isSelected = False
        self.colorTool.bMover.isSelected =False
        pass
    #x, y are the location of when the mouse is not pressed and moving   
    def mouseMotion(self, x, y):
        pass
    #x, y are the location of when the mouse is pressed and moving
    def mouseDrag(self, x, y):
       
        if(self.isEditColorPage):
            if (self.editColorPage.colorTool.rMover.isSelected):
                self.editColorPage.colorTool.rMover.update(x)
            elif (self.editColorPage.colorTool.gMover.isSelected):
                self.editColorPage.colorTool.gMover.update(x)
            elif (self.editColorPage.colorTool.bMover.isSelected):
                self.editColorPage.colorTool.bMover.update(x)
        
        elif (self.textboxSelected!=None): 
            if (self.itemResize ): 
                self.textboxSelected.rescale(y)
            else:
                self.textboxSelected.x = x
                self.textboxSelected.y = y
                if ((self.textboxSelected.x<=self.tshirt.borderx)): 
                    self.textboxSelected.x = self.tshirt.borderx
                if ((self.textboxSelected.x+self.textboxSelected.width>=self.tshirt.borderx+self.tshirt.borderwidth)): 
                    self.textboxSelected.x = self.tshirt.borderx+self.tshirt.borderwidth- self.textboxSelected.width
                if ((self.textboxSelected.y<=self.tshirt.bordery)): 
                    self.textboxSelected.y = self.tshirt.bordery
                if ((self.textboxSelected.y+self.textboxSelected.height>=self.tshirt.bordery+self.tshirt.borderheight)): 
                    self.textboxSelected.y = self.tshirt.bordery+self.tshirt.borderheight- self.textboxSelected.height
        elif (self.imageSelected!=None): 
            if (self.itemResize): 
                self.imageSelected.rescale(x,y)
            else:
                self.imageSelected.x = x
                self.imageSelected.y = y
                if ((self.imageSelected.x<=self.tshirt.borderx)): 
                    self.imageSelected.x = self.tshirt.borderx
                if ((self.imageSelected.x+self.imageSelected.width>=self.tshirt.borderx+self.tshirt.borderwidth)): 
                    self.imageSelected.x = self.tshirt.borderx+self.tshirt.borderwidth- self.imageSelected.width
                if ((self.imageSelected.y<=self.tshirt.bordery)): 
                    self.imageSelected.y = self.tshirt.bordery
                if ((self.imageSelected.y+self.imageSelected.height>=self.tshirt.bordery+self.tshirt.borderheight)): 
                    self.imageSelected.y = self.tshirt.bordery+self.tshirt.borderheight- self.imageSelected.height
       
        elif (self.colorTool.rMover.isSelected):
                self.colorTool.rMover.update(x)
        elif (self.colorTool.gMover.isSelected):
            self.colorTool.gMover.update(x)
        elif (self.colorTool.bMover.isSelected):
            self.colorTool.bMover.update(x)

    def keyPressed(self, code, mod):
        #editing textboxes
        if(self.textboxSelected!=None): 
            if (code == pygame.K_RETURN): 
                self.textboxSelected == None
            else:
                self.textboxSelected.update(code)
        if (self.isEditFontPage== True): 
            
            if (code == pygame.K_UP and self.editFontPage.page>0): 
               
                self.editFontPage.page-=1
            elif (code == pygame.K_DOWN and self.editFontPage.page<self.editFontPage.totalpages): 
                
                self.editFontPage.page+=1
    def keyReleased(self, keyCode, modifier):
        pass


    def timerFired(self, dt):
       
        
        if (self.uploadTextbox ==True):
            newTextbox = Textbox(self.tshirt.borderx, self.tshirt.bordery)
            self.textBoxes.append(newTextbox)
            self.uploadTextbox = not self.uploadTextbox
       
        if (self.isSaveSelected==True): 
            #creating a folder of designs if does not exist
            #code can be modified according to the folder that the programs running in
            pathToFile = os.path.abspath("DesignBoard.py")
            newpath = pathToFile[:pathToFile.find("DesignBoard.py")]+"\Designs"
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            data =""
            (textboxes, images, tshirt) = self.getTshirtDesign()
            for textbox in textboxes: 
                data += "textbox:" + str(textbox)+ "\n"
            for image in images: 
                data+= "image:" + str(image) +"\n"
            data += "tshirtColor:" + str (tshirt.color)
            contentsToWrite = data
            save_path ='Designs'
            # nummber = 
            name_of_file = "Design" +  str (len(self.filesPage.filepaths)+1)
            completeName = os.path.join(save_path, name_of_file+".txt")         
            file1 = open(completeName, "wt")
            file1.write(contentsToWrite)
            file1.close()
            self.filesPage.filepaths.append(completeName)
            self.saveMessage.filename = name_of_file
            self.drawSaveMessage = True
            self.isSaveSelected=not self.isSaveSelected
        if (self.isOpenSelected == True): 
            self.isFilesPage = True
            self.isOpenSelected = not self.isOpenSelected
        if self.tryItOn == True: 
            #make sure all the images are within borders 
            self.outOfBorder=False
            for image in self.images: 
                if ((image.x< int(self.tshirt.borderx) or int(image.x+image.width)>(self.tshirt.borderx + self.tshirt.borderwidth)) 
                    or (image.y<int(self.tshirt.bordery) or int (image.y+image.height)>(self.tshirt.bordery + self.tshirt.borderheight))):
                    self.outOfBorder = True
                    break 

            for textbox in self.textBoxes: 
                if (int(textbox.x)<self.tshirt.borderx or (textbox.x+textbox.width)>int(self.tshirt.borderx + self.tshirt.borderwidth) 
                    or int(textbox.y)<self.tshirt.bordery or (textbox.y+textbox.height)>int(self.tshirt.bordery + self.tshirt.borderheight) ) :
                    self.outOfBorder = True
                    break 
            if (self.outOfBorder): 
                #give error message
                self.isError = True
                self.tryItOn = not self.tryItOn

              
            else: 

                self.playing = False
                
            
        pass










    def redrawAll(self, screen):
       #going through pages ite
        if (self.isStartPage==True): 
            self.startPage.draw(screen)
        elif (self.isImagesPage == True): 
            self.imagesPage.draw(screen)
        elif (self.isEditFontPage==True): 
            self.editFontPage.draw(screen)
        elif(self.isEditColorPage ==True): 
            self.editColorPage.draw(screen)
        elif (self.isFilesPage == True): 
            self.filesPage.draw(screen)
        #main design page
        else: 
            #background
            backgroundColor = (255,255,255) #light gray
            pygame.draw.rect(screen, backgroundColor, (0,0, 
                         self.width, self.height), 0)
            
            self.tshirt.draw(screen)
            self.loadTextButton.draw (screen)
            self.tryItOnButton.draw (screen)
            self.editTextFontButton.draw(screen)
            self.editTextColorButton.draw(screen)
            self.imageButton.draw(screen)
            self.saveButton.draw(screen)
            self.openButton.draw(screen)
            self.colorTool.draw(screen)
            title = "CustomFit"
            font = pygame.font.SysFont("microsoftyaheitruetypemicrosoftyaheiuibold", 80)
            self.title= font.render(title, True, pygame.color.THECOLORS["black"], None)
            screen.blit(self.title, ((self.spaceX),(0)))
            if (self.imageSelected!=None or self.textboxSelected!=None): 
                self.tshirt.draw_tshirtBorders(screen)
                if (self.textboxSelected!=None): 
                    self.textboxSelected.drawIsSelected(screen)
                if (self.imageSelected!=None): 
                    self.imageSelected.drawIsSelected(screen)
            
            for image in self.images: 
                image.draw (screen)
            for textbox in self.textBoxes: 
                textbox.draw (screen)
            if(self.isError): 
                self.errorMessage.draw(screen)
            if (self.drawSaveMessage): 
                self.saveMessage.draw(screen)
    def isKeyPressed(self, key):
        pass
        
    

    """
    Modified Pygame run function
    """
    def run(self):
        clock = pygame.time.Clock()
        self.init()
        screen = pygame.display.set_mode([self.width, self.height])
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        
        self.playing = True
        while self.playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            #making sure that the images and text don't exceed shirt
         
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    self.playing = False
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()
        if (self.tryItOn == True):
            return self.getTshirtDesign()


