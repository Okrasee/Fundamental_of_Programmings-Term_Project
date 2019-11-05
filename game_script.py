from tkinter import *
import math
import pymunk
import random
import pymunk.pygame_util
import pygame
from pymunk.vec2d import Vec2d
import copy
####################################
# Name: Yirui Zhu, id: yiruiz
# Animation barebone from 15112 course website
# rgbString and distance function from 15112 course website
# pymunk library from 
# http://www.pymunk.org/en/latest/tutorials/SlideAndPinJoint.html
# distance function from 15112 course website
# setEventInfo function from 15112 course website
# Color scheme inspired by Alto's adventure and Close Your Eyes
# background music from Contre Jour: The Night
####################################
# customize these functions
####################################
space = pymunk.Space()
space.gravity = (0.0, 90.0)

def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

def distance(x, y, x1, y1):
    return math.sqrt((x - x1) ** 2 + (y - y1) ** 2)

class Atom(object):
# draw the electron and other particles
    def __init__(self, space, radius, mass, pX, pY):
        self.radius = radius
        self.mass = mass
        self.pX = pX
        self.pY = pY
        moment = pymunk.moment_for_circle(self.mass, 0, self.radius)
        body = pymunk.Body(self.mass, moment)
        body.position = (pX, pY)
        body.velocity = Vec2d(0, 0)
        body.angular_velocity = 0
        shape = pymunk.Circle(body, radius)
        space.add(body, shape)
        self.body = body
        self.shape = shape

    def drawAtom(self, canvas, color):
        x = self.body.position.x
        y = self.body.position.y
        r, g, b = color[0], color[1], color[2]
        canvas.create_oval(x - self.radius, y - self.radius,
                           x + self.radius, y + self.radius,
                           fill = rgbString(r, g, b), width = 0)

    def removeAtom(self, data):
        if self.body.position.x > data.width or self.body.position.x < 0:
            space.remove(self.body, self.shape)

class HBlock(object):
    def __init__(self, space, mass, moment, pX, pY, l1, l2, height):
        self.mass = mass
        self.moment = moment
        self.pX, self.pY = pX, pY
        self.l1, self.l2 = l1, l2
        self.height = height
        body = pymunk.Body(body_type = pymunk.Body.KINEMATIC)
        body.position = (pX, pY)
        block = pymunk.Segment(body, (- l1, -l2), (+ l1, + l2), 0)
        #block = pymunk.Segment(space.static_body, (pX - l, pY), (pX + l, pY), 3.0)
        # 另外一种写法，body = space.static_body，坐标是两个endpoint
        space.add(block)
        self.block = block

    def drawBlock(self, canvas, data, color):
        body = self.block.body
        p1 = body.position + self.block.a.rotated(body.angle)
        p2 = body.position + self.block.b.rotated(body.angle)
        r, g, b = color[0], color[1], color[2]
        canvas.create_rectangle(p1.x, p1.y,
                       p2.x, p1.y + self.height, fill = rgbString(r, g, b), width = 0)

class VBlock(object):
    def __init__(self, space, mass, moment, pX, pY, l1, l2, height):
        self.mass = mass
        self.moment = moment
        self.pX, self.pY = pX, pY
        self.l1, self.l2 = l1, l2
        self.height = height
        body = pymunk.Body(body_type = pymunk.Body.KINEMATIC)
        body.position = (pX, pY)
        block = pymunk.Segment(body, (- l1, -l2), (+ l1, + l2), 0)
        #block = pymunk.Segment(space.static_body, (pX - l, pY), (pX + l, pY), 3.0)
        # 另外一种写法，body = space.static_body，坐标是两个endpoint
        space.add(block)
        self.block = block

    def drawBlock(self, canvas, data, color):
        body = self.block.body
        r, g, b = color[0], color[1], color[2]
        p1 = body.position + self.block.a.rotated(body.angle)
        p2 = body.position + self.block.b.rotated(body.angle)
        canvas.create_rectangle(p1.x, p1.y,
                       p2.x - self.height, p2.y, fill = rgbString(r, g, b), width = 0)

class triangleWalls(object):
    def __init__(self, pX, pY, length1, length2):
        self.pX = pX
        self.pY = pY
        self.length1 = length1
        self.length2 = length2

    def bordersAndFill1(self, data, stage):
        if stage == 1:
            data.tiltedblock.append(TiltedBlock(space, 10, 1000, self.pX, self.pY, self.length1, -self.length1))
            data.block.append(VBlock(space, 10, 1000, self.pX + self.length1 + 1, self.pY - 0.5 * self.length1 + 1, 0, 0.5 * self.length1, 2.0))
            data.block.append(HBlock(space, 10, 1000, self.pX + 0.5 * self.length1, self.pY + 2, 0.5 * self.length1, 0, -2.0))
        elif stage == 2:
            data.tiltedblock1.append(TiltedBlock(space, 10, 1000, self.pX, self.pY, self.length1, -self.length1))
            data.block1.append(VBlock(space, 10, 1000, self.pX + self.length1 + 1, self.pY - 0.5 * self.length1 + 1, 0, 0.5 * self.length1, 2.0))
            data.block1.append(HBlock(space, 10, 1000, self.pX + 0.5 * self.length1, self.pY + 2, 0.5 * self.length1, 0, -2.0))
        data.triangleSet.append([(self.pX, self.pY), (self.pX + self.length1, self.pY - self.length1), (self.pX + self.length1, self.pY)])

    def bordersAndFill2(self, data, stage):
        if stage == 1:
            data.tiltedblock.append(TiltedBlock(space, 10, 1000, self.pX, self.pY, -self.length1, -self.length1))
            data.block.append(VBlock(space, 10, 1000, self.pX - self.length1, self.pY - 0.5 * self.length1 + 1, 0, 0.5 * self.length1, -2.0))
            data.block.append(HBlock(space, 10, 1000, self.pX - 0.5 * self.length1, self.pY + 2, 0.5 * self.length1, 0, -2.0))
        elif stage == 2:
            data.tiltedblock1.append(TiltedBlock(space, 10, 1000, self.pX, self.pY, -self.length1, -self.length1))
            data.block1.append(VBlock(space, 10, 1000, self.pX - self.length1, self.pY - 0.5 * self.length1 + 1, 0, 0.5 * self.length1, -2.0))
            data.block1.append(HBlock(space, 10, 1000, self.pX - 0.5 * self.length1, self.pY + 2, 0.5 * self.length1, 0, -2.0))
        data.triangleSet.append([(self.pX, self.pY), (self.pX - self.length1, self.pY - self.length1), (self.pX - self.length1, self.pY)])

    def bordersAndFill3(self, data, stage):
        if stage == 1:
            data.block.append(HBlock(space, 10, 1000, self.pX + 0.5 * self.length1, self.pY, 0.5 * self.length1, 0, 2))
            data.block.append(HBlock(space, 10, 1000, self.pX + 0.5 * self.length1, self.pY + self.length2, 0.5 * self.length1, 0, -2))
            data.block.append(VBlock(space, 10, 1000, self.pX, self.pY + 0.5 * self.length2, 0, 0.5 * self.length2, -2))
            data.block.append(VBlock(space, 10, 1000, self.pX + self.length1, self.pY + 0.5 * self.length2, 0, 0.5 * self.length2, 2))
            data.rectangleSet.append([(self.pX, self.pY), (self.pX + self.length1, self.pY + self.length2)])
        elif stage == 2:
            data.block1.append(HBlock(space, 10, 1000, self.pX + 0.5 * self.length1, self.pY, 0.5 * self.length1, 0, 2))
            data.block1.append(HBlock(space, 10, 1000, self.pX + 0.5 * self.length1, self.pY + self.length2, 0.5 * self.length1, 0, -2))
            data.block1.append(VBlock(space, 10, 1000, self.pX, self.pY + 0.5 * self.length2, 0, 0.5 * self.length2, -2))
            data.block1.append(VBlock(space, 10, 1000, self.pX + self.length1, self.pY + 0.5 * self.length2, 0, 0.5 * self.length2, 2))
            data.rectangleSet1.append([(self.pX, self.pY), (self.pX + self.length1, self.pY + self.length2)])
        elif stage == 11:
            data.bar.append(HBlock(space, 10, 1000, self.pX + 0.5 * self.length1, self.pY, 0.5 * self.length1, 0, 2))
            data.bar.append(HBlock(space, 10, 1000, self.pX + 0.5 * self.length1, self.pY + self.length2, 0.5 * self.length1, 0, -2))
            data.bar.append(HBlock(space, 10, 1000, self.pX - 0.5 * self.length1, self.pY, 0.5 * self.length1, 0, 2))
            data.bar.append(HBlock(space, 10, 1000, self.pX - 0.5 * self.length1, self.pY + self.length2, 0.5 * self.length1, 0, -2))
            data.bar.append(VBlock(space, 10, 1000, self.pX, self.pY + 0.5 * self.length2, 0, 0.5 * self.length2, -2))
            data.bar.append(VBlock(space, 10, 1000, self.pX + self.length1, self.pY + 0.5 * self.length2, 0, 0.5 * self.length2, 2))
            data.playerCreateBar.append([(self.pX - self.length1, self.pY), (self.pX + self.length1, self.pY + self.length2)])
        elif stage == 3:
            data.ladder.append(HBlock(space, 10, 1000, self.pX + 0.5 * self.length1, self.pY, 0.5 * self.length1, 0, 2))
            data.ladder.append(HBlock(space, 10, 1000, self.pX + 0.5 * self.length1, self.pY + self.length2, 0.5 * self.length1, 0, -2))
            data.ladder.append(VBlock(space, 10, 1000, self.pX, self.pY + 0.5 * self.length2, 0, 0.5 * self.length2, -2))
            data.ladder.append(VBlock(space, 10, 1000, self.pX + self.length1, self.pY + 0.5 * self.length2, 0, 0.5 * self.length2, 2))
            data.fixedLadder.append([(self.pX, self.pY), (self.pX + self.length1, self.pY + self.length2)])

class Shells(object):
    def __init__(self, space, mass, moment, pX, pY, l1, l2):
        self.mass = mass
        self.moment = moment
        body = pymunk.Body(body_type = pymunk.Body.KINEMATIC)
        body.position = (pX, pY)
        shell = pymunk.Segment(body, (- l1, - l2), (+ l1, + l2), 3.0)
        #block = pymunk.Segment(space.static_body, (pX - l, pY), (pX + l, pY), 3.0)
        # 另外一种写法，body = space.static_body，坐标是两个endpoint
        space.add(shell)
        self.shell = shell

    def drawShells(self, canvas, color):
        body = self.shell.body
        p1 = body.position + self.shell.a.rotated(body.angle)
        p2 = body.position + self.shell.b.rotated(body.angle)
        r, g, b = color[0], color[1], color[2]
        canvas.create_line(p1.x, p1.y,
                       p2.x, p2.y, fill = rgbString(r, g, b), width = 2) #stage1

class TiltedBlock(object):
    def __init__(self, space, mass, moment, pX, pY, l1, l2):
        self.mass = mass
        self.moment = moment
        body = pymunk.Body(body_type = pymunk.Body.KINEMATIC)
        body.position = (pX, pY)
        block = pymunk.Segment(body, (0, 0), (+ l1, + l2), 2.0)
        #block = pymunk.Segment(space.static_body, (pX - l, pY), (pX + l, pY), 3.0)
        # 另外一种写法，body = space.static_body，坐标是两个endpoint
        space.add(block)
        self.block = block

    def drawTiltedBlock(self, canvas, data, color):
        body = self.block.body
        p1 = body.position + self.block.a.rotated(body.angle)
        p2 = body.position + self.block.b.rotated(body.angle)
        r, g, b = color[0], color[1], color[2]
        canvas.create_line(p1.x, p1.y,
                       p2.x, p2.y, fill = rgbString(r, g, b), width = 2.0) #stage2

class Domino(object):  
    def __init__(self, space, pX, pY, length):
        rotation_center_body = pymunk.Body(0, 0, body_type = pymunk.Body.KINEMATIC)
        rotation_center_body.position = (pX, pY - 20)
        self.rotation_center_body = rotation_center_body

        rotation_limit_body = pymunk.Body(0, 0, body_type = pymunk.Body.KINEMATIC)
        rotation_limit_body.position = (pX, pY)

        body = pymunk.Body(100, 10000)
        body.position = (pX, pY)
        domino = pymunk.Segment(body, (-length, 0), (+length, 0), 2)
        rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0, -20), (0, 0))
        joint_limit = 40
        rotation_limit_joint = pymunk.SlideJoint(body, rotation_limit_body, (0,0), (0,0), 0, joint_limit)
        space.add(domino, body, rotation_center_joint, rotation_limit_joint)
        self.body = body
        self.domino = domino
        self.rotation_center_joint = rotation_center_joint
        self.rotation_limit_joint = rotation_limit_joint

    def drawDomino(self, canvas, data, color):
        body = self.domino.body
        p1 = body.position + self.domino.a.rotated(body.angle)
        p2 = body.position + self.domino.b.rotated(body.angle)
        r, g, b = color[0], color[1], color[2]
        canvas.create_line(p1[0], p1[1], p2[0], p2[1], 
            fill = rgbString(r, g, b), width = 5) # stage1

class Particle(object):
    def __init__(self, a, pX, pY, radius, shell, dir):
        self.a = a
        self.pX = pX
        self.pY = pY
        self.radius = radius
        self.shell = shell
        self.dir = dir

    def onTimerFired(self):
        self.a += 0.3

    def drawParticle(self, canvas, color):
        angle = math.pi // 2 + self.dir * (2 / 30) * math.pi * self.a
        redX = (self.pX + 
                (self.shell + self.radius) * math.cos(angle))
        redY = (self.pY - 
                (self.shell + self.radius) * math.sin(angle))
        r, g, b = color[0], color[1], color[2]
        canvas.create_oval(redX - self.radius, redY - self.radius,
                           redX + self.radius, redY + self.radius,
                           fill = rgbString(r, g, b), width = 0)

class Spark(object):
    def __init__(self, x, y, r, move):
        self.x = x
        self.y = y
        self.r = r
        self.move = move

    def drawSpark(self, canvas):
        canvas.create_oval(self.x - self.r, self.y - self.r, 
                           self.x + self.r, self.y + self.r, fill = rgbString(63, 75, 97), width = 0) #43, 247, 221

    def onTimerFired(self, data):
        self.y += self.move

