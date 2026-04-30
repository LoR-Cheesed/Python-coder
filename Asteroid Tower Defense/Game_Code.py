# Player rotate code Source - https://stackoverflow.com/a/47166984
# Posted by skrx
# Retrieved 2026-03-09, License - CC BY-SA 3.0

# Bullet class Source - https://stackoverflow.com/a/59980344
# Posted by Rabbid76, modified by community. See post 'Timeline' for change history
# Retrieved 2026-03-25, License - CC BY-SA 4.0

import pygame as pg
import math
import random
from pygame.math import Vector2
from pygame.math import Vector3

pg.init()
pg.font.init()
screen = pg.display.set_mode((640, 640))

# Colors for the game
basic_color = (70, 70, 255)
sniper_color = (255, 70, 70)
demo_color = (255, 130, 0)
summon_color = (70, 255, 70)
black = (255, 255, 255)
bg_color = (30, 30, 30)

# images for the game
heart = pg.image.load('images/heart.png').convert_alpha()
heart_rect = heart.get_rect()
asteroid = pg.image.load('images/asteroid.png').convert_alpha()
asteroid_rect = asteroid.get_rect()

# important out-of-function variables
stats = []
set_class = None
bullets = []
last_shot = 0
total_bullets = 0
bul_range = pg.Rect(150, 150, 450, 450)
enemy_list = []
tick1 = 0
new_enemy = random.randint(10,50)

# Class holding the Player and (most) all of its functions
class Player(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        global set_class
        self.image = pg.Surface((1040, 30), pg.SRCALPHA) # Transparent surface
        # A reference to the original image to preserve the quality (no jpeg compression)
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=pos)
        self.vel = Vector2(0, 0)
        self.pos = Vector2(pos)

    def update(self):
        # Subtract pos vector from mouse pos to get the base, then normalize the vector.
        self.vel = (pg.mouse.get_pos() - self.pos).normalize()
        # Rotate the image
        radius, angle = self.vel.as_polar()
        self.image = pg.transform.rotozoom(self.orig_image, -angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    # allows set_class to actually change the triangle
    def add_triangle(self):
        line = pg.draw.line(self.image, pg.Color(170, 30, 30),
                        (525, 15), (1000, 15), width=2)
        if set_class == "basic":
            basic_triangle = pg.draw.polygon(self.image, pg.Color(basic_color),
                    ((500, 0),(500, 30), (550, 15)))
        if set_class == "sniper":
            sniper_triangle = pg.draw.polygon(self.image, pg.Color(sniper_color),
                        ((500, 5), (515, 15), (500, 25), (550, 15)))
        if set_class == "demolitionist":
            demo_triangle = pg.draw.polygon(self.image, pg.Color(demo_color), 
                        ((500, 0), (500, 30), (550, 20), (525, 15), (550, 10)))
        if set_class == "summoner":
            # im STILL blaming demry for this bro ts pmo
            summon_triangle_1 = pg.draw.polygon(self.image, pg.Color(summon_color),
                        ((500, 0), (500, 30), (545, 15)))
            summon_triangle_2 = pg.draw.circle(self.image, bg_color, (530, 15), 10)
            summon_triangle_3 = pg.draw.circle(self.image, pg.Color(summon_color), (535, 15), 10)
            
    # makes the life system exist
    def life_system(self):
        lives = 3
        life = 'life'
        life_count = []
        for i in lives:
            life_count.append(life)
        #if something hits player:
        #lives -= 1
        for life in lives:
            pass
        if lives == 0:
            pass
            #game_over()



# Class holding the bullet, and its base functions
class Bullet:
    # makes the bullet
    def __init__(self, x, y):
        self.pos = (x, y)
        mx, my = pg.mouse.get_pos()
        self.dir = (mx - x, my - y)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0]/length, self.dir[1]/length)
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))

        self.bullet = pg.Surface(stats[3]).convert_alpha()
        self.bullet.fill(pg.Color(stats[4]))
        self.bullet = pg.transform.rotate(self.bullet, angle)
        self.speed = stats[0]

    def update(self):  
        self.pos = (self.pos[0]+self.dir[0]*self.speed, 
                    self.pos[1]+self.dir[1]*self.speed)

    def draw(self, surf):
        global bullet_rect

        bullet_rect = self.bullet.get_rect(center = self.pos)
        surf.blit(self.bullet, bullet_rect)  

