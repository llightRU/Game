import pygame
import sys
import random

pygame.mixer.pre_init()
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((432,768))
clock = pygame.time.Clock()
#feature for game
FPS = 32
screen_width = 432
screen_height = 768
game_sprites = {}
game_sounds = {}
background = r'gallery/sprites/bg.png'
pipe = r'gallery/sprites/pipe-green.png'
floor = r'gallery/sprites/floor.png'


game_sprites['bg'] = pygame.image.load(background).convert()
game_sprites['bg'] = pygame.transform.scale(game_sprites['bg'],(screen_width,screen_height))

game_sprites['floor'] = pygame.image.load(floor).convert()
game_sprites['floor'] = pygame.transform.scale(game_sprites['floor'],(screen_width,screen_height*0.2))

bird_down = pygame.transform.scale(pygame.image.load(r'gallery\sprites\yellowbird-downflap.png').convert_alpha(),(51,36))
bird_mid = pygame.transform.scale(pygame.image.load(r'gallery\sprites\yellowbird-midflap.png').convert_alpha(),(51,36))
bird_up = pygame.transform.scale(pygame.image.load(r'gallery\sprites\yellowbird-upflap.png').convert_alpha(),(51,36))
birds = [bird_down,bird_mid,bird_up]
game_sprites['bird'] = birds
bird_index = 0
bird = game_sprites['bird'][bird_index]
bird_rect = game_sprites['bird'][bird_index].get_rect(center =(100,350))
bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap,200)

game_sprites['pipe'] = pygame.image.load(pipe).convert()
game_sprites['pipe'] = pygame.transform.scale(game_sprites['pipe'],(60,500))
pipes = []
pipe_height =[200,300,400]
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe,1200)

game_sprites['over'] = pygame.transform.scale2x(pygame.image.load(r'gallery\sprites\message.png').convert_alpha())
over_rect = game_sprites['over'].get_rect(center =(216,325))

game_sounds['wing'] = pygame.mixer.Sound('gallery\sound\sfx_wing.wav')
game_sounds['point'] = pygame.mixer.Sound('gallery\sound\sfx_point.wav')
game_sounds['die'] = pygame.mixer.Sound('gallery\sound\sfx_die.wav')
game_sounds['hit'] = pygame.mixer.Sound('gallery\sound\sfx_hit.wav')

font = pygame.font.SysFont('arialblack',40)
def text_screen(text,color,x,y):
    screen_text = font.render(text,True,color)
    screen.blit(screen_text,[x,y])

def draw_floor():
    screen.blit(game_sprites['floor'],(floor_x_pos,screen_height*0.8))
    screen.blit(game_sprites['floor'],(floor_x_pos+432,screen_height*0.8))
def create_pipe():
    ran_pipe_pos = random.choice(pipe_height)
    bottom_pipe = game_sprites['pipe'].get_rect(midtop =(450,ran_pipe_pos))
    top_pipe = game_sprites['pipe'].get_rect(midtop =(450,ran_pipe_pos-650))
    return bottom_pipe,top_pipe
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -=5
        if pipe.centerx == 100:
            global score,FPS
            score +=0.5
            FPS +=0.2
            game_sounds['point'].play()
    return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >=600:
            screen.blit(game_sprites['pipe'],pipe)
        else:
            flip_pipe = pygame.transform.flip(game_sprites['pipe'],False,True)
            screen.blit(flip_pipe,pipe)
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            game_sounds['hit'].play()
            return False
    if bird_rect.top <=-75 or bird_rect.bottom >=screen_height*0.8:
        game_sounds['die'].play()
        return False
    return True
def rotate_Bird(bird):
    new_bird = pygame.transform.rotozoom(bird,-bird_movement,1)
    return new_bird
def bird_animation():
    new_bird = game_sprites['bird'][bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird,new_bird_rect


game_active = True
gravity = 2
bird_movement = 0
floor_x_pos =0
score = 0
high_score = 0 

while(1):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement =-20
                game_sounds['wing'].play()
            elif event.key == pygame.K_SPACE and game_active == False:
                game_active =True
                pipes.clear()
                bird_movement=0
                bird_rect.center= (100,250)

        elif event.type == spawnpipe:
                pipes.extend(create_pipe())

        elif event.type == bird_flap:
            if bird_index < 2:
                bird_index +=1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()

    screen.blit(game_sprites['bg'],(0,0))
    if game_active:
        bird_movement += gravity
        rotated_Bird = rotate_Bird(game_sprites['bird'][bird_index])
        bird_rect.centery += bird_movement
        screen.blit(rotated_Bird,bird_rect)
        game_active = check_collision(pipes)
        pipes = move_pipe(pipes)
        draw_pipe(pipes)
    else:
        high_score = score if score > high_score else high_score
        screen.blit(game_sprites['over'],over_rect)
        text_screen("High Score: "+str(int(high_score)),(255,255,255),70,550)
        score = 0

    text_screen("Score: "+str(int(score)),(255,255,255),10,10)    
    floor_x_pos -=1 
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(FPS)