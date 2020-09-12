import random
import os
import uuid

# import basic pygame modules
import pygame as pg

# import tensorflow to give things brains.
import tensorflow as tf

# see if we can load more than standard BMP
if not pg.image.get_extended():
    raise SystemExit("Sorry, extended image module required")

# Game Constants
SCREENRECT = pg.Rect(0, 0, 1920, 1080)


main_dir = os.path.split(os.path.abspath(__file__))[0]

def load_image(file):
    """ loads an image, prepares it for play
    """
    file = os.path.join(main_dir, "data", file)
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit('Could not load image "%s" %s' % (file, pg.get_error()))
    return surface.convert()


def load_sound(file):
    """ because pygame can be be compiled without mixer.
    """
    if not pg.mixer:
        return None
    file = os.path.join(main_dir, "data", file)
    try:
        sound = pg.mixer.Sound(file)
        return sound
    except pg.error:
        print("Warning, unable to load, %s" % file)
    return None





class Creature(pg.sprite.Sprite):
	""" Represents a creature in this evolution sim.
	"""

	image
	# This is to denote t
	mom = 00000000000000000000000000000000
	dad = 00000000000000000000000000000000
	name = 00000000000000000000000000000000

	radius = 40
	facing = 0

    # Creature stats
    speed = 10
	strength = 10
	waryness = 10
	health = 100
	stamina = 100
	""" Things to try when I get around to it.
	* Pickiness is mating
	* aggression
	* statlines like in an RPG where you could specialize into like a sprint build with no stamina.
	* 	Or ones where you can no longer eat meat, but get extra nutrition from grass.
	* Sort of cone of vision
	* Stat for seeing wider scope with less distance vs farther with narrower scope.
	"""

	def __init__(self):
		pg.sprite.Sprite.__init__(self, self.containers)
		self.image = pygame.draw.circle(screen, BLACK, [round(random.uniform(self.radius, SCREENRECT.right - self.radius)), round(random.uniform(self.radius, SCREENRECT.bottom - self.radius))], self.radius, 1)
        self.rect = self.image.get_rect()
        self.facing = round(random.uniform(0, 359))
        self.name = uuid.uuid4().hex

    def __init__(self, momCreature, dadCreature):
    	pg.sprite.Sprite.__init__(self, self.containers)
		self.image = self.images[0]
        self.rect = self.image.get_rect()
        mom = momCreature.getName()
        dad = dadCreature.getName()
        self.facing = round(random.uniform(0, 359))
        self.name = uuid.uuid4().hex
        # TODO
        # Need to add in the mixing of the genes of the parents here. Not just the stats but also the brains.

    def update(self):

    	# TODO
    	# Lookup how this move_ip works in regards to this creature.
        self.rect.move_ip(self.facing, 0)

        # This section pertains to keeping the thing inside the bounds of the screen. I think I would like to set the walls to be solid, but perhaps that would be better as a starting condition
        # of the entire simulation. So maybe have it be a toggle of how it works.
        if not SCREENRECT.contains(self.rect):
            self.facing = -self.facing
            self.rect.top = self.rect.bottom + 1
            self.rect = self.rect.clamp(SCREENRECT)

    def getName(): return self.name






def main(winstyle=0):
	# Initialize pygame
    if pg.get_sdl_version()[0] == 2:
        pg.mixer.pre_init(44100, 32, 2, 1024)
    pg.init()
    if pg.mixer and not pg.mixer.get_init():
        print("Warning, no sound")
        pg.mixer = None

    fullscreen = False
    # Set the display mode
    winstyle = 0  # |FULLSCREEN
    bestdepth = pg.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pg.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
    background = pg.Surface(SCREENRECT.size)
	pygame.display.set_caption("Evolution Simulator")


	# Initialize Game Groups
	creatures = pg.sprite.Group()
    all = pg.sprite.RenderUpdates()
    lastcreature = pg.sprite.GroupSingle()

    # Assign default groups to each sprite class
    Creature.containers = creatures, all, lastcreature

	done = False
	clock = pygame.time.Clock()
	for i in range(1,20):
		Creature()
	while not done:
	    clock.tick(10)

	    # get input
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_f:
                    if not fullscreen:
                        print("Changing to FULLSCREEN")
                        screen_backup = screen.copy()
                        screen = pg.display.set_mode(
                            SCREENRECT.size, winstyle | pg.FULLSCREEN, bestdepth
                        )
                        screen.blit(screen_backup, (0, 0))
                    else:
                        print("Changing to windowed mode")
                        screen_backup = screen.copy()
                        screen = pg.display.set_mode(
                            SCREENRECT.size, winstyle, bestdepth
                        )
                        screen.blit(screen_backup, (0, 0))
                    pg.display.flip()
                    fullscreen = not fullscreen

        keystate = pg.key.get_pressed()

        # clear/erase the last drawn sprites
        all.clear(screen, background)

        # update all the sprites
        all.update()

	    screen.fill(WHITE)