# class for the enemies that come at you in the game
class Enemy:
    def __init__(self):
        pass
    def render_enemies():
        global enemy_list

        del_list = []
        for i in range(len(enemy_list)):
            p1 = Vector2(enemy_list[i][0][0],enemy_list[i][0][1])
            p2 = Vector2(320,320)
            dir = p2 - p1
            dir = dir.normalize()
            #new_pos = (enemy_list[i][0][0]+math.sin(dir)*enemy_list[i][3],enemy_list[i][0][1]+math.cos(dir)*enemy_list[i][3])
            new_pos = enemy_list[i][0] + dir*enemy_list[i][3]

            enemy_list[i] = (new_pos,(enemy_list[i][1]+enemy_list[i][3])%360,enemy_list[i][2],enemy_list[i][3],enemy_list[i][4])
            
            enemyV = pg.transform.scale(asteroid, (enemy_list[i][2],enemy_list[i][2]))
            enemyV = pg.transform.rotate(enemyV, enemy_list[i][1])
            new_rect = enemyV.get_rect(center=enemy_list[i][0])
            screen.blit(enemyV, new_rect)

            if new_rect.colliderect(pg.Rect(310, 310, 20, 20)):
                del_list.append(i)
            if new_rect.colliderect(bullet_rect):
                del_list.append(i)
            
        for i in range(len(del_list)):
            del enemy_list[del_list[i]]

    def spawn_enemy():
        global enemy_list
        
        es = random.randint(0,1)
        if es == 0:
            ex = random.randint(0,640)
            ey = random.randint(0,1)*640
        else:
            ex = random.randint(0,1)*640
            ey = random.randint(0,640)

        enemy_list.append((Vector2(ex,ey),0,random.randint(50,100),5,3))


# sets the stats of bullets for each class
def bullet_stats():
    # some variables to dictate how bullets work for each class
    # the lists will go in order as such: [bullet speed(0), reload(1), range(2), bullet size(3), color(4),
    #  range position(5), damage(6)]
    global stats
    basic_stats = [20, 400, (450, 450), (5, 6), (200, 200, 255), (100, 100), 2]
    sniper_stats = [40, 800, (640, 640), (30, 2), (255, 200, 200), (0, 0), 4]
    demo_stats = [15, 600, (400, 400), (10, 10), (255, 200, 150), (125, 125), 8]
    summon_stats = [15, 200, (400, 400), (7, 3), (200, 255, 200), (125, 125), 20]
    if set_class == "basic":
        stats = basic_stats
    elif set_class == "sniper":
        stats = sniper_stats
    elif set_class == "demolitionist":
        stats = demo_stats
    elif set_class == "summoner":
        stats = summon_stats
    else:
        stats = basic_stats
    
def fade_out(duration, start_color, end_color, start_time):
    global cts_time
    current_time = pg.time.get_ticks()
    elapsed = current_time - start_time
    progress = min(elapsed / duration, 1.0)
    current_color = start_color.lerp(end_color, progress)
    return current_color

# Simplifies making text appear on screen
def display_text(text, font, pos, color):
    text_surface = font.render(f"{text}", True, color)
    text_pos = text_surface.get_rect(center=(pos))
    screen.blit(text_surface, text_pos)

