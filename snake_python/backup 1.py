import pygame
import random
import pygame_menu
from pygame_menu import themes


l_direction=['LEFT','RIGHT','UP','DOWN']
def direction_random():
    m=random.randint(0,3)
    return(l_direction[m])

def on_grid_random():
    x=random.randint(1,58)
    y=random.randint(1,58)
    return (x*10,y*10)

def collision(c1,c2):
    return (c1[0]==c2[0]) and (c1[1]==c2[1])

UP=0
RIGHT=1
DOWN=2
LEFT=3

pygame.init()
pygame.display.set_caption('Jogo da cobra')

clock = pygame.time.Clock()



cobra=[(200,200),(210,200),(220,200)]
cobra_skin=pygame.Surface((10,10))
cobra_skin.fill('blue')

#maçãs vermelhas
appleR=pygame.Surface((10,10))
appleR.fill((255,0,0))

#maçãs verdes
appleG=pygame.Surface((10,10))
appleG.fill('green')

#maçãs roxas
appleP=pygame.Surface((10,10))
appleP.fill('purple')


roberto=pygame.Surface((20,20))
roberto.fill('yellow')


my_direction=LEFT

font = pygame.font.Font('freesansbold.ttf', 18)
score=0

#importar música
barulho_colisao1=pygame.mixer.Sound('20279__koops__apple_crunch_16.wav')
barulho_colisao2=pygame.mixer.Sound('smw_lemmy_wendy_falls_out_of_pipe.wav')

