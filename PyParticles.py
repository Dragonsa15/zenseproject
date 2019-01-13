import random
import math

'''code for adding 2 vectors'''
def addVectors(angle1, length1, angle2, length2):
    x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y  = math.cos(angle1) * length1 + math.cos(angle2) * length2
    
    angle = 0.5 * math.pi - math.atan2(y, x)
    length  = math.hypot(x, y)

    return (angle, length)

'''code to check if 2 objects collide'''
def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    
    dist = math.hypot(dx, dy)
    if dist < p1.size + p2.size:
        angle = math.atan2(dy, dx) + 0.5 * math.pi
        total_mass = p1.mass + p2.mass

        (p1.angle, p1.speed) = addVectors(p1.angle, p1.speed*(p1.mass-p2.mass)/total_mass,angle, 2*p2.speed*p2.mass/total_mass)
        (p2.angle, p2.speed) = addVectors(p2.angle, p2.speed*(p2.mass-p1.mass)/total_mass,angle+math.pi, 2*p1.speed*p1.mass/total_mass)
        p1.speed *= p1.elasticity
        p2.speed *= p2.elasticity

        overlap = 0.5*(p1.size + p2.size - dist+1)
        p1.x += math.sin(angle)*overlap
        p1.y -= math.cos(angle)*overlap
        p2.x -= math.sin(angle)*overlap
        p2.y += math.cos(angle)*overlap

''' to combine 2 objects one in another (p2 in p1 and p2 gets deleted in the main code or kept as the user wants)'''

def combine(p1, p2):
    if math.hypot(p1.x - p2.x, p1.y - p2.y) < p1.size+p2.size:
        total_mass = p1.mass + p2.mass
        p1.x = (p1.x*p1.mass + p2.x*p2.mass)/total_mass
        p1.y = (p1.y*p1.mass + p2.y*p2.mass)/total_mass
        (p1.angle, p1.speed) = addVectors(p1.angle, p1.speed * p1.mass / total_mass,p2.angle, p2.speed * p2.mass / total_mass)
        p1.speed *= (p1.elasticity * p2.elasticity)
        p1.mass += p2.mass
        p1.collide_with = p2             #here this collide_with even though is not there in particle class but becomes a part of its attributes and when it is called as an object using __dict__ it is shown in its attributes as an object

class Particle():
    def __init__(self,x, y, size, mass=1):
        self.x = x
        self.y = y
        self.size = size
        self.colour = (0, 0, 255)
        self.speed = 0
        self.angle = 0
        self.mass = mass
        self.drag = 1
        self.elasticity = 0.9
    
    def move(self):
        '''code to move a particle based on angle and speed'''
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed

    def experienceDrag(self):
        '''drag if there is wind'''
        self.speed *= self.drag
        
    def accelerate(self, vector):
        '''gravity'''
        (angle1,speed1) = vector
        (self.angle, self.speed) = addVectors(self.angle, self.speed, angle1,speed1)

    def mouseMove(self,x, y):
        '''move the object with mouse if selected(using find particles in main)'''
        dx = x - self.x
        dy = y - self.y
        self.angle = 0.5*math.pi + math.atan2(dy, dx)
        self.speed = math.hypot(dx, dy) * 0.1
    def attract(self, other):
        '''Universal gravitation'''
        dx = (self.x - other.x)
        dy = (self.y - other.y)
        dist = math.hypot(dx, dy)
        
        theta = math.atan2(dy, dx)
        force = 2 * self.mass * other.mass / dist ** 2
        self.accelerate((theta - 0.5 * math.pi, force/self.mass))
        other.accelerate((theta + 0.5 * math.pi, force/other.mass))

''' This is the class which defines screen and all its parameters  ,like updating it from time to time'''

