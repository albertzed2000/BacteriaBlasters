#__________________________________________Game:Bacteria Blasters_________________________________________________________________________
import simplegui
import math
import random


#__________________________________________CONSTANTS AND VARIABLES___________________________________________________________________________

#PICTURES
BACKGROUND_IMAGE = simplegui.load_image('https://i.imgur.com/jzFAhnF.jpg')
BACTERIA_SPRITE = simplegui.load_image("https://the-hollywood-gossip-res.cloudinary.com/iu/s--kdYSRpDh--/t_xlarge_l/cs_srgb,f_auto,fl_strip_profile.lossy,q_auto:420/v1496934596/xxxtentacion-mug-shot.png")
ENEMY_GERM = simplegui.load_image('https://the-hollywood-gossip-res.cloudinary.com/iu/s--kdYSRpDh--/t_xlarge_l/cs_srgb,f_auto,fl_strip_profile.lossy,q_auto:420/v1496934596/xxxtentacion-mug-shot.png')
CHARACTER_IMAGE = simplegui.load_image('https://the-hollywood-gossip-res.cloudinary.com/iu/s--kdYSRpDh--/t_xlarge_l/cs_srgb,f_auto,fl_strip_profile.lossy,q_auto:420/v1496934596/xxxtentacion-mug-shot.png')
CHARACTER_BULLET_IMAGE = simplegui.load_image('https://the-hollywood-gossip-res.cloudinary.com/iu/s--kdYSRpDh--/t_xlarge_l/cs_srgb,f_auto,fl_strip_profile.lossy,q_auto:420/v1496934596/xxxtentacion-mug-shot.png')
ENEMY_BULLET_IMAGE = simplegui.load_image('https://the-hollywood-gossip-res.cloudinary.com/iu/s--kdYSRpDh--/t_xlarge_l/cs_srgb,f_auto,fl_strip_profile.lossy,q_auto:420/v1496934596/xxxtentacion-mug-shot.png')
UPGRADE_IMAGE = simplegui.load_image('https://the-hollywood-gossip-res.cloudinary.com/iu/s--kdYSRpDh--/t_xlarge_l/cs_srgb,f_auto,fl_strip_profile.lossy,q_auto:420/v1496934596/xxxtentacion-mug-shot.png')

#CONSTANTS
IMG_WIDTH = BACKGROUND_IMAGE.get_width()
IMG_HEIGHT = BACKGROUND_IMAGE.get_height()
FRAME_WIDTH = IMG_WIDTH-500
FRAME_HEIGHT = IMG_HEIGHT / 2
ENEMY_SPAWN_RATE = 10000
ENEMY_SPAWN_POSITION = [FRAME_WIDTH/3, FRAME_WIDTH/2, (FRAME_WIDTH/3)*2]
ENEMY_SPAWN_DIRECTION_VELOCITY = [-2, 2]
ENEMY_GERM_WIDTH = ENEMY_GERM.get_width()
ENEMY_GERM_HEIGHT = ENEMY_GERM.get_height()
CHARACTER_IMAGE_WIDTH = CHARACTER_IMAGE.get_width()
CHARACTER_IMAGE_HEIGHT = CHARACTER_IMAGE.get_height()
CHARACTER_BULLET_IMAGE_HEIGHT = CHARACTER_BULLET_IMAGE.get_height()
CHARACTER_BULLET_IMAGE_WIDTH = CHARACTER_BULLET_IMAGE.get_width()
ENEMY_BULLET_IMAGE_WIDTH = ENEMY_BULLET_IMAGE.get_width()
ENEMY_BULLET_IMAGE_HEIGHT = ENEMY_BULLET_IMAGE.get_height()
CHARACTER_SPRITE_WIDTH = CHARACTER_IMAGE_WIDTH/4
CHARACTER_SPRITE_HEIGHT = CHARACTER_IMAGE_HEIGHT/4
UPGRADE_IMAGE_HEIGHT = UPGRADE_IMAGE.get_height()
UPGRADE_IMAGE_WIDTH = UPGRADE_IMAGE.get_width()