def jogo():
    game_over=False
    my_direction=LEFT
    appleR_pos=on_grid_random()
    appleG_pos=on_grid_random()
    appleP_pos=on_grid_random()
    dRoberto=0
    xRoberto=random.randint(0,30)*10
    yRoberto=random.randint(0,58)*10
    score=0
    f=15
    musica_start()
    pygame.mixer.music.play(-1)
    while not game_over:
        clock.tick(f)  # limits FPS to 60
        # poll for events
        # pygame.QUIT event significa que o utilizador clica no X para fechar a janela
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit
    
        #colisão com maçãs vermelhas
        if collision(cobra[0],appleR_pos):
            appleR_pos=on_grid_random()
            cobra.append((0,0))
            f-=3
            score = score + 1
            barulho_colisao1.play()

        #colisão com maçãs verdes
        if collision(cobra[0],appleG_pos):
            appleG_pos=on_grid_random()
            cobra.append((0,0))
            f+=4
            score = score + 1
            barulho_colisao1.play()
    
        #colisão com maçãs roxas
        if collision(cobra[0],appleP_pos) and score>=5:
            appleP_pos=on_grid_random()
            cobra.append((0,0))
            cobra.append((0,0))
            cobra.append((0,0))
            cobra.append((0,0))
            cobra.append((0,0))
            score= score+3
            barulho_colisao1.play()


        #colisão com as bordas
        if cobra[0][0] == 600 or cobra[0][1] == 600 or cobra[0][0] < 0 or cobra[0][1] < 0:
            game_over = True
            break

        #colisão consigo mesma
        for i in range (1,len(cobra)-1):
            if cobra[0][0]==cobra[i][0] and cobra[0][1]==cobra[i][1]:
                game_over=True
                break

        #colisão com o roberto
        for i in range (1,len(cobra)-1):
            if score>=5:
                if (xRoberto==cobra[i][0] and yRoberto==cobra[i][1]) or (xRoberto+10==cobra[i][0] and yRoberto==cobra[i][1]) or (xRoberto==cobra[i][0] and yRoberto+10==cobra[i][1]) or (xRoberto+10==cobra[i][0] and yRoberto+10==cobra[i][1]):
                    barulho_colisao2.play()
                    game_over=True
                    break 

        if game_over:
            break


        #Mudar a direção da cobra
        keys=pygame.key.get_pressed()
        if keys[pygame.K_UP] and my_direction!=DOWN:
            my_direction=UP
        if keys[pygame.K_DOWN] and my_direction!=UP:
            my_direction=DOWN
        if keys[pygame.K_LEFT] and my_direction!=RIGHT:
            my_direction=LEFT
        if keys[pygame.K_RIGHT] and my_direction!=LEFT:
            my_direction=RIGHT
        
        
        
        for i in range(len(cobra)-1,0,-1):
            cobra[i]=(cobra[i-1][0], cobra[i-1][1])
    
        #fazer a cobra andar sempre
        keys = pygame.key.get_pressed()
        if my_direction==UP:
            cobra[0]=(cobra[0][0],cobra[0][1]-10)
        if my_direction==DOWN:
            cobra[0]=(cobra[0][0],cobra[0][1]+10)
        if my_direction==RIGHT:
            cobra[0]=(cobra[0][0]+10,cobra[0][1])
        if my_direction==LEFT:
            cobra[0]=(cobra[0][0]-10,cobra[0][1])

        #mudança de direção roberto
        if score>=5:
            if cobra[0][1]<yRoberto:
                dRoberto='UP'
            elif cobra[0][0]>xRoberto:
                dRoberto='RIGHT'
            elif cobra[0][1]>yRoberto:
                dRoberto='DOWN'
            elif cobra[0][0]<xRoberto:
                dRoberto='LEFT'
            
        


        #fazer o roberto andar
        if dRoberto=='UP':
            yRoberto=yRoberto -5
        if dRoberto=='DOWN':
            yRoberto=yRoberto +5
        if dRoberto=='RIGHT':
            xRoberto=xRoberto +5
        if dRoberto=='LEFT':
            xRoberto=xRoberto -5

        

        screen.fill((0,0,0))
        screen.blit(appleR, appleR_pos)
        screen.blit(appleG,appleG_pos)
     
        if score >=5:
            screen.blit(appleP, appleP_pos)

        if score>=5:
            screen.blit(roberto,(xRoberto,yRoberto))


        #colocar marcador de pontos
        score_font = font.render('Score: %s' % (score), True, (255, 255, 255))
        score_rect = score_font.get_rect()
        score_rect.topleft = (600 - 120, 10)
        screen.blit(score_font, score_rect)

        for pos in cobra:
            screen.blit(cobra_skin,pos)  

        pygame.display.update()

    while game_over==True:
        game_over_font = pygame.font.Font('freesansbold.ttf', 75)
        game_over_screen = game_over_font.render('Game Over', True, (255, 255, 255))
        game_over_rect = game_over_screen.get_rect()
        game_over_rect.midtop = (600 / 2, 10)
        screen.blit(game_over_screen, game_over_rect)
        pygame.display.update()
        pygame.time.wait(500)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

def musica_start():
    match level.get_attribute('musica_type'):
        case 2:
            musica_de_fundo=pygame.mixer.music.load('BoxCat Games - Tricks.mp3')
        case 3:
            musica_de_fundo=pygame.mixer.music.load('Alan Walker - Spectre [NCS Release].mp3')
        case _:
            musica_de_fundo=pygame.mixer.music.load('all-my-fellas-made-with-Voicemod-technology.mp3')


 
def musica_sel(value, musica):
    level.set_attribute('musica_type', musica)

def como_jogar():
    mainmenu._open(como)

pygame.init()

screen = pygame.display.set_mode((600, 600))

mainmenu = pygame_menu.Menu('Menu', 600, 600,
                            theme=themes.THEME_BLUE)
como = pygame_menu.Menu('Como jogar', 600, 600, theme=themes.THEME_BLUE)
mainmenu.add.button('Jogar',jogo)
mainmenu.add.button('Como Jogar', como_jogar)
mainmenu.add.selector('Música:', [('All my fellas', 1), ('Tricks', 2), ('The-Spectre', 3)], onchange=musica_sel)
mainmenu.add.button('Sair', pygame_menu.events.EXIT)
como.add.image('Screenshot 2024-01-16 213844.png')
level = pygame_menu.Menu('Minijogos', 600, 400,
                         theme=themes.THEME_BLUE)


mainmenu.mainloop(screen)

pygame.quit()