from vpython import *
from time import *
import numpy as np
from random import randrange
import random as r
import matplotlib.pyplot as plt

def RandomSearch():

    mradius = 0.1
    sradius = 0.01
    scoils = 7
    k = 0.05          # spring constant
    m= 0.1          # mass
    sthickness = 0.05
    g = -9.81       # acceleration due to gravity
    T = 0
    dt = 0.001

    floor = box(pos=vector(0,0,0),size=vector(100,0.2,75),color=color.green)

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

    pos1 = vector(0,2,0)
    pos2 = vector(1,2,0)
    pos3 = vector(1,2,1)
    pos4 = vector(0,2,1)
    pos5 = vector(0,3,0)
    pos6 = vector(1,3,0)
    pos7 = vector(1,3,1)
    pos8 = vector(0,3,1)
    pos9 = vector(2,3,0)
    pos10 = vector(2,3,1)
    pos11 = vector(2,2,0)
    pos12 = vector(2,2,1)


    positions = []
    positions.append(pos1)
    positions.append(pos2)
    positions.append(pos3)
    positions.append(pos4)
    positions.append(pos5)
    positions.append(pos6)
    positions.append(pos7)
    positions.append(pos8)
    positions.append(pos9)
    positions.append(pos10)
    positions.append(pos11)
    positions.append(pos12)

    maxtrans = 0
    for z in range(2):
        maxtrans += 2       # increase the allowable translation distance every iteration
        numtranslations = r.randrange(0, len(positions)-1)
        for y in range(0, numtranslations):
        # randomize translation (direction + units)
            x = positions[y]
            coin = r.randrange(0, 2)
            translate = r.uniform(-1*maxtrans, maxtrans)

            if coin == 0:    # translate in x
                posx = movesphere(1, translate, 0, 0, x)
                positions.append(posx)
            # masses.append(sphere(pos=posx,velocity=vector(0,0,0),radius=mradius,mass=m,color=color.red))
            elif coin == 1:    # translate in y
                posx = movesphere(1, 0, translate, 0, x)
                positions.append(posx)
            # masses.append(sphere(pos=posx,velocity=vector(0,0,0),radius=mradius,mass=m,color=color.red))
            elif coin == 2:    # translate in z
                posx = movesphere(1, 0, 0, translate, x)
                positions.append(posx)
            # masses.append(sphere(pos=posx,velocity=vector(0,0,0),radius=mradius,mass=m,color=color.red))


    masses = []
    springs=[]
    eqs=[]
    springL = []
    springk = []
    accelerations = []

    for i in range(len(positions)):
        b = sphere(pos=vector(positions[i].x, positions[i].y, positions[i].z), radius=0.1, velocity=vector(0, 0, 0), mass=m, color=color.red)
        masses.append(b)


    for i in range(len(positions)-1):
        for j in range(i+1,len(positions)):
            s=helix(pos=vector(positions[i].x,positions[i].y,positions[i].z),
                   axis=vector(positions[j].x-positions[i].x,positions[j].y-positions[i].y,positions[j].z-positions[i].z), color=color.blue, thickness=0.05, coils=7, radius=0.01, stiffness=10, texture = None)
            springlength = np.sqrt((positions[j].x-positions[i].x)**2+(positions[j].y-positions[i].y)**2+(positions[j].z-positions[i].z)**2)-0.3
            springL.append(springlength)
            springs.append(s)
            eq=vector((positions[j].x-positions[i].x)/2,(positions[j].y-positions[i].y)/2,(positions[j].z-positions[i].z)/2)   #assigning equilibrium at center of springs
            eqs.append(eq)

            # randomize stiffness of spring, and assign 0 stiffness (obsolete) to some springs
            if j % randrange(1,10) == 0:
                k = 0
                springk.append(k)
            else:
                k = r.uniform(0,1)
                springk.append(k)

    vbest = 0
    fitnessV, iters = [], []
    ind = 0

    while T<2220:
        rate(5)
        vmag, vsum = 0, 0
        count = 0
        for i in range(0,len(masses)):
            for j in range(0,len(springL)):
                a = r.uniform(0,2)
                b = 2/(r.randrange(1,10))
                c = r.randrange(-150,150)
                w = r.randrange(-5,5)

                Lo = vector(a + b*np.sin(w*dt+c),a + b*np.sin(w*dt+c),a + b*np.sin(w*dt+c))
                acc = (eqs[j] - Lo) * springk[j]/m


                masses[i].velocity.x = (masses[i].velocity.x +acc.x*dt) * 0.991
                masses[i].velocity.y = masses[i].velocity.y + acc.y*dt  + 0.4*g*dt
                masses[i].velocity.z = (masses[i].velocity.z +acc.z*dt) * 0.991

                vmag = np.sqrt(masses[i].velocity.x**2 + masses[i].velocity.y**2 + masses[i].velocity.z**2)
                vsum = vsum + vmag

                masses[i].pos = masses[i].pos + (masses[i].velocity * dt)

                masses[i].velocity.y = 0.999*masses[i].velocity.y

                if ((i >= 4) and (i <= 9)):
                    if masses[i].pos.y < floor.pos.y + 0.95 + masses[i].radius:
                        masses[i].velocity.y = -masses[i].velocity.y
                else:
                    if masses[i].pos.y < floor.pos.y + 0.1 + masses[i].radius:
                        masses[i].velocity.y = -masses[i].velocity.y


                if masses[i].pos.x < floor.pos.x - 50 :
                    masses[i].velocity.x = -masses[i].velocity.x
            
                if masses[i].pos.z < floor.pos.z - 35:
                    masses[i].velocity.z = -masses[i].velocity.z

        vavg= vsum/len(springs)
        if vavg > vbest:
            vbest = vavg
            fitnessV.append(vbest)
            opta, optb, optc, optw = a, b, c, w
        else:
            fitnessV.append(vbest)

        for i in range(len(masses)-1):
            for j in range(i+1, len(masses)):
                springs[count].axis = masses[j].pos - masses[i].pos
                springs[count].pos = masses[i].pos

                count += 1
        iters.append(ind)
        ind = ind + 1

        T = T + dt

    # Plotting results
    fig = gdisplay(xtitle='Iterations', ytitle='Velocity Magnitude (m/s', title='Random Search Learning Curve')
    f1 = gcurve(color=color.cyan,label="RS")
    f1.plot(pos=(fitnessV,iters))

    print("Random Search Optimal Parameters: a =",opta,", b =", optb, ", c =", optc, ", w =", optw)