#VARIABLES

#Game Traits
game_started = False
scroll_position = [IMG_WIDTH/2, 0]
click_position = [0,0]
high_score = 0

#Player Traits
right_moving = False
left_moving = False
up_moving = False
down_moving = False
character_firing_bullets = False
character_attack = 0
has_died = False

#Enemy Traits
enemy_spawn_size = 30
enemy_spawn = 0

#Upgrade Traits
upgrade_list = ['health', 'attack_speed', 'bullet_size', 'bullet_speed', 'regen']
enemy_upgrade_list = ['health', 'bullet_size', 'bullet_speed', 'damage']

#Wait for images to load before starting game
while BACKGROUND_IMAGE.get_width == 0 or UPGRADE_IMAGE.get_width == 0:   
    pass

#__________________________________________CLASSES__________________________________________________________________________________
def health_color(health):
    #Health changes color based off of remaining health
    if health >= 4375:
        return '#196619'
    elif health >= 3750:
        return '#70db70'
    elif health >=3125:
        return '#ffff99'
    elif health >= 2500:
        return '#cccc00'
    elif health >= 1875:
        return '#ffa64d'
    elif health >= 1250:
        return '#ff0000'
    elif health >= 625:
        return '#660000'
    elif health >= 0:
        return 'black'
    else:
        return 'black'

def distance_between(pos1,pos2):
    #Calculates the distances between two given objects
    a = pos2[0] - pos1[0]
    b = pos2[1] - pos1[1]
    c = math.sqrt(a**2 + b**2)
    return c


def new_game():
    #Resets/starts game and sets all variable to start-of-game value
    global character_list, player_one, character_bullet_list
    global enemy_bullet_size, enemy_bullet_speed
    global regen, character_bullet_speed, character_bullet_size
    global character_attack_speed, points, character_direction
    global max_health, upgrade_spawn_rate, enemy_list
    global upgrade_spawn, upgrades, regen_rate
    global enemy_bullet_list, enemy, enemies_killed
    global enemy_attack_speed, enemy_bullet_damage, enemy_health
    #____________________________________________________________________
    max_health = 5000
    player_health = max_health
    character_bullet_list = []
    enemy_attack_speed = 1000
    enemy_list = []
    enemy_bullet_list = []
    player_one = Character(60, 'red', [15, 15], [FRAME_WIDTH/2, FRAME_HEIGHT+30], player_health, CHARACTER_IMAGE)
    enemy_bullet_size = 20
    enemy_bullet_speed = [0, 10] 
    enemy_bullet_damage = 250
    enemy_health = 3
    character_direction = 0
    character_bullet_speed = [0, -10]
    character_bullet_size = 20
    upgrades = []
    upgrade_spawn = 0
    upgrade_spawn_rate = 3
    character_attack_speed = 0.1
    regen = 0
    regen_rate = 0.1
    points = 0
    enemies_killed = 0
    

