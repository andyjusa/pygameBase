import functools

import pygame

events = {}
pressedKeys = []
keys = {}
keyUps = {}
colliderList = {}
debugging = False
gameObjects = {}
colliderFun = {}
animManagerList = []


class GameObject:
    def __init__(self, image, position, size, collider, name):
        self.name = name
        self.size = size
        self.image: pygame.surface = image
        self.realImage = pygame.transform.scale(self.image, (
            self.image.get_rect()[2] * size[0], self.image.get_rect()[3] * size[1]))
        self.x = position[0]
        self.y = position[1]
        self.offset = (0, 0)
        if collider:
            colliderList[name] = self.realImage.get_rect()[2:4]
        gameObjects[self.name] = self

    def Moveto(self, x, y):
        self.x = x
        self.y = y

    def Position(self):
        return self.x, self.y

    def Done(self, imsi):
        imsi.blit(self.realImage, tuple(sum(elem) for elem in zip(self.Position(), self.offset)))

    def setImage(self, img):
        self.image = img
        self.realImage = pygame.transform.scale(self.image, (
            self.image.get_rect()[2] * self.size[0], self.image.get_rect()[3] * self.size[1]))

    def setCollider(self, collider):
        colliderList[self.name] = collider


class animOption:
    def __init__(self, timing, num, offset):
        self.timing = timing
        self.num = num
        self.offset = offset


class animManager:
    def __init__(self, targetName, animList, animOptions, animCondition, resourceAddr):
        self.id = 0
        self.timing = 0
        self.targetName = targetName
        self.animList = animList
        self.animOptions = animOptions
        self.animCondition = animCondition
        self.resource = resourceAddr
        self.realAnimList = []
        for i in animList:
            if type(i) is str:
                self.realAnimList.append(tuple(pygame.image.load(f"{resourceAddr}{i}") for a in range(0, 1)))
            else:
                self.realAnimList.append(tuple(pygame.image.load(resourceAddr + elem) for elem in i))
        print(self.realAnimList)
        for i in self.animCondition:
            print(i)
        animManagerList.append(self)

    def Done(self, df):
        for i in range(0, len(self.animCondition)):
            if self.animCondition[i](pressedKeys):
                self.id = i
        self.timing += df
        gameObjects[self.targetName].setImage(self.realAnimList[self.id][
                                                  (self.timing // self.animOptions[self.id].timing) % self.animOptions[
                                                      self.id].num])
        gameObjects[self.targetName].offset = self.animOptions[self.id].offset


def getGameObj(s):
    return gameObjects[s]


def eventDef(event):
    def Deco(func):
        events[event] = func

        def wrap(*args, **kwargs):
            return func(*args, **kwargs)

        return wrap

    return Deco


def colliderDef(event):
    def Deco(func):
        colliderFun[event] = func

        def wrap(*args, **kwargs):
            return func(*args, **kwargs)

        return wrap

    return Deco


def keyDef(keyName):
    def Deco(func):
        keys[keyName] = func

        def wrap(*args, **kwargs):
            return func(*args, **kwargs)

        return wrap

    return Deco


def keyUpDef(keyName):
    def Deco(func):
        keyUps[keyName] = func

        def wrap(*args, **kwargs):
            return func(*args, **kwargs)

        return wrap

    return Deco


@eventDef(pygame.KEYDOWN)
def onKeyDown(event):
    pressedKeys.append(event.key)
    if debugging:
        print(f"KeyDown : keycode.{event.keyDef}")


@eventDef(pygame.KEYUP)
def onKeyUp(event):
    try:
        pressedKeys.remove(event.key)
        keyUps[event.key]()
    except KeyError:
        pass
    except ValueError:
        pass
    if debugging:
        print(f"KeyUp : keycode.{event.keyDef}")


def removeKey(e):
    try:
        pressedKeys.remove(e)
    except ValueError:
        pass


@keyDef(pygame.K_SPACE)
def SpaceKey(event):
    print('hello world')


def loop(lists, screen, df):
    for event in lists:
        try:
            events[event.type](event)
        except KeyError:
            if debugging:
                print(event)

    for i in gameObjects:
        gameObjects[i].Done(screen)

    for i in pressedKeys:
        try:
            keys[i]()
        except KeyError:
            pass

    for i in colliderList.keys():
        for j in colliderList.keys():
            if i != j:
                if check_rec(
                        gameObjects[i].Position(),
                        tuple(sum(elem) for elem in zip(gameObjects[i].Position(), colliderList[i])),
                        gameObjects[j].Position(),
                        tuple(sum(elem) for elem in zip(gameObjects[j].Position(), colliderList[j]))
                ):
                    try:
                        colliderFun[i](j)
                    except KeyError:
                        pass
    for i in animManagerList:
        i.Done(df)


@functools.lru_cache
def getDeltaMove(speed, ddd):
    return ddd * speed / 100


def check_rec(obj1, obj11, obj2, obj22):
    return not (obj11[0] < obj2[0] or obj1[0] > obj22[0] or obj1[1] > obj22[1] or obj11[1] < obj2[1])
