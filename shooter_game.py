
from time import *
from pygame import *
from random import *
win_w = 700
win_h = 500
class game_sprite(sprite.Sprite):
    def __init__(self, player_image,player_x,player_y,size_x,size_y,player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()        
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x,self.rect.y))
class Player(game_sprite):
    def update(self):
        klavisha = key.get_pressed()
        if klavisha[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if klavisha[K_RIGHT] and self.rect.x < win_w - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)
lost = 0
class Enemy(game_sprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_h:
            self.rect.y = 0
            self.rect.x = randint(80,win_w - 80)
            lost += 1
class Bullet(game_sprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
bullets = sprite.Group()
asteroids = sprite.Group()
for i  in range(1,3):
    asteroid = Enemy('asteroid.png',randint(30,win_w-30),-40,80,50,randint(1,7))
    asteroids.add(asteroid)
score = 0
goal = 10
max_lost = 3
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy('ufo.png',randint(80,win_w - 80),-40,80,50,randint(1,5))
    monsters.add(monster)
window = display.set_mode((win_w,win_h))
display.set_caption('space game')
background = transform.scale(
    image.load('galaxy.jpg'),
    (win_w,win_h)
)
finish = False
mixer.init()
mixer.music.load('space.ogg')
#mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
image_hero = 'rocket.png'
game = True
fps = 60
clock = time.Clock()
ship = Player(image_hero,5,win_h - 100,80,100,10)
font.init()
font1 = font.Font(None,36)
font2 = font.Font(None,80)

win = font2.render('you win',True,(255,255,255))
lose = font2.render('you lose',True,(55,255,255))
life = 3
num_fire = 0
real_time = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game  = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and real_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and real_time == False:
                    last_time = time()
                    real_time = True
    if not finish:
        window.blit(background,(0,0))
        ship.update()
        bullets.update()
        monsters.update()
        asteroids.update()
        ship.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
        if real_time == True:
            now_time = time()
            if now_time - last_time < 3:
                reload = font2.render('подождите перезарядка!!!!!!!!',1,(255,255,255))           
                window.blit(reload,(260,460))
            else:
                num_fire = 0
                real_time = False
        collides = sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            score += 1
            monster = Enemy('ufo.png',randint(80,win_w - 80),-40,80,50,randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(ship,monsters,False) or sprite.spritecollide(ship,asteroids,False):
            sprite.spritecollide(ship,monsters,True)
            sprite.spritecollide(ship,asteroids,True)
            life -= 1
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))
        if score >= goal:
            finish = True 
            window.blit(win,(200,200))
        text_lose = font1.render('Пропущено: ' + str(lost), 1,(255,255,255))
        window.blit(text_lose,(10,50))
        text_win = font1.render('Счёт: ' + str(score), 1,(255,255,255))
        window.blit(text_win,(10,10))
        display.update()
    clock.tick(fps)
