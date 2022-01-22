from vpython import *
from time import *
import numpy as np
import random as r
#import matplotlib.pyplot as plt

mradius = 0.1
sradius = 0.01
scoils = 7
k = 1  # spring constant
m = 0.1  # mass
sthickness = 0.05
g = -9.81     # acceleration due to gravity
T = 0
dt = 0.0003

floor = box(pos=vector(0, 0, 0), size=vector(75, 0.2, 50), color=color.green)

def movesphere(units, x, y, z, posvector):
    pos = posvector
    x, y, z = int(x), int(y), int(z)

    if(x != 0):
        posvector = posvector + vector(x, 0, 0)
        pos = posvector

    if(y != 0):
        posvector = posvector + vector(0, y, 0)
        pos = posvector

    if(z != 0):
        posvector = posvector + vector(0, 0, z)
        pos = posvector

    return pos

population = []
randstart = 0
for i in range(10):
    randstart += 3
    randx = r.uniform(-1*randstart,randstart)
    randy = r.uniform(0,randstart)
    randz = r.uniform(-1*randstart,randstart)
    pos1 = vector(0, 2, 0) + vector(randx,randy,randz)
    pos2 = vector(1, 2, 0) + vector(randx,randy,randz)
    pos3 = vector(1, 2, 1) + vector(randx,randy,randz)
    pos4 = vector(0, 2, 1) + vector(randx,randy,randz)
    pos5 = vector(0, 3, 0) + vector(randx,randy,randz)
    pos6 = vector(1, 3, 0) + vector(randx,randy,randz)
    pos7 = vector(1, 3, 1) + vector(randx,randy,randz)
    pos8 = vector(0, 3, 1) + vector(randx,randy,randz)

    positions = []
    positions.append(pos1)
    positions.append(pos2)
    positions.append(pos3)
    positions.append(pos4)
    positions.append(pos5)
    positions.append(pos6)
    positions.append(pos7)
    positions.append(pos8)

    maxtrans = 0
    for z in range(1):
        maxtrans += 2       # increase the allowable translation distance every iteration
        numtranslations = r.randrange(0, len(positions)-1)
        for y in range(0, numtranslations):
            # randomize translation (direction + units)
            x = positions[y]
            coin = r.randrange(0, 2)
            translate = r.uniform(-1*maxtrans, maxtrans)
            transy = r.uniform(0,maxtrans)

            if coin == 0:    # translate in x
                posx = movesphere(1, translate, 0, 0, x)
                positions.append(posx)
                # masses.append(sphere(pos=posx,velocity=vector(0,0,0),radius=mradius,mass=m,color=color.red))
            elif coin == 1:    # translate in y
                posy = movesphere(1, 0, maxtrans, 0, x)
                positions.append(posy)
                # masses.append(sphere(pos=posx,velocity=vector(0,0,0),radius=mradius,mass=m,color=color.red))
            elif coin == 2:    # translate in z
                posz = movesphere(1, 0, 0, translate, x)
                positions.append(posz)
                # masses.append(sphere(pos=posx,velocity=vector(0,0,0),radius=mradius,mass=m,color=color.red))

    population.append(positions)
    length = len(positions) - 1
    ind = 0

    # Checking for duplicate masses
    for x in range(0, length):       # starting at each mass
        for y in range(x, length):   # iterating through every other mass
            if (x == y):    # ignore same position
                continue

            # have to skip iteration if index is greater than updated list length
            if (x >= length) or (y >= length):
                continue

            # if two positions are equal, delete the second one
            if (positions[x] == positions[y]):
                del(positions[y])
                length = len(positions) - 1
        ind += 1

masspop = []
springspop = []
eqspop = []
springLpop = []
springkpop = []
poplen = len(population)-1

for i in range(0,poplen):
    masses = []
    for j in range(len(population[i])):
        #b = sphere(pos=positions[i],radius=0.1, velocity=vector(0, 0, 0), mass=m, color=color.red)
        masses.append(sphere(pos=population[i][j],radius=0.1, velocity=vector(0, 0, 0), mass=m, color=color.red))
    masspop.append(masses)


