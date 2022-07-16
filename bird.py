import pygame as pg
from settings import *
from collections import deque


class Bird(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__(game.all_sprites_group)
        self.game = game
        self.image = game.bird_images[0]
        self.mask = pg.mask.from_surface(game.mask_image)
        self.rect = self.image.get_rect()
        self.rect.center = BIRD_POS

        self.images = deque(game.bird_images)
        self.animation_event = pg.USEREVENT + 0
        pg.time.set_timer(self.animation_event, BIRD_ANIMATION_TIME)

        self.falling_velocity = 0
        self.first_jump = False
        self.angle = 0

    def check_collision(self):
        hit = pg.sprite.spritecollide(self, self.game.pipe_group, dokill=False,
                                      collided=pg.sprite.collide_mask)
        if hit or self.rect.bottom > GROUND_Y or self.rect.top < -self.image.get_height():
            self.game.sound.hit_sound.play()
            pg.time.wait(1000)
            self.game.new_game()

    def rotate(self):
        if self.first_jump:
            if self.falling_velocity < -BIRD_JUMP_VALUE:
                self.angle = BIRD_JUMP_ANGLE
            else:
                self.angle = max(-2.5 * self.falling_velocity, -90)
            self.image = pg.transform.rotate(self.image, self.angle)
            # new mask
            mask_image = pg.transform.rotate(self.game.mask_image, self.angle)
            self.mask = pg.mask.from_surface(mask_image)

    def jump(self):
        self.game.sound.wing_sound.play()
        self.first_jump = True
        self.falling_velocity = BIRD_JUMP_VALUE

    def use_gravity(self):
        if self.first_jump:
            self.falling_velocity += GRAVITY
            self.rect.y += self.falling_velocity + 0.5 * GRAVITY

    def update(self):
        self.check_collision()
        self.use_gravity()

    def animate(self):
        self.images.rotate(-1)
        self.image = self.images[0]

    def check_event(self, event):
        if event.type == self.animation_event:
            self.animate()
            self.rotate()
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.jump()