import csv
from pickle import TRUE
import random
import sys
import pygame
import numpy

background_color = (251,247,245)
original_grid_element_color = (52, 31, 151)
buffer = 5
def input_matrix(difficult ='easy'):
    matrix=[]
    choice = str(random.randint(1,3))
    file = 'metric'+'/'+difficult+'/'+choice+'.csv'
    with open(file) as f:
        reader = csv.reader(f)
        matrix = [str(row)[2:11] for row in reader if len(row)>0]
        matrix = [list(map(int,row)) for row in matrix] 
        f.close()
    return matrix

grid = input_matrix()
grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]
grid_solve = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]

def insert(win,matrix, position,condition,hint):
    i,j = position[1], position[0]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                if not (pos[0] >=50 and pos[0] <=500 and pos[1]>=50 and pos[1]<=500):
                    print('false')
                    return
            if event.type == pygame.KEYDOWN:
                if(grid_original[i-1][j-1] != 0):
                    return
                if(event.key == 48): #checking with 0
                    matrix[i-1][j-1] = event.key - 48
                    pygame.draw.rect(win, background_color, (position[0]*50 + buffer, position[1]*50+ buffer,50 -2*buffer , 50 - 2*buffer))
                    return
                if(0 < event.key - 48 <10):  #We are checking for valid input
                    value = str(event.key-48)
                    if hint:
                        value = str(grid_solve[i-1][j-1])
                    pygame.draw.rect(win, background_color, (position[0]*50 + buffer, position[1]*50+ buffer,50 -2*buffer , 50 - 2*buffer))
                    if condition and not check(matrix,value,i-1,j-1):
                        text_screen(value,(255,0,0),position[0]*50 +15, position[1]*50,35)
                    else:
                        text_screen(value,(0,0,0),position[0]*50 +15, position[1]*50,35)
                    matrix[i-1][j-1] = value
                    return
                return
def draw_grid():
    for i in range(0,10):
        if(i%3 == 0):
            pygame.draw.line(win, (0,0,0), (50 + 50*i, 50), (50 + 50*i ,500 ), 4 )
            pygame.draw.line(win, (0,0,0), (50, 50 + 50*i), (500, 50 + 50*i), 4 )

        pygame.draw.line(win, (0,0,0), (50 + 50*i, 50), (50 + 50*i ,500 ), 2 )
        pygame.draw.line(win, (0,0,0), (50, 50 + 50*i), (500, 50 + 50*i), 2 )
def text_screen(text,color,x,y,size):
    font = pygame.font.SysFont('Arial',size)
    screen_text = font.render(text,True,color)
    win.blit(screen_text,(x,y))
def print_matrix(matrix):
    for i in range(0, len(matrix[0])):
        for j in range(0, len(matrix[0])):
            if(0<matrix[i][j]<10):
                text_screen(str(matrix[i][j]),original_grid_element_color,(j+1)*50 + 15,(i+1)*50,35)
def check(m, valid, r, c):
    for i in range(9):
        if str(m[r][i]) == str(valid):
            return False
        if str(m[i][c]) == str(valid):
            return False
    it = r//3
    jt = c//3
    for i in range(it * 3, it * 3 + 3):
        for j in range (jt * 3, jt * 3 + 3):
            if str(m[i][j])== str(valid):
                return False
    return TRUE
def time_update():
    tick = pygame.time.get_ticks()
    global sec
    global time
    if tick - sec >=999:
        sec=tick
        time[4] += 1
        if time[4]==10:
            time[4] = 0
            time[3] +=1
            if time[3] ==6:
                time[3] =0
                time[1] +=1
                if time[1] ==10:
                    time[0]+=1
                    time[1]=0

    return ''.join([str(c) for c in time]) 
def menu_game(difficult):
    global grid,grid_original,time,time_dis,sec
    grid = input_matrix(difficult)
    grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]
    win.fill(background_color)
    print_matrix(grid_original)
    draw_grid()
    text_screen('Difficulty:',(0,0,0),20,15,15)
    text_screen('Auto-Check for Mistakes',(192,192,192),200,20,10)
    pygame.draw.rect(win, (51,153,255), (70, 520,50 , 40))
    pygame.draw.rect(win, (0,128,255), (130, 520,50 , 40))
    pygame.draw.rect(win, (51,51,255), (190, 520,50 , 40))
    pygame.draw.rect(win, (0,0,255), (250, 520,50 , 40))
    text_screen('Easy',(0,0,0),80,535,10)
    text_screen('Medium',(0,0,0),130,535,10)
    text_screen('Hard',(0,0,0),200,535,10)
    text_screen('Very Hard',(0,0,0),250,535,10) 
    time = [0,0,':',0,0]
    time_dis = '00:00'
def find_0(m):
    for d in range(len(m)):
        for c in range(len(m[0])):
            if m[d][c] == 0:
                return d, c
    return None
def solve(m):
    tim_thay = find_0(m)
    if not tim_thay:
        return True
    else:
        d, c = tim_thay
    for i in range(1,10):
        if check(m, i, d, c):
            m[d][c] = i
            if solve(m):
                return True
            else:
                m[d][c] = 0 
    return False
def compare(a,b):
    for i in range(9):
        for j in range(9):
            if int(a[i][j])!= int(b[i][j]):
                return False
    return True
