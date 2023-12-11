from pygame import *
from time  import time as timer
from random import * 

w, h = 700,500

WINDOW = display.set_mode((w,h))

clock = time.Clock()

game = True
finish = False
BaGr = transform.scale(image.load("galaxy.jpg"),(w,h))

class GameSprite(sprite.Sprite):
    def __init__(self,pImage,x,y,sizeX,sizeY,speed):
        super().__init__()
        self.image = transform.scale(image.load(pImage), (sizeX,sizeY))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x =  x
        self.rect.y = y 
    def draw(self):
        WINDOW.blit(self.image, (self.rect.x,self.rect.y))

class Button(sprite.Sprite):
    def __init__(self, pImage, x, y, sizeX, sizeY):
        super().__init__()
        self.image = transform.scale(image.load(pImage), (sizeX,sizeY))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw(self):
        WINDOW.blit(self.image, (self.rect.x,self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x >= 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x <= w-65:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png",self.rect.centerx-7,self.rect.top,15,30,15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        global hearts 
        if self.rect.y > h:
            try:

                hearts.pop()
            except:
                pass
            self.rect.x = randint(0,600)
            self.rect.y = randint(-60,-40)
            lost += 1
enemies = sprite.Group()


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()


mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
mixer.music.set_volume(0.30)

peremoga_sound = mixer.Sound("peremoga.ogg")
fire_sound = mixer.Sound("fire.ogg")

fire_sound.set_volume(0.2)

font.init()
mainfont = font.Font("mainfont.ttf",40)
mainfont_23 = font.Font("mainfont.ttf",20)

bullets = sprite.Group()
ship = Player("rocket.png",0,400,65,95,5)
enemies = sprite.Group()

score = 0
lost = 0
def create_enemies():
    for i in range(12):
        imageies = ["asteroid.png","ufo.png"]
        enemy_image = choice(imageies)
        enemy = Enemy(enemy_image,randint(0,600),randint(-60,-40),50,50,randint(2,3))
        enemies.add(enemy)
create_enemies()

reload_time = False
num_fire = 0



hearts = []
x = 300
def create_heart():
    x = 300
    for i in range(10):
        heart = GameSprite("heart.png",x,10,30,30,0)
        hearts.append(heart)
        x += 30
create_heart()

start = Button("start.png", 225, 225, 195, 80)
exit_button = Button("exit.png", 625, 425, 50, 50)

finish = True
menu = True



while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                x, y = e.pos
                if start.rect.collidepoint(x, y):
                    menu = False
                    finish = False
                if exit_button.rect.collidepoint(x,y):
                    game = False



        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if reload_time == False and num_fire < 20: 
                    fire_sound.play()
                    ship.fire()
                    num_fire += 1
                elif num_fire >= 20 and reload_time == False:
                    reload_time = True
                    reload_start = timer()
            if e.key == K_ESCAPE and finish == True:
                print("restart")
                for enemy in enemies:
                    enemies.remove(enemy)
                create_enemies()
                create_heart()
                score = 0
                lost = 0
                finish = False

    if menu:
        WINDOW.blit(BaGr,(0,0))
        start.draw()
        exit_button.draw()
        

    if not finish:
        WINDOW.blit(BaGr,(0,0))
        score_text = mainfont.render("SCORE: " +str(score),True,(255,0,0))
        lost_text = mainfont.render("LOST: " +str(lost),True,(0,255,0))


        WINDOW.blit(score_text,(5,5))
        WINDOW.blit(lost_text,(5,50))
        bullets.update()
        bullets.draw(WINDOW)


        for heart in hearts:
            heart.draw()


        enemies.update()
        enemies.draw(WINDOW)

        collides = sprite.groupcollide(enemies,bullets,True, True)
        for c in collides:
            imageies = ["asteroid.png","ufo.png"]
            enemy_image = choice(imageies)
            enemy = Enemy(enemy_image,randint(0,600),randint(-60,-40),50,50,randint(2,3))
            enemies.add(enemy)
            score += 1
            
        if reload_time:
            reload_timer = timer()
            if reload_timer - reload_start < 3:
                RELOADING_text = mainfont.render("RELOADING " ,True,(255,0,0))
                WINDOW.blit(RELOADING_text,(200,200))
            else:
                num_fire = 0
                reload_time = False

        if len(hearts) == 0:
            finish = True
            RELOADING_text = mainfont.render("POKA NYBASIK " ,True,(255,0,0))
            RESTART_text = mainfont_23.render("FOR RESTART ENTER THE ESC " ,True,(255,0,255))
            WINDOW.blit(RELOADING_text,(200,200))
            WINDOW.blit(RESTART_text,(150,250))




        if score == 10:
            finish = True
            RELOADING_text = mainfont.render("PEREMOGA" ,True,(0,255,0))
            RESTART_text = mainfont_23.render("FOR RESTART ENTER THE ESC " ,True,(255,0,255))
            peremoga_sound.play()
            WINDOW.blit(RELOADING_text,(200,200))
            WINDOW.blit(RESTART_text,(150,250))
        ship.draw()
        ship.update()

    display.update()
    clock.tick(60)