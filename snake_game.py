import pygame,sys,random
from pygame.math import Vector2


class FURIT:
    def __init__(self):
        self.randomized()
        self.pokemon = pygame.image.load('graphic_sound/pokemon.png')
        self.pokemon_sound = pygame.mixer.Sound('graphic_sound/pokemon_sound.mp3')
    def draw_fruit(self):
        furit_rect = pygame.Rect(self.pos.x*cell_size,self.pos.y*cell_size,cell_size,cell_size)
        #pygame.draw.rect(screen,(126,166,114),furit_rect)
        screen.blit(self.pokemon,furit_rect)
    def randomized(self):
        self.x = random.randint(0,cell_number-1)
        self.y = random.randint(0,cell_number-1)
        self.pos = Vector2(self.x,self.y)

class SNAKE:
    def __init__(self):
        self.body = [Vector2(7,10),Vector2(6,10),Vector2(5,10)]
        self.direction = Vector2(1,0)


        self.head_up = pygame.image.load('graphic_sound/head_up.png')
        self.head_down = pygame.image.load('graphic_sound/head_down.png')     	    
        self.head_right = pygame.image.load('graphic_sound/head_right.png')
        self.head_left = pygame.image.load('graphic_sound/head_left.png')
		
        self.tail_up = pygame.image.load('graphic_sound/tail_up.png')
        self.tail_down = pygame.image.load('graphic_sound/tail_down.png')
        self.tail_right = pygame.image.load('graphic_sound/tail_right.png')
        self.tail_left = pygame.image.load('graphic_sound/tail_left.png')

        self.body_vertical = pygame.image.load('graphic_sound/body_vertical.png')
        self.body_horizontal = pygame.image.load('graphic_sound/body_horizontal.png')

        self.body_tr = pygame.image.load('graphic_sound/body_tr.png')
        self.body_tl = pygame.image.load('graphic_sound/body_tl.png')
        self.body_br = pygame.image.load('graphic_sound/body_br.png')
        self.body_bl = pygame.image.load('graphic_sound/body_bl.png')

    
    def draw_snake(self):
        self.update_graphics()

        for index,block in enumerate(self.body):
            snake_rect = pygame.Rect(block.x * cell_size,block.y*cell_size,cell_size,cell_size)
            
            if index == 0:
                screen.blit(self.head,snake_rect)
            elif index == len(self.body)- 1:
                screen.blit(self.tail,snake_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block 
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical,snake_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal,snake_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x== -1:
                        screen.blit(self.body_tl,snake_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl,snake_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x== 1:
                        screen.blit(self.body_tr,snake_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br,snake_rect)


    def update_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down

        tail_relation =  self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

    def move_snake(self):
        body_copy = self.body[:-1]
        body_copy.insert(0,body_copy[0] + self.direction )
        self.body = body_copy
    
    def add_block(self):
        body_copy = self.body[:]
        body_copy.insert(0,body_copy[0] + self.direction )
        self.body = body_copy

    def restart(self):
        self.body = [Vector2(7,10),Vector2(6,10),Vector2(5,10)]
        self.direction = Vector2(1,0)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.furit = FURIT()
    
    def draw_elements(self):
        self.draw_grass()
        self.furit.draw_fruit()
        self.snake.draw_snake()
        self.game_score()

    def update(self):
        self.snake.move_snake()
        self.collision()
        self.fail()

    def collision(self):
        if self.furit.pos == self.snake.body[0]:
            pygame.mixer.Sound.play(self.furit.pokemon_sound)
            self.furit.randomized()
            self.snake.add_block()

    def fail(self):
        if not  0<= self.snake.body[0].x < cell_number or not  0<= self.snake.body[0].y < cell_number : 
            self.game_restart()
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_restart()

        for block in self.snake.body[1:]:
            if block ==  self.furit.pos:
                self.furit.randomized()
                
    def draw_grass(self):
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size,row*cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,(167,209,61),grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 !=0:
                        grass_rect = pygame.Rect(col * cell_size,row*cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,(167,209,61),grass_rect)

    def game_score(self):
        game_text = game_font.render(str(len(self.snake.body) - 3),True,(56,74,12))
        text_rect = game_text.get_rect(center = (cell_size*cell_number-60,cell_number*cell_size -40))
        screen.blit(game_text,text_rect)

        pokemon_rect = self.furit.pokemon.get_rect(midright=(text_rect.left, text_rect.centery))
        screen.blit(self.furit.pokemon,pokemon_rect)


    def game_restart(self):
        self.snake.restart()  

pygame.init()
clock = pygame.time.Clock()

cell_number = 20 
cell_size = 40
screen = pygame.display.set_mode((cell_number*cell_size,cell_size*cell_number))
pygame.display.set_caption('snake')

game_font = pygame.font.Font(None,40)
main_game = MAIN()


screen_update = pygame.USEREVENT
pygame.time.set_timer(screen_update,150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == screen_update:
            main_game.update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                   main_game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)

    screen.fill((175,215,70))
    main_game.draw_elements()

    clock.tick(60)
    pygame.display.update()