def HillClimber():

    mradius = 0.1
    sradius = 0.01
    scoils = 7
    k = 0.05          # spring constant
    m= 0.1          # mass
    sthickness = 0.05
    g = -9.81       # acceleration due to gravity
    T = 0
    dt = 0.001

    floor = box(pos=vector(0,0,0),size=vector(100,0.2,75),color=color.green)

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

    pos1 = vector(0,2,0)
    pos2 = vector(1,2,0)
    pos3 = vector(1,2,1)
    pos4 = vector(0,2,1)
    pos5 = vector(0,3,0)
    pos6 = vector(1,3,0)
    pos7 = vector(1,3,1)
    pos8 = vector(0,3,1)
    pos9 = vector(2,3,0)
    pos10 = vector(2,3,1)
    pos11 = vector(2,2,0)
    pos12 = vector(2,2,1)


    positions = []
    positions.append(pos1)
    positions.append(pos2)
    positions.append(pos3)
    positions.append(pos4)
    positions.append(pos5)
    positions.append(pos6)
    positions.append(pos7)
    positions.append(pos8)
    positions.append(pos9)
    positions.append(pos10)
    positions.append(pos11)
    positions.append(pos12)

    maxtrans = 0
    for z in range(2):
        maxtrans += 3       # increase the allowable translation distance every iteration
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
                posx = movesphere(1, 0, transy, 0, x)
                positions.append(posx)
            # masses.append(sphere(pos=posx,velocity=vector(0,0,0),radius=mradius,mass=m,color=color.red))
            elif coin == 2:    # translate in z
                posx = movesphere(1, 0, 0, translate, x)
                positions.append(posx)
            # masses.append(sphere(pos=posx,velocity=vector(0,0,0),radius=mradius,mass=m,color=color.red))


    masses = []
    springs=[]
    eqs=[]
    springL = []
    springk = []
    accelerations = []

    for i in range(len(positions)):
        b = sphere(pos=vector(positions[i].x, positions[i].y, positions[i].z), radius=0.1, velocity=vector(0, 0, 0), mass=m, color=color.red)
        masses.append(b)


    for i in range(len(positions)-1):
        for j in range(i+1,len(positions)):
            s=helix(pos=vector(positions[i].x,positions[i].y,positions[i].z),
                   axis=vector(positions[j].x-positions[i].x,positions[j].y-positions[i].y,positions[j].z-positions[i].z), color=color.blue, thickness=0.05, coils=7, radius=0.01, stiffness=10, texture = None)
            springlength = np.sqrt((positions[j].x-positions[i].x)**2+(positions[j].y-positions[i].y)**2+(positions[j].z-positions[i].z)**2)-0.3
            springL.append(springlength)
            eq=vector((positions[j].x-positions[i].x)/2,(positions[j].y-positions[i].y)/2,(positions[j].z-positions[i].z)/2)   #assigning equilibrium at center of springs
            eqs.append(eq)

            # randomize stiffness of spring, and assign 0 stiffness (obsolete) to some springs
            if j % randrange(1,10) == 0:
                k = 0
                springk.append(k)
                s.color = color.black
                springs.append(s)
            else:
                k = r.uniform(0,1)
                if k < .30:
                    s.color = color.blue
                elif (k>.30) and (k<.70):
                    s.color = color.green
                elif (k>.70) and (k<=1):
                    s.color = color.yellow
                springs.append(s)
                springk.append(k)

    vbest = 0
    fitnessV, iters = [], []
    ind = 0

    while T<2220:
        rate(5)
        vmag, vsum = 0, 0
        count = 0
        for i in range(0,len(masses)):
            for j in range(0,len(springL)):
                a = r.uniform(0,2)
                b = 2/(r.randrange(1,10))+ r.uniform(-0.5,0.5)  # Add random mutation
                c = r.randrange(-150,150)
                w = r.randrange(-5,5)

                Lo = vector(a + b*np.sin(w*dt+c),a + b*np.sin(w*dt+c),a + b*np.sin(w*dt+c))
                acc = (eqs[j] - Lo) * springk[j]/m


                masses[i].velocity.x = (masses[i].velocity.x +acc.x*dt) * 0.991
                masses[i].velocity.y = masses[i].velocity.y + acc.y*dt  + 0.4*g*dt
                masses[i].velocity.z = (masses[i].velocity.z +acc.z*dt) * 0.991

                vmag = np.sqrt(masses[i].velocity.x**2 + masses[i].velocity.y**2 + masses[i].velocity.z**2)
                vsum = vsum + vmag

                masses[i].pos = masses[i].pos + (masses[i].velocity * dt)

                masses[i].velocity.y = 0.999*masses[i].velocity.y

                if ((i >= 4) and (i <= 9)):
                    if masses[i].pos.y < floor.pos.y + 0.95 + masses[i].radius:
                        masses[i].velocity.y = -masses[i].velocity.y
                else:
                    if masses[i].pos.y < floor.pos.y + 0.1 + masses[i].radius:
                        masses[i].velocity.y = -masses[i].velocity.y


                if masses[i].pos.x < floor.pos.x - 50 :
                    masses[i].velocity.x = -masses[i].velocity.x
            
                if masses[i].pos.z < floor.pos.z - 35:
                    masses[i].velocity.z = -masses[i].velocity.z

        vavg= vsum/len(springs)
        if vavg > vbest:
            vbest = vavg
            fitnessV.append(vbest)
            opta, optb, optc, optw = a, b, c, w
        else:
            fitnessV.append(vbest)

        for i in range(len(masses)-1):
            for j in range(i+1, len(masses)):
                springs[count].axis = masses[j].pos - masses[i].pos
                springs[count].pos = masses[i].pos

                count += 1
        iters.append(ind)
        ind = ind + 1

        T = T + dt

    print("HIll Climber Optimal Parameters: a =",opta,", b =", optb, ", c =", optc, ", w =", optw)