class Character:
    #Character class
    def __init__(self, radius, color, velocity, position, health, image):
        self.radius = radius
        self.color = color
        self.velocity = velocity
        self.position = position
        self.health = health
        self.image = image
        self.animated = False
        self.time = 0
        self.can_regen = False
    def draw(self, canvas):
        tile_center = [CHARACTER_SPRITE_WIDTH/2 + (CHARACTER_SPRITE_WIDTH * (math.ceil(self.time%4)-1)), 
                       CHARACTER_SPRITE_HEIGHT/2 + (CHARACTER_SPRITE_HEIGHT * character_direction) ]
        if not self.animated:
            tile_center = [CHARACTER_SPRITE_WIDTH/2, CHARACTER_SPRITE_HEIGHT/2]
        canvas.draw_image(self.image, 
                          tile_center, 
                          [CHARACTER_SPRITE_WIDTH, CHARACTER_SPRITE_HEIGHT], 
                          self.position,
                          [2*self.radius,2*self.radius])


    def has_collided(self, other):
        return math.fabs((self.position[0]+self.velocity[0])-(other.position[0]+other.velocity[0]))<=self.radius+other.radius

        
    def update(self):
        global regen
        #Movement

        if up_moving:
            self.position[1] += self.velocity[1] * -1
        if down_moving:
            self.position[1] += self.velocity[1]
        if right_moving:
            self.position[0] += self.velocity[0]
        if left_moving:
            self.position[0] += self.velocity[0] * -1
        if self.position[0] <self.radius:
            self.position[0] = self.radius
            
        #Constraints on character's position
        #Character cannot leave contraints
        if self.position[0] >FRAME_WIDTH - self.radius:
            self.position[0] = FRAME_WIDTH - self.radius
        if self.position[1] >FRAME_HEIGHT - self.radius:
            self.position[1] = FRAME_HEIGHT - self.radius
        if self.position[1] < 568 - self.radius:
            self.position[1] = 568 - self.radius
        
        #Regeneration
        if self.health < max_health:
            can_regen = True
        elif self.health == max_health:
            can_regen = False
        if can_regen:
            if regen >= 5:
                self.health += 1
                regen = 0

        #Updates the 'time' of the character, allowing an animation process to occur
        if self.animated:
            self.time += 0.2
        if self.time >=4:
            self.time = 0.2

    def improve(self):        
        #Different types of upgrades
        global character_attack_speed, regen, character_bullet_speed
        global max_health, regen_rate, character_bullet_size
        upgrade_name = random.choice(upgrade_list)
        
        if upgrade_name == 'health':
            if max_health <= 10000:
                max_health += 500
                self.health += 500
       
        elif upgrade_name == 'attack_speed':
            if character_attack_speed >=6:
                character_attack_speed -= 3
           
            

        elif upgrade_name == 'regen':
            if regen_rate <= 20:
                regen_rate += 1
                
        if upgrade_name == 'bullet_speed':
            if character_bullet_speed >= -25:
                character_bullet_speed[1] -= 4
                
        elif upgrade_name == 'bullet_size':
             if character_bullet_size <= 80:
                character_bullet_size += 10

