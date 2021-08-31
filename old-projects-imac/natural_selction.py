import pygame, random

pygame.init()

map_width = 800
map_height = 800
size = [map_width, map_height]
screen = pygame.display.set_mode(size)
colors = pygame.color.THECOLORS
pygame.display.set_caption("Natural Selection Game")
done = False
clock = pygame.time.Clock()
def id_generator():
    i = 0
    while True:
        i += 1
        yield i
ids = id_generator()
def collide(a, b):
    if a.id == b.id:
        return False
    return pygame.sprite.collide_mask(a, b)

class Organism(pygame.sprite.Sprite):

    def __init__(self, id, org_list, color = None):
        pygame.sprite.Sprite.__init__(self, org_list)
        self.org_list = org_list
        self.id = id
        self.change_x = random.randrange(0,6)
        self.change_y = random.randrange(0,6)
        width = random.randrange(5,50)
        height = random.randrange(5,50)
        x = random.randrange(0 + width, map_width - width)
        y = random.randrange(0 + height, map_height - height)
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.image = pygame.surface.Surface((width, height))
        self.image.fill(colors['hotpink2'])
        self.image.set_colorkey(colors['hotpink2'])
        self.color = color or random.choice([colors['red'], colors['green'], colors['blue']])
        pygame.draw.ellipse(self.image, self.color, [0, 0, width, height])
        self.mask = pygame.mask.from_surface(self.image) 
        self.collisions = set()
        self.age = 0
        self.children = 0
    def update(self):
        self.age += 1
        self.rect.move_ip(self.change_x, self.change_y)
        if self.rect.left < 0 or self.rect.right > map_width:
            self.change_x *= -1
        if self.rect.top < 0 or self.rect.bottom > map_height:
            self.change_y *= -1
        if self.age < 200:
            return
        if self.age > 350:
            print str(self.id) + ' died of age'
            self.kill()
            return
        if self.children > 4:
            print str(self.id) + ' died of too many children'
            self.kill()
            return
        collided = pygame.sprite.spritecollideany(self, self.org_list, collide)
        if collided and not collided.id in self.collisions and collided.age > 200 and len(self.org_list) < 100:
            self.collisions.add(collided.id)
            collided.collisions.add(self.id)
            r, g, b = (self.color[0] + collided.color[0]) / 2, \
                      (self.color[1] + collided.color[1]) / 2, \
                      (self.color[2] + collided.color[2]) / 2
            color = [r, g, b]
            if random.randrange(0, 100) < 10:
                color[random.randrange(0, 3)] = random.randrange(0, 256)
                print 'Offspring of ' + str(self.id) + ' and ' + str(collided.id) + ' mutates'
            Organism(next(ids), self.org_list, map(int, color))
            self.children += 1
            collided.children += 1
        else:
            self.collisions = set()
org_list = pygame.sprite.Group()
for _ in range(15):
    Organism(next(ids), org_list)
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    org_list.update()
    screen.fill(colors['white'])
    org_list.draw(screen)
    clock.tick(60)
    pygame.display.flip()
pygame.quit()
