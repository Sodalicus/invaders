#!/usr/bin/env python3
# Invaders Game
# Author: Paweł Krzemiński 
# Modified LiveWires module from "Python for absolute beginers book" by Michael Dawson

import random, time
from livewires import games, color

WIDTH = 640
HEIGHT = 480

games.init(screen_width = 640, screen_height = 480, fps = 50)

class Ship(games.Sprite):
    """Supposed to be a wrapper class for Player and Alien classes"""
    TIMEOUT = 40 


class Player(Ship):
    """Player's ship class, loads individual image, sets up alignment variables.
    its methods update and fire handle keyboard ship control and projectiles
    firing retrospectively. """
    image = games.load_image("media/ship.bmp")

    def __init__(self):
        super(Player, self).__init__(image=Player.image, x=WIDTH/2, y=HEIGHT-50)
        self.deadly = False
        self.alien = False 
        self.projectile_timeout = 0

    def update(self):
        """ Keys to movement assigment, game screen edges detection
        and collision with alien projectiles handling"""
        if self.projectile_timeout > 0: self.projectile_timeout -=1
        if games.keyboard.is_pressed(games.K_RIGHT): self.x+=2
        if games.keyboard.is_pressed(games.K_LEFT): self.x-=2
        if self.left < 0: self.left = 0
        if self.right > WIDTH: self.right = WIDTH
        if games.keyboard.is_pressed(games.K_SPACE):
            self.fire()
        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                if sprite.deadly == True and sprite.alien == True:
                    sprite.destroy()
                    self.die()



    def fire(self):
        """Fire projectile from player's ship"""
        if self.projectile_timeout == 0:
            new_projectile = Projectile(x=self.x, y=self.y-20, dy = -4)
            games.screen.add(new_projectile)
            self.projectile_timeout = Ship.TIMEOUT

    def die(self):
        """ Destroy player's ship, display game over message and quit"""
        self.destroy()
        game_over = games.Message(value="GAME OVER", size=60, color=color.red,\
                x=WIDTH/2, y=HEIGHT/2, lifetime=180, \
                after_death=games.screen.quit)
        games.screen.add(game_over)



class Alien(Ship):
    """Enemy`s class, loads enemy image, controls it`s movement and attacks""" 
    image = games.load_image("media/satelite.bmp")
    alien_count = 0
    def __init__(self, x, y, dx, game):
        super(Alien, self).__init__(image = Alien.image, x=x, y=y, dx=dx)
        self.projectile_timeout = random.randrange(200) 
        self.deadly = False
        self.alien = True
        Alien.alien_count+=1
        self.game = game

    def update(self):
        self.angle +=1
        if self.projectile_timeout > 0: self.projectile_timeout -=1
        self.fire()
        if self.right > WIDTH:
            self.right = WIDTH
            self.dx = -self.dx
        if self.left < 0:
            self.left = 0
            self.dx = -self.dx
        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                if sprite.deadly == True and sprite.alien == False:
                    sprite.destroy()
                    self.die()

    def fire(self):
        if self.projectile_timeout == 0:
            new_projectile = Projectile(x=self.x, y=self.y+30, dy = 2,color=1)
            games.screen.add(new_projectile)
            self.projectile_timeout = random.randrange(200) 

    def die(self):
        self.destroy()
        self.game.score += 20
        self.game.score_display.value = "Score: "+str(self.game.score)
        self.game.score_display.right = WIDTH-30
        if Alien.alien_count > 0: Alien.alien_count-=1
        if Alien.alien_count == 0: self.game.level_up()



class Projectile(games.Sprite):
    images = (games.load_image("media/projectile.bmp"),\
            games.load_image("media/alien_projectile.bmp"))
    def __init__(self, x,y,dy,color=0): 
        self.deadly = True 
        if color == 0: self.alien = False
        elif color == 1:self.alien = True
        super(Projectile, self).__init__(image = Projectile.images[color],x=x,y=y,dy=dy)
    def update(self):
        if self.top < 0:self.destroy()



class Game(games.Sprite):
    def __init__(self):
        self.ship = Player()
        games.screen.add(self.ship)
        background = games.load_image("media/background.bmp")
        games.screen.set_background(background)
        self.level = 0
        self.score = 0
        self.score_display = games.Text(value="Score: 0", size = 20, color=color.white, top = 10,\
            right = WIDTH-30, is_collideable=False)
        games.screen.add(self.score_display)
        self.level_display = games.Text(value="Level: 0", size = 20, color=color.white, top = 10,\
            left = 30, is_collideable=False)
        games.screen.add(self.level_display)

    def level_up(self):
        self.level+=1
        self.level_display.value = "Level: "+str(self.level)
        self.level_display.left = 30
        for alien in range(self.level):
            direction = random.choice((-1,1))
            altitude = random.choice((50, 80, 110, 140, 170))
            position = random.randrange(WIDTH)
            alien = Alien(x = position, y = altitude, dx = direction, game=self)
            games.screen.add(alien)

    def main(self):
        self.level_up()
        games.screen.mainloop()

game = Game()
game.main()