# Allows user to pick what role they want to play as (UNOPTIMIZED, DO NOT OPEN UNLESS NESSECARY)
def role_chooser():
    global set_class, mouse_buttons
    cursor_pos = pg.mouse.get_pos()
    mouse_buttons = pg.mouse.get_pressed(3)
    # the overlay of the class chooser
    overlay_rect = pg.Rect((0, 0), (640, 640))
    overlay = pg.draw.rect(screen, pg.Color('black'), overlay_rect, width=0)
    overlay_font = pg.font.SysFont(None, 75, True)
    overlay_text = display_text("CHOOSE YOUR CLASS", overlay_font, (320, 50), pg.Color('white'))
    
    # All four buttons for the classes, with the text showing which class
    # it is, and what the class's player icon will look like.

    if set_class == None:
        # The Basic class's button
        basic_ins_color = [255, 255, 255]
        basic_rect = pg.Rect((160, 160), (150, 150))
        basic_button = pg.draw.rect(screen, pg.Color(basic_color), basic_rect, width=0)
        basic_font = pg.font.SysFont(None, 50, True)
        basic_text = display_text("BASIC", basic_font, (232.5, 180), pg.Color(basic_ins_color))
        basic_icon = pg.draw.polygon(screen, pg.Color(basic_ins_color),
                            ((190, 210),(190, 280), (280, 245)))
        basic_hovering = False

        # The Sniper class's button
        sniper_ins_color = [255, 255, 255]
        sniper_rect = pg.Rect((330, 160), (150, 150))
        sniper_button = pg.draw.rect(screen, pg.Color(sniper_color), sniper_rect, width=0)
        sniper_font = pg.font.SysFont(None, 50, True)
        sniper_text = display_text("SNIPER", sniper_font, (402.5, 180), pg.Color(sniper_ins_color))
        sniper_icon = pg.draw.polygon(screen, pg.Color(sniper_ins_color),
                            ((350, 220), (370, 245), (350, 270), (450, 245)))
        sniper_hovering = False

        # The Demolitionist class's 
        demo_ins_color = [255, 255, 255]
        demo_rect = pg.Rect((160, 330), (150, 150))
        demo_button = pg.draw.rect(screen, pg.Color(demo_color), demo_rect, width=0)
        demo_font = pg.font.SysFont(None, 25, True)
        demo_text = display_text("DEMOLITIONIST", demo_font, (232.5, 350), pg.Color(demo_ins_color))
        demo_icon = pg.draw.polygon(screen, pg.Color(demo_ins_color),
                                    ((190, 380), (190, 450), (280, 425), (240, 415), (280, 405)))
        demo_hovering = False

        # The Summoner class's button
        summon_ins_color = [255, 255, 255]
        summon_rect = pg.Rect((330, 330), (150, 150))
        summon_button = pg.draw.rect(screen, pg.Color(summon_color), summon_rect, width=0)
        summon_font = pg.font.SysFont(None, 35, True)
        summon_text = display_text("SUMMONER", summon_font, (405, 350), pg.Color(summon_ins_color))
        # I blame Demry for this vvv
        summon_icon_1 = pg.draw.polygon(screen, pg.Color(summon_ins_color),
                        ((360, 380),(360, 450), (450, 415)))
        summon_icon_2 = pg.draw.circle(screen, summon_color, (425, 415), 25)
        summon_icon_3 = pg.draw.circle(screen, pg.Color(summon_ins_color), (425, 415), 20)
        summon_hovering = False

    # Next, is the while functions that will show if the mouse is over a certain class's button.
        
        # basic's button
        if (cursor_pos[0] >= 160 and cursor_pos[0] <= 310) and (cursor_pos[1] >= 160 and cursor_pos[1] <= 310):
            basic_hovering = True
            basic_ins_color = basic_color
            basic_button = pg.draw.rect(screen, pg.Color('white'), basic_rect, width=0)
            basic_text = display_text("BASIC", basic_font, (232.5, 180), pg.Color(basic_ins_color))
            basic_icon = pg.draw.polygon(screen, pg.Color(basic_ins_color),
                                ((190, 210),(190, 280), (280, 245)))
        else:
            basic_hovering = False
        
        # sniper's button
        if (cursor_pos[0] >= 330 and cursor_pos[0] <= 480) and (cursor_pos[1] >= 160 and cursor_pos[1] <= 310):
            sniper_hovering = True
            sniper_ins_color = sniper_color
            sniper_button = pg.draw.rect(screen, pg.Color('white'), sniper_rect, width=0)
            sniper_text = display_text("SNIPER", sniper_font, (402.5, 180), pg.Color(sniper_ins_color))
            sniper_icon = pg.draw.polygon(screen, pg.Color(sniper_ins_color),
                        ((350, 220), (370, 245), (350, 270), (450, 245)))
        else:
            sniper_hovering = False
        
        # demolitionist's button
        if (cursor_pos[0] >= 160 and cursor_pos[0] <= 310) and (cursor_pos[1] >= 330 and cursor_pos[1] <= 480):
            demo_hovering = True
            demo_ins_color = demo_color
            demo_button = pg.draw.rect(screen, pg.Color('white'), demo_rect, width=0)
            demo_text = display_text("DEMOLITIONIST", demo_font, (232.5, 350), pg.Color(demo_ins_color))
            demo_icon = pg.draw.polygon(screen, pg.Color(demo_ins_color),
                        ((190, 380), (190, 450), (280, 425), (240, 415), (280, 405)))
        else:
            demo_hovering = False
        
        # summoner's button
        if (cursor_pos[0] >= 330 and cursor_pos[0] <= 480) and (cursor_pos[1] >= 330 and cursor_pos[1] <= 480):
            summon_hovering = True
            summon_ins_color = summon_color
            summon_button = pg.draw.rect(screen, pg.Color('white'), summon_rect, width=0)
            summon_text = display_text("SUMMONER", summon_font, (405, 350), pg.Color(summon_ins_color))
        # I still blame Demry for this vvv
            summon_icon_1 = pg.draw.polygon(screen, pg.Color(summon_ins_color),
                        ((360, 380),(360, 450), (450, 415)))
            summon_icon_2 = pg.draw.circle(screen, pg.Color('white'), (425, 415), 25)
            summon_icon_3 = pg.draw.circle(screen, pg.Color(summon_ins_color), (425, 415), 20)
        else:
            summon_hovering = False
    
    # Now, making the buttons clickable.

     #basic button's clickable
        if basic_hovering == True:
            if mouse_buttons[0] == True:
                set_class = "basic"

     #sniper button's clickable
        if sniper_hovering == True:
            if mouse_buttons[0] == True:
                set_class = "sniper"
    
     #demolitionist button's clickable
        if demo_hovering == True:
            if mouse_buttons[0] == True:
                set_class = "demolitionist"
    
     #summoner button's clickable
        if summon_hovering == True:
            if mouse_buttons[0] == True:
                set_class = "summoner"

