#imports
import pygame, sys
from pygame.locals import *
import random, time

# Inicialização do Pygame
pygame.init()

# Carregando e reproduzindo a música de fundo
pygame.mixer.music.load('sounds/background.wav')
pygame.mixer.music.play(-1, 0.0)

# Configuração do FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Definição de algumas cores
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Informações da tela
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0

#setando fontes
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, WHITE)

background = pygame.image.load("assets/AnimatedStreet.png")

# Criação da superfície de exibição com dimensões 400x600 pixels
DISPLAYSURF = pygame.display.set_mode((400, 600))

# Preenchimento da superfície com a cor branca
DISPLAYSURF.fill(WHITE)

# Definição do título da janela do jogo
pygame.display.set_caption("Game")

# Definição da classe Enemy que herda de pygame.sprite.Sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Carregamento da imagem do inimigo
        self.image = pygame.image.load("assets/Enemy.png")

        # Criação de um retângulo para representar o inimigo
        self.rect = pygame.Rect(0, 0, 44, 44)

        # Posicionamento inicial do inimigo no topo da tela
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE

        # Movimentação do inimigo para baixo
        self.rect.move_ip(0, SPEED)

        # Verificação se o inimigo atingiu a parte inferior da tela
        if self.rect.bottom > 600:
            # Incremento da pontuação
            SCORE += 1

            # Reposicionamento do inimigo no topo da tela
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Power(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Carregamento da imagem do power-up
        self.image = pygame.image.load("assets/Player.png")

        # Criação de um retângulo para representar o power-up
        self.rect = pygame.Rect(0, 0, 44, 44)
    def move(self):
        global SCORE

        # Movimentação do power-up para baixo
        self.rect.move_ip(0, SPEED)

        # Verificação se o power-up atingiu a parte inferior da tela
        if self.rect.bottom > 600:
            # Reposicionamento do power-up no topo da tela
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Definição da classe Player que herda de pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Carregamento da imagem do jogador
        self.image = pygame.image.load("assets/Player.png")

        # Criação de um retângulo para representar o jogador
        self.rect = pygame.Rect(0, 0, 44, 44)

        # Posicionamento inicial do jogador no centro da parte inferior da tela
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        # Verificação das teclas pressionadas para mover o jogador
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

    def draw(self, surface):
        # Desenho do jogador na superfície especificada
        surface.blit(self.image, self.rect)


# Definição da classe Background
class Background():
    def __init__(self):
        # Carregamento da imagem de fundo
        self.bgimage = pygame.image.load('assets/AnimatedStreet.png')

        # Criação de um retângulo para a imagem de fundo
        self.rectBGimg = self.bgimage.get_rect()

        # Posicionamento inicial da imagem de fundo
        self.bgY1 = self.rectBGimg.height
        self.bgX1 = 0

        self.bgY2 = 0
        self.bgX2 = 0

        self.moving_speed = SPEED

    def update(self):
        # Atualização da velocidade de movimento do fundo
        self.moving_speed = SPEED * 0.5

        # Atualização das posições Y do fundo
        self.bgY2 += self.moving_speed
        self.bgY1 += self.moving_speed

        # Verificação se as posições Y ultrapassaram o limite
        if self.bgY2 >= self.rectBGimg.height:
            self.bgY2 = -self.rectBGimg.height
        if self.bgY1 >= self.rectBGimg.height:
            self.bgY1 = -self.rectBGimg.height

    def render(self):
        # Desenho do fundo na superfície DISPLAYSURF
        DISPLAYSURF.blit(self.bgimage, (self.bgX1, self.bgY1))
        DISPLAYSURF.blit(self.bgimage, (self.bgX2, self.bgY2))

# Criação das instâncias das sprites
P1 = Player()  # Jogador
E1 = Enemy()  # Inimigo
PW = Power()  # Power-up    

# Criação da instância do fundo
back_ground = Background()

# Criação dos grupos de sprites
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(PW)

# Adição de um novo evento do usuário
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Loop principal do jogo
while True:
    # Iteração sobre todos os eventos do Pygame
    for event in pygame.event.get():
        # Verificação do evento de incremento de velocidade
        if event.type == INC_SPEED:
            SPEED += 0.5
        # Verificação do evento de fechar a janela
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    # Atualização e renderização do fundo
    back_ground.update()
    back_ground.render()
    
    # Renderização da pontuação na tela
    scores = font_small.render(str(SCORE), True, WHITE)
    DISPLAYSURF.blit(scores, (10, 10))
    
    # Movimentação e redesenho das sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
    
    # Verificação de colisão entre o jogador e o power-up
    
    # Verificação de colisão entre o jogador e o inimigo
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('sounds/crash.wav').play()
        pygame.mixer.music.stop()
        time.sleep(0.5)
        
        # Exibição da tela de Game Over
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(game_over, (30, 250))
        
        pygame.display.update()
        
        # Remoção de todas as sprites
        for entity in all_sprites:
            entity.kill()
        
        time.sleep(2)
        pygame.quit()
        sys.exit()
    
    pygame.display.update()
    FramePerSec.tick(FPS)
