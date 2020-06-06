import math
import numpy as np
import cv2
import imutils
from PIL import ImageGrab as ig
from PIL import Image
import time
import pyautogui as pag
import os
from skimage.measure import compare_ssim
from pynput.mouse import Button, Controller

class minesweeper_bot:
    def __init__(self):
        self.screenXStart = 10
        self.screenYStart = 120
        self.screenWidth = 620
        self.screenHeight = 450

        self.gameImages = 'C:/programozas/python/opencv_minesweeper/images/game'
        self.botImgsPath = 'C:/programozas/python/opencv_minesweeper/images/bot'


        self.start = False
        self.startTime = time.time()

        self.totalShapes = 0
        self.squares = 0
        self.otherShapes = 0

        self.xs = [0] * 480
        self.ys = [0] * 480

        self.putFlagsOn = []
        self.put_flag = ''
        self.destroyWalls = []

        rnum = np.random.randint(0, 480)
        ideiglenes = 13 * 30 + 5

        # 0 - number, 1 - X, 2 - Y, 3 - position in string, 4 - neighbors, 5 - neighbors positions[], 6 - self image, 7 - self type
        """
        neighbor positions:
        0 1 2
        3   4
        5 6 7

        exists(?), square number, neighbor type

        neighbor types:
        0 - empty
        1 - 1
        2 - 2
        3 - 3
        4 - 4
        5 - 5
        6 - 6
        7 - 7
        8 - 8
        9 - wall
        10 - flag
        11 - nn_flag
        12 - bomb
        13 - bomb_activated
        """
        self.testSquare = [0, 0, 0, 'not defined', 0, [[False, 0, 0]] * 8, None, 'not defined']
        self.neighborImgs = [None] * 8

    
    def image_setup(self):
        cv2.imwrite('images/bot/5.jpg', self.testSquare[6])
    
    def checking(self):
        self.originalscreen = cv2.cvtColor(np.array(self.printscreen_pil), cv2.COLOR_BGR2RGB)

        copyScreen = self.originalscreen.copy()

        testX = self.xs[self.testSquare[0]]
        testY = self.ys[self.testSquare[0]]
        test_square = self.testSquare[0] + 1
        size = 19

        neighbor_topLeft = [True, test_square + 30, 0]
        neighbor_topMid = [True, test_square + 29, 0]
        neighbor_topRight = [True, test_square + 28, 0]
        neighbor_left = [True, test_square, 0]
        neighbor_right = [True, test_square - 2, 0]
        neighbor_bottomLeft = [True, test_square - 30, 0]
        neighbor_bottomMid = [True, test_square - 31, 0]
        neighbor_bottomRight = [True, test_square - 32, 0]
        neighbor_no = [False, 0, 0]

        neighbors = [neighbor_topLeft, neighbor_topMid, neighbor_topRight, neighbor_left, neighbor_right, neighbor_bottomLeft, neighbor_bottomMid, neighbor_bottomRight]

        # Top left
        if test_square > 450 and (test_square % 30) == 0:
            self.resized = copyScreen[testY:testY + size * 2, testX:testX + size * 2]
            self.testSquare[3] = 'Top left'
            self.testSquare[4] = 3
            self.testSquare[5][0] = neighbor_no
            self.testSquare[5][1] = neighbor_no
            self.testSquare[5][2] = neighbor_no
            self.testSquare[5][3] = neighbor_no
            self.testSquare[5][5] = neighbor_no

            self.testSquare[5][4] = neighbors[4]
            self.testSquare[5][6] = neighbors[6]
            self.testSquare[5][7] = neighbors[7]

        
        # Top right
        elif test_square > 450 and ((test_square - 1) % 30) == 0:
            self.resized = copyScreen[testY:testY + size * 2, testX - size:testX + size]
            self.testSquare[3] = 'Top right'
            self.testSquare[4] = 3

            self.testSquare[5][0] = neighbor_no
            self.testSquare[5][1] = neighbor_no
            self.testSquare[5][2] = neighbor_no
            self.testSquare[5][4] = neighbor_no
            self.testSquare[5][7] = neighbor_no


            self.testSquare[5][3] = neighbors[3]
            self.testSquare[5][5] = neighbors[5]
            self.testSquare[5][6] = neighbors[6]

        # Top
        elif test_square > 450:
            self.resized = copyScreen[testY:testY + size * 2, testX - size:testX + size * 2]
            self.testSquare[3] = 'Top'
            self.testSquare[4] = 5

            self.testSquare[5][0] = neighbor_no
            self.testSquare[5][1] = neighbor_no
            self.testSquare[5][2] = neighbor_no


            self.testSquare[5][3] = neighbors[3]
            self.testSquare[5][4] = neighbors[4]
            self.testSquare[5][5] = neighbors[5]
            self.testSquare[5][6] = neighbors[6]
            self.testSquare[5][7] = neighbors[7]


        # Bottom left
        elif test_square <= 30 and (test_square % 30) == 0:
            self.resized = copyScreen[testY - size:testY + size, testX:testX + size * 2]
            self.testSquare[3] = 'Bottom left'
            self.testSquare[4] = 3

            self.testSquare[5][0] = neighbor_no
            self.testSquare[5][3] = neighbor_no
            self.testSquare[5][5] = neighbor_no
            self.testSquare[5][6] = neighbor_no
            self.testSquare[5][7] = neighbor_no


            self.testSquare[5][1] = neighbors[1]
            self.testSquare[5][2] = neighbors[2]
            self.testSquare[5][4] = neighbors[4]

        
        # Bottom right
        elif test_square < 30 and ((test_square - 1) % 30) == 0:
            self.resized = copyScreen[testY - size:testY + size, testX - size:testX + size]
            self.testSquare[3] = 'Bottom right'
            self.testSquare[4] = 3

            self.testSquare[5][2] = neighbor_no
            self.testSquare[5][4] = neighbor_no
            self.testSquare[5][5] = neighbor_no
            self.testSquare[5][6] = neighbor_no
            self.testSquare[5][7] = neighbor_no

            self.testSquare[5][0] = neighbors[0]
            self.testSquare[5][1] = neighbors[1]
            self.testSquare[5][3] = neighbors[3]

        # Left
        elif (test_square % 30) == 0:
            self.resized = copyScreen[testY - size:testY + size * 2, testX:testX + size * 2]
            self.testSquare[3] = 'Left'
            self.testSquare[4] = 5

            self.testSquare[5][0] = neighbor_no
            self.testSquare[5][3] = neighbor_no
            self.testSquare[5][5] = neighbor_no

            self.testSquare[5][1] = neighbors[1]
            self.testSquare[5][2] = neighbors[2]
            self.testSquare[5][4] = neighbors[4]
            self.testSquare[5][6] = neighbors[6]
            self.testSquare[5][7] = neighbors[7]

        
        # Right
        elif ((test_square - 1) % 30) == 0:
            self.resized = copyScreen[testY - size:testY + size * 2, testX - size:testX + size]
            self.testSquare[3] = 'Right'
            self.testSquare[4] = 5

            self.testSquare[5][2] = neighbor_no
            self.testSquare[5][4] = neighbor_no
            self.testSquare[5][7] = neighbor_no

            self.testSquare[5][0] = neighbors[0]
            self.testSquare[5][1] = neighbors[1]
            self.testSquare[5][3] = neighbors[3]
            self.testSquare[5][5] = neighbors[5]
            self.testSquare[5][6] = neighbors[6]

        
        # Bottom
        elif test_square < 30:
            self.resized = copyScreen[testY - size:testY + size, testX - size:testX + size * 2]
            self.testSquare[3] = 'Bottom'
            self.testSquare[4] = 5

            self.testSquare[5][5] = neighbor_no
            self.testSquare[5][6] = neighbor_no
            self.testSquare[5][7] = neighbor_no

            self.testSquare[5][0] = neighbors[0]
            self.testSquare[5][1] = neighbors[1]
            self.testSquare[5][2] = neighbors[2]
            self.testSquare[5][3] = neighbors[3]
            self.testSquare[5][4] = neighbors[4]

        
        # Anywhere else
        else:
            self.resized = copyScreen[testY - size:testY + size * 2, testX - size:testX + size * 2]
            self.testSquare[3] = 'Center'
            self.testSquare[4] = 8
            self.testSquare[5][0] = neighbors[0]
            self.testSquare[5][1] = neighbors[1]
            self.testSquare[5][2] = neighbors[2]
            self.testSquare[5][3] = neighbors[3]
            self.testSquare[5][4] = neighbors[4]
            self.testSquare[5][5] = neighbors[5]
            self.testSquare[5][6] = neighbors[6]
            self.testSquare[5][7] = neighbors[7]
        
        # Creating self image
        self.testSquare[6] = self.originalscreen.copy()[testY:testY + size, testX:testX + size]

        # Putting True flags
        for i in range(8):
            if self.testSquare[5][i][1] != 0 and self.testSquare[5][i][2] != 0:
                self.testSquare[5][i][1] = True
        
        # Creating neighbor images
        i = 0
        for elements in self.testSquare[5]:
            if elements[0] == True:
                neighborNumber = elements[1]
                X = self.xs[neighborNumber]
                Y = self.ys[neighborNumber]
                neighborImg = copyScreen
                neighborImg = neighborImg[Y:Y + size, X:X + size]
                self.neighborImgs[i] = neighborImg
                i += 1
            else:
                self.neighborImgs[i] = None
                i += 1
        
        # Checking for self type
        


    def self_type_check(self):
        scores = []
        names = []
        for imgName in os.listdir(self.botImgsPath):
            botImg = cv2.cvtColor(np.array(Image.open(self.botImgsPath + '/' + imgName)), cv2.COLOR_BGR2RGB)
            (score, diff) = compare_ssim(botImg, self.testSquare[6], full=True, multichannel=True)
            scores.append(score)
            names.append(imgName[0:-4])
        self_type = names[scores.index(max(scores))]

        if self_type == 'wall':
            self_type = 9
        elif self_type == 'flag':
            self_type = 10
        elif self_type == 'nn-flag':
            self_type = 11
        elif self_type == 'bomb':
            self_type = 12
        elif self_type == 'bomb_activated':
            self_type = 13
        else:
            self_type = int(self_type)
        
        self.testSquare[7] = self_type

    
    def neighbors_type_check(self):
        i = 0
        for img in self.neighborImgs:
            try:
                if img == None:
                    i += 1
            except:
                scores = []
                names = []
                for imgName in os.listdir(self.botImgsPath):
                    botImg = cv2.cvtColor(np.array(Image.open(self.botImgsPath + '/' + imgName)), cv2.COLOR_BGR2RGB)
                    (score, diff) = compare_ssim(botImg, img, full=True, multichannel=True)
                    scores.append(score)
                    names.append(imgName[0:-4])
                neighbor_type = str(names[scores.index(max(scores))])

                if neighbor_type == 'wall':
                    neighbor_type = 9
                elif neighbor_type == 'flag':
                    neighbor_type = 10
                elif neighbor_type == 'nn-flag':
                    neighbor_type = 11
                elif neighbor_type == 'bomb':
                    neighbor_type = 12
                elif neighbor_type == 'bomb_activated':
                    neighbor_type = 13
                else:
                    neighbor_type = int(neighbor_type)

                self.testSquare[5][i][2] = neighbor_type

                i += 1

    
    def debug_screen_setup(self):
        bottom = 800
        gaps = 40
        black_screen = np.zeros((bottom + 20, 500, 3), np.uint8)

        tShapes = 'Total Shapes: ' + str(self.totalShapes)
        tSquares = 'Squares: ' + str(self.squares)
        tOthers = 'Others: ' + str(self.otherShapes)
        try:
            runtime = 'Runtime: ' + str(int((time.time() - self.startTime))) + ' seconds'
            testSquareNumber = 'Test Square: ' + str(self.testSquare[0])
            testSquarePosX = 'Test Square X: ' + str(self.testSquare[1])
            testSquarePosY = 'Test Square Y: ' + str(self.testSquare[2])
            testSquarePosition = 'Position: ' + self.testSquare[3]
            testSquareNeighbors = 'Neighbors: ' + str(self.testSquare[4])
            testSquareType = 'Type: ' + str(self.testSquare[7])
            putFlag = 'Put flag: ' + self.put_flag

            texts = [runtime, tOthers, tSquares, tShapes, testSquarePosY, testSquarePosX, testSquareNumber, testSquarePosition, testSquareNeighbors, testSquareType, putFlag]

            """for i in range(8):
                if self.testSquare[5][i][0]:
                    texts.append(('Neighbor ' + str(i) + ': ' + str(self.testSquare[5][i][0])) + ' | ' + str(self.testSquare[5][i][1]))"""

            for i in range(8):
                texts.append(('Neighbor ' + str(i) + ': ' + str(self.testSquare[5][i][0])) + ' | ' + str(self.testSquare[5][i][1]) + ' | ' + str(self.testSquare[5][i][2]))

            count = 0

            for text in texts:
                if count != 0:
                    cv2.putText(black_screen, text, (10, bottom - gaps * count), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                else:
                    cv2.putText(black_screen, text, (10, bottom), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                count += 1
        except:
            pass

        self.debug_screen = black_screen


    def edge_detection(self, img):
        self.gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return cv2.Canny(self.gray, 1, 300)
    
    def shape_detection(self):
        self.totalShapes = 0
        self.squares = 0
        self.otherShapes = 0

        self.shape_img = self.originalscreen

        _, thresh = cv2.threshold(self.gray, 100, 200, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        squareShapes = [0] * 480

        for i, contour in enumerate(contours):
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
            cv2.drawContours(self.shape_img, [approx], 0, (0, 255, 0), 2)
            self.totalShapes += 1


            if len(approx) == 4 and cv2.contourArea(contour) < 300:
                try:
                    squareShapes[self.squares] = i
                except:
                    pass
                self.squares += 1
                try:
                    self.xs[self.squares - 1] = approx.ravel()[0]
                    self.ys[self.squares - 1] = approx.ravel()[1]
                except:
                    pass
                cv2.drawContours(self.shape_img, [approx], 0, (255, 0, 0), 2)
                """if i == self.testSquare:
                    cv2.drawContours(self.shape_img, [approx], 0, (0, 0, 155), 2)
                else:
                    cv2.drawContours(self.shape_img, [approx], 0, (255, 0, 0), 2)"""
            else:
                self.otherShapes += 1
        
        # Drawing focused square
        approx = cv2.approxPolyDP(contours[squareShapes[self.testSquare[0]]], 0.02 * cv2.arcLength(contour, True), True)
        cv2.drawContours(self.shape_img, [approx], 0, (0, 0, 155), 2)
        self.testSquare[1] = self.xs[self.testSquare[0]]
        self.testSquare[2] = self.ys[self.testSquare[0]]
        
        # Drawing neighbors
        try:
            for neighbor in self.testSquare[5]:
                if neighbor[0]:
                    approx = cv2.approxPolyDP(contours[squareShapes[neighbor[1]]], 0.02 * cv2.arcLength(contour, True), True)
                    cv2.drawContours(self.shape_img, [approx], 0, (100, 150, 255), 2)
        except Exception as e:
            print(e)
        
        # Drawing should-flagged squares
        for should_flagged_pos in self.putFlagsOn:
            approx = cv2.approxPolyDP(contours[squareShapes[should_flagged_pos]], 0.02 * cv2.arcLength(contour, True), True)
            cv2.drawContours(self.shape_img, [approx], 0, (255, 255, 255), 2)
    
    def neighbors_screen_setup(self):
        imgs = []
        for img in self.neighborImgs:
            try:
                if img == None:
                    pass
                else:
                    print('d')
            except:
                img = cv2.resize(img, (17, 17))
                imgs.append(img)
                
        # Neighbor images in one window
        self.neighbors_screen = np.concatenate(imgs, axis=0)
    
    def check_for_available_marking(self):
        if self.testSquare[7] < 9:
            i = 0
            self_type = self.testSquare[7]
            walls = [0] * 8
            flags = [0] * 8
            others = [0] * 8
            for neighbor in self.testSquare[5]:
                if neighbor[0]:
                    if neighbor[2] == 9:
                        walls[i] += 1
                    elif neighbor[2] == 10:
                        flags[i] += 1
                    elif neighbor[2] < 9:
                        others[i] += 1
                    i += 1
                else:
                    i += 1
            
            #print(f'walls: {sum(walls)}\nflags: {sum(flags)}\nothers: {sum(others)}\n')

            if (self_type - sum(flags)) == 0:
                self.put_flag = 'no need'
                flag_pos = []

                flagged = 0
                for flag in flags:
                    if flag:
                        flag_pos.append(flagged)
                    flagged += 1
                
                #print(flag_pos)

                for pos in flag_pos:
                    i = 0
                    for neighbor in self.testSquare[5]:
                        if pos == i:
                            if (self.putFlagsOn.count(neighbor[1])) == 1:
                                self.putFlagsOn.remove(neighbor[1])
                            i += 1
                        else:
                            i += 1
                
                walls_to_destroy = []

                wall_pos = 0
                for wall in walls:
                    if wall:
                        walls_to_destroy.append(wall_pos)
                    wall_pos += 1
                
                for pos in walls_to_destroy:
                    i = 0
                    for neighbor in self.testSquare[5]:
                        if pos == i:
                            if (self.destroyWalls.count(neighbor[1])) == 0:
                                self.destroyWalls.append(neighbor[1])
                            i += 1
                        else:
                            i += 1
                #print(f'destroyWalls: {self.destroyWalls}')
            elif (self_type - (sum(walls) + sum(flags))) == 0:
                self.put_flag = 'put flag'

                should_flag_pos = []
                has_to_flag = False
                wall_pos = 0
                for wall in walls:
                    if wall:
                        should_flag_pos.append(wall_pos)
                        has_to_flag = True
                    wall_pos += 1
                #print(f'should_flag_pos: {should_flag_pos}')
                for pos in should_flag_pos:
                    i = 0
                    for neighbor in self.testSquare[5]:
                        if pos == i:
                            if (self.putFlagsOn.count(neighbor[1])) == 0:
                                self.putFlagsOn.append(neighbor[1])
                            i += 1
                        else:
                            i += 1
                #print(self.putFlagsOn)

            elif sum(walls) == 0:
                self.put_flag = 'no need'
            elif (sum(walls) - self_type) > 0:
                self.put_flag = 'unsure'
            #print(self.putFlagsOn)
        else:
            self.put_flag = 'wall'
        
    
    def change_focusSquare(self):
        if self.testSquare[0] < 479:
            self.testSquare[0] += 1
        else:
            self.testSquare[0] = 0
    
    
    def flag_it(self):
        mouse = Controller()
        for pos in self.putFlagsOn:
            X = self.xs[pos] + self.screenXStart + 7
            Y = self.ys[pos] + self.screenYStart + 7
            mouse.position = (X, Y)
            mouse.click(Button.right)
            self.putFlagsOn.remove(pos)

    def destroy_walls(self):
        mouse = Controller()
        for pos in self.destroyWalls:
            X = self.xs[pos] + self.screenXStart + 7
            Y = self.ys[pos] + self.screenYStart + 7
            mouse.position = (X, Y)
            mouse.click(Button.left)
            self.destroyWalls.remove(pos)
    
    def run_commands(self):
        # Get the screenshot
        self.printscreen_pil = ig.grab(bbox=(self.screenXStart, self.screenYStart, self.screenWidth, self.screenHeight))

        # Turn the screenshot into a numpy array
        self.printscreen_numpy = cv2.cvtColor(np.array(self.printscreen_pil), cv2.COLOR_BGR2RGB)

        # Saving the original screenshot as another variable, leaving the previous one as a backup
        self.originalscreen = self.printscreen_numpy

        # Edge detection, then showing it
        self.edge_img = self.edge_detection(self.originalscreen)

        # Shape detection, then showing it
        self.shape_detection()

        # Reset screen
        self.originalscreen = cv2.cvtColor(np.array(self.printscreen_pil), cv2.COLOR_BGR2RGB)

        # Setting up debug screen
        self.debug_screen_setup()

        # Understanding the focus-square and its neighbors
        self.checking()
        self.self_type_check()
        self.neighbors_type_check()
        self.check_for_available_marking()
        self.flag_it()
        self.destroy_walls()

        
        
        #self.check_for_available_marking()

        # Setting up neighbors screen
        self.neighbors_screen_setup()

        # Change to the next square
        self.change_focusSquare()

        
    
    def draw(self):
        # Showing original screenshot
        cv2.imshow('original', self.originalscreen)

        # Showing edge detection screen
        cv2.imshow('edge', self.edge_img)

        # Showing the gray-scale image
        cv2.imshow('gray', self.gray)

        # Showing shape detection screen
        cv2.imshow('shapes', self.shape_img)
        
        # Showing debug screen
        cv2.imshow('text', self.debug_screen)

        # Showing focus-square and its neighbors
        cv2.imshow('resized', self.resized)
        
        # Showing neighbors only
        cv2.imshow('neighbors', self.neighbors_screen)

        # Self image
        cv2.imshow('Self image', self.testSquare[6])
            

bot = minesweeper_bot()
timeShow = False
timeStamp = time.time()
randomOn = False

os.system('cls')
while(True):
    timeBefore = time.time()
    bot.run_commands()
    bot.draw()
    timeTook = time.time() - timeBefore
    timeNow = time.time()
    if (timeNow - timeStamp) > 2 and randomOn:
        bot.testSquare[0] = np.random.randint(0, 480)
        timeStamp = timeNow
    if timeShow:
        print(timeTook)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
    elif cv2.waitKey(20) & 0xFF == ord('s'):
        bot.start = True
    elif cv2.waitKey(20) & 0xFF == ord('t'):
        timeShow = (not timeShow)
        

"""mouseX = bot.xs[bot.putFlagsOn[0]] + bot.screenXStart
mouseY = bot.ys[bot.putFlagsOn[0]] + bot.screenYStart
bot.change_mouse_position(mouseX + 7, mouseY + 7)"""
#bot.image_setup()