# adds a cooldown bar for the bullets
def cooldown():
    current_time = pg.time.get_ticks()
    reload_time = stats[1]
    time_between = 0
    time_between = current_time - last_shot
    cooldown_base_length = 50
    time_var = cooldown_base_length / reload_time
    cooldown_length = time_between * time_var
    if  0 < cooldown_length <= 50:
        bar_rect = pg.Rect(295, 355, cooldown_length, 3)
        bar = pg.draw.rect(screen, pg.Color("white"), bar_rect, width=0)

# puts the bullet and its position in a list, used for fire_bullet to work
def list_bullet():
    global bullets, last_shot, total_bullets
    if len(stats) != 0:
        current_time = pg.time.get_ticks()
        reload_time = stats[1]
        time_between = current_time - last_shot
        if (time_between >= reload_time):
            bullets.append(Bullet(320, 320))
            total_bullets += 1
            last_shot = current_time   

# lets the bullet fired be seen, and adds a range to it
def fire_bullet():
    global bullet
    if len(stats)!= 0:
        bul_range = pg.Rect(*stats[5], *stats[2])
        for bullet in bullets[:]:
            bullet.update()
            if not bul_range.collidepoint(bullet.pos):
                bullets.remove(bullet)
        for bullet in bullets:
            bullet.draw(screen)

def click_to_shoot():
    current_color = fade_out(5000, Vector3(255, 255, 255), Vector3(30, 30, 30), cts_time)
    cts_font = pg.font.SysFont(None, 50, None)
    cts_text = display_text("Click/Hold to Shoot", cts_font, (320, 100), current_color)


# The main loop, holding (most) all the functions made.
def main():
    global current_time, cts_time, tick1, new_enemy
    # some important things that will break the game if they dont exist
    clock = pg.time.Clock()
    all_sprites = pg.sprite.Group()
    player = Player((320, 320), all_sprites)
    done = False
    # the TRUE main loop, where all the functions go
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
        # checks to see if theres a class set yet
        if set_class == None:
                role_chooser()
                if set_class != None:
                    bullet_stats()
                    cts_time = pg.time.get_ticks()
        else:
            # adds a reload time, so the user can't just spamfire
            if mouse_buttons[0] == True:
                list_bullet()
            tick1 += 1
            if tick1 > new_enemy:
                new_enemy = tick1+random.randint(20,60)
                Enemy.spawn_enemy()
            
            # adds some important things
            player.add_triangle()
            all_sprites.update()
            screen.fill(bg_color)
            click_to_shoot()
            all_sprites.draw(screen)
            cooldown()
            Enemy.render_enemies()
        # shoots the bullet, makes the clock, and makes the screen seeable
        mouse_buttons = pg.mouse.get_pressed(3)
        if len(stats) != 0:
            fire_bullet()
        pg.display.flip()
        clock.tick(30)

# the main loop
main()
pg.quit()

"""
TO-DO LIST:
- add basic enemies
- add lives for player
- add enemy health
- add damage animation for enemies
- add easy way to make waves
- add demo & summon's abilities
"""
