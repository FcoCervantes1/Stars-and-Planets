import pygame
import math
import random

class Time:
    """Tiempo define el diferencial a trabajar, el 'clock' de pygame y cuenta
       el tiempo que ha transcurrido"""

    def __init__(self, dt=0.01):
        self.t = 0                          #Iniciamos con tiempo = 0
        self.dt = dt                        #El diferencial de tiempo
        self.clock = pygame.time.Clock()    #'Clock' de pygame
        #El clock de pygame nos ayuda a definir la frecuencia en hacer
        #las iteraciones en el while

    def update(self):
        self.t += self.dt                   #Aumentamos el tiempo en dt
        time.clock.tick(int(1/time.dt))

class Space:
    def __init__(self, limit_sup = [1336,700], limit_inf = [0,0]):
        self.x_min = limit_inf[0]
        self.y_min = limit_inf[1]
        self.x_max = limit_sup[0]
        self.y_max = limit_sup[1]
        self.x_center = (self.x_min + self.x_max)/2
        self.y_center = (self.y_min + self.y_max)/2
        self.center = [self.x_center, self.y_center]
        pygame.init()
        self.screen = pygame.display.set_mode(limit_sup)
        pygame.display.set_caption("Planets")

    def update(self):
        self.screen.fill((0, 0, 0))

class Celestial_object:
    """Objects created in the Universe"""
    list = []

    def __init__(self, pos, vel, density, mass, color):
        self.density = density
        self.mass = mass
        self.volume = mass / density
        self.radio  = (3 * self.volume / (4 * math.pi)) ** (1/3)
        self.pos = pos
        self.vel = vel
        self.ace = [0,0]
        self.color = color
        Celestial_object.list.append(self)

    def update(self, time, space):
        self.volume = self.mass / self.density
        self.radio  = (3 * self.volume / (4 * math.pi)) ** (1/3)
        self.acelerating(time, space)
        self.vel[0] += self.ace[0]*time.dt
        self.vel[1] += self.ace[1]*time.dt
        self.pos[0] += self.vel[0]*time.dt
        self.pos[1] += self.vel[1]*time.dt
        r = int(self.radio)
        c = self.color
        x = self.pos[0]
        y = space.y_max - self.pos[1]
        pygame.draw.circle(space.screen, c, [x,y], r)
        if self.pos[0] > space.x_max or self.pos[0] < space.x_min:
            self.remove()
        elif self.pos[0] > space.x_max or self.pos[0] < space.x_min:
            self.remove()

    def remove(self):
        if self in Celestial_object.list:
            Celestial_object.list.remove(self)
        if self in Planet.list:
            Planet.list.remove(self)
        elif self in Sun.list:
            Sun.list.remove(self)

    def acelerating(self, time, space):
        ax = 0
        ay = 0
        for obj in Celestial_object.list[:]:
            if obj == self:
                continue
            distances = distance(obj, self)
            ax += (0.001*obj.mass/distances[2]**3)*distances[0]
            ay += (0.001*obj.mass/distances[2]**3)*distances[1]
            if distances[2] <= self.radio + obj.radio:
                if (self in Sun.list and obj in Sun.list) or (self in Planet.list and obj in Planet.list):
                    color_ = self.color[:]
                    if self.mass < obj.mass:
                        color_ = obj.color[:]
                    if obj in Planet.list[:]:
                        Planet(pos_prom(self, obj),
                               vel =vel_prom(self, obj),
                               mass = self.mass + obj.mass,
                               color = color_)
                    else:
                        Sun(pos_prom(self, obj),
                            vel =vel_prom(self, obj),
                            mass = self.mass + obj.mass)
                    self.remove()
                    obj.remove()
                elif (self in Sun.list and obj in Planet.list) or (self in Planet.list and obj in Sun.list):
                    vel = vel_prom(self, obj)
                    if self in Sun.list:
                        self.mass += obj.mass
                        self.vel = vel
                        obj.remove()
                    elif obj in Sun.list:
                        obj.mass += self.mass
                        obj.vel = vel
                        self.remove()
        self.ace = [ax, ay]

class Sun(Celestial_object):
    """Its a fucking sun!!!"""
    list = []

    def __init__(self, pos, vel = [0,0], density = 1408, mass = 10**10, color = [255, 255, 0]):
        self.lowing = True
        Sun.list.append(self)
        super().__init__(pos, vel[:], density, mass, color[:])

    def update(self, time, space):
        self.update_color(time)
        super().update(time, space)

    def update_color(self, time):
        if self.lowing:
            self.color[1] -= 3
        else:
            self.color[1] += 3
        if self.color[1] >= 255 and not self.lowing:
            self.color[1] = 255
            self.lowing = True
        if self.color[1] <= 0 and self.lowing:
            self.color[1] = 0
            self.lowing = False

class Planet(Celestial_object):
    """Los planetas pueden ser comidos por soles, o formar otro planeta al
       chocar con otro"""
    list = []

    def __init__(self, pos, vel = [0,0], density = 5515, mass = 10**7, color = [0, 0, 0]):
        self.color = color[:]
        Planet.list.append(self)
        super().__init__(pos, vel = vel[:], density = density, mass=mass, color = self.color)

    def update(self, time, space):
        super().update(time, space)

def distance(obj1, obj2):
    x = obj1.pos[0] - obj2.pos[0]
    y = obj1.pos[1] - obj2.pos[1]
    return [x, y, (x**2+y**2)**(1/2)]

def pos_prom(obj1, obj2):
    x = (obj1.mass*obj1.pos[0]+obj2.mass*obj2.pos[0])/(obj1.mass+obj2.mass)
    y = (obj1.mass*obj1.pos[1]+obj2.mass*obj2.pos[1])/(obj1.mass+obj2.mass)
    return [x,y]

def vel_prom(obj1, obj2):
    vx = (obj1.mass*obj1.vel[0]+obj2.mass*obj2.vel[0])/(obj1.mass+obj2.mass)
    vy = (obj1.mass*obj1.vel[1]+obj2.mass*obj2.vel[1])/(obj1.mass+obj2.mass)
    return [vx, vy]

class Creator:
    def __init__(self):
        "Nada"

    def start(self, event):
        self.posi = [event.pos[0], space.y_max-event.pos[1]]

    def end(self, event):
        self.pose = [event.pos[0], space.y_max-event.pos[1]]
        vel = [self.pose[0]-self.posi[0],self.pose[1]-self.posi[1]]
        if event.button == 1:
            self.color = [0,0,0]
            self.color[random.choice([1,2])] = 255
            Planet(self.posi[:], color = self.color[:], vel = vel[:])
        elif event.button == 3:
            Sun(self.posi[:], vel=vel[:])

space = Space()
time = Time()
mouse = Creator()
working = True
while working:
    time.update()
    space.update()
    for obj in Sun.list[:]:
        obj.update(time, space)
    for obj in Planet.list[:]:
        obj.update(time, space)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse.start(event)
        if event.type == pygame.MOUSEBUTTONUP:
            mouse.end(event)
        elif event.type == pygame.QUIT:
            pygame.quit()
            working = False
