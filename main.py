import pygame
from background import Background
import math
import time

pygame.init()
pygame.mixer.init()

WIDTH , HEIGHT = 800 , 600
win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Brick Breaker')


fonte_8bit = pygame.font.Font('fonte\8-BIT WONDER.TTF', 27) #fonte 8-bit

FPS = 120
platform_width = 100
platform_height = 15
ball_radius = 30
FONTE_VIDAS = pygame.font.SysFont("arial", 25)
humberto_img = pygame.image.load('assets/img/1berto.png').convert_alpha()
humberto_img_small = pygame.transform.scale(humberto_img, (60, 60))
som_acerto_tijolo = pygame.mixer.Sound('efeitos sonoros\hit_sound.wav')
som_acerto_tijolo.set_volume(0.2)

class Platform: #plataforma
    VEL = 5

    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self,win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(win, (255, 255, 255), (self.x - 2, self.y - 2, self.width + 4, self.height + 4))
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def movement(self, direction=1):
        self.x = self.x + self.VEL * direction

class Ball: #bola
    VEL = 5

    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.alpha = 0
        self.x_vel = 2
        self.y_vel = -self.VEL


    def movement(self): #movimento da bola
        self.x += self.x_vel
        self.y += self.y_vel

    def set_velocity(self,x_vel,y_vel): #vel da bola
        self.x_vel = x_vel
        self.y_vel = y_vel

    def draw(self,win): #desenha a bolinha
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)


class Tijolos():
    def __init__(self, x, y, largura, altura, vida, cores):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.vida = 2
        self.vida_maxima = vida
        self.cores = cores
        self.cor = cores[0]

    def draw(self, win):
        pygame.draw.rect(win, self.cor, (self.x, self.y, self.largura, self.altura))

    def colisao(self, ball):
        if not (ball.x <= self.x + self.largura and ball.x >= self.x):
            return False
        if not (ball.y - ball.radius <= self.y + self.altura):
            return False
        self.acerto()
        ball.set_velocity(ball.x_vel, ball.y_vel * -1)
        return True
    
    def acerto(self):
        self.vida -= 1
        self.cor = self.interpolar(*self.cores, self.vida/self.vida_maxima)
        som_acerto_tijolo.play()
    
    @staticmethod
    def interpolar(cor1, cor2, t):
        return tuple(int(a + (b - a) * t) for a, b in zip(cor1, cor2))

def draw(win,platform,tijolos,vidas,score): #colorir
    fonte_8bit = pygame.font.Font('fonte\8-BIT WONDER.TTF', 18) #fonte 8-bit
    platform.draw(win)
    for tijolo in tijolos:
        tijolo.draw(win)

    vidas_texto = fonte_8bit.render(f"{vidas} vidas", 1, "red")
    win.blit(vidas_texto, (10, HEIGHT - vidas_texto.get_height() - 30))

    score_text = fonte_8bit.render(f'{score} pontos', 1, 'white')
    win.blit(score_text, (WIDTH - score_text.get_width() - 10, HEIGHT - score_text.get_height() - 30))


def ball_collision(ball): # colisoes com paredes
    if ball.x -ball_radius <= 0 or ball.x + ball_radius>= WIDTH:
        ball.set_velocity(ball.x_vel * -1,ball.y_vel)
    if ball.y + ball_radius>= HEIGHT or ball.y - ball_radius <= 0:
        ball.set_velocity(ball.x_vel, ball.y_vel * -1)

def platform_ball_collision(ball, platform): # colisao entre bola e plataforma
    if not (ball.x <= platform.x + platform.width and ball.x >= platform.x):
        return
    if not (ball.y + ball.radius >= platform.y):
        return
    
    platform_center = platform.x + platform.width/2
    distance_to_center = ball.x - platform_center

    percent_width = distance_to_center / platform.width
    ang = percent_width * 90
    ang_rad = math.radians(ang)

    x_vel = math.sin(ang_rad) * ball.VEL
    y_vel = math.cos(ang_rad) * ball.VEL * -1

    ball.set_velocity(x_vel, y_vel)

