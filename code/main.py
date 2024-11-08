import pygame
from pygame.locals import *
from pygame.sprite import AbstractGroup
from world_datas import World_data as wd

pygame.init()
clock = pygame.time.Clock()

screen_width = 1000
screen_height = 1000
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Bunneta')

icon = pygame.image.load('../assets_img/app_icon.png')
pygame.display.set_icon(icon)

tile_size = 50
enemie_group = pygame.sprite.Group()

def draw_grid():
	for line in range(0, 20):
		pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
		pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))
                
class Player():
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1,5):
            img_right = pygame.image.load((f'../assets_img/Player/player_{num}.png'))
            img_right = pygame.transform.scale(img_right, (50,80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0

    def update(self):
        dy = 0
        dx = 0
        w_cooldown = 7
        key = pygame.key.get_pressed()
        #Jump
        if key[pygame.K_SPACE] and self.jumped == False:
            self.vel_y += -20
            self.jumped = True
        if key[pygame.K_SPACE] == False:
            self.jumped = False
        #Movement
        if key[pygame.K_LEFT]:
            dx -= 5
            self.counter += 1
            self.direction = -1
        if key[pygame.K_RIGHT]:
            dx += 5
            self.counter += 1
            self.direction = 1
        
        if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
            self.counter = 0
            self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]
        #anim
        if self.counter > w_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_right):
               self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]

        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y
        #col
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0

        self.rect.x += dx         
        self.rect.y += dy 

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0

        screen.blit(self.image, self.rect)

class World():
    def __init__(self, data):
        self.tile_list = []
        gn_img = pygame.image.load('../assets_img/Tiles/gn.png')
        grass_img = pygame.image.load('../assets_img/Tiles/grass.png')
        
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(gn_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count *  tile_size
                    img_rect.y = row_count *  tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count *  tile_size
                    img_rect.y = row_count *  tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    enemie = Enemy(col_count * tile_size, row_count * tile_size + 15)
                    enemie_group.add(enemie)
                    
                col_count += 1
            row_count += 1
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            #pygame.draw.rect(screen, ('#FF0000'), tile[1], 2)

class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('../assets_img/Enemies/enemie_1.png')
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_direction = 1
		self.move_counter = 0

	def update(self):
		self.rect.x += self.move_direction
		self.move_counter += 1
		if abs(self.move_counter) > 50:
			self.move_direction *= -1
			self.move_counter *= -1
                        
     


world = World(wd.world_data)
#enemie_group = pygame.sprite.Group()

player = Player(100, screen_height - 130)
run = True

#import images
while run:
    screen.fill('#000000')
    clock.tick(60)
    world.draw()
    enemie_group.update()
    enemie_group.draw(screen)
    player.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()