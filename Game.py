import pygame
import random 
import time
import numpy
import os 

#initialize pygame
pygame.init()

#set global variables 
gray = (205,210,205)
red = (255,0,0)
blue = (0,0,255)
black = (0,0,0)
WIDTH = 800
HEIGHT = 600
window_size = (WIDTH,HEIGHT)
boxes = []
swap = {0: 1, 1: 0}
#line coordinates x and y 


#define game x and 0 graphics
flame_png_path = os.path.join("assets", "flame.png")
ice_png_path = os.path.join("assets", "ice.png")
fire = pygame.image.load(flame_png_path)
ice = pygame.image.load(ice_png_path)
fire = pygame.transform.scale(fire,(257,200))
ice = pygame.transform.scale(ice,(257,200))

class Line():
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    def return_point_coordinates(self):
        return [[self.x1, self.y1], [self.x2, self.y2]]

class Box():
    def __init__(self, coordinates):
        self.x1 = coordinates[0]
        self.y1 = coordinates[1]
        self.x2 = coordinates[2]
        self.y2 = coordinates[3]
        self.pressed = False
        self.value = None 

    def display_image(self, screen, img_index):
         if(img_index == 1):
            screen.blit(fire, (self.x1, self.y1))
         else:
            screen.blit(ice, (self.x1, self.y1))


line_1 = Line(266,0,266,600) 
line_2 = Line(532,0,532,600)
line_3 = Line(0,200,800,200)
line_4 = Line(0,400,800,400)

coordinates = {'line_1': line_1,
               'line_2': line_2,
               'line_3': line_3,
               'line_4': line_4}

lines = [(266,0,266,600), (532,0,532,600), (0,200,800,200), (0,400,800,400)]


def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

#create the screen
screen = pygame.display.set_mode(window_size)


def populate_box_coordinates():
    outputCoordinatesBox = []
    
    #firstBox
    x,y =line_intersection(coordinates['line_1'].return_point_coordinates(),coordinates['line_3'].return_point_coordinates())
    outputCoordinatesBox.append([0,0,x,y])
    #secondBox
    x,y = line_intersection(coordinates['line_2'].return_point_coordinates(),coordinates['line_3'].return_point_coordinates())
    outputCoordinatesBox.append([266,0,x,y])
    #thirdBox
    outputCoordinatesBox.append([532,0,800,200])
    #forthBox
    x,y = line_intersection([[266,0],[266,600]],[[0,400],[800,400]])
    x8,y8 = x,y
    outputCoordinatesBox.append([0,200,x,y])
    #fifthBox
    x1,y1 = line_intersection([[266,0],[266,600]],[[0,200],[800,200]])
    x5,y5 = line_intersection(coordinates['line_2'].return_point_coordinates(), coordinates['line_4'].return_point_coordinates())
    outputCoordinatesBox.append([x1,y1,x5,y5])
    #sixthBox
    x,y = line_intersection(coordinates['line_2'].return_point_coordinates(), coordinates['line_3'].return_point_coordinates())
    outputCoordinatesBox.append([x,y,coordinates['line_4'].x2,coordinates['line_4'].y2])
    #seventhBox
    outputCoordinatesBox.append([coordinates['line_4'].x1, coordinates['line_4'].y1, coordinates['line_1'].x2, coordinates['line_1'].y2])
    #eigthBox
    outputCoordinatesBox.append([x8,y8, coordinates['line_2'].x2, coordinates['line_2'].y2])
    #ninthBox
    outputCoordinatesBox.append([x5,y5,WIDTH,HEIGHT])
    #test the coordinates
    """ for box in outputCoordinatesBox:
        display_image(1,box[0],box[1]) """
    return outputCoordinatesBox


boxes_coordinates = populate_box_coordinates()
for box_object in boxes_coordinates:
    boxes.append(Box(box_object))


#Title and Icon
pygame.display.set_caption("Tic Tac Toe")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)


def draw_game_screen():
    screen.fill(gray)
    for line in lines:
        #line is in the shape[x1,y1,x2,y2]
        pygame.draw.line(screen,black,(line[0],line[1]),(line[2],line[3]),5)
    for box in boxes:
        box.value = None
        box.pressed = False

def game_validation():
    validation_combs = [[1,2,3], [4,5,6], [7,8,9], [3,5,7], [1,5,9], [1,4,7], [2,5,8], [3,6,9]]
    validation_combs = numpy.array(validation_combs) - 1
    box = boxes[0]
    box_width = coordinates['line_1'].x1 - 5
    box_height = box.y2 - 5
    validation_surface = pygame.Surface((box_width, box_height))
    validation_surface.fill((0,255,0))
    status = False
    
    for combination in validation_combs:
        if(boxes[combination[0]].value == boxes[combination[1]].value == boxes[combination[2]].value
          and boxes[combination[0]].value != None and boxes[combination[1]].value != None and boxes[combination[2]].value != None ):
            display_value = boxes[combination[2]].value
            status = True
            print("Game Won")
            print(f"Winner is {boxes[combination[0] - 1].value}")

            screen.blit(validation_surface, (boxes[combination[0]].x1 + 4, boxes[combination[0]].y1 + 2))
            boxes[combination[0]].display_image(screen, display_value)

            screen.blit(validation_surface, (boxes[combination[1]].x1 + 2, boxes[combination[1]].y1 + 5))
            boxes[combination[1]].display_image(screen, display_value)

            screen.blit(validation_surface, (boxes[combination[2]].x1 + 2, boxes[combination[2]].y1 + 5))
            boxes[combination[2]].display_image(screen, display_value)

    return status 

#main loop variables
run_game = True
firstDrawn = True
graphic_index = random.choice([0,1])
press_cnt = 0
game_status = False

while run_game:
    if(firstDrawn):
        draw_game_screen()
        firstDrawn = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # if the left button is pressed
            if event.button == 1:
                x_mouse, y_mouse = pygame.mouse.get_pos()

                for box in boxes:
                    if(x_mouse > box.x1 and x_mouse < box.x2 and y_mouse > box.y1 and y_mouse < box.y2 and box.pressed == False):
                        image_index = swap[graphic_index]
                        graphic_index = image_index
                        box.display_image(screen, image_index)
                        box.pressed = True
                        box.value = image_index
                        press_cnt += 1
                        break
    
    pygame.display.update()
    if(press_cnt > 4):
        game_status = game_validation()
        pygame.display.update()
    if(game_status):
        pygame.time.delay(2500000)