class Fog(object):
    def __init__(self, r, pX, pY, thread, x, v):
        self.r = r
        self.pX = pX
        self.pX1 = pX
        self.pY = pY
        self.thread = thread
        self.x = x
        self.v = v

    def drawFog(self, canvas):
        canvas.create_rectangle(self.pX - self.r, self.pY - self.r,
                                self.pX + self.r, self.pY + self.r, fill = "grey", width = 0) #222, 219, 204)

    def onTimerFired(self):
        self.pY -= self.v
        if self.pY <= self.thread:
            self.pX = self.pX1 + self.x

def createFog(data):
    for i in range(1, 6):
        data.fog1.append(Fog(6, 60, 375, 340, random.randint(-15, 15), i))
        data.fog2.append(Fog(6, 755, 615, 570, random.randint(-15, 15), i))

def curve(L):
    coodList = []
    indexList = []
    for i in range(0, 101):
        num = i / 100
        indexList.append(num)
    def BezierX(t, L, n = 4, p = 3, prevP = 3):
        if n == 2:
            if p == prevP - 1:
                return ((1 - t)*L[prevP - 2][0] + t * L[prevP - 1][0])
            elif p == prevP:
                return (1 - t)*L[prevP - 1][0] + t * L[prevP][0]
        else:
            prevP = p
            return (1 - t) * BezierX(t, L, n - 1, p - 1, prevP) + t * BezierX(t, L, n - 1, p, prevP)

    def BezierY(t, L, n = 4, p = 3, prevP = 3):
        if n == 2:
            if p == prevP - 1:
                return ((1 - t)*L[prevP - 2][1] + t * L[prevP - 1][1])
            elif p == prevP:
                return (1 - t)*L[prevP - 1][1] + t * L[prevP][1]
        else:
            prevP = p
            return (1 - t) * BezierY(t, L, n - 1, p - 1, prevP) + t * BezierY(t, L, n - 1, p, prevP)
    for i in range(0, 101):
        coodList.append((BezierX(indexList[i], L), BezierY(indexList[i], L)))
    return coodList

def allColors():
    colorScheme = [(33, 60, 53), (36, 20, 52), (110, 88, 137), (155, 130, 170), (132, 35, 58)]
    # [(200, 229, 145), (15, 30, 37), (47, 101, 75), (82, 149, 106)]
    #[(33, 60, 53), (36, 12, 50), (88, 60, 108), (109, 87, 136), (203, 134, 171), (186, 123, 164)]
    return colorScheme

def stage1init(data):
# all the basic structure in stage 1
    data.block, data.domino, data.tool, data.shell, data.domino1 = [], [], [], [], [] # for stage 1
    data.rectangleSet = []
    data.tiltedblock = []
    data.dir, data.dir1, data.dir2 = 1, 1, 1
    data.color = allColors()
    data.bar, data.playerCreateBar = [], [] # stores the position of the bars player creates, only two are allowed
    data.click = 0
    data.stage1Color = [(38, 40, 27), (49, 95, 84), (68, 132, 116), (222, 219, 204), (72, 60, 110)] #33, 60, 53
    data.fixed = [(140, 450), (480, 530), (570, 480), (650, 560), (500, 300), (200, 60)]
    data.pause = 0 # make the shells stop rotating when data.pause = 1
    data.particle = []
    data.fog1, data.fog2 = [], []
    data.fogTimeCount = 0
    data.a = 0
    data.fogColor = [(222, 219, 204), (112, 109, 104), (89, 84, 80)]
    data.fogColorIndex = 0
    data.stage1GameOver = False
    data.stage1Win = False
    data.exp = 0

def stage1Walls(data):
    data.block.append(HBlock(space, 100, 1000, 400, 20, 400, 0, -20)) #1
    data.block.append(VBlock(space, 100, 1000, 20, 320, 0, 320, 20)) #2
    data.block.append(HBlock(space, 100, 1000, 400, 680, 400, 0, 20)) #3
    data.block.append(VBlock(space, 100, 1000, 780, 30, 0, 30, -20)) #4
    data.block.append(VBlock(space, 100, 1000, 110, 230, 0, 20, 10)) ###moving
    triangleWalls(0, 550, 200, 10).bordersAndFill3(data, 1)
    triangleWalls(190, 440, 10, 120).bordersAndFill3(data, 1)
    triangleWalls(180, 560, 20, 60).bordersAndFill3(data, 1)
    triangleWalls(180, 620, 240, 680).bordersAndFill3(data, 1)
    triangleWalls(280, 600, 140, 20).bordersAndFill3(data, 1)
    triangleWalls(300, 580, 120, 20).bordersAndFill3(data, 1)
    triangleWalls(330, 560, 90, 20).bordersAndFill3(data, 1)
    triangleWalls(360, 555, 60, 5).bordersAndFill3(data, 1)
    triangleWalls(720, 560, 10, 140).bordersAndFill3(data, 1)
    triangleWalls(730, 620, 50, 60).bordersAndFill3(data, 1)
    triangleWalls(650, 320, 10, 160).bordersAndFill3(data, 1)
    triangleWalls(360, 420, 300, 40).bordersAndFill3(data, 1)
    triangleWalls(220, 380, 140, 120).bordersAndFill3(data, 1)
    triangleWalls(0, 380, 280, 20).bordersAndFill3(data, 1)
    triangleWalls(100, 250, 10, 130).bordersAndFill3(data, 1) ###
    triangleWalls(100, 60, 10, 140).bordersAndFill3(data, 1)
    triangleWalls(100, 200, 300, 20).bordersAndFill3(data, 1)
    triangleWalls(390, 110, 10, 140).bordersAndFill3(data, 1)
    triangleWalls(390, 240, 300, 20).bordersAndFill3(data, 1)
    triangleWalls(340, 280, 20, 100).bordersAndFill3(data, 1)
    triangleWalls(680, 60, 20, 230).bordersAndFill3(data, 1)
    triangleWalls(720, 60, 80, 40).bordersAndFill3(data, 1)
    triangleWalls(700, 120, 50, 40).bordersAndFill3(data, 1)
    triangleWalls(750, 120, 10, 40).bordersAndFill3(data, 1)
    triangleWalls(780, 100, 20, 100).bordersAndFill3(data, 1)
    triangleWalls(720, 180, 80, 30).bordersAndFill3(data, 1) ##
    triangleWalls(700, 230, 100, 60).bordersAndFill3(data, 1) ##
    triangleWalls(780, 290, 20, 680).bordersAndFill3(data, 1)

def stage1Lists(data):
    data.protagonist = Atom(space, 8, 10, 50, 480)
    data.block.append(HBlock(space, 10, 1000, 55, 520, 15, 0, 5))
    stage1Walls(data)
    allCurves(data)
    # levers
    data.domino.append(Domino(space, 140, 500, 30))
    data.domino.append(Domino(space, 480, 580, 30))
    data.domino.append(Domino(space, 570, 530, 30))
    data.domino.append(Domino(space, 650, 610, 30))
    data.domino.append(Domino(space, 500, 350, 100))
    data.domino.append(Domino(space, 200, 110, 40))
    data.domino1.append(Domino(space, 180, 330, 40))
    data.a = 0
    data.index = [(450, 105), (450, 145), (540, 105), (540, 145), (630, 105), (630, 145)]
    data.shell.append(Shells(space, 1, 100, 450, 105, 30, 0))
    data.shell.append(Shells(space, 1, 100, 450, 145, 30, 0))
    data.shell.append(Shells(space, 1, 100, 540, 105, 30, 0))
    data.shell.append(Shells(space, 1, 100, 540, 145, 30, 0))
    data.shell.append(Shells(space, 1, 100, 630, 105, 30, 0))
    data.shell.append(Shells(space, 1, 100, 630, 145, 30, 0))
    data.particle.append(Particle(0, 100, 620, 3, 35, 1))
    data.particle.append(Particle(0, 100, 620, 5, 20, -1))

def clearStage1(data):
    space.remove(data.protagonist.body, data.protagonist.shape)
    for i in range(len(data.domino)):
        space.remove(data.domino[i].domino, data.domino[i].body, data.domino[i].rotation_limit_joint, data.domino[i].rotation_center_joint)
    for i in range(len(data.shell)):
        space.remove(data.shell[i].shell)
    for i in range(len(data.block)):
        space.remove(data.block[i].block)
    for i in range(len(data.tiltedblock)):
        space.remove(data.tiltedblock[i].block)

def findCoord(L):
    length = len(curve(L))
    info = []
    for i in range(0, length - 2):
        pX1 = curve(L)[i][0]
        pY1 = curve(L)[i][1]
        pX2 = curve(L)[i + 1][0]
        pY2 = curve(L)[i + 1][1]
        l1 = pX2 - pX1
        l2 = pY2 - pY1
        info.append((pX1, pY1, l1, l2))
    info.append((405, 560))
    return info

def allCurves(data):
    data.curveInfoList1 = findCoord([(361, 560), (361, 520), (418, 520), (418, 560)])
    for i in range(len(data.curveInfoList1) - 1):
        pX1 = data.curveInfoList1[i][0]
        pY1 = data.curveInfoList1[i][1]
        l1 = data.curveInfoList1[i][2]
        l2 = data.curveInfoList1[i][3]
        data.tiltedblock1.append(TiltedBlock(space, 10, 10, pX1, pY1, -l1, -l2))

def stage1TimerFired(data):
    data.exp += 1
    data.fogTimeCount += 1
    for fog in data.fog1:
        fog.onTimerFired()
        if fog.pY <= 250:
            data.fog1.remove(fog)
    for fog in data.fog2:
        fog.onTimerFired()
        if fog.pY <= 540:
            data.fog2.remove(fog)
    if data.a >= 180:
        data.a = 0
        data.pause = 0
    if data.a == 0 and data.pause < 10:
        data.a = 0
        data.pause += 1
    elif data.pause == 10:
        data.a += 5
    data.block[0].block.body.position += data.dir * Vec2d(1, 0)
    if data.block[0].block.body.position.x < 50: 
        data.dir = +1
    elif data.block[0].block.body.position.x > 60: 
        data.dir = -1
    data.block[5].block.body.position -= data.dir1 * Vec2d(0, 1)
    if data.block[5].block.body.position.y < 200:
        data.dir1 = -1
    elif data.block[5].block.body.position.y > 230:
        data.dir1 = 1
    for i in range(len(data.shell)):
        if i % 2 == 0:
            data.shell[i].shell.body.position = Vec2d(data.index[i][0] + 20 * math.cos(math.radians(90 - data.a)), data.index[i][1] + 20 - 20 * math.sin(math.radians(90 - data.a)))
        if i % 2 == 1:
            data.shell[i].shell.body.position = Vec2d(data.index[i][0] + 20 * math.cos(math.radians(90 + data.a)), data.index[i][1] - 20 + 20 * math.sin(math.radians(90 + data.a)))
        data.shell[0].shell.body.angle = math.radians(data.a)
        data.shell[1].shell.body.angle = math.radians(data.a)
        data.shell[2].shell.body.angle = math.radians(data.a)
        data.shell[3].shell.body.angle = math.radians(data.a)
        data.shell[4].shell.body.angle = math.radians(data.a)
        data.shell[5].shell.body.angle = math.radians(data.a)
    for particle in data.particle:
        particle.onTimerFired()
    if (data.protagonist.body.position.x > 400 and data.protagonist.body.position.x < 680
    and data.protagonist.body.position.y > 200 and data.protagonist.body.position.y < 250):
        data.stage1GameOver = True
    elif (data.protagonist.body.position.x > 105 and data.protagonist.body.position.x < 400
    and data.protagonist.body.position.y > 140 and data.protagonist.body.position.y < 200):
        data.stage1GameOver = True
    elif (data.protagonist.body.position.x > 105 and data.protagonist.body.position.x < 350
    and data.protagonist.body.position.y > 330 and data.protagonist.body.position.y < 380):
        data.stage1GameOver = True
    elif (data.protagonist.body.position.x > 360 and data.protagonist.body.position.x < 660
    and data.protagonist.body.position.y > 390 and data.protagonist.body.position.y < 440):
        data.stage1GameOver = True
    elif (data.protagonist.body.position.x > 20 and data.protagonist.body.position.x < 200
    and data.protagonist.body.position.y > 530 and data.protagonist.body.position.y < 550):
        data.stage1GameOver = True
    elif (data.protagonist.body.position.x > 420 and data.protagonist.body.position.x < 720
    and data.protagonist.body.position.y > 640 and data.protagonist.body.position.y < 680):
        data.stage1GameOver = True