for x in range(0,poplen):
    springs, eqs, springL, springk = [], [], [], []
    for i in range(len(population[x])-1):
        for j in range(i+1, len(population[x])):
            pos1 = population[x][i]
            pos2 = population[x][j]
            s = helix(pos=pos1, axis=(pos2-pos1),color=color.blue, thickness=0.05, coils=7, radius=0.01, stiffness=10, texture=None)
            springlength = np.sqrt((pos2.x-pos1.x)**2+(pos2.y-pos1.y)**2+(pos2.z-pos1.z)**2)-0.3
            springL.append(springlength)
            eq = vector((pos2.x-pos1.x)/2, (pos2.y-pos1.y)/2, (pos2.z-pos1.z)/2)  # assigning equilibrium at center of springs
            eqs.append(eq)

        # randomize stiffness of spring, and assign 0 stiffness (obsolete/air) to some springs
            if j % r.randrange(1,10) == 0:
                k = 0
                springk.append(k)
                s.color = color.black
                springs.append(s)
            else:
                k = r.uniform(0,100)
                if k < 30:
                    s.color = color.blue
                elif (k>30) and (k<70):
                    s.color = color.green
                elif (k>70) and (k<=100):
                    s.color = color.yellow
                springs.append(s)
                springk.append(k)

    springLpop.append(springL)
    springspop.append(springs)
    eqspop.append(eqs)
    springkpop.append(springk)

vbest = 0
fitnessV, iters = [], []

while T < 5:
    rate(1)
    for x in range(0,poplen):
        vmag, vsum = 0, 0
        count = 0
        ind = 0
        for i in range(0, len(masspop[x])):
            for j in range(0, len(springLpop[x])):
                a = r.uniform(0, 2)
                b = 2/(r.randrange(1, 10))
                c = r.randrange(-150, 150)
                w = r.randrange(-5, 5)

                Lo = vector(a + b*np.sin(w*dt+c), a + b *np.sin(w*dt+c), a + b*np.sin(w*dt+c))
                eq = eqspop[x][j]
                k = springkpop[x][j]
                acc = (eq - Lo) * k/m

                masspop[x][i].velocity.x = (masspop[x][i].velocity.x + acc.x*dt) * 0.991
                masspop[x][i].velocity.y = masspop[x][i].velocity.y + acc.y*dt + 0.4*g*dt
                masspop[x][i].velocity.z = (masspop[x][i].velocity.z + acc.z*dt) * 0.991

                vmag = np.sqrt(masspop[x][i].velocity.x**2 + masspop[x][i].velocity.y**2 + masspop[x][i].velocity.z**2)
                vsum = vsum + vmag

                masspop[x][i].pos = masspop[x][i].pos + (masspop[x][i].velocity * dt)

                masspop[x][i].velocity.y = 0.999*masspop[x][i].velocity.y

                if ((i >= 4) and (i <= 9)):
                    if masspop[x][i].pos.y < floor.pos.y + 0.95 + masspop[x][i].radius:
                        masspop[x][i].velocity.y = -masspop[x][i].velocity.y
                else:
                    if masspop[x][i].pos.y < floor.pos.y + 0.1 + masspop[x][i].radius:
                        masspop[x][i].velocity.y = -masspop[x][i].velocity.y

                if masspop[x][i].pos.x < floor.pos.x - 50:
                    masspop[x][i].velocity.x = -masspop[x][i].velocity.x

                if masspop[x][i].pos.z < floor.pos.z - 35:
                    masspop[x][i].velocity.z = -masspop[x][i].velocity.z

        vavg = vsum/len(springspop[x])
        if vavg > vbest:
            vbest = vavg
            fitnessV.append(vbest)
            opta, optb, optc, optw = a, b, c, w
        else:
            fitnessV.append(vbest)

        for i in range(len(masspop[x])-1):
            for j in range(i+1, len(masspop[x])):
                springspop[x][count].axis = masspop[x][j].pos - masspop[x][i].pos
                springspop[x][count].pos = masspop[x][i].pos

                count += 1
        iters.append(ind)
        ind = ind + 1

        T = T + dt

# Plotting results
#fig = gdisplay(xtitle='Iterations', ytitle='Velocity Magnitude (m/s', title='Random Search Learning Curve')
#f1 = gcurve(color=color.cyan,label="RS")
# f1.plot(pos=(fitnessV,iters))
print(fitnessV)

print("Random Search Optimal Parameters: a =", opta,
      ", b =", optb, ", c =", optc, ", w =", optw)
