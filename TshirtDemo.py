#TshirtDemo.py
# Made by Clement Wong, clementw
from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
from DesignBoard import *

import ctypes
import _ctypes
import pygame
import sys
import math


if sys.hexversion >= 0x03000000:
    import _thread as thread
else:
    import thread

"""
Citation: 
Modification of the Microsoft Kinect Workshop Code

"""
class BackArrow (object):
    def __init__(self): 
        self.colorOn = pygame.color.THECOLORS["red"]
        self.colorOff = pygame.color.THECOLORS["violet"]
    def drawOn (self, screen, frame):
        screenWidth = screen.get_width()
        screenHeight = screen.get_height()
        pygame.draw.polygon(frame, self.colorOn,((screenWidth/16, screenHeight/8), (3*screenWidth/16, screenHeight/16), 
            (3*screenWidth/16,screenHeight/8), (5*screenWidth/16,screenHeight/8), 
            (5*screenWidth/16, 3*screenHeight/16), (3*screenWidth/16, 3*screenHeight/16), 
            (3*screenWidth/16, 2*screenHeight/8), (screenWidth/16, screenHeight/8)))
    def drawOff(self,screen, frame):
        screenWidth = screen.get_width()
        screenHeight = screen.get_height()
        pygame.draw.polygon(frame, self.colorOff, ((screenWidth/16, screenHeight/8), (3*screenWidth/16, screenHeight/16), 
            (3*screenWidth/16,screenHeight/8), (5*screenWidth/16,screenHeight/8), 
            (5*screenWidth/16, 3*screenHeight/16), (3*screenWidth/16, 3*screenHeight/16), 
            (3*screenWidth/16, 2*screenHeight/8), (screenWidth/16, screenHeight/8)))
    def containsPoint(self, x, y, screen): 
        screenWidth = screen.get_width()
        screenHeight = screen.get_height()
        return (screenWidth/16<x<5*screenWidth/16 and 1*screenHeight/16<y<5*screenHeight/16)