def EA():

    mradius = 0.1
    sradius = 0.01
    scoils = 7
    k = 1               # spring constant
    m= 0.1              # mass
    sthickness = 0.05
    g = -9.81           # acceleration due to gravity
    T = 0
    dt = 0.00005
    population, popfitness = [], []
    poplen = 10         # length of population/number of individuals

    floor = box(pos=vector(0,0,0),size=vector(75,0.2,50),color=color.green)

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

    pos1 = vector(0,2,0)
    pos2 = vector(1,2,0)
    pos3 = vector(1,2,1)
    pos4 = vector(0,2,1)
    pos5 = vector(0,3,0)
    pos6 = vector(1,3,0)
    pos7 = vector(1,3,1)
    pos8 = vector(0,3,1)
    pos9 = vector(2,3,0)
    pos10 = vector(2,3,1)
    pos11 = vector(2,2,0)
    pos12 = vector(2,2,1)


    positions = []
    positions.append(pos1)
    positions.append(pos2)
    positions.append(pos3)
    positions.append(pos4)
    positions.append(pos5)
    positions.append(pos6)
    positions.append(pos7)
    positions.append(pos8)
    positions.append(pos9)
    positions.append(pos10)
    positions.append(pos11)
    positions.append(pos12)

    maxtrans = 0
    for z in range(2):
        maxtrans += 2       # increase the allowable translation distance every iteration
        numtranslations = r.randrange(0, len(positions)-1)
        for y in range(0, numtranslations):
        # randomize translation (direction + units)
            x = positions[y]
            coin = r.randrange(0, 2)
            translate = r.uniform(-1*maxtrans, maxtrans)
            transy = r.uniform(0, maxtrans)

            if coin == 0:    # translate in x
                posx = movesphere(1, translate, 0, 0, x)
                positions.append(posx)
            # masses.append(sphere(pos=posx,velocity=vector(0,0,0),radius=mradius,mass=m,color=color.red))
            elif coin == 1:    # translate in y
                posx = movesphere(1, 0, transy, 0, x)
                positions.append(posx)
            # masses.append(sphere(pos=posx,velocity=vector(0,0,0),radius=mradius,mass=m,color=color.red))
            elif coin == 2:    # translate in z
                posx = movesphere(1, 0, 0, translate, x)
                positions.append(posx)
            # masses.append(sphere(pos=posx,velocity=vector(0,0,0),radius=mradius,mass=m,color=color.red))

    w = 3.768                    # global frequency
    a = 0                       # initial Lo of 0.1 m
    b = 1
    c = 43

    masses = []
    springs=[]
    eqs=[]
    springL = []
    springk = []
    accelerations = []

    for i in range(len(positions)):
        b = sphere(pos=vector(positions[i].x, positions[i].y, positions[i].z), radius=0.1, velocity=vector(0, 0, 0), mass=m, color=color.red)
        masses.append(b)


    for i in range(len(positions)-1):
        for j in range(i+1,len(positions)):
            s=helix(pos=vector(positions[i].x,positions[i].y,positions[i].z),
                   axis=vector(positions[j].x-positions[i].x,positions[j].y-positions[i].y,positions[j].z-positions[i].z), color=color.blue, thickness=0.05, coils=7, radius=0.01, stiffness=10, texture = None)
            springlength = np.sqrt((positions[j].x-positions[i].x)**2+(positions[j].y-positions[i].y)**2+(positions[j].z-positions[i].z)**2)-0.3
            springL.append(springlength)
            eq=vector((positions[j].x-positions[i].x)/2,(positions[j].y-positions[i].y)/2,(positions[j].z-positions[i].z)/2)   #assigning equilibrium at center of springs
            eqs.append(eq)
        
            # randomize stiffness of spring, and assign 0 stiffness (obsolete) to some springs
            if j % randrange(1,10) == 0:
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

    vbest = 0

    for x in range(0,poplen):
        fitnessV, iters = [], []
        while T<30:
            iters = []
            rate(5)
            vmag, vsum = 0, 0
            count, ind = 0, 0
            for i in range(0,len(masses)):
                for j in range(0,len(springL)):
                    a = r.uniform(0,2)
                    b = 2/(r.randrange(1,10)) + r.uniform(-0.5,0.5)  # Add random mutation
                    c = r.randrange(-150,150)
                    w = r.randrange(-5,5)

                    Lo = vector(a + b*np.sin(w*dt+c),a + b*np.sin(w*dt+c),a + b*np.sin(w*dt+c))
                    acc = (eqs[j] - Lo) * springk[j]/m

                    masses[i].velocity.x = masses[i].velocity.x +acc.x*dt 
                    masses[i].velocity.y = masses[i].velocity.y + acc.y*dt 
                    masses[i].velocity.z = masses[i].velocity.z +acc.z*dt

                    vmag = np.sqrt(masses[i].velocity.x**2 + masses[i].velocity.y**2 + masses[i].velocity.z**2)
                    vsum = vsum + vmag

                    masses[i].pos = masses[i].pos + (masses[i].velocity * dt)
                    if masses[i].pos.y < floor.pos.y + 0.5 + masses[i].radius:
                        masses[i].velocity.y = -masses[i].velocity.y

            if vsum > vbest:
                vbest = vsum
                fitnessV.append(vbest)
                opta, optb, optc, optw = a, b, c, w

            else:
                fitnessV.append(vbest)

            for i in range(len(masses)-1):
                for j in range(i+1, len(masses)):
                    springs[count].axis = masses[j].pos - masses[i].pos
                    springs[count].pos = masses[i].pos

                    count += 1
                
            iters.append(ind)
            ind = ind + 1

            T = T + dt

        optparameters = [opta,optb,optc,optw,vbest]
        population.append(optparameters)
        popfitness.append(fitnessV)

        # crossover every 2 individuals
        if (x%2 == 0):
            opta1 = population[x-1][0]       # optimal a from parent 1
            optb2 = population[x][1]         # optimal b from parent 2
            optc2 = population[x][2]         # optimal c from parent 2
            optw1 = population[x-1][3]       # optimal w from parent 1

            # Iterate robot with child's parameter to get its best velocity
            vsum, vbest = 0, 0
            ind = 0
            t = 0                   # repeat loop for child
            fitnessV = []
            iters = []
            while t<5:
                for i in range(0,len(masses)):
                    for j in range(0,len(springL)):

                        Lo = vector(opta1 + optb2*np.sin(optw1*dt+optc2), opta1 + optb2*np.sin(optw1*dt+optc2), opta1 + optb2*np.sin(optw1*dt+optc2))
                        acc = (eqs[j] - Lo) * springk[j]/m

                        masses[i].velocity.x = masses[i].velocity.x + acc.x*dt 
                        masses[i].velocity.y = masses[i].velocity.y + acc.y*dt 
                        masses[i].velocity.z = masses[i].velocity.z + acc.z*dt

                        vmag = np.sqrt(masses[i].velocity.x**2 + masses[i].velocity.y**2 + masses[i].velocity.z**2)
                        vsum = vsum + vmag

                if vsum > vbest:
                    vbest = vsum
                    fitnessV.append(vbest)
                    opta, optb, optc, optw = a, b, c, w

                else:
                    fitnessV.append(vbest)

                ind = ind + 1
                iters.append(ind) 
                t = t + dt

            vavg = vsum/(len(masses)*len(springs))
            popfitness.append(fitnessV)             



            # Compare best velocity from all 3 and remove lowest
            if vavg > population[x-1][4]:       # child is faster than parent x-1, remove parent add child to population
                del(population[x-1])
                optparameters = [opta1,optb2,optc2,optw1,vavg]
                population.append(optparameters)
                del(popfitness[x-1])
                continue
            elif vavg > population[x][4]:       # child is faster than parent x, remove parent add child to population
                del(population[x])
                del(popfitness[x])
                optparameters = [opta1,optb2,optc2,optw1,vavg]
                population.append(optparameters)

            # Population remains constant size

    # Iterate through population for best individual
    vbest = 0
    bestfitness = []
    for x in range(0,poplen):
        vind = population[x]
        if vind > vbest:            # Select the optimal parameters of the best individual
            vbest = vind
            besta, bestb, bestc, bestw = population[x][0], population[x][1], population[x][2], population[x][3]
            bestfitness = popfitness[x]

    plt.figure()
    plt.plot(iters,bestfitness, label = "EA")
    plt.xlabel("Iterations")
    plt.ylabel("Velocity Magnitude")


    print("EA Optimal Parameters: a =",opta,", b =", optb, ", c =", optc, ", w =", optw)

#RandomSearch()
HillClimber()
#EA()
