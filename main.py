import pygame as pg
import os
from sys import exit
from random import randint

# GAME PARAMETERS
scr_width, scr_hight = 1400, 900
ground_level = scr_hight * 0.8
jump_speed = -32
chute_on = 0
chute_speed = 1
acceleration = 1
player_speed = 5
fly_speed = 12
fly_frequency = 2
fly_screen_range = [.4, .6]
snail_speed = 9
snail_frequency = 3
player_initial_position = scr_width / 2
scale_factor = 1
window_caption = 'Pixel Runner'
game_on = True

# COLORS
text_color = (111,196,169)
bg_color = (94,129,162)

# FILES
font_file = os.path.join('font', 'Pixeltype.ttf')

bg_sound_file = os.path.join('audio', 'music.wav')
jump_sound_file = os.path.join('audio', 'jump.mp3')
run_sound_file = os.path.join('audio', 'run.mp3')
score_sound_file = os.path.join('audio', 'score.wav')
game_over_sound_file = os.path.join('audio', 'game_over.wav')

sky_image_file = os.path.join('graphics', 'Sky.png')
ground_image_file = os.path.join('graphics', 'ground.png')

player_stand_image_file = os.path.join('graphics', 'Player', 'player_stand.png')
player_chute_image_file = os.path.join('graphics', 'Player', 'player_chute.png')
player_jump_image_file = os.path.join('graphics', 'Player', 'player_jump.png')
player_sit_image_file = os.path.join('graphics', 'Player', 'player_sit.png')
player_walk_left_1_image_file = os.path.join('graphics', 'Player', 'player_walk_left_1.png')
player_walk_left_2_image_file = os.path.join('graphics', 'Player', 'player_walk_left_2.png')
player_walk_right_1_image_file = os.path.join('graphics', 'Player', 'player_walk_right_1.png')
player_walk_right_2_image_file = os.path.join('graphics', 'Player', 'player_walk_right_2.png')

fly_1_image_file = os.path.join('graphics', 'Fly', 'Fly1.png')
fly_2_image_file = os.path.join('graphics', 'Fly', 'Fly2.png')

snail_1_image_file = os.path.join('graphics', 'snail', 'snail1.png')
snail_2_image_file = os.path.join('graphics', 'snail', 'snail2.png')


