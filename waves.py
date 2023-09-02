import pygame
from math import sin, cos, pi
from random import randrange

time_speed = 20
calmness = 8

# pygame setup
pygame.init()
screen = pygame.display.set_mode((512, 512), pygame.RESIZABLE)
pygame.display.set_caption("Waves")
#pygame.display.set_icon(pygame.image.load('./boat.png'))
clock = pygame.time.Clock()
running = True

w, h = pygame.display.get_surface().get_size()

class Ship:
    def __init__(self, x, y, size, speed):
        self.x = x
        self.y = y
        self.xv = 0
        self.yv = 0
        self.angle = 0
        self.size = size
        self.speed = speed
    
    def draw(self):
        offset = (self.x, int(h/2+4)+ocean_wave(self.x))
    
        self.angle = derivative_ocean(self.x) / 2
        
        pygame.draw.polygon(screen, (160, 60, 1), [
            change((-1, -0.8), self.angle, offset, self.size),
            change((1, -0.8), self.angle, offset, self.size),
            change((0.6, -0.2), self.angle, offset, self.size),
            change((0, 0), self.angle, offset, self.size),
            change((-0.6, -0.2), self.angle, offset, self.size)
        ])
        
        pygame.draw.polygon(screen, (0, 0, 0), [
            change((-1, -0.8), self.angle, offset, self.size),
            change((1, -0.8), self.angle, offset, self.size),
            change((0.6, -0.2), self.angle, offset, self.size),
            change((0, 0), self.angle, offset, self.size),
            change((-0.6, -0.2), self.angle, offset, self.size)
        ], 2)
        
        pygame.draw.polygon(screen, (160, 60, 1), [
            change((-0.1, -0.8), self.angle, offset, self.size),
            change((-0.1, -1.6), self.angle, offset, self.size),
            change((0.1, -1.6), self.angle, offset, self.size),
            change((0.1, -0.8), self.angle, offset, self.size)
        ])
        
        pygame.draw.polygon(screen, (0, 0, 0), [
            change((-0.1, -0.8), self.angle, offset, self.size),
            change((-0.1, -1.6), self.angle, offset, self.size),
            change((0.1, -1.6), self.angle, offset, self.size),
            change((0.1, -0.8), self.angle, offset, self.size)
        ], 2)
        
        pygame.draw.polygon(screen, (240, 240, 255), [
            change((-0.7, -1.6), self.angle, offset, self.size),
            change((0, -2.4), self.angle, offset, self.size),
            change((0.7, -1.6), self.angle, offset, self.size)
        ])
        
        pygame.draw.polygon(screen, (0, 0, 0), [
            change((-0.7, -1.6), self.angle, offset, self.size),
            change((0, -2.4), self.angle, offset, self.size),
            change((0.7, -1.6), self.angle, offset, self.size)
        ], 2)
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.xv -= self.speed
        if keys[pygame.K_RIGHT]:
            self.xv += self.speed
        
        global calmness
        if keys[pygame.K_UP] and calmness < 20:
            calmness += 0.1
        if keys[pygame.K_DOWN] and calmness > 1.2:
            calmness -= 0.1
        
        self.xv = max(min(self.xv, self.speed), -self.speed)
        
        self.xv += self.angle / (3 * pi)
        
        self.x += self.xv
        self.xv /= 1.05
        
        self.x = max(min(self.x, w + self.size * 3), -(w + self.size * 3))

ship = Ship(w/2, h/2, 20, 2)

class Wave:
    def __init__(self, amp,mod,dil):
        self.amp = amp
        self.mod = mod
        self.dil = dil

waves = [
    Wave(10,100,20),
    Wave(23,70,30),
    Wave(11,40,14),
    Wave(30,90,10.3),
    # Wave(5, 40, 15),
    # Wave(80, 500, 50)
]

class Particle:
    def __init__(self, x, y, xv, yv, col):
        self.x = x
        self.y = y
        self.xv = xv
        self.yv = yv
        self.col = col
        self.lx = x
        self.ly = y
        self.ttd = 0
    
    def draw(self):
        line(self.lx, self.ly, self.x, self.y, self.col, 2)
    
    def update(self):
        self.lx = self.x
        self.ly = self.y
        self.x += self.xv
        self.y += self.yv
        
        
        if self.ttd > 180:
            particles.remove(self)
        else:
            self.ttd += 1


particles = []

# Trig functions

def sine_wave(x, amp, mod, dil):
    return sin(pi * x * (1 / mod) + ((pygame.time.get_ticks() / time_speed)/dil)) * amp

def derivative_sine(x, amp, mod, dil):
    return cos(pi * x * (1 / mod) + ((pygame.time.get_ticks() / time_speed)/dil)) * amp * (pi / mod)

def ocean_wave(x):
    val = 0
    for i in waves:
        val += sine_wave(x, i.amp, i.mod, i.dil)
    return val / calmness

def derivative_ocean(x):
    val = 0
    for i in waves:
        val += derivative_sine(x, i.amp, i.mod, i.dil)
    return val / calmness

def rotate(x,y,a):
    return (x * cos(a) - y*sin(a), x*sin(a) + y*cos(a))

def clamp(v, mini, maxi):
    return max(min(v, maxi), mini)


# Drawing functions

def pset(x,y,c):
    pygame.draw.rect(screen, c, (x,y,1,1))

def line(x,y,x2,y2,c,w = 1):
    pygame.draw.line(screen, c, (x, y), (x2, y2), w)




# Helper functions
def add_tuple(a, b):
    return tuple(map(sum,zip(a,b)))

# Pointe, angle, offset, size
def change(t, a, o, s):
    return add_tuple(rotate(t[0] * s, t[1] * s, a), o)

def dist(a, b):
    return tuple(map(lambda i, j: i - j, a,b))

def get_offsetted(o):
    return (o, ocean_wave(o))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    w, h = pygame.display.get_surface().get_size()


    if calmness < 2:
        for i in range(int((w / 256)* (1 / calmness))):
            particles.append(
                Particle(
                    randrange(-w, w),
                    0,
                    randrange(8, 10),
                    10,
                    (0,randrange(0, 100),randrange(50, 200))
                )
            )

    ship.update()

    for i in particles:
        i.update()
    
    screen.fill((clamp(152 + (calmness * 7.15), 0, 255),clamp(152 + (calmness * 7.15), 0, 255),clamp(152 + (calmness * 7.15), 0, 255)))
    
    
    for i in particles:
        i.draw()
    
    for i in range(0, w):
        line(i, int(h/2)+1 + ocean_wave(i), i, h, (0, clamp(80 + (calmness * 3.6), 0, 255), clamp(112 + (calmness * 7.15), 0, 255)), 1) # Draw the water
        line(i, int(h/2) + ocean_wave(i), i+1, int(h/2) + ocean_wave(i+1),(0,0,0), 2) # Draw the outline
    
    
    ship.draw()
    
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()