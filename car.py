#imports
import pygame, sys
from pygame.locals import *
import random, time

#inicialização
pygame.init()

pygame.mixer.music.load('background.wav')
pygame.mixer.music.play(-1, 0.0)

#setando o fps
FPS = 60
FramePerSec = pygame.time.Clock()

#setando o background


#definindo algumas cores
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)

#informações da tela
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0

#setando fontes
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, WHITE)

background = pygame.image.load("AnimatedStreet.png")

#criando a tela branca de fundo
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


class Enemy(pygame.sprite.Sprite):
      def __init__(self):
          super().__init__()
          self.image =  pygame.image.load("Enemy.png")
          self.rect = self.image.get_rect()
          self.rect.center=(random.randint(40,SCREEN_WIDTH-40),0)
          
      def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.bottom > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40),0)
            
class Player(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160,520)
        
      def move(self):
        pressed_keys = pygame.key.get_pressed()
        #if pressed_keys[K_UP]:
              #self.rect.move_ip(0, -5)
        #if pressed_keys[K_DOWN]:
              #self.rect.move_ip(0,5)
              
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
                  
      def draw(self, surface):
          surface.blit(self.image, self.rect)
     
class Background():
      def __init__(self):
            self.bgimage = pygame.image.load('AnimatedStreet.png')
            self.rectBGimg = self.bgimage.get_rect()
            
            self.bgY1 = self.rectBGimg.height
            self.bgX1 = 0
            
            self.bgY2 = 0
            self.bgX2 = 0
            
            self.moving_speed = 5
            
      # def update(self):
      #       self.bgY2 -= self.moving_speed
      #       self.bgY1 -= self.moving_speed
      #       if self.bgY2 <= -self.rectBGimg.height:
      #             self.bgY2 = self.rectBGimg.height
      #       if self.bgY1 <= -self.rectBGimg.height:
      #             self.bgY1 = self.rectBGimg.height
         
      def update(self):
            self.bgY2 += self.moving_speed
            self.bgY1 += self.moving_speed
            if self.bgY2 >= self.rectBGimg.height:
                  self.bgY2 = -self.rectBGimg.height
            if self.bgY1 >= self.rectBGimg.height:
                  self.bgY1 = -self.rectBGimg.height           
                  
                  
      def render(self):
         DISPLAYSURF.blit(self.bgimage, (self.bgX1, self.bgY1))
         DISPLAYSURF.blit(self.bgimage, (self.bgX2, self.bgY2))

#setando as sprites          
P1 = Player()
E1 = Enemy()

back_ground = Background()

#criando grupos de sprites
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

#adicionando um novo user event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

#game loop
while True:
  
    #fazendo o ciclo de todos os eventos
    for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED += 0.5
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    back_ground.update()
    back_ground.render()
                    
    #DISPLAYSURF.blit(background, (0,0))
    scores = font_small.render(str(SCORE), True, WHITE)
    DISPLAYSURF.blit(scores, (10,10))
    
    #movimentando e redesenhando as sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
        
    #pra rodar caso ocorra colisão entre o jogador e o inimigo
    if pygame.sprite.spritecollideany(P1, enemies):
          pygame.mixer.Sound('crash.wav').play()
          pygame.mixer.music.stop()
          time.sleep(0.5)
          
          DISPLAYSURF.fill(BLACK)
          DISPLAYSURF.blit(game_over, (30,250))
          
          pygame.display.update()
          for entity in all_sprites:
                entity.kill()
          time.sleep(2)
          pygame.quit()
          sys.exit()
          
    pygame.display.update()
    FramePerSec.tick(FPS)