class Player(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.player_rest = pg.image.load(player_stand_image_file).convert_alpha()
        self.player_chute = pg.image.load(player_chute_image_file).convert_alpha()
        self.player_sit = pg.image.load(player_sit_image_file).convert_alpha()
        self.player_jump = pg.image.load(player_jump_image_file).convert_alpha()
        self.player_walk_left_1 = pg.image.load(player_walk_left_1_image_file).convert_alpha()
        self.player_walk_left_2 = pg.image.load(player_walk_left_2_image_file).convert_alpha()
        self.player_walk_right_1 = pg.image.load(player_walk_right_1_image_file).convert_alpha()
        self.player_walk_right_2 = pg.image.load(player_walk_right_2_image_file).convert_alpha()

        self.player_rest = pg.transform.rotozoom(self.player_rest, 0, scale_factor)
        self.player_chute = pg.transform.rotozoom(self.player_chute, 0, scale_factor)
        self.player_sit = pg.transform.rotozoom(self.player_sit, 0, scale_factor)
        self.player_jump = pg.transform.rotozoom(self.player_jump, 0, scale_factor)
        self.player_walk_left_1 = pg.transform.rotozoom(self.player_walk_left_1, 0, scale_factor)
        self.player_walk_left_2 = pg.transform.rotozoom(self.player_walk_left_2, 0, scale_factor)
        self.player_walk_right_1 = pg.transform.rotozoom(self.player_walk_right_1, 0, scale_factor)
        self.player_walk_right_2 = pg.transform.rotozoom(self.player_walk_right_2, 0, scale_factor)


        self.player_walk_left = [self.player_walk_left_1, self.player_walk_left_2]
        self.player_walk_right = [self.player_walk_right_1, self.player_walk_right_2]

        self.image = self.player_rest
        self.rect_update()

        self.speed = 0
        self.y_position = ground_level

        self.jump_sound = pg.mixer.Sound(jump_sound_file)
        self.jump_sound.set_volume(0.6)

    def rect_update(self):
        x_position = self.rect.midbottom[0] if hasattr(self, 'rect') else player_initial_position
        self.rect = self.image.get_rect(midbottom=(x_position, ground_level))

    def reset(self):
        self.speed = 0
        self.y_position = ground_level
        self.image = self.player_rest
        self.rect_update()

    def sit_down(self):
        if self.rect.bottom == ground_level:
            self.image = self.player_sit
            self.rect_update()
    
    def stand_up(self):
        if self.rect.bottom == ground_level:
            self.image = self.player_rest
            self.rect_update()

    def go_left(self):
        if self.rect.bottom == ground_level:
            self.image = self.player_walk_left[pg.time.get_ticks() // 100 % 2]
            self.rect_update()
        self.rect.x -= player_speed

    def go_right(self):
        if self.rect.bottom == ground_level:
            self.image = self.player_walk_right[pg.time.get_ticks() // 100 % 2]
            self.rect_update()
        self.rect.x += player_speed

    def gravity(self):
        self.speed += acceleration
        if chute_on:
            if self.speed > 0 and self.rect.bottom < ground_level:
                self.speed = chute_speed
                self.image = self.player_chute
                self.rect_update()
            else: 
                self.speed
        self.y_position += self.speed
        self.y_position = min(self.y_position, ground_level)
        self.rect.bottom = self.y_position

    def kb_input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT] and self.rect.left > 0:
            self.go_left()

        if keys[pg.K_RIGHT] and self.rect.right < scr_width:
            self.go_right()

        if keys[pg.K_UP] and self.rect.bottom == ground_level:
            self.speed = jump_speed
            self.image = self.player_jump
            self.jump_sound.play()

        if keys[pg.K_DOWN]:
            self.sit_down()

        if  not keys[pg.K_LEFT] and not keys[pg.K_RIGHT] and not keys[pg.K_UP] and not keys[pg.K_DOWN] and self.rect.bottom == ground_level:
            self.image = self.player_rest
            self.rect_update()

    def update(self):
        # print(self.rect.y)
        self.gravity()
        self.kb_input()


class Fly(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.fly_1_surface = pg.image.load(fly_1_image_file).convert_alpha()
        self.fly_2_surface = pg.image.load(fly_2_image_file).convert_alpha()

        self.frames = [self.fly_1_surface, self.fly_2_surface]
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(center=(randint(scr_width, int(scr_width * 1.1)), randint(int(scr_hight*fly_screen_range[0]), int(scr_hight*fly_screen_range[1]))))

    def destroy(self):
        if self.rect.x < -100:
            self.kill()

    def update(self):
        self.image = self.frames[pg.time.get_ticks() // 50 % 2]
        self.rect.x -= fly_speed
        self.destroy()


class Snail(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.snail_1_surface = pg.image.load(snail_1_image_file).convert_alpha()
        self.snail_2_surface = pg.image.load(snail_2_image_file).convert_alpha()

        self.frames = [self.snail_1_surface, self.snail_2_surface]
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(scr_width, int(scr_width * 1.3)), ground_level))

    def destroy(self):
        if self.rect.x < -100:
            self.kill()

    def update(self):
        self.image = self.frames[pg.time.get_ticks() // 250 % 2]
        self.rect.x -= snail_speed
        self.destroy()


def snail_collision(player, snail_group):
    if pg.sprite.spritecollide(player, snail_group, False):
        snail_group.empty()
        fly_group.empty()
        player.reset()
        game_over_sound.play()
        return False
    else:
        return True


pg.init()
screen = pg.display.set_mode((scr_width, scr_hight))
pg.display.set_caption(window_caption)

clock = pg.time.Clock()

test_font = pg.font.Font(font_file, 70)

bg_sound = pg.mixer.Sound(bg_sound_file)
bg_sound.set_volume(0.02)
bg_sound.play(loops=-1)

run_sound = pg.mixer.Sound(run_sound_file)
run_sound.set_volume(0.6)

score_sound = pg.mixer.Sound(score_sound_file)
score_sound.set_volume(0.2)

game_over_sound = pg.mixer.Sound(game_over_sound_file)
game_over_sound.set_volume(0.2)

score = 0


# WELCOME SCREEN
player_logo = pg.image.load(player_stand_image_file).convert_alpha()
player_logo = pg.transform.rotozoom(player_logo, 0, 3)
player_logo_rectangle = player_logo.get_rect(center=(scr_width/2, scr_hight/2))

game_name = test_font.render(window_caption, False, text_color)
game_name_rectangle = game_name.get_rect(center=(scr_width/2, player_logo_rectangle.top-80))

game_message = test_font.render('Press space to start', False, text_color)
game_message_rectangle = game_message.get_rect(center=(scr_width/2,player_logo_rectangle.bottom+80))


# GAME SCREEN
sky_surface = pg.image.load(sky_image_file).convert()
sky_surface = pg.transform.scale(sky_surface, (scr_width, ground_level))
ground_surface = pg.image.load(ground_image_file).convert()
ground_surface = pg.transform.scale(ground_surface, (scr_width, scr_hight-ground_level))

player = pg.sprite.GroupSingle()
player.add(Player())
fly_group = pg.sprite.Group()
snail_group = pg.sprite.Group()


fly_timer = pg.USEREVENT + 1
pg.time.set_timer(fly_timer, int(fly_frequency * 1000))

snail_timer = pg.USEREVENT + 2
pg.time.set_timer(snail_timer, int(snail_frequency * 1000))



while True:

    for event in pg.event.get():

        if event.type == pg.QUIT:
            pg.quit()
            exit()

        if game_on:

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    game_on = False
                    snail_group.empty()
                    fly_group.empty()
                    player.sprite.reset()
                if event.key in (pg.K_LEFT, pg.K_RIGHT) and player.sprite.rect.bottom == ground_level:
                    run_sound.play(loops=-1)

            if event.type == pg.KEYUP:
                if  event.key == pg.K_DOWN:
                    player.sprite.stand_up()
                if event.key in (pg.K_LEFT, pg.K_RIGHT):
                    run_sound.stop()

            if event.type == fly_timer:
                fly_group.add(Fly())
            if event.type == snail_timer:
                snail_group.add(Snail())

        else:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    score = 0
                    game_on = True

    if game_on:

        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0, ground_level))
        score_surface = test_font.render(f"Score: {score}", False, text_color)
        screen.blit(score_surface, (30, 30))
        
        player.draw(screen)
        player.sprite.update()

        fly_group.draw(screen)
        fly_group.update()
        snail_group.draw(screen)
        snail_group.update()

        if pg.sprite.spritecollide(player.sprite, fly_group, True):
            score += 10
            score_sound.play()
        game_on = snail_collision(player.sprite, snail_group)
        
    else:

        screen.fill(bg_color)
        screen.blit(player_logo, player_logo_rectangle)
        score_message = test_font.render(f"Your score: {score}", False, text_color)
        score_message_rectangle = score_message.get_rect(center=(scr_width/2,player_logo_rectangle.top-80))
        if score:
            screen.blit(score_message, score_message_rectangle)
        else:
            screen.blit(game_name, game_name_rectangle)
        screen.blit(game_message, game_message_rectangle)
        

    pg.display.update()
    clock.tick(60)