class TshirtDisplay(object):
    def __init__(self, textboxes, images, tshirt):
        """
        Settings Code Modified from Microsoft Kinect Workshop
        """
        pygame.init()
        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()
        # Set the width and height of the screen [width, height]
        self._infoObject = pygame.display.Info()
        self._screen = pygame.display.set_mode((self._infoObject.current_w >> 1, self._infoObject.current_h >> 1), 
                                               pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)
        pygame.display.set_caption("Custom Fit")

        # Loop until the user clicks the close button.
        self._done = False

        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()

        # Kinect runtime object, we want only color and body frames 
        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)

        # back buffer surface for getting Kinect color frames, 32bit color, width and height equal to the Kinect color frame size
        self._frame_surface = pygame.Surface((self._kinect.color_frame_desc.Width, self._kinect.color_frame_desc.Height), 0, 32)

        #allows for mulitple bodies
        self._bodies = None

        self.backArrow = BackArrow()
        self.backArrowPressed = False
        self.textboxes = textboxes
        self.images = images
        self.tshirt = tshirt
        self.textboxConversions = dict()
        self.imageConversions = dict()
        for textbox in self.textboxes: 
            conversionX = (textbox.x - self.tshirt.borderx)/self.tshirt.borderwidth
            conversionY = (textbox.y - self.tshirt.bordery)/self.tshirt.borderheight
            conversionHeight = textbox.textSize/self.tshirt.borderheight
            self.textboxConversions[textbox] = (conversionX, conversionY, conversionHeight)
        for image in self.images:
            conversionX = (image.x - self.tshirt.borderx)/self.tshirt.borderwidth
            conversionY = (image.y - self.tshirt.bordery)/self.tshirt.borderheight
            conversionWidth = image.width/self.tshirt.borderwidth
            conversionHeight = image.height/self.tshirt.borderheight
            self.imageConversions[image] = (conversionX, conversionY, conversionWidth, conversionHeight)
    def draw_Tshirt(self, joints, jointPoints):
        #needed joints to draw tshirt 
        tshirtjoints = [PyKinectV2.JointType_Neck, PyKinectV2.JointType_SpineShoulder, 
                    PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_ShoulderRight, PyKinectV2.JointType_ShoulderLeft, 
                    PyKinectV2.JointType_HipRight, PyKinectV2.JointType_HipLeft, PyKinectV2.JointType_ElbowRight, 
                    PyKinectV2.JointType_ElbowLeft]
        
        #getting angle of right arm movement 
        (A1, A2) = (joints[PyKinectV2.JointType_ElbowRight].Position.x, joints[PyKinectV2.JointType_ElbowRight].Position.y)
        (B1, B2) = (joints[PyKinectV2.JointType_ShoulderRight].Position.x, joints[PyKinectV2.JointType_ShoulderRight].Position.y)
        (C1, C2) = (joints[PyKinectV2.JointType_ShoulderRight].Position.x, joints[PyKinectV2.JointType_HipRight].Position.y)
        (BA1, BA2) = (B1-A1, B2 - A2)
        (BC1, BC2) = (B1 - C1, B2 -C2)
        dotProduct = BA1*BC1 + BA2*BC2
        rightArmAngle = 0  
        try: 
            rightArmAngle = math.acos(dotProduct/(((BA1**2+BA2**2)**.5)* (BC1**2 + BC2**2)**.5)) 
        except: 
            pass
       
        #getting angle of left arm movement
        (A1, A2) = (joints[PyKinectV2.JointType_ElbowLeft].Position.x, joints[PyKinectV2.JointType_ElbowLeft].Position.y)
        (B1, B2) = (joints[PyKinectV2.JointType_ShoulderLeft].Position.x, joints[PyKinectV2.JointType_ShoulderLeft].Position.y)
        (C1, C2) = (joints[PyKinectV2.JointType_ShoulderLeft].Position.x, joints[PyKinectV2.JointType_HipLeft].Position.y)
        (BA1, BA2) = (B1-A1, B2 - A2)
        (BC1, BC2) = (B1 - C1, B2 -C2)
        dotProduct = BA1*BC1 + BA2*BC2
        leftArmAngle = 0  
        try: 
            leftArmAngle = math.acos(dotProduct/(((BA1**2+BA2**2)**.5)* (BC1**2 + BC2**2)**.5)) 
        except: 
            pass
        """
        Tracking State code from Kinect Workshop 
        """
        #don't run if the necessary joints are not tracked
        for joint in tshirtjoints: 
            jointState = joints[joint].TrackingState
            if (jointState == PyKinectV2.TrackingState_NotTracked):
                return
            if (jointState == PyKinectV2.TrackingState_Inferred):
                return
        sR = joints[PyKinectV2.JointType_ShoulderRight]
        sL = joints[PyKinectV2.JointType_ShoulderLeft]
        n =  joints[PyKinectV2.JointType_Neck]
        b =  joints[PyKinectV2.JointType_SpineBase]
        actualW = (( sR.Position.x- sL.Position.x)**2 + ( sR.Position.y- sL.Position.y)**2+ ( sR.Position.z- sL.Position.z)**2)**.5
        actualH = (( n.Position.x- b.Position.x)**2 + ( n.Position.y- b.Position.y)**2+ ( n.Position.z- b.Position.z)**2)**.5
        wToH= actualW/actualH
        #all necessary joints should be on the screen so can draw
        (neckX, neckY) =(jointPoints[PyKinectV2.JointType_Neck].x, jointPoints[PyKinectV2.JointType_Neck].y)
        (spineshoulderX, spineshoulderY) = (jointPoints[PyKinectV2.JointType_SpineShoulder].x, jointPoints[PyKinectV2.JointType_SpineShoulder].y)
        (hiprightX, hiprightY )= (jointPoints[PyKinectV2.JointType_ShoulderRight].x, jointPoints[PyKinectV2.JointType_HipRight].y)
        (hipleftX, hipleftY) = (jointPoints[PyKinectV2.JointType_ShoulderLeft].x, jointPoints[PyKinectV2.JointType_HipLeft].y)
        (spinebaseX, spinebaseY) = (jointPoints[PyKinectV2.JointType_SpineBase].x, jointPoints[PyKinectV2.JointType_SpineBase].y)
        (shoulderrightX, shoulderrightY) = (jointPoints[PyKinectV2.JointType_ShoulderRight].x, jointPoints[PyKinectV2.JointType_ShoulderRight].y)
        (shoulderleftX, shoulderleftY)= (jointPoints[PyKinectV2.JointType_ShoulderLeft].x, jointPoints[PyKinectV2.JointType_ShoulderLeft].y)
        (elbowrightX, elbowrightY)  = (jointPoints[PyKinectV2.JointType_ElbowRight].x, jointPoints[PyKinectV2.JointType_ElbowRight].y)
        (elbowleftX, elbowleftY)  = (jointPoints[PyKinectV2.JointType_ElbowLeft].x, jointPoints[PyKinectV2.JointType_ElbowLeft].y)

        #tshirt dimensions from my own measurements and research about the body
        mWidth = 49
        mArmSpace = 20
        mHeight = 67
        mNeck = 14
        mSideHeight = 42
        height = ((neckX - spinebaseX)**2 + (neckY-spinebaseY)**2)**.5
        width = ((shoulderrightX - shoulderleftX)**2 + (shoulderrightY-shoulderleftY)**2)**.5 
        midLeftArmX = (shoulderleftX+elbowleftX)/2
        midLeftArmY = (shoulderleftY+ elbowleftY)/2 
        midRightArmX = (shoulderrightX+elbowrightX)/2
        midRightArmY = (shoulderrightY+ elbowrightY)/2 
        armSpace= (mArmSpace/mWidth)*width
        
        try:
            p1 = (round (neckX - (mNeck/mWidth)*width/2) , round(neckY))
            #leftarmpoints
            p2 = (round(shoulderleftX), round((neckY+spineshoulderY)/2)) 
            p3 = (round(midLeftArmX - armSpace*math.cos(leftArmAngle)/2), round(midLeftArmY - armSpace*math.sin(leftArmAngle)/2))
            
            p4 = (round(midLeftArmX + armSpace*math.cos(leftArmAngle)/2), round(midLeftArmY + armSpace*math.sin(leftArmAngle)/2))

            #right arm points
            p9 = (round(midRightArmX - armSpace*math.cos(rightArmAngle)/2), round(midRightArmY + armSpace*math.sin(rightArmAngle)/2))
            
            p10 = (round(midRightArmX + armSpace*math.cos(rightArmAngle)/2), round(midRightArmY - armSpace*math.sin(rightArmAngle)/2))
            p11 = (round(shoulderrightX), round((neckY+spineshoulderY)/2)) 
            
            p5 = (round(shoulderleftX), round(neckY + (1-mSideHeight/mHeight)*height))
            p6 = (round(shoulderleftX), round(neckY+height-(hiprightY-hipleftY)/2))
            p7 = (round(shoulderrightX), round(neckY+height+(hiprightY-hipleftY)/2))
            p8 = (round(shoulderrightX), round(neckY + (1-mSideHeight/mHeight)*height))
            p12 = (round (neckX + (mNeck/mWidth)*width/2) , round(neckY)) 

       
            #left arm
            pygame.draw.polygon(self._frame_surface, self.tshirt.color, (p2, p3,p4,p5), 0)

            #right arm
            pygame.draw.polygon(self._frame_surface, self.tshirt.color, (p8,p9,p10, p11), 0)
            #main body
            pygame.draw.polygon(self._frame_surface, self.tshirt.color, (p1,p2,p5,p6,p7,p8,p11,p12), 0)
            pygame.draw.polygon(self._frame_surface, pygame.color.THECOLORS["black"], (p1,p2,p3, p4, p5,p6,p7,p8,p9, p10, p11,p12), 1) #outline
            
            #designs 
            #magic numbers based on the porportions of the border used in design border
            borderx = shoulderleftX + (1/52)*width
            bordery = neckY + height*10/67
            borderwidth = width*50/52
            borderheight = height*55/67 
            hipAngle = -math.atan((hipleftY-hiprightY)/(shoulderleftX-shoulderrightX))*360/(2*math.pi)
            
            for image in self.imageConversions: 
                adjustedX = borderwidth * (self.imageConversions[image][0] ) +borderx
                adjustedY = borderheight * (self.imageConversions[image][1] ) +bordery
                adjustedWidth = borderwidth *(self.imageConversions[image][2])
                adjustedHeight = borderheight*(self.imageConversions[image][3])
                adjustedImage = Image (image.name, adjustedX, adjustedY, adjustedWidth, adjustedHeight)
                adjustedImage.image = pygame.transform.rotate(adjustedImage.image, hipAngle)
                adjustedImage.draw(self._frame_surface)
            
            for textbox in self.textboxConversions:

                adjustedX = borderwidth * (self.textboxConversions[textbox][0] ) +borderx
                adjustedY = borderheight *(self.textboxConversions[textbox][1] ) + bordery
                adjustedTextSize = borderheight *(self.textboxConversions[textbox][2])
                adjustedTextbox = Textbox( adjustedX, adjustedY, textbox.text, textbox.font, adjustedTextSize)
                adjustedTextbox.fontColor = textbox.fontColor 
                adjustedTextbox.angle = hipAngle
                adjustedTextbox. widthConversion= (width/height)/(wToH)
                adjustedTextbox.draw(self._frame_surface)
        except: 
            pass
    
    def draw_color_frame(self, frame, target_surface):
        target_surface.lock()
        address = self._kinect.surface_as_array(target_surface.get_buffer())
        ctypes.memmove(address, frame.ctypes.data, frame.size)
        del address
        target_surface.unlock()
    def draw_size (self, joints, jointPoints): 
        try:
            #length is distance between spine shoulder  and spine base 
            (neckX, neckY) =(jointPoints[PyKinectV2.JointType_Neck].x, jointPoints[PyKinectV2.JointType_Neck].y)
            (shoulderleftX, shoulderleftY)= (jointPoints[PyKinectV2.JointType_ShoulderLeft].x, jointPoints[PyKinectV2.JointType_ShoulderLeft].y)
            (x,y) = (round(shoulderleftX),neckY) 
            (x1,y1,z1) = (joints[PyKinectV2.JointType_SpineBase].Position.x, joints[PyKinectV2.JointType_SpineBase].Position.y, joints[PyKinectV2.JointType_SpineBase].Position.z )
            (x2, y2, z2) = (joints[PyKinectV2.JointType_Neck].Position.x, joints[PyKinectV2.JointType_Neck].Position.y, joints[PyKinectV2.JointType_Neck].Position.z )
            length = ((x2-x1)**2 + (y2-y1)**2 + (z2 - z1)**2)**.5
            (shoulderrightX, shoulderrightY, shoulderrightZ) = (joints[PyKinectV2.JointType_ShoulderRight].Position.x, joints[PyKinectV2.JointType_ShoulderRight].Position.y, joints[PyKinectV2.JointType_ShoulderRight].Position.z)
            (shoulderleftX, shoulderleftY, shoulderleftZ)= (joints[PyKinectV2.JointType_ShoulderLeft].Position.x, joints[PyKinectV2.JointType_ShoulderLeft].Position.y, joints[PyKinectV2.JointType_ShoulderLeft].Position.z)
            width = ((shoulderrightX-shoulderleftX)**2 + (shoulderrightY-shoulderleftY)**2 + (shoulderrightZ-shoulderleftZ)**2)**.5
            # print (length, width)
            size = None
            #tshirt measurements based on http://cospaus.com/tshirt_size_chart.html and measuring tshirts
            #length overrules
            if (length/width >62/38): 
                if (.57<length<.63):
                    size = "S"
                elif (.63<length<.67): 
                    size = "M"
                elif (.67<length<.71):
                    size = "L"
                elif (.71<length<.77): 
                    size ="XL"
            #width overrules
            else: 
                if (.30<width<.34):
                    size = "S"
                elif (.34<width<.38): 
                    size = "M"
                elif (.38<width<.42):
                    size = "L"
                elif (.42<width<.46): 
                    size ="xl"
            if (size == None): size = "Size Undermined"
            sizeTextbox = Textbox( x, y, size, "raavi", 50)
            sizeTextbox.x -=sizeTextbox.width
            sizeTextbox.y-=sizeTextbox.height
            pygame.draw.rect(self._frame_surface, (255,255,255), (sizeTextbox.x-10, sizeTextbox.y, sizeTextbox.width+20,sizeTextbox.height), )

            sizeTextbox.draw(self._frame_surface)
        except: 
            pass
    """run function from Microsoft Kinect Workshop Code
    """
    def run(self):
        # -------- Main Program Loop -----------
        while not self._done:
            # --- Main event loop
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self._done = True # Flag that we are done so we exit this loop

                elif event.type == pygame.VIDEORESIZE: # window resized
                    self._screen = pygame.display.set_mode(event.dict['size'], 
                                               pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)
            
            

            # --- Getting frames and drawing  
            if self._kinect.has_new_color_frame():
                frame = self._kinect.get_last_color_frame()
                self.draw_color_frame(frame, self._frame_surface)
                frame = None

            if self._kinect.has_new_body_frame(): 
                self._bodies = self._kinect.get_last_body_frame()
            
            # --- draw tshirts onto _frame_surface
            if self._bodies is not None: 
                for i in range(0, self._kinect.max_body_count):
                    body = self._bodies.bodies[i]
                    if not body.is_tracked: 
                        continue 
                    
                    joints = body.joints 
    
                    joint_points = self._kinect.body_joints_to_color_space(joints) # converts 3D world coordinates to screen coordinates
                    self.draw_size (joints, joint_points)
                    self.draw_Tshirt(joints, joint_points)
                    rhandX = joint_points[PyKinectV2.JointType_HandRight].x 
                    rhandY = joint_points[PyKinectV2.JointType_HandRight].y
                    lhandX = joint_points[PyKinectV2.JointType_HandLeft].x 
                    lhandY = joint_points[PyKinectV2.JointType_HandLeft].y
                    if (self.backArrow.containsPoint(rhandX, rhandY,self._screen) or self.backArrow.containsPoint(lhandX,lhandY, self._screen)): 
                        self.backArrow.drawOn(self._screen, self._frame_surface)
                        
    
                        self._done = True
                        self.backArrowPressed = True
                    else: 
                        self.backArrow.drawOff(self._screen, self._frame_surface)

                  

            
            # --- copy back buffer surface pixels to the screen, resize it if needed and keep aspect ratio
            # --- (screen size may be different from Kinect's color frame size) 
            h_to_w = float(self._frame_surface.get_height()) / self._frame_surface.get_width()
            target_height = int(h_to_w * self._screen.get_width())
            surface_to_draw = pygame.transform.scale(self._frame_surface, (self._screen.get_width(), target_height));
            self._screen.blit(surface_to_draw, (0,0))
            surface_to_draw = None
            pygame.display.update()



            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit to 60 frames per second
            self._clock.tick(60)

        # Close our Kinect sensor, close the window and quit.
        self._kinect.close()
        pygame.quit()
        #reopens DesignBoard
        if (self.backArrowPressed): 
            return True