def stage1redrawAll(canvas, data):
    for i in range(len(data.domino)):
        x, y = data.domino[i].domino.body.position.x, data.domino[i].domino.body.position.y
        x1, y1 = data.fixed[i][0], data.fixed[i][1]
        canvas.create_line(x, y, x1, y1, fill = rgbString(data.stage1Color[1][0], data.stage1Color[1][1], data.stage1Color[1][2]), width = 2)
    if data.fogTimeCount % 15 == 0:
        createFog(data)
    for fog in data.fog1:
        r, g, b = data.fogColor[data.fogColorIndex][0], data.fogColor[data.fogColorIndex][1], data.fogColor[data.fogColorIndex][2]
        canvas.create_rectangle(fog.pX - fog.r, fog.pY - fog.r,
                                fog.pX + fog.r, fog.pY + fog.r, fill = "grey", width = 0)
    for fog in data.fog2:
        fog.drawFog(canvas)
    for block in data.block:
        block.drawBlock(canvas, data, (32, 60, 52))
    for domino in data.domino:
        domino.drawDomino(canvas, data, (38, 40, 27))
    canvas.create_oval(140 - 4, 500 - 50 - 4, 140 + 4, 500 - 50 + 4, fill = rgbString(data.stage1Color[1][0], data.stage1Color[1][1], data.stage1Color[1][2]), width = 0)
    canvas.create_oval(480 - 4, 580 - 50 - 4, 480 + 4, 580 - 50 + 4, fill = rgbString(data.stage1Color[1][0], data.stage1Color[1][1], data.stage1Color[1][2]), width = 0)
    canvas.create_oval(570 - 4, 530 - 50 - 4, 570 + 4, 530 - 50 + 4, fill = rgbString(data.stage1Color[1][0], data.stage1Color[1][1], data.stage1Color[1][2]), width = 0)
    canvas.create_oval(650 - 4, 610 - 50 - 4, 650 + 4, 610 - 50 + 4, fill = rgbString(data.stage1Color[1][0], data.stage1Color[1][1], data.stage1Color[1][2]), width = 0)
    canvas.create_oval(500 - 4, 350 - 50 - 4, 500 + 4, 350 - 50 + 4, fill = rgbString(data.stage1Color[1][0], data.stage1Color[1][1], data.stage1Color[1][2]), width = 0)
    canvas.create_oval(200 - 4, 110 - 50 - 4, 200 + 4, 110 - 50 + 4, fill = rgbString(data.stage1Color[1][0], data.stage1Color[1][1], data.stage1Color[1][2]), width = 0)
    canvas.create_oval(450 - 7, 125 - 7, 450 + 7, 125 + 7, fill = rgbString(data.stage1Color[3][0], data.stage1Color[3][1], data.stage1Color[3][2]), width = 0)
    canvas.create_oval(540 - 7, 125 - 7, 540 + 7, 125 + 7, fill = rgbString(data.stage1Color[3][0], data.stage1Color[3][1], data.stage1Color[3][2]), width = 0)
    canvas.create_oval(630 - 7, 125 - 7, 630 + 7, 125 + 7, fill = rgbString(data.stage1Color[3][0], data.stage1Color[3][1], data.stage1Color[3][2]), width = 0)
    canvas.create_oval(100 - 53, 620 - 53, 100 + 53, 620 + 53, fill = rgbString(data.stage1Color[4][0], data.stage1Color[4][1], data.stage1Color[4][2]), width = 0)
    canvas.create_oval(100 - 52, 620 - 52, 100 + 52, 620 + 52, fill = rgbString(114, 157, 140), width = 0)
    canvas.create_oval(100 - 38, 620 - 38, 100 + 38, 620 + 38, fill = rgbString(data.stage1Color[4][0], data.stage1Color[4][1], data.stage1Color[4][2]), width = 0)
    canvas.create_oval(100 - 37, 620 - 37, 100 + 37, 620 + 37, fill = rgbString(114, 157, 140), width = 0)
    canvas.create_oval(100 - 25, 620 - 25, 100 + 25, 620 + 25, fill = rgbString(data.stage1Color[4][0], data.stage1Color[4][1], data.stage1Color[4][2]), width = 0)
    canvas.create_oval(100 - 24, 620 - 24, 100 + 24, 620 + 24, fill = rgbString(114, 157, 140), width = 0)
    canvas.create_oval(100 - 8, 620 - 8, 100 + 8, 620 + 8, fill = "pink", width = 0)
    data.protagonist.drawAtom(canvas, (255, 255, 255))
    canvas.create_rectangle(105, 140, 400, 200, fill = "light blue", width = 0) # alternative to 167, 209, 173
    canvas.create_rectangle(400, 200, 680, 250, fill = "light blue", width = 0)
    canvas.create_rectangle(105, 330, 350, 380, fill = "light blue", width = 0)
    canvas.create_rectangle(360, 390, 660, 440, fill = "light blue", width = 0)
    canvas.create_rectangle(20, 530, 200, 550, fill = "light blue", width = 0)
    canvas.create_rectangle(420, 640, 720, 680, fill = "light blue", width = 0)
    for tool in data.tool:
        tool.drawAtom(canvas, (0, 0, 0))
    for i in range(len(data.shell)):
        data.shell[i].drawShells(canvas, data.stage1Color[3])
    for tiltedblock in data.tiltedblock:
        tiltedblock.drawTiltedBlock(canvas, data, data.color[0])
    for rectangle in data.rectangleSet: # first layer
        coor1, coor2 = rectangle[0], rectangle[1]
        canvas.create_rectangle(coor1, coor2, fill = rgbString(32, 60, 52), width = 0)
    for bar in data.bar:
        bar.drawBlock(canvas, data, data.stage1Color[0])
    for bar in data.playerCreateBar: # first layer
        coor1, coor2 = bar[0], bar[1]
        canvas.create_rectangle(coor1, coor2, fill = rgbString(data.stage1Color[0][0], data.stage1Color[0][1], data.stage1Color[0][2]), width = 0)
    data.particle[0].drawParticle(canvas, (247, 242, 181))
    data.particle[1].drawParticle(canvas, (7, 248, 236))
    drawCurves(canvas)
    if data.stage1GameOver == True:
        canvas.create_text(data.width // 2, data.height // 2, text = "Game Over", font = "Arial 55", fill = "white")
    elif data.stage1Win == True:
        canvas.create_text(data.width // 2, data.height // 2, text = "Great job!", font = "Arial 55", fill = "white")
        #canvas.create_text(data.width // 2, data.height // 2 + 60, text = "Congrats!", font = "Arial 55", fill = "white")
    if data.protagonist.body.position.x <= 200:
        canvas.create_text(60, 480, text = "Here it is!", font = "Arial 15")
        canvas.create_text(60, 650, text = "This is its home!", font = "Arial 15")
        canvas.create_text(150, 430, text = "Use the levers wisely", font = "Arial 15")
        canvas.create_text(700, 40, text = "Here's the way to home", font = "Arial 15")
    elif data.protagonist.body.position.x > 700 and data.protagonist.body.position.y > 500:
        canvas.create_text(700, 500, text = "Create two bars", font = "Arial 15")
        canvas.create_text(700, 530, text = "to help it jump", font = "Arial 15")

def drawCurves(canvas):
# draw curves in stage 1
    canvas.create_oval(360, 530, 420, 590, fill = rgbString(32, 60, 52), width = 0)

def stage1keyPressed(event, data):
    if (data.protagonist.body.position.x > 780 and 
    data.protagonist.body.position.y > 210 and data.protagonist.body.position.y < 230):
        data.protagonist.body.position = Vec2d(10, 670)
    elif (data.protagonist.body.position.x > 10 and data.protagonist.body.position.x < 60
    and data.protagonist.body.position.y > 650 and data.protagonist.body.position.y < 690):
        data.stage1Win = True
    if event.keysym == "r":
        space.remove(data.protagonist.body)

def stage1MousePressed(event, data):
    if data.playerCreateBar == []:
        data.playerCreateBar.append(triangleWalls(event.x, event.y, 20, 0).bordersAndFill3(data, 11))
        data.playerCreateBar.remove(None)
    else:
        for i in range(len(data.playerCreateBar)):
            if ((event.x < data.playerCreateBar[i][0][0] or event.x > data.playerCreateBar[i][1][0]) and
                (event.y > data.playerCreateBar[i][0][1] + 2 or event.y < data.playerCreateBar[i][0][1] - 2)) and len(data.playerCreateBar) < 2:
                data.playerCreateBar.append(triangleWalls(event.x, event.y, 20, 0).bordersAndFill3(data, 11))
                data.playerCreateBar.remove(None)
            elif (event.x > data.playerCreateBar[i][0][0] and event.x < data.playerCreateBar[i][1][0] and
                event.y <= data.playerCreateBar[i][0][1] + 2 and event.y >= data.playerCreateBar[i][0][1] - 2):
                data.playerCreateBar.remove(data.playerCreateBar[i])
                if i == 0:
                    space.remove(data.bar[0].block)
                    space.remove(data.bar[1].block)
                    space.remove(data.bar[2].block)
                    space.remove(data.bar[3].block)
                    space.remove(data.bar[4].block)
                    space.remove(data.bar[5].block)
                    data.bar = data.bar[6:12]
                elif i == 1:
                    space.remove(data.bar[6].block)
                    space.remove(data.bar[7].block)
                    space.remove(data.bar[8].block)
                    space.remove(data.bar[9].block)
                    space.remove(data.bar[10].block)
                    space.remove(data.bar[11].block)
                    data.bar = data.bar[0:6]

class Pulley(object):
    def __init__(self, anchorAx, anchorAy, anchorBx, anchorBy, radius, l1, l2, bodyAlength, bodyBlength):
        self.anchorAx = anchorAx
        self.anchorAy = anchorAy
        self.anchorBx = anchorBx
        self.anchorBy = anchorBy
        self.radius = radius
        self.l1 = l1
        self.l2 = l2
        self.pX1 =self.anchorAx # body anchor value, body center position
        self.pY1 = self.anchorAy + self.radius + self.l1
        self.bodyAlength = bodyAlength # half of the length of the static blocks
        self.pX2 =self.anchorBx # body anchor value, body center position
        self.pY2 = self.anchorBy + self.radius + self.l2
        self.bodyBlength = bodyBlength

    def drawPulleyJoint(self, canvas, color):
        canvas.create_oval(self.anchorAx, self.anchorAy,
                           self.anchorAx + 2 * self.radius, self.anchorAy + 2 * self.radius,
                           fill = color, width = 0)
        canvas.create_oval(self.anchorBx, self.anchorBy,
                           self.anchorBx - 2 * self.radius, self.anchorBy + 2 * self.radius,
                           fill = color, width = 0)
        canvas.create_line(self.anchorAx + self.radius, self.anchorAy + 1, self.anchorBx - self.radius, self.anchorBy + 1, fill = color, width = 2)
        canvas.create_line(self.anchorAx + 1, self.anchorAy + self.radius, self.anchorAx + 1, self.anchorAy + self.radius + self.l1, fill = color, width = 2)
        canvas.create_line(self.anchorBx - 1, self.anchorBy + self.radius, self.anchorBx - 1, self.anchorBy + self.radius + 0.8 * self.l2, fill = color, width = 2)
        canvas.create_line(self.anchorBx - 1, self.anchorBy + self.radius + 0.8 * self.l2, self.anchorBx - 1 - self.bodyBlength, self.anchorBy + self.radius + self.l2, fill = color, width = 2)
        canvas.create_line(self.anchorBx - 1, self.anchorBy + self.radius + 0.8 * self.l2, self.anchorBx - 1 + self.bodyBlength, self.anchorBy + self.radius + self.l2, fill = color, width = 2)

def stage2init(data):
    data.dir2, data.dir3 = 1, 1 # shell moves
    data.color = allColors()
    data.block1, data.tiltedblock1, data.pulley, data.tool= [], [], [], []
    data.pulleyBars = []
    data.dot1, data.dot2, data.dot3, data.dot4 = [], [], [], []
    data.shell1 = []
    data.timerCount = 0
    data.fall = False
    data.l2 = 255
    data.pulleyLength = [294, 376, 744]
    data.pulleyInfo = []
    data.fall = [False] * 5 # the 1st one does not count, in case an accident click
    data.timerCount = [0] * 5
    data.acce = [0] * 5
    data.toolPos = [(240, 210.0)]
    data.Near = {1: None, 2: None, 3: None, 4: None}
    data.newBall = False
    data.index = 0 # the index of the pulley system
    data.triangleSet = [] # polygon coordinates
    data.rectangleSet1 = [] # rectangle coordinates
    data.guanka = 680
    data.domino2 = []
    data.fall1 = False
    data.fallOther = [False, False, False, False]
    data.upTimes = 0
    data.signalInLevel2 = []
    data.starInLevel2 = []
    data.timerCountInLevel2 = 0
    shells(data)
    data.stage2Win = False

def stage2Lists(data):
    data.protagonist = Atom(space, 8, 10, 280, 225)
    data.tool.append(Atom(space, 8, 10, 340, 250)) # a ball already given
    # 8, 10, 340, 250
    data.pulley.append(Pulley(130, 330, 231, 330, 10, 100, 255, 30, 30))
    data.pulley.append(Pulley(220, 120, 430, 140, 10, 60, 370, 30, 30))
    data.pulley.append(Pulley(55, 30, 745, 30, 10, 280, 580, 30, 30))
    pulleyInfo(data)
    pulleyBlocks(data)
    stage2WallsFinal(data)
    data.domino2.append(Domino(space, 520, 430, 40))
    for i in range(30):
        data.signalInLevel2.append(Signal(random.randint(1, 3), random.uniform(82, 108), 675, random.uniform(1, 6), data.stage3Color[random.randint(8, 12)]))
    data.starInLevel2 = [(744, 600), (744, 500), (744, 400), (429, 450), (429, 350)]

def clearStage2(data):
    #space.remove(data.protagonist.body, data.protagonist.shape)
    for i in range(len(data.tool)):
        space.remove(data.tool[i].body, data.tool[i].shape)
    for i in range(len(data.block1)):
        space.remove(data.block1[i].block)
    for i in range(len(data.shell1)):
        space.remove(data.shell1[i].block)
    for i in range(len(data.domino2)):
        space.remove(data.domino2[i].domino)
    for i in range(len(data.tiltedblock1)):
        space.remove(data.tiltedblock1[i].block)
    for i in range(len(data.pulleyBars)):
        space.remove(data.pulleyBars[i].block)

def stage2WallsFinal(data):
    data.block1.append(HBlock(space, 100, 1000, 400, 20, 400, 0, -20)) #1
    data.block1.append(VBlock(space, 100, 1000, 20, 345, 0, 345, 20)) #2
    data.block1.append(HBlock(space, 100, 1000, 400, 680, 400, 0, 20)) #3
    data.block1.append(VBlock(space, 100, 1000, 780, 345, 0, 345, -20)) #4
    triangleWalls(0, 560, 100, 40).bordersAndFill3(data, 2)
    triangleWalls(100, 480, 40, 100).bordersAndFill3(data, 2)
    triangleWalls(140, 530, 30, 20).bordersAndFill3(data, 2)
    triangleWalls(169, 548, -30, 0).bordersAndFill1(data, 2)
    triangleWalls(120, 580, -40, 0).bordersAndFill1(data, 2)
    triangleWalls(50, 600, 30, 80).bordersAndFill3(data, 2)
    triangleWalls(170, 600, 30, 80).bordersAndFill3(data, 2)
    triangleWalls(110, 630, 30, 50).bordersAndFill3(data, 2)
    triangleWalls(110, 630, 30, 0).bordersAndFill1(data, 2)
    triangleWalls(160, 600, 40, 0).bordersAndFill1(data, 2)
    triangleWalls(140, 600, 30, 30).bordersAndFill3(data, 2)

    triangleWalls(260, 470, 20, 190).bordersAndFill3(data, 2)
    triangleWalls(280, 500, 20, 160).bordersAndFill3(data, 2)
    triangleWalls(300, 640, 20, 20).bordersAndFill3(data, 2)
    triangleWalls(320, 640, 20, 0).bordersAndFill2(data, 2)

    triangleWalls(240, 455, 61, 20).bordersAndFill3(data, 2)
    triangleWalls(240, 455, 60, 0).bordersAndFill1(data, 2)
    triangleWalls(300, 395, 50, 30).bordersAndFill3(data, 2)
    triangleWalls(160, 415, -60, 0).bordersAndFill2(data, 2)
    triangleWalls(319, 395, 30, 0).bordersAndFill1(data, 2)
    triangleWalls(339, 375, 20, 0).bordersAndFill1(data, 2)
    triangleWalls(359, 307, 25, 70).bordersAndFill3(data, 2)
    triangleWalls(399, 360, -15, 0).bordersAndFill1(data, 2)
    triangleWalls(369, 240, 30, 120).bordersAndFill3(data, 2)
    triangleWalls(349, 260, 20, 0).bordersAndFill1(data, 2)
    triangleWalls(330, 260, 25, 20).bordersAndFill3(data, 2)

    triangleWalls(290, 360, -50, 0).bordersAndFill1(data, 2)
    triangleWalls(270, 360, 30, 15).bordersAndFill3(data, 2)
    triangleWalls(314, 360, -14, 0).bordersAndFill1(data, 2)
    triangleWalls(319, 360, 30, 0).bordersAndFill2(data, 2)
    triangleWalls(259, 360, 30, 0).bordersAndFill1(data, 2)
    triangleWalls(209, 255, -90, 0).bordersAndFill2(data, 2)
    triangleWalls(270, 236, 20, 20).bordersAndFill3(data, 2)
    triangleWalls(310, 256, 20, 0).bordersAndFill2(data, 2)
    triangleWalls(233, 280, 25, 0).bordersAndFill2(data, 2)
    triangleWalls(233, 280, -25, 0).bordersAndFill1(data, 2)
    triangleWalls(190, 255, 20, 52).bordersAndFill3(data, 2)
    triangleWalls(140, 305, 50, 0).bordersAndFill1(data, 2)

    triangleWalls(380, 550, 10, 100).bordersAndFill3(data, 2)
    triangleWalls(380, 550, 280, 20).bordersAndFill3(data, 2)
    triangleWalls(660, 380, 40, 190).bordersAndFill3(data, 2)
    triangleWalls(440, 355, 220, 15).bordersAndFill3(data, 2)
    triangleWalls(605, 400, 15, 80).bordersAndFill3(data, 2)
    triangleWalls(505, 500, 115, 50).bordersAndFill3(data, 2)
    triangleWalls(435, 600, 10, 80).bordersAndFill3(data, 2)
    triangleWalls(505, 600, 10, 80).bordersAndFill3(data, 2)
    triangleWalls(565, 570, 10, 60).bordersAndFill3(data, 2)
    triangleWalls(635, 600, 10, 80).bordersAndFill3(data, 2)
    triangleWalls(435, 650, 345, 30).bordersAndFill3(data, 2)
    triangleWalls(660, 320, 10, 60).bordersAndFill3(data, 2)
    triangleWalls(670, 370, 40, 10).bordersAndFill3(data, 2)

    triangleWalls(80, 20, 25, 200).bordersAndFill3(data, 2)
    triangleWalls(80, 219, -20, 0).bordersAndFill2(data, 2)
    triangleWalls(100, 219, 50, 22).bordersAndFill3(data, 2)
    triangleWalls(100, 130, 60, 22).bordersAndFill3(data, 2)
    triangleWalls(200, 170, 40, 0).bordersAndFill2(data, 2)
    triangleWalls(140, 150, -20, 0).bordersAndFill2(data, 2)
    triangleWalls(125, 130, 20, 0).bordersAndFill2(data, 2)
    triangleWalls(125, 150, -20, 0).bordersAndFill1(data, 2)
    triangleWalls(100, 45, 60, 22).bordersAndFill3(data, 2)
    triangleWalls(180, 65, 20, 0).bordersAndFill2(data, 2)
    triangleWalls(150, 65, 30, 20).bordersAndFill3(data, 2)
    triangleWalls(150, 85, -30, 0).bordersAndFill2(data, 2) 
    triangleWalls(180, 85, 100, 31).bordersAndFill3(data, 2)
    triangleWalls(310, 85, -30, 0).bordersAndFill1(data, 2)
    triangleWalls(280, 85, 30, 0).bordersAndFill1(data, 2)
    triangleWalls(310, 55, 70, 30).bordersAndFill3(data, 2) 
    triangleWalls(409, 83, 29, 0).bordersAndFill2(data, 2)
    triangleWalls(388, 83, -20, 0).bordersAndFill2(data, 2)
    triangleWalls(170, 241, 22, 0).bordersAndFill2(data, 2)       

def stage2keyPressed(event, data):
    if event.keysym == "r":
        print(len(data.tool))
        data.tool.pop()

def shells(data):
    data.shell1.append(HBlock(space, 5, 100, 480, 320, 20, 0, 2))
    data.shell1.append(HBlock(space, 5, 100, 480, 100, 20, 0, 2))
    data.shell1.append(HBlock(space, 5, 100, 460, 180, 20, 0, 2))
    data.shell1.append(HBlock(space, 5, 100, 620, 80, 20, 0, 2))
    data.shell1.append(TiltedBlock(space, 5, 100, 460, 280, 35, -35))
    data.shell1.append(TiltedBlock(space, 5, 100, 540, 70, 35, -35))
    data.shell1.append(TiltedBlock(space, 5, 100, 540, 130, 35, 35))

def countTime(data, i):
    if i == 0:
        if data.tool[0].body.position.y != data.toolPos[0][1]:
            data.fall[0] = True
        elif abs(data.tool[0].body.position.y - data.pulleyBars[1].block.body.position.y) <= data.tool[0].radius: # how to know which bar is the tool approaching
            data.fall[0] = False
        if data.fall[0] == True:
            data.timerCount[0] += 1
    else:
        if data.tool[i].body.position.y != data.toolPos[i][1]:
            data.fall[i] = True
        if (abs(data.tool[i].body.position.y - data.pulleyBars[0].block.body.position.y) <= data.tool[i].radius and
        data.pulleyBars[0].block.body.position.x - 30 < data.tool[i].body.position.x and 
        data.pulleyBars[0].block.body.position.x + 30 > data.tool[i].body.position.x): # how to know which bar is the tool approaching
            data.fall[i] = False
            data.Near[i] = 0
        if (abs(data.tool[i].body.position.y - data.pulleyBars[2].block.body.position.y) <= data.tool[i].radius and
        data.pulleyBars[2].block.body.position.x - 30 < data.tool[i].body.position.x and 
        data.pulleyBars[2].block.body.position.x + 30 > data.tool[i].body.position.x):
            data.fall[i] = False
            data.Near[i] = 2
        if (abs(data.tool[i].body.position.y - data.pulleyBars[4].block.body.position.y) <= data.tool[i].radius and
        data.pulleyBars[4].block.body.position.x - 30 < data.tool[i].body.position.x and 
        data.pulleyBars[4].block.body.position.x + 30 > data.tool[i].body.position.x):
            data.fall[i] = False
            data.Near[i] = 4
        if data.fall[i] == True:
            data.timerCount[i] += 1

def countAcce(data, i):
    s = abs(data.toolPos[i][1] - data.tool[i].body.position.y)
    if data.timerCount[i] > 0:
        data.acce[i] = 2 * s / data.timerCount[i]

def pulleyMove(data, i):
    if i != 0:
        if data.Near[i] == 0: data.index = 0 # figure out which pulley system
        elif data.Near[i] == 2: data.index = 1
        elif data.Near[i] == 4: data.index = 2
    '''
    if (i == 0 and data.pulley[0].l1 > 20 and 
    abs(data.tool[0].body.position.y - data.pulleyBars[1].block.body.position.y) <= data.tool[0].radius):
        data.pulley[0].l1 -= 2
        data.pulley[0].l2 += 2
        #data.pulley[0].l1 -= 2#1000 * data.tool[0].mass * data.acce[0]
        #data.pulley[0].l2 += 2#1000 * data.tool[0].mass * data.acce[0]
        # 3 pulley system
        data.pulleyBars[1].block.body.position += Vec2d(0, 2)
        data.pulleyBars[0].block.body.position -= Vec2d(0, 2)
        #data.pulleyBars[1].block.body.position += Vec2d(0, 2)#Vec2d(0, 1000 * data.tool[0].mass * data.acce[0])
        #data.pulleyBars[0].block.body.position -= Vec2d(0, 2)#Vec2d(0, 1000 * data.tool[0].mass * data.acce[0])
    if (i != 0 and data.Near[i] != None and data.pulley[data.index].l2 > 20 and 
    abs(data.tool[i].body.position.y - data.pulleyBars[data.Near[i]].block.body.position.y) <= data.tool[i].radius):
        print(data.index, data.Near[i]) # 2, 4
        data.pulley[data.index].l1 += 500 * data.tool[i].mass * data.acce[i]
        data.pulley[data.index].l2 -= 500 * data.tool[i].mass * data.acce[i]
        data.pulleyBars[data.Near[i]].block.body.position += Vec2d(0, 500 * data.tool[i].mass * data.acce[i])
        # data.pulleyBars has six Hblocks
        data.pulleyBars[data.Near[i] + 1].block.body.position -= Vec2d(0, 500 * data.tool[i].mass * data.acce[i])
    '''
def pulleyInfo(data):
    for pulley in data.pulley:
        pX1 = pulley.pX1
        pY1 = pulley.pY1
        pX2 = pulley.pX2
        pY2 = pulley.pY2
        bodyAlength = pulley.bodyAlength
        bodyBlength = pulley.bodyBlength
        data.pulleyInfo.append((pX1, pY1, pX2, pY2, bodyAlength, bodyBlength))

def pulleyBlocks(data):
    for block in data.pulleyInfo:
        pX1 = block[0]
        pY1 = block[1]
        bodyAlength = block[4]
        pX2 = block[2]
        pY2 = block[3]
        bodyBlength = block[5]
        data.pulleyBars.append(HBlock(space, 10, 1000, pX1, pY1, bodyAlength, 0, 15))
        data.pulleyBars.append(HBlock(space, 10, 1000, pX2, pY2, bodyBlength, 0, 15))
    data.pulleyBars.append(HBlock(space, 100, 10000, 640, 440, 20, 0, 50)) #bodies connected by the lever
    data.pulleyBars.append(HBlock(space, 100, 10000, 360, 630, 20, 0, 50)) #bodies connected by the lever

def oneDecimal(x):
    x = int(x * 10)
    return x / 10

def createDot1(data):
    for i in range(0, random.randint(5, 20)):
        data.dot1.append(Spark(random.randint(460, 500), 150, random.uniform(0.1, 2), random.uniform(-0.1, -0.5)))
        data.dot1.append(Spark(random.randint(460, 500), 150, random.uniform(0.1, 2), random.uniform(0.1, 0.5)))

def removeDot1(data):
    for dot in data.dot1:
        if dot.y >= 155 or dot.y <= 145:
            data.dot1.remove(dot)

def createDot2(data):
    for i in range(0, random.randint(5, 20)):
        data.dot2.append(Spark(random.randint(540, 580), 300, random.uniform(0.1, 2), random.uniform(-0.1, -0.5)))
        data.dot2.append(Spark(random.randint(540, 580), 300, random.uniform(0.1, 2), random.uniform(0.1, 0.5)))

def removeDot2(data):
    for dot in data.dot2:
        if dot.y >= 305 or dot.y <= 295:
            data.dot2.remove(dot)

def createDot3(data):
    for i in range(0, random.randint(5, 20)):
        data.dot3.append(Spark(random.randint(600, 640), 300, random.uniform(0.1, 2), random.uniform(-0.1, -0.5)))
        data.dot3.append(Spark(random.randint(600, 640), 300, random.uniform(0.1, 2), random.uniform(0.1, 0.5)))

def removeDot3(data):
    for dot in data.dot3:
        if dot.y >= 305 or dot.y <= 295:
            data.dot3.remove(dot)

def createDot4(data):
    for i in range(0, random.randint(5, 20)):
        data.dot4.append(Spark(random.randint(600, 640), 200, random.uniform(0.1, 2), random.uniform(-0.1, -0.5)))
        data.dot4.append(Spark(random.randint(600, 640), 200, random.uniform(0.1, 2), random.uniform(0.1, 0.5)))

def removeDot4(data):
    for dot in data.dot4:
        if dot.y >= 205 or dot.y <= 195:
            data.dot4.remove(dot)

def stage2MousePressed(event, data):
    if len(data.toolPos) <= 3:
        data.toolPos.append((event.x, event.y))
        data.tool.append(Atom(space, 8, 10, event.x, event.y))
        data.newBall = True # to find out the value of i

def findToolExactInitalPos(data):
    prevX, prevY = data.toolPos[-1][0], data.toolPos[-1][1]
    currX, currY = data.tool[-1].body.position.x, data.tool[-1].body.position.y
    if currX != prevX or currY != prevY:
        prevX = currX
        prevY = currY
    data.toolPos[-1] = (oneDecimal(currX), oneDecimal(currY))

def stage2redrawAll(canvas, data):
    for pos in data.starInLevel2:
        x, y = pos[0], pos[1]
        canvas.create_polygon((x, y - 10), (x + 7, y), (x, y + 10), (x - 7, y), fill = rgbString(255, 253, 184))
    canvas.create_oval(620 - 10, 250 - 10, 620 + 10, 250 + 10, fill = rgbString(data.color[4][0], data.color[4][1], data.color[4][2]), width = 0)
    canvas.create_oval(620 - 9, 250 - 9, 620 + 9, 250 + 9, fill = rgbString(207, 167, 193), width = 0)
    canvas.create_oval(620 - 8, 250 - 8, 620 + 8, 250 + 8, fill = rgbString(data.color[4][0], data.color[4][1], data.color[4][2]), width = 0)
    canvas.create_oval(620 - 7, 250 - 7, 620 + 7, 250 + 7, fill = rgbString(207, 167, 193), width = 0)
    canvas.create_rectangle(260, 660, 320, data.guanka, fill = rgbString(data.color[1][0], data.color[1][1], data.color[1][2]), width = 0)
    canvas.create_polygon(350, 680, 560, 580, 560, 680, fill = rgbString(data.color[3][0], data.color[3][1], data.color[3][2]), width = 0)
    canvas.create_rectangle(560, 580, 660, 610, fill = rgbString(data.color[3][0], data.color[3][1], data.color[3][2]), width = 0)
    canvas.create_rectangle(660, 580, 690, 680, fill = rgbString(data.color[3][0], data.color[3][1], data.color[3][2]), width = 0)
    canvas.create_rectangle(690, 610, 780, 680, fill = rgbString(data.color[3][0], data.color[3][1], data.color[3][2]), width = 0)
    canvas.create_rectangle(148, 241, 170, 289, fill = rgbString(data.color[3][0], data.color[3][1], data.color[3][2]), width = 0)
    canvas.create_rectangle(0, 0, 80, 60, fill = rgbString(data.color[3][0], data.color[3][1], data.color[3][2]), width = 0)
    canvas.create_rectangle(0, 510, 70, 540, fill = rgbString(data.color[2][0], data.color[2][1], data.color[2][2]), width = 0)
    canvas.create_polygon(70, 510, 70, 540, 90, 540, fill = rgbString(data.color[2][0], data.color[2][1], data.color[2][2]), width = 0)
    canvas.create_rectangle(20, 530, 40, 680, fill = rgbString(data.color[2][0], data.color[2][1], data.color[2][2]), width = 0)
    canvas.create_rectangle(40, 640, 100, 680, fill = rgbString(data.color[2][0], data.color[2][1], data.color[2][2]), width = 0)
    canvas.create_polygon(100, 640, 100, 680, 180, 680, fill = rgbString(data.color[2][0], data.color[2][1], data.color[2][2]), width = 0)
    data.pulley[0].drawPulleyJoint(canvas, rgbString(49, 61, 85))
    data.pulley[1].drawPulleyJoint(canvas, rgbString(211, 211, 211))
    data.pulley[2].drawPulleyJoint(canvas, rgbString(118, 109, 136))
    for i in range(0, 8):
        if i == 0 or i == 1:
            data.pulleyBars[i].drawBlock(canvas, data, (49, 61, 85))
        elif i == 2 or i == 3:
            data.pulleyBars[i].drawBlock(canvas, data, (211, 211, 211))
        elif i == 4 or i == 5:
            data.pulleyBars[i].drawBlock(canvas, data, (118, 109, 136))
        elif i == 6 or i == 7:
            data.pulleyBars[i].drawBlock(canvas, data, (118, 109, 136))
    for i in range(20): # first layer
        coor1, coor2, coor3 = data.triangleSet[i][0], data.triangleSet[i][1], data.triangleSet[i][2]
        canvas.create_polygon(coor1, coor2, coor3, fill = rgbString(data.color[1][0], data.color[1][1], data.color[1][2]), width = 0)
    for i in range(18): # first layer
        coor1, coor2 = data.rectangleSet1[i][0], data.rectangleSet1[i][1]
        canvas.create_rectangle(coor1, coor2, fill = rgbString(data.color[1][0], data.color[1][1], data.color[1][2]), width = 0)
    for i in range(20, 32): # first layer
        coor1, coor2, coor3 = data.triangleSet[i][0], data.triangleSet[i][1], data.triangleSet[i][2]
        canvas.create_polygon(coor1, coor2, coor3, fill = rgbString(data.color[3][0], data.color[3][1], data.color[3][2]), width = 0)
    for i in range(18, 31): # first layer
        coor1, coor2 = data.rectangleSet1[i][0], data.rectangleSet1[i][1]
        canvas.create_rectangle(coor1, coor2, fill = rgbString(data.color[2][0], data.color[2][1], data.color[2][2]), width = 0)
    for i in range(31, 38): # first layer
        coor1, coor2 = data.rectangleSet1[i][0], data.rectangleSet1[i][1]
        canvas.create_rectangle(coor1, coor2, fill = rgbString(data.color[3][0], data.color[3][1], data.color[3][2]), width = 0)
    for i in range(116): # 116, first layer
        data.block1[i].drawBlock(canvas, data, data.color[1])
    for i in range(116, 168):
        data.block1[i].drawBlock(canvas, data, data.color[2])
    for i in range(168, 219):
        data.block1[i].drawBlock(canvas, data, data.color[3])
    for i in range(0, 20):
        data.tiltedblock1[i].drawTiltedBlock(canvas, data, data.color[1])
    for i in range(20, 32):
        data.tiltedblock1[i].drawTiltedBlock(canvas, data, data.color[3])
    canvas.create_line(data.pulleyBars[-2].block.body.position.x, data.pulleyBars[-2].block.body.position.y, data.pulleyBars[-2].block.body.position.x, 380, fill = rgbString(118, 109, 136), width = 2)
    canvas.create_line(data.pulleyBars[-1].block.body.position.x, data.pulleyBars[-1].block.body.position.y, data.pulleyBars[-1].block.body.position.x, 380, fill = rgbString(118, 109, 136), width = 2)
    canvas.create_line(data.pulleyBars[-1].block.body.position.x, 380, data.pulleyBars[-2].block.body.position.x, 380, fill = rgbString(118, 109, 136), width = 2)
    for tool in data.tool:
        tool.drawAtom(canvas, (0, 0, 0))
    for i in range(4):
        data.shell1[i].drawBlock(canvas, data, data.color[4])
    for i in range(4, len(data.shell1)):
        data.shell1[i].drawTiltedBlock(canvas, data, data.color[4])
    canvas.create_oval(230 - 25, 58 - 25, 230 + 25, 58 + 25, fill = rgbString(data.color[4][0], data.color[4][1], data.color[4][2]), width = 0)
    canvas.create_oval(230 - 24, 58 - 24, 230 + 24, 58 + 24, fill = rgbString(207, 167, 193), width = 0)
    canvas.create_oval(230 - 15, 58 - 15, 230 + 15, 58 + 15, fill = rgbString(data.color[4][0], data.color[4][1], data.color[4][2]), width = 0)
    canvas.create_oval(230 - 14, 58 - 14, 230 + 14, 58 + 14, fill = rgbString(207, 167, 193), width = 0)
    canvas.create_oval(230 - 6, 58 - 6, 230 + 6, 58 + 6, fill = rgbString(232, 111, 120), width = 0)
    data.protagonist.drawAtom(canvas, (255, 255, 255))
    canvas.create_rectangle(500, 670, 800, 680, fill = rgbString(data.color[1][0], data.color[1][1], data.color[1][2]), width = 0)
    canvas.create_polygon((470, 680), (500, 680), (500, 670), fill = rgbString(data.color[1][0], data.color[1][1], data.color[1][2]), width = 0)
    canvas.create_rectangle(550, 640, 580, 680, fill = rgbString(data.color[1][0], data.color[1][1], data.color[1][2]), width = 0)
    canvas.create_rectangle(580, 660, 610, 680, fill = rgbString(data.color[1][0], data.color[1][1], data.color[1][2]), width = 0)
    canvas.create_rectangle(610, 665, 640, 680, fill = rgbString(data.color[1][0], data.color[1][1], data.color[1][2]), width = 0)
    canvas.create_rectangle(700, 665, 730, 680, fill = rgbString(data.color[1][0], data.color[1][1], data.color[1][2]), width = 0)
    canvas.create_rectangle(730, 660, 760, 680, fill = rgbString(data.color[1][0], data.color[1][1], data.color[1][2]), width = 0)
    canvas.create_rectangle(760, 640, 790, 680, fill = rgbString(data.color[1][0], data.color[1][1], data.color[1][2]), width = 0)
    removeDot1(data)
    if len(data.dot1) < 15: createDot1(data)
    removeDot2(data)
    if len(data.dot2) < 15: createDot2(data)
    removeDot3(data)
    if len(data.dot3) < 15: createDot3(data)
    removeDot4(data)
    if len(data.dot4) < 15: createDot4(data)
    for dot in data.dot1:
        dot.drawSpark(canvas)
    for dot in data.dot2:
        dot.drawSpark(canvas)
    for dot in data.dot3:
        dot.drawSpark(canvas)
    for dot in data.dot4:
        dot.drawSpark(canvas)
    for domino in data.domino2:
        domino.drawDomino(canvas, data, data.color[2])
    canvas.create_line(520, 360, data.domino2[0].domino.body.position.x, data.domino2[0].domino.body.position.y,
                       fill = rgbString(data.color[2][0], data.color[2][1], data.color[2][2]), width = 2)
    for signal in data.signalInLevel2:
        signal.drawSignal(canvas)
    if (data.protagonist.body.position.x > 260 and data.protagonist.body.position.x < 290 and 
        data.protagonist.body.position.y > 220 and data.protagonist.body.position.y < 230):
        canvas.create_text(280, 210, text = "Here it is!", font = "Arial 15", fill = "black")
        canvas.create_text(290, 40, text = "This is its home", font = "Arial 15", fill = "black")
        canvas.create_text(360, 230, text = "Push the ball", font = "Arial 15", fill = "black")
        canvas.create_text(100, 600, text = "Gateway that", font = "Arial 15", fill = "white")
        canvas.create_text(100, 620, text = "opens door 1", font = "Arial 15", fill = "white")
        canvas.create_text(290, 670, text = "Door 1", font = "Arial 15", fill = "white")
    elif (data.protagonist.body.position.x > 760 and data.protagonist.body.position.x < 800 and 
        data.protagonist.body.position.y > 450 and data.protagonist.body.position.y < 650):
        canvas.create_text(744, 550, text = "Eat the stars!")
    if data.stage2Win == True:
        canvas.create_text(data.width // 2, data.height // 2, text = "Congrats!", font = "Arial 55", fill = "white")
        canvas.create_text(data.width // 2, data.height // 2 + 65, text = "Almost there", font = "Arial 55", fill = "white")

def stage2TimerFired(data):
    for pos in data.starInLevel2:
        x, y = pos[0], pos[1]
        if distance(data.protagonist.body.position.x, data.protagonist.body.position.y, x, y) < data.protagonist.radius:
            data.starInLevel2.remove(pos)
    if data.newBall == False:
        findToolExactInitalPos(data) # in case the ball falls down, its position is no longer (event.x, event.y), updates its position
        countTime(data, 0)
        countAcce(data, 0)
        if (data.pulley[0].l1 > 20 and 
        abs(data.tool[0].body.position.y - data.pulleyBars[1].block.body.position.y) <= data.tool[0].radius):
            data.fall1 = True
        elif data.pulley[0].l1 <= 20:
            data.fall1 = False
    if data.fall1 == True:
        data.pulley[0].l1 -= 500 * data.tool[0].mass * data.acce[0]
        data.pulley[0].l2 += 500 * data.tool[0].mass * data.acce[0]
        data.pulleyBars[1].block.body.position += Vec2d(0, 500 * data.tool[0].mass * data.acce[0])
        data.pulleyBars[0].block.body.position -= Vec2d(0, 500 * data.tool[0].mass * data.acce[0])
    elif data.newBall == True:
        findToolExactInitalPos(data) 
        countTime(data, len(data.tool) - 1)
        countAcce(data, len(data.tool) - 1)
        pulleyMove(data, len(data.tool) - 1)
        if (data.Near[len(data.tool) - 1] != None and data.pulley[data.index].l2 > 50 and 
        abs(data.tool[len(data.tool) - 1].body.position.y - 
            data.pulleyBars[data.Near[len(data.tool) - 1]].block.body.position.y) 
            <= data.tool[len(data.tool) - 1].radius):
                data.fallOther[len(data.tool) - 1] = True
        elif data.pulley[data.index].l2 <= 30:
            data.fallOther[len(data.tool) - 1] = False
    #print(data.fallOther[len(data.tool) - 1])
    if data.fallOther[len(data.tool) - 1] == True:
        if len(data.tool) == 2:
            data.pulley[data.index].l1 += 40 * data.tool[len(data.tool) - 1].mass * data.acce[len(data.tool) - 1]
            data.pulley[data.index].l2 -= 40 * data.tool[len(data.tool) - 1].mass * data.acce[len(data.tool) - 1]
            data.pulleyBars[data.Near[len(data.tool) - 1]].block.body.position += Vec2d(0, 40 * data.tool[len(data.tool) - 1].mass * data.acce[len(data.tool) - 1])
            data.pulleyBars[data.Near[len(data.tool) - 1] + 1].block.body.position -= Vec2d(0, 40 * data.tool[len(data.tool) - 1].mass * data.acce[len(data.tool) - 1])
        else:
            data.pulley[data.index].l1 += 80 * data.tool[len(data.tool) - 1].mass * data.acce[len(data.tool) - 1]
            data.pulley[data.index].l2 -= 150 * data.tool[len(data.tool) - 1].mass * data.acce[len(data.tool) - 1]
            data.pulleyBars[data.Near[len(data.tool) - 1]].block.body.position += Vec2d(0, 80 * data.tool[len(data.tool) - 1].mass * data.acce[len(data.tool) - 1])
            # data.pulleyBars has six Hblocks
            data.pulleyBars[data.Near[len(data.tool) - 1] + 1].block.body.position -= Vec2d(0, 150 * data.tool[len(data.tool) - 1].mass * data.acce[len(data.tool) - 1])
    data.shell1[3].block.body.position += data.dir3 * Vec2d(0, 1.5)
    data.shell1[1].block.body.position -= data.dir3 * Vec2d(0, 1.5)
    data.shell1[2].block.body.position += data.dir3 * Vec2d(1, 0)
    data.shell1[-1].block.body.position += data.dir3 * Vec2d(0, 0.8)
    data.shell1[-2].block.body.position += data.dir3 * Vec2d(0, 1.5)
    data.shell1[-3].block.body.position -= data.dir3 * Vec2d(0, 1)
    if data.shell1[-1].block.body.position.y >= 160:
        data.dir3 = -1
    elif data.shell1[-2].block.body.position.y <= 70:
        data.dir3 = 1
    for dot in data.dot1:
        dot.onTimerFired(data)
    for dot in data.dot2:
        dot.onTimerFired(data)
    for dot in data.dot3:
        dot.onTimerFired(data)
    for dot in data.dot4:
        dot.onTimerFired(data)
    if data.tool[0].body.position.y >= 650 and data.tool[0].body.position.y > 80 and data.tool[0].body.position.x < 110:
        data.guanka -= 1
        if data.guanka <= 660:
            data.guanka = 650
    if (data.protagonist.body.position.x >= 620 and data.protagonist.body.position.x <= 660
    and data.protagonist.body.position.y >= 430):
        if data.pulleyBars[-2].block.body.position.y <= 500:
            data.pulleyBars[-2].block.body.position += Vec2d(0, 2)
            data.pulleyBars[-1].block.body.position -= Vec2d(0, 2)
    if len(data.tool) == 2:
        if (abs(data.tool[1].body.position.y - data.pulleyBars[0].block.body.position.y) > data.tool[0].radius
        and data.tool[1].body.position.y > data.pulleyBars[0].block.body.position.y
        and (data.tool[1].body.position.x < data.pulleyBars[0].block.body.position.x - 30)
        and data.pulley[0].l1 >= 20):
            data.pulley[0].l1 -= 2
            data.pulley[0].l2 += 2
            # 3 pulley system
            data.pulleyBars[1].block.body.position += Vec2d(0, 2)
            data.pulleyBars[0].block.body.position -= Vec2d(0, 2)
    for signal in data.signalInLevel2:
        signal.onTimerFired1()
        if signal.pY < 650:
            data.signalInLevel2.remove(signal)
    data.timerCountInLevel2 += 1
    if data.timerCountInLevel2 % 15 == 0:
        for i in range(30):
            data.signalInLevel2.append(Signal(random.randint(1, 3), random.uniform(82, 108), 675,random.uniform(1, 6), data.stage3Color[random.randint(8, 12)]))
    elif (data.protagonist.body.position.x > 220 and data.protagonist.body.position.x < 240 and 
        data.protagonist.body.position.y > 50 and data.protagonist.body.position.y < 60):
        print(data.protagonist.body.position)
        data.stage2Win = True

def introPage(data):
    data.system.append(Particle(0, 200, 200, 3, 120, 1))
    data.system.append(Particle(0, 200, 200, 6, 100, -1))
    data.system.append(Particle(0, 200, 200, 10, 60, 1))
    data.system.append(Particle(0, 650, 350, 3, 120, -1))
    data.system.append(Particle(0, 650, 350, 7, 80, -1))
    data.system.append(Particle(0, 650, 350, 11, 60, 1))
    data.system.append(Particle(0, 300, 500, 2, 150, 1))
    data.system.append(Particle(0, 300, 500, 7, 110, 1))
    data.system.append(Particle(0, 300, 500, 10, 70, -1))

def intropageInit(data):
    data.comet = []
    data.x = random.randint(700, 800)
    data.y = random.randint(0, 100)
    data.system = []
    data.motionPosn = (0, 0)
    data.stars, data.comet = [], []
    data.introColor = [(255, 255, 255), (150, 164, 177)]
    for i in range(200):
        data.stars.append([random.randint(0, 800), random.randint(0, 800), random.uniform(0.5, 2), random.randint(0, 1)])
    data.cometCount = 0
    data.v = 0
    comet(data)

def comet(data):
    data.comet = []
    data.comet.append([random.randint(100, 800), random.randint(100, 400), random.randint(20, 90)])

def intropageTimerFired(data):
    data.x -= 10
    data.y -= 10
    for particle in data.system:
        particle.onTimerFired()
    data.v += 10
    if data.v >= 500: data.v = 0
    data.cometCount += 1
    if data.cometCount % 5 == 0:
        comet(data)

def introredrawAll(canvas, data):
    stars(canvas, data) #97, 117, 134
    canvas.create_oval(200 - 120 - 3, 200 - 120 - 3, 200 + 120 + 3, 200 + 120 + 3, fill = "white", width = 0)
    canvas.create_oval(200 - 120 - 2, 200 - 120 - 2, 200 + 120 + 2, 200 + 120 + 2, fill = rgbString(25, 35, 44), width = 0)
    canvas.create_oval(200 - 100 - 6, 200 - 100 - 6, 200 + 100 + 6, 200 + 100 + 6, fill = "white", width = 0)
    canvas.create_oval(200 - 100 - 5, 200 - 100 - 5, 200 + 100 + 5, 200 + 100 + 5, fill = rgbString(25, 35, 44), width = 0)
    canvas.create_oval(200 - 60 - 10, 200 - 60 - 10, 200 + 60 + 10, 200 + 60 + 10, fill = rgbString(254, 254, 210), width = 0)
    canvas.create_oval(200 - 60 - 9, 200 - 60 - 9, 200 + 60 + 9, 200 + 60 + 9, fill = rgbString(25, 35, 44), width = 0)
    canvas.create_oval(650 - 120 - 3, 350 - 120 - 3, 650 + 120 + 3, 350 + 120 + 3, fill = "white", width = 0)
    canvas.create_oval(650 - 120 - 2, 350 - 120 - 2, 650 + 120 + 2, 350 + 120 + 2, fill = rgbString(25, 35, 44), width = 0)
    canvas.create_oval(650 - 80 - 7, 350 - 80 - 7, 650 + 80 + 7, 350 + 80 + 7, fill = "white", width = 0)
    canvas.create_oval(650 - 80 - 6, 350 - 80 - 6, 650 + 80 + 6, 350 + 80 + 6, fill = rgbString(25, 35, 44), width = 0)
    canvas.create_oval(650 - 60 - 11, 350 - 60 - 11, 650 + 60 + 11, 350 + 60 + 11, fill = "white", width = 0)
    canvas.create_oval(650 - 60 - 10, 350 - 60 - 10, 650 + 60 + 10, 350 + 60 + 10, fill = rgbString(25, 35, 44), width = 0)
    canvas.create_oval(300 - 150 - 2, 500 - 150 - 2, 300 + 150 + 2, 500 + 150 + 2, fill = rgbString(254, 254, 210), width = 0)
    canvas.create_oval(300 - 150 - 1, 500 - 150 - 1, 300 + 150 + 1, 500 + 150 + 1, fill = rgbString(25, 35, 44), width = 0)
    canvas.create_oval(300 - 110 - 7, 500 - 110 - 7, 300 + 110 + 7, 500 + 110 + 7, fill = "white", width = 0)
    canvas.create_oval(300 - 110 - 6, 500 - 110 - 6, 300 + 110 + 6, 500 + 110 + 6, fill = rgbString(25, 35, 44), width = 0)
    canvas.create_oval(300 - 70 - 10, 500 - 70 - 10, 300 + 70 + 10, 500 + 70 + 10, fill = rgbString(254, 254, 210), width = 0)
    canvas.create_oval(300 - 70 - 9, 500 - 70 - 9, 300 + 70 + 9, 500 + 70 + 9, fill = rgbString(25, 35, 44), width = 0)
    canvas.create_oval(200 - 30, 200 - 30, 200 + 30, 200 + 30, fill = "white", width = 0)
    canvas.create_oval(650 - 30, 350 - 30, 650 + 30, 350 + 30, fill = "white", width = 0)
    canvas.create_oval(300 - 30, 500 - 30, 300 + 30, 500 + 30, fill = "white", width = 0)
    for particle in data.system:
        particle.drawParticle(canvas, (255, 255, 255)) 
    canvas.create_text(200, 200, text = "1", font = "Hannotate 25")
    canvas.create_text(650, 350, text = "2", font = "Hannotate 25")
    canvas.create_text(300, 500, text = "3", font = "Hannotate 25")
    canvas.create_oval(630 - 160, 50 - 160, 630 + 160, 50 + 160, fill = rgbString(97, 117, 134), width = 0)
    canvas.create_oval(620 - 160, 30 - 160, 620 + 160, 30 + 160, fill = rgbString(25, 35, 44), width = 0)
    canvas.create_oval(560 - 60, 120 - 60, 570 + 60, 120 + 60, fill = rgbString(43, 56, 72), width = 0)
    canvas.create_oval(550 - 60, 120 - 60, 550 + 60, 120 + 60, fill = rgbString(8, 16, 18), width = 0)
    canvas.create_oval(740 - 160, 680 - 160, 740 + 160, 680 + 160, fill = rgbString(8, 16, 18), width = 0)
    cometDraw(canvas, data)
    canvas.create_text(550, 120, text = "Press me!\n For more info", font = "Hannotate 15", fill = "white")

def stars(canvas, data):
    for star in data.stars:
        x = star[0]
        y = star[1]
        radius = star[2]
        color = star[3]
        canvas.create_polygon((x, y - radius), (x + radius, y), (x, y + radius), (x - radius, y), 
            fill = rgbString(data.introColor[color][0], data.introColor[color][1], data.introColor[color][2]))

def cometDraw(canvas, data):
    x = data.comet[0][0]
    y = data.comet[0][1]
    length = data.comet[0][2]
    canvas.create_line(x - data.v, y + data.v, x + length - data.v, y - length + data.v, fill = "white")

def stage3init(data):
    data.ladder = []
    data.motionPosn = None
    data.leftPosn = None
    data.motion = False
    data.playerCreateLadder1 = []
    data.stats = []
    data.stage3Color = [(25, 106, 117), (28, 124, 139), (53, 129, 141), 
    (52, 137, 139), (51, 142, 143), (86, 157, 145), (107, 165, 164), 
    (126, 162, 158), (135, 186, 173), (139, 175, 177), (158, 193, 182),
    (178, 207, 180), (198, 223, 168), (238, 246, 195), (244, 228, 176),
    (244, 182, 146), (220, 156, 126), (230, 129, 119), (228, 79, 78), 
    (231, 89, 100), (220, 97, 92), (222, 101, 93), (240, 124, 138), (221, 141, 159)]
    #data.stage3Color = [(28, 36, 29), (65, 93, 124), (53, 27, 41), (66, 61, 49)]
    data.curveInfoList2 = []
    data.tiltedblock2 = []
    data.changeColor = 0
    data.movableLadder1 = [] #vertical
    data.movableLadder2 = [] #horizontal
    data.movableLadder3 = []
    data.movableLadder4 = []
    data.x, data.y = 400, 300
    data.length = []
    data.snowball = []
    data.HBlockPos = [] #stores the y position of HBlocks
    data.capsuleXValue = []
    data.Ypos = []
    data.capsule = []
    for i in range(100):
        data.snowball.append([random.randint(0, 800), random.randint(0, 800), random.uniform(0.5, 2), random.randint(0, 1)])
    data.sample = []
    data.moveX, data.moveY = 300, 300
    data.ladder = []
    data.fixedLadder = []
    data.curveInfoList2 = findCoord([(460, 500), (460, 650), (680, 650), (680, 500)])
    data.createdLadder = []
    data.i = 0
    data.signal11, data.signal12, data.signal21, data.signal22, data.signal31, data.signal32, data.signal41, data.signal42 = [], [], [], [], [], [], [], []
    data.timerCount3 = 0
    data.starPos, data.starDown = [], []
    for i in range(0, 19):
        data.starPos.append((570 - 100 * math.cos(math.radians(10 * i)), 500 + 100 * math.sin(math.radians(10 * i))))
    for i in range(0, 19):
        data.starDown.append((570 - 100 * math.cos(math.radians(10 * i)), 500 + 100 * math.sin(math.radians(10 * i)) + 5))
    data.stage3Win = False

class Capsule(object):
    def __init__(self, length, order, start):
        self.length = length
        self.order = order
        self.start = start

    def drawCapsule(self, canvas, color, Ypos):
        r, g, b = color[0], color[1], color[2]
        canvas.create_rectangle(self.start + self.order * 12, Ypos, self.start + 10 + self.order * 12, Ypos - self.length, fill = rgbString(r, g, b), width = 0)
        canvas.create_oval(self.start + self.order * 12, Ypos - 5, self.start + 10 + self.order * 12, Ypos + 5, fill = rgbString(r, g, b), width = 0)
        canvas.create_oval(self.start + self.order * 12, Ypos - 5 - self.length, self.start + 10 + self.order * 12, Ypos + 5 - self.length, fill = rgbString(r, g, b), width = 0)

def clearStage3(data):
    #space.remove(data.protagonist.body, data.protagonist.shape)
    for i in range(len(data.tiltedblock2)):
        space.remove(data.tiltedblock2[i].block)
    for i in range(len(data.ladder)):
        space.remove(data.ladder[i].block)

def stage3Lists(data):
    data.protagonist = Atom(space, 8, 10, 160, 60)  
    for i in range(len(data.curveInfoList2) - 1):
        pX1 = data.curveInfoList2[i][0]
        pY1 = data.curveInfoList2[i][1]
        l1 = data.curveInfoList2[i][2]
        l2 = data.curveInfoList2[i][3]
        data.tiltedblock2.append(TiltedBlock(space, 10, 10, pX1, pY1, -l1, -l2))
    triangleWalls(0, 0, 50, 690).bordersAndFill3(data, 3)
    triangleWalls(200, 0, 60, 200).bordersAndFill3(data, 3)
    triangleWalls(140, 80, 60, 10).bordersAndFill3(data, 3)
    triangleWalls(220, 200, 20, 50).bordersAndFill3(data, 3) ###
    triangleWalls(200, 250, 60, 240).bordersAndFill3(data, 3)
    triangleWalls(200, 250, 60, 240).bordersAndFill3(data, 3)
    triangleWalls(210, 490, 40, 50).bordersAndFill3(data, 3) ###
    triangleWalls(200, 540, 60, 150).bordersAndFill3(data, 3)
    triangleWalls(380, 0, 60, 90).bordersAndFill3(data, 3)
    triangleWalls(380, 70, 80, 200).bordersAndFill3(data, 3)
    triangleWalls(405, 270, 35, 60).bordersAndFill3(data, 3) ###
    triangleWalls(380, 330, 80, 370).bordersAndFill3(data, 3)
    triangleWalls(380, 600, -50, 20).bordersAndFill3(data, 3)
    triangleWalls(600, 0, 20, 120).bordersAndFill3(data, 3) ###
    triangleWalls(590, 120, 40, 140).bordersAndFill3(data, 3)
    triangleWalls(600, 230, 20, 50).bordersAndFill3(data, 3) ###
    triangleWalls(580, 280, 60, 50).bordersAndFill3(data, 3)
    triangleWalls(750, 0, 50, 150).bordersAndFill3(data, 3)
    triangleWalls(780, 150, 20, 60).bordersAndFill3(data, 3)
    triangleWalls(760, 210, 40, 30).bordersAndFill3(data, 3)

class Signal(object):
    def __init__(self, r, pX, pY, v, color):
        self.r = r
        self.pX = pX
        self.pY = pY
        self.color = color
        self.v = v

    def drawSignal(self, canvas):
        r, g, b = self.color[0], self.color[1], self.color[2]
        canvas.create_polygon(self.pX, self.pY, self.pX + self.r, self.pY + self.r, 
            self.pX, self.pY + 2 * self.r, self.pX - self.r, self.pY + self.r,
            fill = rgbString(r, g, b), width = 0)

    def onTimerFired(self):
        self.pX -= self.v

    def onTimerFired1(self):
        self.pY -= self.v

def createSignal(data):
    for i in range(50):
        data.signal11.append(Signal(random.randint(1, 3), 230, random.uniform(200, 250), random.uniform(1, 6), data.stage3Color[random.randint(0, 7)]))
        data.signal12.append(Signal(random.randint(1, 3), 430, random.uniform(270, 330), random.uniform(1, 6), data.stage3Color[random.randint(0, 7)]))
        data.signal21.append(Signal(random.randint(1, 3), 250, random.uniform(490, 530), -random.uniform(1, 6), data.stage3Color[random.randint(8, 12)]))
        data.signal22.append(Signal(random.randint(1, 3), 430, random.uniform(0, 60), -random.uniform(1, 6), data.stage3Color[random.randint(8, 12)]))
        data.signal31.append(Signal(random.randint(1, 3), 780, random.uniform(150, 210), random.uniform(1, 6), data.stage3Color[random.randint(18, 23)]))
        data.signal32.append(Signal(random.randint(1, 3), 430, random.uniform(270, 325), -random.uniform(1, 6), data.stage3Color[random.randint(18, 23)]))
        data.signal41.append(Signal(random.randint(1, 3), 600, random.uniform(80, 120), random.uniform(1, 6), data.stage3Color[random.randint(13, 16)]))
        data.signal42.append(Signal(random.randint(1, 3), 610, random.uniform(260, 280), random.uniform(1, 6), data.stage3Color[random.randint(13, 16)]))

def snowball(canvas, data):
    #data.introColor[color][0], data.introColor[color][1], data.introColor[color][2]
    for snowball in data.snowball:
        x = snowball[0]
        y = snowball[1]
        radius = snowball[2]
        color = snowball[3]
        canvas.create_oval((x - radius, y - radius), (x + radius, y + radius), 
            fill = rgbString(75, 75, 85), width = 0)

def stage3MousePressed(event, data):
    prevL = len(data.playerCreateLadder1)
    data.playerCreateLadder1.append((event.x, event.y)) #stores the position of new dots
    currL = len(data.playerCreateLadder1)
    if prevL != currL and currL > 1:
        x, y = data.playerCreateLadder1[-2][0], data.playerCreateLadder1[-2][1]
        l1 = data.playerCreateLadder1[-1][0] - data.playerCreateLadder1[-2][0]
        l2 = data.playerCreateLadder1[-1][1] - data.playerCreateLadder1[-2][1]
        data.createdLadder.append(TiltedBlock(space, 10, 10, x, y, l1, l2)) #add ladder to space
        prevL = currL
        #data.playerCreateLadder1.pop()

def stage3keyPressed(event, data):
    if event.keysym == "d":
        if len(data.createdLadder) > 0:
            space.remove(data.createdLadder[-1].block)
            data.createdLadder.pop()
            data.playerCreateLadder1.pop()
        elif len(data.createdLadder) == 0:
            data.playerCreateLadder1 = []
    elif event.keysym == "space":
        data.protagonist.body.position = Vec2d(138, 75)
    elif event.keysym == "t":
        data.protagonist.body.position = Vec2d(775, 205)
        data.starPos, data.starDown = [], []
        for i in range(0, 19):
            data.starPos.append((570 - 100 * math.cos(math.radians(10 * i)), 500 + 100 * math.sin(math.radians(10 * i))))
        for i in range(0, 19):
            data.starDown.append((570 - 100 * math.cos(math.radians(10 * i)), 500 + 100 * math.sin(math.radians(10 * i)) + 5))

def stage3TimerFired(data):
    #[(400, 325), (445, 65), (595, 275), (775, 205)]
    if 19 - len(data.starPos) >= 10:
        data.stage3Win = True
    if 19 - len(data.starPos) >= 10:
        data.stage3Win = True
    data.timerCount3 += 1
    if data.protagonist.body.position.x >= 210 and data.protagonist.body.position.x <= 220 and data.protagonist.body.position.y >= 240 and data.protagonist.body.position.y <= 250:
        data.protagonist.body.position = Vec2d(395, 325.5)
    elif data.protagonist.body.position.x <= 260 and data.protagonist.body.position.x >= 255 and data.protagonist.body.position.y >= 525 and data.protagonist.body.position.y <= 535:
        data.protagonist.body.position = Vec2d(445, 65)
    elif data.protagonist.body.position.x >= 590 and data.protagonist.body.position.x <= 600 and data.protagonist.body.position.y >= 110 and data.protagonist.body.position.y <= 120:
        data.protagonist.body.position = Vec2d(595, 275)
    elif data.protagonist.body.position.x <= 450 and data.protagonist.body.position.x >= 446 and data.protagonist.body.position.y >= 320 and data.protagonist.body.position.y <= 330:
        data.protagonist.body.position = Vec2d(775, 205)
    if data.protagonist.body.position == Vec2d(775, 205):
        data.show = True
    for signal in data.signal11:
        signal.onTimerFired()
        if signal.pX < 190:
            data.signal11.remove(signal)
    for signal in data.signal12:
        signal.onTimerFired()
        if signal.pX < 370:
            data.signal12.remove(signal)
    for signal in data.signal21:
        signal.onTimerFired()
        if signal.pX > 290:
            data.signal21.remove(signal)
    for signal in data.signal22:
        signal.onTimerFired()
        if signal.pX > 480:
            data.signal22.remove(signal)
    for signal in data.signal31:
        signal.onTimerFired()
        if signal.pX < 740:
            data.signal31.remove(signal)
    for signal in data.signal32:
        signal.onTimerFired()
        if signal.pX > 470:
            data.signal32.remove(signal)
    for signal in data.signal41:
        signal.onTimerFired()
        if signal.pX < 570:
            data.signal41.remove(signal)
    for signal in data.signal42:
        signal.onTimerFired()
        if signal.pX < 580:
            data.signal42.remove(signal)
    for down in data.starDown:
        i = data.starDown.index(down)
        if distance(down[0], down[1], data.protagonist.body.position.x, data.protagonist.body.position.y) <= data.protagonist.radius:
            data.starDown.remove(down)
            data.starPos.remove(data.starPos[i])

def stage3redrawAll(canvas, data):
    canvas.create_rectangle(500, 0, 550, 160, fill = rgbString(166, 146, 113), width = 0) # most inner side
    canvas.create_rectangle(520, 160, 530, 210, fill = rgbString(166, 146, 113), width = 0)
    canvas.create_rectangle(500, 210, 550, 410, fill = rgbString(166, 146, 113), width = 0)
    canvas.create_rectangle(490, 410, 550, 500, fill = rgbString(166, 146, 113), width = 0)
    canvas.create_rectangle(515, 500, 535, 560, fill = rgbString(166, 146, 113), width = 0)
    canvas.create_rectangle(500, 560, 550, 690, fill = rgbString(166, 146, 113), width = 0)
    canvas.create_rectangle(70, 0, 120, 120, fill = rgbString(88, 83, 66), width = 0)
    canvas.create_rectangle(90, 120, 100, 170, fill = rgbString(88, 83, 66), width = 0)
    canvas.create_rectangle(70, 170, 120, 600, fill = rgbString(88, 83, 66), width = 0)
    canvas.create_rectangle(80, 600, 110, 640, fill = rgbString(88, 83, 66), width = 0)
    canvas.create_rectangle(70, 640, 120, 690, fill = rgbString(88, 83, 66), width = 0)
    canvas.create_rectangle(680, 0, 730, 200, fill = rgbString(88, 83, 66), width = 0)
    canvas.create_rectangle(690, 200, 720, 260, fill = rgbString(88, 83, 66), width = 0)
    canvas.create_rectangle(670, 260, 740, 560, fill = rgbString(88, 83, 66), width = 0)
    canvas.create_rectangle(700, 560, 710, 600, fill = rgbString(88, 83, 66), width = 0)
    canvas.create_rectangle(680, 600, 730, 690, fill = rgbString(88, 83, 66), width = 0)
    canvas.create_rectangle(340, 0, 390, 220, fill = rgbString(132, 116, 90), width = 0)
    canvas.create_rectangle(350, 220, 380, 270, fill = rgbString(132, 116, 90), width = 0)
    canvas.create_rectangle(340, 270, 390, 560, fill = rgbString(132, 116, 90), width = 0)
    canvas.create_rectangle(360, 560, 370, 610, fill = rgbString(132, 116, 90), width = 0)
    canvas.create_rectangle(340, 610, 390, 690, fill = rgbString(132, 116, 90), width = 0)
    canvas.create_rectangle(540, 0, 590, 300, fill = rgbString(132, 116, 90), width = 0)
    canvas.create_rectangle(560, 300, 570, 360, fill = rgbString(132, 116, 90), width = 0)
    canvas.create_rectangle(540, 360, 590, 690, fill = rgbString(132, 116, 90), width = 0)
    canvas.create_rectangle(180, 0, 230, 260, fill = rgbString(166, 146, 113), width = 0) #129, 113, 87
    canvas.create_rectangle(190, 260, 220, 330, fill = rgbString(166, 146, 113), width = 0)
    canvas.create_rectangle(180, 330, 220, 690, fill = rgbString(166, 146, 113), width = 0)
    if data.timerCount3 % 15 == 0:
        createSignal(data)
    for signal in data.signal11:
        signal.drawSignal(canvas)
    for signal in data.signal12:
        signal.drawSignal(canvas)
    for signal in data.signal21:
        signal.drawSignal(canvas)
    for signal in data.signal22:
        signal.drawSignal(canvas)
    for signal in data.signal31:
        signal.drawSignal(canvas)
    for signal in data.signal32:
        signal.drawSignal(canvas)
    for signal in data.signal41:
        signal.drawSignal(canvas)
    for signal in data.signal42:
        signal.drawSignal(canvas)
    for starPos in data.starPos:
        x = starPos[0]
        y = starPos[1]
        canvas.create_polygon((x, y - 5), (x + 5, y), (x, y + 5), (x - 5, y), fill = rgbString(255, 253, 184))
    data.protagonist.drawAtom(canvas, (255, 255, 255))
    canvas.create_rectangle(590, 0, 630, 80, fill = rgbString(52, 52, 41), width = 0)
    canvas.create_rectangle(590, 220, 460, 230, fill = rgbString(52, 52, 41), width = 0)
    canvas.create_rectangle(260, 40, 300, 50, fill = rgbString(52, 52, 41), width = 0)
    canvas.create_polygon((300, 40), (320, 70), (320, 80), (300, 50), fill = rgbString(52, 52, 41), width = 0)
    canvas.create_rectangle(320, 70, 400, 80, fill = rgbString(52, 52, 41), width = 0)
    for ladder in data.ladder:
        ladder.drawBlock(canvas, data, (52, 52, 41))
    for ladder in data.fixedLadder:
        coor1, coor2 = ladder[0], ladder[1]
        canvas.create_rectangle(coor1, coor2, fill = rgbString(52, 52, 41), width = 0)
    for curve in data.tiltedblock2:
        curve.drawTiltedBlock(canvas, data, (52, 52, 41)) #52, 52, 41
    for ladder in data.createdLadder:
        ladder.drawTiltedBlock(canvas, data, (209, 246, 205)) #37, 181, 162
    for oval in data.playerCreateLadder1:
        x, y = oval[0], oval[1]
        r, g, b = data.stage3Color[0][0], data.stage3Color[0][1], data.stage3Color[0][2]
        canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill = rgbString(37, 181, 162), width = 0)
    canvas.create_polygon((30, 30), (40, 40), (30, 50), (20, 40), fill = rgbString(255, 253, 184))
    canvas.create_text((30, 70), text = 19 - len(data.starPos), font = "Arial 25", fill = rgbString(255, 253, 184))
    if data.c == True:
        if data.protagonist.body.position.x < 58:
            canvas.create_text((230, 30), text = "How", font = "Arial 15", fill = "white")
            canvas.create_text((230, 45), text = "to", font = "Arial 15", fill = "white")
            canvas.create_text((230, 60), text = "go", font = "Arial 15", fill = "white")
            canvas.create_text((230, 75), text = "through", font = "Arial 15", fill = "white")
            canvas.create_text((230, 90), text = "the", font = "Arial 15", fill = "white")
            canvas.create_text((230, 105), text = "dark", font = "Arial 15", fill = "white")
            canvas.create_text((230, 120), text = "brown", font = "Arial 15", fill = "white")
            canvas.create_text((230, 135), text = "block?", font = "Arial 15", fill = "white")
        if data.protagonist.body.position.y > 680:
            canvas.create_text(data.width // 2, data.height // 2, text = "Whoooops", font = "Arial 55", fill = "white")
    if data.protagonist.body.position.y <= 73 and data.protagonist.body.position.x <= 155 and data.protagonist.body.position.x >= 145:
        canvas.create_text((415, 30), text = "build", font = "Arial 15", fill = "white")
        canvas.create_text((415, 45), text = "your", font = "Arial 15", fill = "white")
        canvas.create_text((415, 60), text = "own", font = "Arial 15", fill = "white")
        canvas.create_text((415, 75), text = "path", font = "Arial 15", fill = "white")
        canvas.create_text((415, 90), text = "the", font = "Arial 15", fill = "white")
        canvas.create_text((415, 105), text = "electron", font = "Arial 15", fill = "white")
        canvas.create_text((415, 120), text = "transverse", font = "Arial 15", fill = "white")
        canvas.create_text((415, 135), text = "through", font = "Arial 15", fill = "white")
        canvas.create_text((415, 150), text = "gateways", font = "Arial 15", fill = "white")
        canvas.create_text((415, 165), text = "of", font = "Arial 15", fill = "white")
        canvas.create_text((415, 180), text = "same", font = "Arial 15", fill = "white")
        canvas.create_text((415, 195), text = "color", font = "Arial 15", fill = "white")
    if data.show == True:
        canvas.create_text((650, 200), text = "Disallowed to move", font = "Arial 15", fill = "white")
        canvas.create_text((660, 220), text = "the electron on curve", font = "Arial 15", fill = "white")
        canvas.create_text((660, 240), text = "Press 't' to go back here", font = "Arial 15", fill = "white")
        canvas.create_text((660, 260), text = "for another chance", font = "Arial 15", fill = "white")
    canvas.create_text(570, 500, text = "Destination", font = "Arial 15", fill = "white")
    if data.stage3Win == True:
        canvas.create_text(data.width // 2, data.height // 2, text = "3Q~~", font = "Arial 55", fill = "white")
        canvas.create_text(data.width // 2, data.height // 2 + 70, text = "You have sent the electron", font = "Arial 55", fill = "white")
        canvas.create_text(data.width // 2, data.height // 2 + 140, text = "back home", font = "Arial 55", fill = "white")


def init(data):
    data.controlUp = 0
    data.length = 80
    intropageInit(data)
    introPage(data)
    stage1init(data)
    stage2init(data)
    stage3init(data)
    data.mode = "intropage"
    data.click = 0
    data.leftPosn = [100, 100]
    data.c = True
    data.show = False

def background(canvas, data):
    canvas.create_text(data.width // 2, data.height // 4, text = "Long long time ago, there was an electron far far away",
        font = "Hannotate 30", fill = "white")
    canvas.create_text(data.width // 2, data.height // 4 + 40, text = 
        "And it was separated from its atom!", font = "Hannotate 30", fill = "white")
    canvas.create_text(data.width // 2, data.height // 4 + 80, text = 
        "Let's help it find its home", font = "Hannotate 30", fill = "white")
    canvas.create_text(data.width // 2, data.height // 4 + 120, text = 
        "There will be three levels for you complete", font = "Hannotate 30", fill = "white")
    canvas.create_text(data.width // 2, data.height // 4 + 160, text = 
        "In each of them you will complete different tasks", font = "Hannotate 30", fill = "white")
    canvas.create_text(data.width // 2, data.height // 4 + 200, text = 
        "Press a for instructions on Level 1;", font = "Hannotate 30", fill = "white")
    canvas.create_text(data.width // 2, data.height // 4 + 240, text = 
        "Press b for instructions on Level 2;", font = "Hannotate 30", fill = "white")
    canvas.create_text(data.width // 2, data.height // 4 + 280, text = 
        "Press c for instructions on Level 3", font = "Hannotate 30", fill = "white")
    canvas.create_text(data.width // 2, data.height // 4 + 320, text = 
        "Press 'i' to go back to the homescreen", font = "Hannotate 30", fill = "white")

def ins1(canvas, data):
    canvas.create_text(data.width // 2, data.height // 4, text = "In level 1, your task is to help the electron get to the atom", font = "Hannotate 25", fill = "white")
    canvas.create_text(data.width // 2, data.height // 4 + 40, text = "Press 'Up', 'Right', 'Left', 'Down' to move the electron", font = "Hannotate 25", fill = "white")
    canvas.create_text(data.width // 2, data.height // 4 + 80, text = "You are only allowed to continuously press 'Up' twice", font = "Hannotate 25", fill = "white")
    canvas.create_text(data.width // 2, data.height // 4+ 120, text = "Avoid the lakes!", font = "Hannotate 25", fill = "white")
    canvas.create_text(data.width // 2, data.height // 4 + 160, text = "You have a chance to create TWO bars along the path", font = "Hannotate 25", fill = "white")
    canvas.create_text(data.width // 2, data.height // 4 + 200, text = "Click on the existing bar to replace it", font = "Hannotate 25", fill = "white")
    canvas.create_text(data.width // 2, data.height // 4 + 240, text = "Press 1 to go back to Level 1", font = "Hannotate 25", fill = "white")

def ins2(canvas, data):
    canvas.create_text(data.width // 2, data.height // 4, text = "In level 2, your task is still to help the electron get to the atom", font = "Hannotate 25", fill = "white")
    canvas.create_text(data.width // 2, data.height // 4 + 40, text = "Press 'Up', 'Right', 'Left', 'Down' to move the electron", font = "Hannotate 25", fill = "white")
    canvas.create_text(data.width // 2, data.height // 4 + 80, text = "You are only allowed to continuously press 'Up' twice", font = "Hannotate 25", fill = "white")
    canvas.create_text(data.width // 2, data.height // 4 + 120, text = "You can create THREE balls to control the pulley joints", font = "Hannotate 25", fill = "white")
    canvas.create_text(data.width // 2, data.height // 4 + 160, text = "Press 'r' to delete the ball", font = "Hannotate 25", fill = "white")
    canvas.create_text(data.width // 2, data.height // 4+ 200, text = "Go through the electron shells", font = "Hannotate 25", fill = "white")
    canvas.create_text(data.width // 2, data.height // 4+ 240, text = "Eat the stars to gain power", font = "Hannotate 25", fill = "white")
    canvas.create_text(data.width // 2, data.height // 4 + 280, text = "Press 2 to go back to Level 2", font = "Hannotate 25", fill = "white")

def ins3(canvas, data):
    canvas.create_text(data.width // 2, data.height // 4, text = "In level 3, your task is help the electron gain more power", font = "Hannotate 25", fill = "white")
    canvas.create_text(data.width // 2, data.height // 4+ 40, text = "through eating the stars at the right bottom", font = "Hannotate 25", fill = "white")
    canvas.create_text(data.width // 2, data.height // 4+ 80, text = "as many as possible (>= 10)!", font = "Hannotate 25", fill = "white")
    canvas.create_text(data.width // 2, data.height // 4 + 120, text = "You not only need to move the electron", font = "Hannotate 25", fill = "white")
    canvas.create_text(data.width // 2, data.height // 4 + 160, text = "to pass through gateways", font = "Hannotate 25", fill = "white")
    canvas.create_text(data.width // 2, data.height // 4 + 200, text = "BUT you also need to construct the path (through clicking)!", font = "Hannotate 25", fill = "white")
    #canvas.create_text(data.width // 2, data.height // 4 + 120, text = "You can create THREE balls to control the pulley joints", font = "Hannotate 25", fill = "white")
    canvas.create_text(data.width // 2, data.height // 4 + 240, text = "Press 'd' to delete the last part of the path", font = "Hannotate 25", fill = "white")
    #canvas.create_text(data.width // 2, data.height // 4+ 200, text = "Go through the electron shells", font = "Hannotate 25", fill = "white")
    #canvas.create_text(data.width // 2, data.height // 4+ 160, text = "Eat the stars to gain power,", font = "Hannotate 25", fill = "white")
    canvas.create_text(data.width // 2, data.height // 4 + 280, text = "You have three chances to help the electron eat stars", font = "Hannotate 25", fill = "white")
    canvas.create_text(data.width // 2, data.height // 4 + 320, text = "through pressing 't'", font = "Hannotate 25", fill = "white")
    canvas.create_text(data.width // 2, data.height // 4 + 360, text = "Press 3 to go back to Level 3", font = "Hannotate 25", fill = "white")

def mousePressed(event, data):
    if data.mode == "intropage":
        if distance(event.x, event.y, 200, 200) <= 30:
            data.mode = "stage1"
            stage1Lists(data)
        elif distance(event.x, event.y, 650, 350) <= 30:
            data.mode = "stage2"
            stage2Lists(data)
        elif distance(event.x, event.y, 300, 500) <= 30:
            data.mode = "stage3"
            stage3Lists(data)
        elif distance(event.x, event.y, 550, 120) <= 60:
            data.mode = "explain"
    elif data.mode == "stage1":
        stage1MousePressed(event, data)
    elif data.mode == "stage2":
        stage2MousePressed(event, data)
    elif data.mode == "stage3":
        stage3MousePressed(event, data)

def keyPressed(event, data):
    if event.keysym == "i":
        data.c = not data.c
        data.mode = "intropage"
        clearStage1(data)
        clearStage2(data)
        clearStage3(data)
        init(data)
    elif data.mode == "stage1":
        stage1keyPressed(event, data)
    elif data.mode == "stage2":
        stage2keyPressed(event, data)
    elif data.mode == "stage3":
        stage3keyPressed(event, data)
    if event.keysym == "a":
        data.mode = "ins1"
    elif event.keysym == "1":
        data.mode = "stage1"
    elif event.keysym == "b":
        data.mode = "ins2"
    elif event.keysym == "2":
        data.mode = "stage2"
    elif event.keysym == "c":
        data.mode = "ins3"
    elif event.keysym == "3":
        data.mode = "stage3"
    elif stage3Win == True:
        data.mode = "end"
    if event.keysym == "Right":
        data.click = 0
        data.protagonist.body.apply_impulse_at_local_point(Vec2d(200, 0))
    elif event.keysym == "Up" and data.click < 2:
        data.click += 1
        velocity = math.sqrt(2 * space.gravity.y * 10)
        impulse = 1.5 * data.protagonist.mass * velocity * Vec2d(0, -1)
        data.protagonist.body.apply_impulse_at_local_point(impulse)
    elif event.keysym == "Left":
        data.click = 0
        data.protagonist.body.apply_impulse_at_local_point(Vec2d(-200, 0))
    elif event.keysym == "Down":
        data.click = 0
        data.protagonist.body.apply_impulse_at_local_point(Vec2d(0, 5))

def timerFired(data):
    #data.domino[0].rotation_center_body.position += data.dir * Vec2d(-0.1, 0)
    data.cometCount += 1
    if data.mode == "intropage":
        intropageTimerFired(data)
    elif data.mode == "stage1":
        stage1TimerFired(data)
    elif data.mode == "stage2":
        stage2TimerFired(data)
    elif data.mode == "stage3":
        stage3TimerFired(data)
   
def redrawAll(canvas, data):
    #canvas.create_rectangle(70, 90, 231, 100, fill = rgbString(244, 241, 156), width = 0)
    space.step(1/20.0)
    if data.mode == "intropage":
        introredrawAll(canvas, data)    
    elif data.mode == "stage1":
        stage1redrawAll(canvas, data)
    elif data.mode == "stage2":
        stage2redrawAll(canvas, data)
    elif data.mode == "stage3":
        stage3redrawAll(canvas, data)
    elif data.mode == "explain":
        background(canvas, data)
    elif data.mode == "ins1":
        ins1(canvas, data)
    elif data.mode == "ins2":
        ins2(canvas, data)
    elif data.mode == "ins3":
        ins3(canvas, data)
    elif data.mode == "end":
        canvas.create_text(30, 50, text = "I'd like to thank Prof. Kosbie and ", font = "Arial 25", fill = "white", anchor = NW)
        canvas.create_text(30, 120, text = "my mentor Sanjna for offering my great suggestions and help.", font = "Arial 25", fill = "white", anchor = NW)
        canvas.create_text(30, 190, text = "I'd also like to thank ", font = "Arial 25", fill = "white", anchor = NW)
        canvas.create_text(60, 260, text = "Victor Blomqvist,", font = "Arial 25", fill = "white", anchor = NW)
        canvas.create_text(90, 330, text = "Yue Yao,", font = "Arial 25", fill = "white", anchor = NW)
        canvas.create_text(120, 400, text = "my roommate Lily Du, ", font = "Arial 25", fill = "white", anchor = NW)
        canvas.create_text(150, 470, text = "Matthew Kong, ", font = "Arial 25", fill = "white", anchor = NW)
        canvas.create_text(180, 540, text = "and Mike Yuan", font = "Arial 25", fill = "white", anchor = NW)
        canvas.create_text(210, 610, text = "for their help and support.", font = "Arial 25", fill = "white", anchor = NW)

def setEventInfo(event, data, eventName):
    ctrl  = ((event.state & 0x0004) != 0)
    shift = ((event.state & 0x0001) != 0)    
    msg = ""
    if ctrl:  msg += "ctrl-"
    if shift: msg += "shift-"
    msg += eventName
    msg += " at " + str((event.x, event.y))
    data.info = msg

####################################
# use the run function as-is
####################################
def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        if data.mode == "intropage" or data.mode == "explain":
            canvas.create_rectangle(0, 0, data.width, data.height,
                                fill=rgbString(25, 35, 44), width=0)
        elif data.mode == "stage1" or data.mode == "ins1":
            canvas.create_rectangle(0, 0, data.width, data.height, #114, 157, 140
                                fill=rgbString(114, 157, 140), width=0) #fill=rgbString(9, 28, 22) #151, 190, 172
        elif data.mode == "stage2" or data.mode == "ins2":
            canvas.create_rectangle(0, 0, data.width, data.height,
                                fill=rgbString(207, 167, 193), width=0) #(200, 229, 145)
        elif data.mode == "stage3" or data.mode == "ins3":
            canvas.create_rectangle(0, 0, data.width, data.height,
                                fill=rgbString(203, 169, 125 ), width=0) #121, 110, 106 7, 35, 56 166, 146, 113
        elif data.mode == "end":
            canvas.create_rectangle(0, 0, data.width, data.height,
                                fill=rgbString(0, 0, 0), width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def mouseWrapper(mouseFn, event, canvas, data):
        mouseFn(event, data)
        timerFired(data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 20 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    root.bind("<Button-1>", lambda event:
                            mouseWrapper(leftPressed, event, canvas, data))
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(800, 690)