def gerar_tijolos(linhas, colunas):
    tijolos = []

    altura_tijolo = 20
    largura_tijolo = (WIDTH // colunas) - 2

    for linha in range(linhas):
        for coluna in range(colunas):
            tijolo = Tijolos(largura_tijolo * coluna + 2 * coluna, altura_tijolo * linha + 2 * linha, largura_tijolo, altura_tijolo, 5, [(0, 255, 0), (255, 0, 0)])
            tijolos.append(tijolo)
    
    return tijolos

def tela_inicial():
    pygame.mixer.init()

    pygame.mixer.music.load(r'efeitos sonoros\475943_Skyrim-8-Bit-Theme.mp3')
    pygame.mixer.music.set_volume(0.4) 
    pygame.mixer.music.play(-1) 

    imagem_fundo = pygame.image.load('backgrounds\initscreen.jpg').convert()
    imagem_fundo = pygame.transform.scale(imagem_fundo, (WIDTH, HEIGHT))

    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False


        win.blit(imagem_fundo, (0, 0))
        texto_linha1 = fonte_8bit.render("   BertoBreaker", True, (255, 255, 100))
        texto_linha2 = fonte_8bit.render("Para jogar utilize as arrow keys", True, (255, 255, 255))
        texto_linha3 = fonte_8bit.render("Pressione espaco para iniciar", True, (255, 255, 255))

        win.blit(texto_linha1, (WIDTH/2 - texto_linha1.get_width()/2, HEIGHT/3 - texto_linha1.get_height()))
        posicao_linha2 = (WIDTH/2 - texto_linha2.get_width()/2, HEIGHT/2)
        posicao_linha3 = (WIDTH/2 - texto_linha3.get_width()/2, HEIGHT/2 + texto_linha2.get_height() + 40)  # Posição ajustada verticalmente
        win.blit(texto_linha2, posicao_linha2)
        win.blit(texto_linha3, posicao_linha3)
        pygame.display.update()




def main():
    clock = pygame.time.Clock()

    pygame.mixer.music.load('músicas\AceOfSpades_8bit.mp3')
    pygame.mixer.music.set_volume(0.2) 

    score = 0

    platform_x = WIDTH/2 - platform_width / 2
    platform_y = HEIGHT - platform_height - 5
    platform = Platform(platform_x, platform_y,platform_width ,platform_height, 'black')

    vidas = 3

    ball = Ball(WIDTH/2, platform_y - ball_radius, ball_radius,'black')
    tijolos = gerar_tijolos(3, 10)

    def reiniciar():
        platform.x = platform_x
        platform.y = platform_y
        ball.x = WIDTH/2
        ball.y = platform_y - ball_radius
    
    def mostrar_texto():

        fonte_8bit = pygame.font.Font('fonte/8-BIT WONDER.TTF', 14)  # Carregar a fonte 8-bit com tamanho 14

        texto1 = "VOCE PERDEU"
        texto2 = "Pressione ESC para sair"
        texto3 = "Pressione ESPACO para jogar novamente"

        renderizar_texto1 = fonte_8bit.render(texto1, True, (255, 0, 0))  # Texto vermelho
        renderizar_texto2 = fonte_8bit.render(texto2, True, (255, 0, 0))  # Texto vermelho
        renderizar_texto3 = fonte_8bit.render(texto3, True, (255, 0, 0))  # Texto vermelho

        win.blit(renderizar_texto1, (WIDTH/2 - renderizar_texto1.get_width()/2, HEIGHT/2 - renderizar_texto1.get_height()/2 - 80))
        win.blit(renderizar_texto2, (WIDTH/2 - renderizar_texto2.get_width()/2, HEIGHT/2))
        win.blit(renderizar_texto3, (WIDTH/2 - renderizar_texto3.get_width()/2, HEIGHT/2 + renderizar_texto2.get_height() + 20)) # Posição ajustada para ficar abaixo do texto2

        pygame.display.flip()
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return True
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
            pygame.display.flip()
    imagem_fundo = pygame.image.load('backgrounds\Foto-1.jpg').convert()
    imagem_fundo = pygame.transform.scale(imagem_fundo, (WIDTH, HEIGHT))
    run = True
    pygame.mixer.music.play(loops=-1)
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
        keys = pygame.key.get_pressed()
        pygame.display.flip()
        win.blit(imagem_fundo, (0, 0))

        draw(win, platform, tijolos, vidas, score)
            
        if keys[pygame.K_LEFT] and platform.x - platform.VEL >= 0:
                    platform.movement(-1)
        if keys[pygame.K_RIGHT] and platform.x + platform.width + platform.VEL <= WIDTH:
                    platform.movement(1)

        ball.movement()
        ball_collision(ball)
        platform_ball_collision(ball,platform)


        for tijolo in tijolos[:]:
            tijolo.colisao(ball)
            if tijolo.vida <= 0:
                score += 100
                tijolos.remove(tijolo)

        #PERDER VIDAS
        if ball.y + ball.radius >= HEIGHT:
            vidas -= 1
            ball.x = platform.x + platform_width/2 
            ball.y = platform_y - ball_radius
            ball.set_velocity(0, ball.VEL *- 1)

        if vidas <= 0:
            score = 0
            mostrar_texto()
            pygame.display.flip()
            reiniciar()
            vidas = 3
            tijolos = gerar_tijolos(3, 10)
            reiniciar() # plataforma vai para o centro
            tijolos = gerar_tijolos(3,10)            
            if keys[pygame.K_SPACE]:
                vidas = 3
                score = 0
            elif keys[pygame.K_ESCAPE]:
                break
        
        if len(tijolos) == 0:
            mostrar_texto('Voce ganhou! Aperte ESC para sair ou ESPAÇO para jogar novamente')
            reiniciar()
            if keys[pygame.K_SPACE]:
                vidas = 3
                score = 0
                tijolos = gerar_tijolos(3,10)
            elif keys[pygame.K_ESCAPE]:
                break



        win.blit(humberto_img_small, (ball.x-40, ball.y-35))
        draw(win, platform, tijolos, vidas, score)
        
        pygame.display.flip()

    pygame.quit()
    quit()

if __name__ == '__main__':
    pygame.init()
    tela_inicial()
    main()