def grayscale(img):
    arr = pygame.surfarray.array3d(img)
    #luminosity filter
    avgs = [[(r*0.298 + g*0.587 + b*0.114) for (r,g,b) in col] for col in arr]
    arr = numpy.array([[[avg,avg,avg] for avg in col] for col in avgs])
    return pygame.surfarray.make_surface(arr)
solve(grid_solve)
solved = solve(grid_solve)
pygame.mixer.pre_init()
pygame.init()
win = pygame.display.set_mode((550, 600))
pygame.display.set_caption("Sudoku")
win.fill(background_color)
myfont = pygame.font.SysFont('Comic Sans MS', 35)
win_sound = pygame.mixer.Sound('123.mp3')
sec = 0
time = [0,0,':',0,0]
activate = False
time_dis = '00:00'
game_pause = pygame.image.load('img/pause.png')
game_pause = pygame.transform.scale(game_pause,(450,450))
icon_win =pygame.image.load('img/icon_win.jpg')
icon_win = pygame.transform.scale(icon_win,(450,450))
pause_button = pygame.image.load('img/pauseButton.png')
pause_button = pygame.transform.scale(pause_button,(20,20))
resume_button = pygame.image.load('img/resumeButton.png')
resume_button = pygame.transform.scale(resume_button,(20,20))
auto_check_open = pygame.image.load('img/auto_check_open.png')
auto_check_open = pygame.transform.scale(auto_check_open,(20,20))
auto_check = pygame.image.load('img/auto_check.png')
auto_check = pygame.transform.scale(auto_check,(20,20))
hint = pygame.image.load('img/hint.png')
hint = pygame.transform.scale(hint,(40,50))
hint_off = grayscale(hint)
win.fill(background_color)
print_matrix(grid_original)
draw_grid()            
condition = False
c_hint = False
passed = False
difficult = 'easy'
text_screen('Difficulty:',(0,0,0),20,15,15)
text_screen('Auto-Check for Mistakes',(192,192,192),200,20,10)
pygame.draw.rect(win, (51,153,255), (70, 520,50 , 40))
pygame.draw.rect(win, (0,128,255), (130, 520,50 , 40))
pygame.draw.rect(win, (51,51,255), (190, 520,50 , 40))
pygame.draw.rect(win, (0,0,255), (250, 520,50 , 40))
text_screen('Easy',(0,0,0),80,535,10)
text_screen('Medium',(0,0,0),130,535,10)
text_screen('Hard',(0,0,0),200,535,10)
text_screen('Very Hard',(0,0,0),250,535,10) 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if  passed:
                pygame.mixer.stop()
                menu_game(difficult)
                passed = False
            pos = pygame.mouse.get_pos()
            if pos[0] >= 70 and pos[0]<=120 and pos[1] >=520 and pos[1]<=560:
                difficult='easy'
                menu_game(difficult)
            elif pos[0] >= 130 and pos[0]<=180 and pos[1] >=520 and pos[1]<=560:
                difficult='medium'
                menu_game(difficult)
            elif pos[0] >= 190 and pos[0]<=240 and pos[1] >=520 and pos[1]<=560:
                difficult='hard'
                menu_game(difficult)
            elif pos[0] >= 250 and pos[0]<=300 and pos[1] >=520 and pos[1]<=560:
                difficult='veryHard'
                menu_game(difficult)
            elif pos[0] >=50 and pos[0] <=500 and pos[1]>=50 and pos[1]<=500:
                insert(win, grid,(pos[0]//50, pos[1]//50),condition,c_hint)
            elif pos[0] >=500 and pos[0] <=520 and pos[1] >=15 and pos[1] <=35:
                if activate ==True:
                    activate =False
                else:
                    activate = True
            elif pos[0] >=320 and pos[0]<=340 and pos[1]>=15 and pos[1]<=35:
                if condition ==True:
                    condition=False
                else:
                    condition = True
            elif pos[0] >=0 and pos[0]<=40 and pos[1]>=50 and pos[1]<=100:
                if difficult !='easy':
                    continue
                if c_hint ==True:
                    c_hint=False
                else:
                    if solved:
                        c_hint = True
    if compare(grid,grid_solve):
        passed = True
        win_sound.play(3)
        win.blit(icon_win,(50,50))
        text_screen('Congratulation',(255,0,0),120,300,50)    
    if c_hint:
        win.blit(hint,(0,50))
    else:
        win.blit(hint_off,(0,50))
    if condition:
        win.blit(auto_check_open,(320,15))
    else:
        win.blit(auto_check,(320,15))
    if activate:
        win.blit(pause_button,(500,15))
        time_dis = time_update()
    else:
        win.blit(resume_button,(500,15))
        sec = pygame.time.get_ticks()
    pygame.draw.rect(win, background_color, (85, 15,100 , 20))
    text_screen(difficult,(192,192,192),85,15,15)
    text_screen('Only Valid',(255,0,0),2,120,10)
    text_screen('for easy',(255,0,0),2,130,10)
    text_screen('mode',(255,0,0),2,140,10)
    pygame.draw.rect(win, background_color, (460, 17,35 ,20))
    text_screen(time_dis,(192,192,192),460,17,13)
    pygame.display.update()
   