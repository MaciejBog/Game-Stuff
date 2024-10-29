import pygame, sys

from scripts.entities import PhysicsEntity, Player, Trash

from scripts.utils import load_image, load_images, Animation

from scripts.tilemap import Tilemap

from scripts.bubbles import Bubbles



class Game:
    def __init__(self):
        pygame.init()

        screen_width = 1024
        screen_height = 384

        pygame.display.set_caption('Trashcrab!')

        self.screen = pygame.display.set_mode((screen_width,screen_height))

        self.display = pygame.Surface((512,192))

        self.clock = pygame.time.Clock()

        self.movement = [False, False]

        self.dead = 0

        self.game_active = False

        self.winning = False

        self.game_start = True

        self.trash_counter = 0

        self.font = pygame.font.Font('Data/font/Pixelon-OGALo.ttf', 48)

        self.game_name = self.font.render('Trashcrab!', False, 'Black')
        self.start_text = self.font.render('Press "Space" To Start', False, 'Black')
        self.winning_textline1 = self.font.render('Congratulations!', False, 'Black')
        self.winning_textline2 = self.font.render('You cleaned the trash', False, 'Black')
        self.dead_textline1 = self.font.render('Oh no, you fell!', False, 'Black')
        self.dead_textline2 = self.font.render('Press Space to try again', False, 'Black')
        self.counter = self.font.render(f"{self.trash_counter}", False, 'Black')
        self.clean_up_text = self.font.render('Clean up the trash!', False, 'Black')
        self.clean_up_text_x = 150
        self.clean_up_text_y = 20

        self.assets = {
            'ground': load_images('tiles/ground'),
            'weeds': load_images('tiles/weeds'),
            'player': load_image('player/crabbo.png'),
            'background': load_image('background/backdrop_.png'),
            'spawners': load_images('spawners'),
            'bubbles': load_images('bubbles'),
            'corals': load_images('corals'),
            'rocks': load_images('rocks'),
            'trash': load_images('trash/idle'),
            'trash/idle': Animation(load_images('trash/idle'), img_dur=20),
            'urchin': load_images('urchin'),
            'player/idle': Animation(load_images('player/idle'), img_dur = 10),
            'player/run': Animation(load_images('player/run'), img_dur = 4),
            'player/jump': Animation(load_images('player/jump'), img_dur = 5)
                            }

        self.bubbles = Bubbles(self.assets['bubbles'], count=30)

        self.player = Player(self, (50,100), (30,15))


        self.tilemap = Tilemap(self, tile_size=16)
        self.tilemap.load('map.json')

        self.scroll = [0,0]
        self.trash = []

        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
            else:
                self.trash.append(Trash(self, spawner['pos'], (20,22)))



    def run(self):
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_SPACE:
                        if self.game_active == False:
                            self.game_active = True
                        else:
                            self.player.jump()      
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            if self.game_active:            
                self.display.blit(self.assets['background'], (0,0))    
                self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
                # self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
                render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

                self.bubbles.update()
                self.bubbles.render(self.display, offset=render_scroll)

                self.tilemap.render(self.display, offset=render_scroll)

                for trash in self.trash.copy():
                    trash.render(self.display, offset=render_scroll)

                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset=render_scroll)            

                if self.dead:
                    self.dead += 1
                    if self.dead > 30:
                        self.game_active = False
                        self.game_start = False

                player_rect = self.player.rect()

                for trash in self.trash:
                    trash_rect = trash.rect()
                    if pygame.Rect.colliderect(trash_rect, player_rect):
                        self.trash.remove(trash)
                        self.trash_counter += 1
                        self.counter = self.font.render(f"{self.trash_counter}", False, 'Black')

                self.display.blit(self.counter, (10,10))
                # self.clean_up_text_x = self.clean_up_text_x - render_scroll[0] / 120
                # self.display.blit(self.clean_up_text,(self.clean_up_text_x, self.clean_up_text_y))              
            
                self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))

                if self.trash_counter == 5:
                    self.game_active = False
                    self.winning = True
                    self.game_start = False

            else:
                self.dead = 0
                self.player.air_time = 0
                self.player.pos[0] = 50
                self.player.pos[1] = 100
                self.screen.fill('Blue')
                self.big_player = pygame.transform.scale(self.assets['player'], (120,60))
                self.screen.blit(self.big_player, (450, 150))
                self.screen.blit(self.game_name, (390, 70))

                if self.winning == True:
                    self.screen.blit(self.winning_textline1, (340, 250))
                    self.screen.blit(self.winning_textline2, (270, 300))     
                elif self.game_start == True:
                    self.screen.blit(self.start_text, (280, 250))
                else:
                    self.screen.blit(self.dead_textline1, (350, 250))
                    self.screen.blit(self.dead_textline2, (230, 300))    

            pygame.display.update()
            self.clock.tick(60)


Game().run()