class Bullet:
    def __init__(self, radius, color, velocity, position, damage, image):
        self.radius = radius
        self.color = color
        self.velocity = velocity
        self.damage = damage
        self.position = position
        self.image = image
        self.rotation = 0
        
        
    def draw(self, canvas):
        
        canvas.draw_image(self.image, [CHARACTER_BULLET_IMAGE_WIDTH//2, CHARACTER_BULLET_IMAGE_HEIGHT//2],
                    [CHARACTER_BULLET_IMAGE_WIDTH, CHARACTER_BULLET_IMAGE_HEIGHT], self.position, [self.radius*2, self.radius*2], self.rotation)


    def update(self):
        self.position[1] += self.velocity[1]
        self.rotation += 0.2
        
        
class Enemy:
    def __init__(self, radius, color, velocity, position, health, attack_speed, image):
        self.radius = radius
        self.color = color
        self.velocity = velocity
        self.position = position
        self.health = health
        self.attack_speed = attack_speed
        self.image = image
    def draw(self, canvas):
         canvas.draw_image(self.image, [ENEMY_GERM_WIDTH//2, ENEMY_GERM_HEIGHT//2],
                    [ENEMY_GERM_WIDTH, ENEMY_GERM_HEIGHT], self.position, [self.radius*2, self.radius*2])

        
    def update(self):
        #Updates its own velocity as well as firing
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        if self.position[0]-self.radius <= 0:
            self.velocity[0] *= -1
            self.position[0] = self.radius
        if self.position[0]+self.radius >= FRAME_WIDTH:
            self.velocity[0] *= -1
            self.position[0] = FRAME_WIDTH-self.radius
        self.attack_speed += 1
        if self.attack_speed == enemy_attack_speed:
            self.attack_speed = 0
            enemy_bullet_list.append(Enemy_Bullet(enemy_bullet_size, 'green', enemy_bullet_speed, 
                                                  [self.position[0], self.position[1]+self.radius], enemy_bullet_damage, ENEMY_BULLET_IMAGE))


    
    def has_collided(self, other):
        return math.fabs((self.position[0]+self.velocity[0])-(other.position[0]+other.velocity[0]))<=self.radius+other.radius

        
class Enemy_Bullet:
    def __init__(self, radius, color, velocity, position, damage, image):
        self.radius = radius
        self.color = color
        self.velocity = velocity
        self.position = position
        self.damage = damage
        self.image = image
        self.rotation = 0
                           
    def draw(self, canvas):
          canvas.draw_image(self.image, [ENEMY_BULLET_IMAGE_WIDTH//2, ENEMY_BULLET_IMAGE_HEIGHT//2],
                    [ENEMY_BULLET_IMAGE_WIDTH, ENEMY_BULLET_IMAGE_HEIGHT], self.position, [self.radius*2, self.radius*2], self.rotation)


        
    def update(self):
        self.position[1] += enemy_bullet_speed[1]
        self.rotation += 0.3
class Upgrade:
    #Upgrades class
    def __init__(self, radius, color, velocity, position, image):
        self.radius = radius
        self.color = color
        self.velocity = velocity
        self.position = position
        self.image = image
        
    def draw(self, canvas):
        canvas.draw_image(self.image, [UPGRADE_IMAGE_WIDTH//2, UPGRADE_IMAGE_HEIGHT//2],
                          [UPGRADE_IMAGE_WIDTH, UPGRADE_IMAGE_HEIGHT], self.position,
                          [self.radius*2, self.radius*2])
    def update(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        
       
        
#________________________________________HANDLERS__________________________________________________________________________


def mouse_handler(position):
    
    #Returns position of where mouse has been clicked
    global click_position
    click_position = position
    
def draw(canvas):
                           
    #Long list of global statements
    global game_started, click_position, has_died, high_score
    global character_list, player_one, character_bullet_list, character_attack
    global enemy_spawn, enemy_list, enemy_attack_speed, enemy_health
    global enemies_killed, points, regen, upgrade_spawn
    global enemy_bullet_damage, enemy_bullet_size
    
    #Start Screen if game has not ever been played
    if game_started == False:
        if not has_died:
            canvas.draw_circle((100, 400), 65, 0.001, 'Green', "Green")
            canvas.draw_image(ENEMY_GERM, (ENEMY_GERM_WIDTH/2, ENEMY_GERM_HEIGHT/2), (ENEMY_GERM_WIDTH, ENEMY_GERM_HEIGHT)
            , (100, 400), (200, 200))

            canvas.draw_text('BACTERIA BLASTERS', (65, 100), 80, 'Green', 'sans-serif')
            canvas.draw_text('PLAY GAME', (200, 425), 50, 'Green', 'sans-serif')
            if click_position[0] >= 20 and click_position[0] <= 180:
                if click_position[1] >= 320 and click_position[1] <= 510:
                    game_started = True
                    new_game()
                    
        #Alternate start screen for someone who died, which displays score            
        elif has_died:
            canvas.draw_circle((100, 400), 65, 0.001, 'Green', "Green")
            canvas.draw_image(ENEMY_GERM, (ENEMY_GERM_WIDTH/2, ENEMY_GERM_HEIGHT/2), (ENEMY_GERM_WIDTH, ENEMY_GERM_HEIGHT)
            , (100, 400), (200, 200))

            canvas.draw_text('YOU DIED!', (65, 100), 80, 'Green', 'sans-serif')
            canvas.draw_text('PLAY AGAIN?', (200, 425), 50, 'Green', 'sans-serif')
            if high_score == points:
                canvas.draw_text('NEW HIGH SCORE! ' + str(high_score) + " POINTS", (400, 625), 30, 'Green', 'sans-serif')
            else:
                canvas.draw_text('HIGH SCORE: ' + str(high_score) + " POINTS", (400, 625), 30, 'Green', 'sans-serif')
                canvas.draw_text('SCORE THIS ROUND:' + str(points) + " POINTS", (400, 675), 30, 'Green', 'sans-serif')
            
            if click_position[0] >= 20 and click_position[0] <= 180:
                if click_position[1] >= 320 and click_position[1] <= 510:
                    game_started = True
                    new_game() 

        
        
    #Draw handler portion for actual game    
    if game_started:

        #Scrolls Background Image
        canvas.draw_image(BACKGROUND_IMAGE, (IMG_WIDTH/2,IMG_HEIGHT/2), (IMG_WIDTH, IMG_HEIGHT), scroll_position, (IMG_WIDTH,IMG_HEIGHT))
        scroll_position[1] = (scroll_position[1] +8)%(IMG_HEIGHT/2)
        
        #Regen rate is moderated here
        regen += regen_rate
                           
        #Displays character health
        canvas.draw_text(str(player_one.health) + " Health",
                                 [720, 720], 40, health_color(player_one.health), 'sans-serif')

        #Fires bullet at a moderated attack speed
        character_attack += 1
        if character_firing_bullets:

            if character_attack >=character_attack_speed:
                fire = Bullet(character_bullet_size, 'blue', character_bullet_speed, [player_one.position[0], player_one.position[1]-player_one.radius], 1, CHARACTER_BULLET_IMAGE)
                character_bullet_list.append(fire)
                character_attack = 0
                
        #Draws and updates character
        player_one.draw(canvas)
        player_one.update()

        #Checks if player has died
        if player_one.health <= 0:
            if points >= high_score:
                high_score = points
            click_position = [0, 0]
            game_started = False
            has_died = True
            

        #Slows each enemy's attack speed depending on number of enemies
        enemy_attack_speed = 10+10*len(enemy_list)    
        
        #Draws and updates character's bullets, and if they reach edge of screen, deletes them
        for ball in character_bullet_list:
            ball.draw(canvas)
            ball.update()
            if ball.position[1]<0:
                character_bullet_list.remove(ball)

        #Draws and updates enemies in enemy list
        for enemy in enemy_list:
            enemy.draw(canvas)
            enemy.update()

        #Spawns enemies in one of three positions randomly
        #Enemies are spawned in somewhat random intervals
        enemy_spawn += random.randint(50,150)
        if len(enemy_list) <= 20:
            can_spawn = True
            spawn_position = random.choice(ENEMY_SPAWN_POSITION)
                          
            """Disallows enemies from being spawned if
            position it wants to spawn at currently occupies
            an enemy"""
            if enemy_spawn >= ENEMY_SPAWN_RATE:
                for enemy in enemy_list:
                    if enemy.position[0]>= (spawn_position-(enemy.radius*2)) and enemy.position[0] <= spawn_position+(enemy.radius*2):
                        can_spawn = False
                        break
                if can_spawn:
                    enemy_list.append(Enemy(enemy_spawn_size, 'red', [random.choice(ENEMY_SPAWN_DIRECTION_VELOCITY), 0], 
                                            [spawn_position, enemy_spawn_size], enemy_health, 0, ENEMY_GERM))
                    enemy_spawn = 0
                    
        #Updates upgrades as they move
        for upgrade in upgrades:
            upgrade.draw(canvas)
            upgrade.update()
            
            #Collisions with upgrades will improve player and award points
            if distance_between(player_one.position, upgrade.position)<= player_one.radius+upgrade.radius:
                player_one.improve()
                upgrades.remove(upgrade)
                points += 250


        #Checks collisions between enemies and character bullets, collisions with each other and collisions on walls
        for enemy in enemy_list:
            for bullet in character_bullet_list:
                if distance_between(enemy.position, bullet.position) <= enemy.radius+bullet.radius:
                    enemy.health -= bullet.damage
                    character_bullet_list.remove(bullet)
                    
            #Collisions can kill enemy and award points        
            if enemy.health <= 0:
                #enemy_upgrade_list = ['health', 'bullet_size', 'bullet_speed', 'damage']
                enemy_list.remove(enemy)
                upgrade_spawn += 1
                points += 500
                enemies_killed += 1
                
                if enemies_killed >= 5:
                    upgrade_type = random.choice(enemy_upgrade_list)
                    if upgrade_type == 'health':
                        enemy_health += 1
                        
                    elif upgrade_type == 'bullet_size':
                        if enemy_bullet_size < 50:
                            enemy_bullet_size += 5
                            
                    elif upgrade_type == 'bullet_speed':
                        if enemy_bullet_speed[1] <= 12:
                            enemy_bullet_speed[1] += 1
                    
                    elif upgrade_type == 'damage':
                        if enemy_bullet_damage <= 500:
                            enemy_bullet_damage += 25
                    

                
                #Spawns Upgrades when enemy dies
                if upgrade_spawn >= upgrade_spawn_rate:
                    upgrades.append(Upgrade(25, 'blue', [0, 8], enemy.position, UPGRADE_IMAGE))    
                    upgrade_spawn = 0

        #Checks for if enemies have collided with each other, and if so, bounce them
        for enemy1 in enemy_list:
            for enemy2 in enemy_list:
                if enemy1 != enemy2:
                    if enemy1.has_collided(enemy2):
                        enemy1.velocity[0] *= -1
                        enemy1.position[0] += enemy1.velocity[0]
                        enemy2.velocity[0] *= -1

        #Checks enemy bullet collisions                
        for enemy_bullet in enemy_bullet_list:
            enemy_bullet.draw(canvas)
            enemy_bullet.update()
            
            #Removes bullet if it goes out of screen
            if enemy_bullet.position[1]>=FRAME_HEIGHT + enemy_bullet.radius:
                enemy_bullet_list.remove(enemy_bullet)
                
            #Damages player if it collides with bullet
            if distance_between(enemy_bullet.position, player_one.position)<=enemy_bullet.radius+player_one.radius:
                player_one.health -= enemy_bullet.damage
                enemy_bullet_list.remove(enemy_bullet)





def key_down(key):
    global right_moving, left_moving, up_moving, down_moving, character_firing_bullets, character_direction
    
    #Handles cases where movement keys/space key is pressed down
    if key == simplegui.KEY_MAP['right']:
        right_moving = True
        player_one.animated = True
        character_direction = 2
        
    if key == simplegui.KEY_MAP['left']:
        left_moving = True
        character_direction = 1
        player_one.animated = True
        
    if key == simplegui.KEY_MAP['up']:
        up_moving = True
        character_direction = 3
        player_one.animated = True
        
    if key == simplegui.KEY_MAP['down']:
        down_moving = True
        player_one.animated = True
        character_direction = 0
        
    if key == simplegui.KEY_MAP['space']:
        character_firing_bullets = True
        

        
def key_up(key):                               
    global right_moving, left_moving, up_moving, down_moving, character_firing_bullets
                           
    #Handles cases where movement keys/space keys is not pressed    
    if key == simplegui.KEY_MAP['right']:
        right_moving = False
        player_one.animated = False
        
    if key == simplegui.KEY_MAP['left']:
        left_moving = False
        player_one.animated = False
        
    if key == simplegui.KEY_MAP['up']:
        up_moving = False
        player_one.animated = False
        
    if key == simplegui.KEY_MAP['down']:
        down_moving = False
        player_one.animated = False
        
    if key == simplegui.KEY_MAP['space']:
        character_firing_bullets = False
        

#Handler assignments
frame = simplegui.create_frame('BACTERIA BLASTERS', FRAME_WIDTH, FRAME_HEIGHT)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)
frame.set_mouseclick_handler(mouse_handler)
frame.set_draw_handler(draw)
          
                           
#Arguably the single most important line of code!                           
frame.start()