class Environment:
    def __init__(self,width, height):
        self.width = width
        self.height = height
        self.particles = []
        self.colour = (255,255,255)
        self.mass_of_air = 0.2
        self.elasticity = 0.75
        self.acceleration = (math.pi,1)
        #here the below part is kind of a use of functions as objects of call so we call only those function we want and not writing a lot in the main function
        self.particle_functions1 = []
        self.particle_functions2 = []
        self.function_dict = {                                        
        'move': (1, lambda p: p.move()),
        'drag': (1, lambda p: p.experienceDrag()),
        'bounce': (1, lambda p: self.bounce(p)),
        'accelerate': (1, lambda p: p.accelerate(self.acceleration)),
        'collide': (2, lambda p1, p2: collide(p1, p2)),
        'attract': (2, lambda p1, p2: p1.attract(p2)),
        'combine': (2, lambda p1, p2: combine(p1, p2))}

    def addFunctions(self, function_list):
        """ Look up functions names in dictionary and add to particle function lists"""
        
        for func in function_list:
            (n, f) = self.function_dict.get(func, (-1, None))
            if n == 1:
                self.particle_functions1.append(f)
            elif n == 2:
                self.particle_functions2.append(f)
            else:
                print("No such function: %s" % f)

    def addParticles(self, n=1, **kargs):
        ''' This function is used to add new particles on a screen (kargs) is usually used to check if the following elements are entered
as parameters and takes them instead of random values kind of like *argc[] in C'''        
        
        for i in range(n):
            size = kargs.get('size', random.randint(10, 20))
            mass = kargs.get('mass', random.randint(1, 100))
            x = kargs.get('x', random.uniform(size, self.width-size))
            y = kargs.get('y', random.uniform(size, self.height-size))
            p = Particle(x, y, size, mass)
            p.speed = kargs.get('speed', random.random())
            p.angle = kargs.get('angle', random.uniform(0, math.pi*2))
            p.colour = kargs.get('colour',(255,255,255))
            p.drag = (p.mass/(p.mass + self.mass_of_air)) ** p.size
            self.particles.append(p)
    
    def findParticle(self, x, y):
        '''Used to find if a object is within other object(for circles usually)'''
        for p in self.particles:
            if math.hypot(p.x-x, p.y-y) <= p.size:
                return p
        return None

    def bounce(self, particle):    
        if particle.x > self.width - particle.size:
            particle.x = 2*(self.width - particle.size) - particle.x
            particle.angle = - particle.angle
            particle.speed *= self.elasticity

        elif particle.x < particle.size:
            particle.x = 2*particle.size - particle.x
            particle.angle = - particle.angle
            particle.speed *= self.elasticity

        if particle.y > self.height - particle.size:
            particle.y = 2*(self.height - particle.size) - particle.y
            particle.angle = math.pi - particle.angle
            particle.speed *= self.elasticity

        elif particle.y < particle.size:
            particle.y = 2*particle.size - particle.y
            particle.angle = math.pi - particle.angle
            particle.speed *= self.elasticity

    def update(self):
        '''updates the screen after every call'''

        for i, particle in enumerate(self.particles):
            for f in self.particle_functions1:
                f(particle)
            for particle2 in self.particles[i+1:]:
                for f in self.particle_functions2:
                    f(particle, particle2)

''' Here this section is  used to change the display of screen no real mechanics here'''
class UniverseScreen:
    def __init__ (self, width, height):
        self.width = width
        self.height = height
        (self.dx, self.dy) = (0, 0)
        (self.mx, self.my) = (0, 0)
        self.magnification = 1.0
        
    def scroll(self, dx=0, dy=0):
        self.dx += dx * self.width / (self.magnification*10)
        self.dy += dy * self.height / (self.magnification*10)
        
    def zoom(self, zoom):
        self.magnification *= zoom
        self.mx = (1-self.magnification) * self.width/2
        self.my = (1-self.magnification) * self.height/2
        
    def reset(self):
        (self.dx, self.dy) = (0, 0)
        (self.mx, self.my) = (0, 0)
        self.magnification = 1.0

    
