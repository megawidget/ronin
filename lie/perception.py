# Copyright (c) 2011 Igor Kaplounenko.
# Licensed under the Open Software License version 3.0.

import logging
import globals
from asp_spa import FOV
from reality import Grid
from objects import Actor

class PTile(object):
    def __init__(self, tile):
        super(PTile, self).__init__()
        self.tile=tile
        self._cover=1
        self._d2=0
        self.was_seen=False
        self.dirty=1
        self.memory=None
    
    def setCover(self,val):
        if self._cover==val:
            return
        self._cover=val
        self.dirty=1
        if(val<1):
            self.was_seen=True
    
    def getCover(self):
        return self._cover

    cover=property(getCover,setCover)

    def setD2(self,val):
        if self._d2==val:
            return
        self._d2=val
        self.dirty=1
    
    def getD2(self):
        return self._d2

    d2=property(getD2,setD2)

    def top(self):
        if not self.was_seen:
            return None
        if self.cover==1:
            return self.memory
        self.memory=self.tile.top()
        return self.memory

class PGrid(Grid):
    def __init__(self, grid, actor):
        super(PGrid, self).__init__(grid.width, grid.height)
        self.grid=[[PTile(grid[i,j]) for j in xrange(grid.height)] for i in xrange(grid.width)]
        self.fov=FOV()
        self.actor=actor

    def calculateFOV(self, radius=None):
        loc=self.actor.parent.loc
        tile=self[loc[0],loc[1]].tile
        me=(loc[0],loc[1],tile.blocksLOS())
        world=[(i,j,self[i,j].tile.blocksLOS()) for i in xrange(self.width) for j in xrange(self.height)]
        ret=self.fov.calculateHexFOV(me,world)
        for r in ret:
            self[r[0][0],r[0][1]].d2=r[2]
            if r[1]>1:
                logging.error(str(me))
                logging.error(str(r))
                raise AssertionError("cover > 1")
            self[r[0][0],r[0][1]].cover=r[1]
        visible_actors=set([tile.top() for tile in self.tiles if tile.cover<1 and isinstance(tile.top(), Actor)])
        for tile in self.tiles:
            if tile.cover==1 and tile.memory in visible_actors:
                tile.memory=None
    
    def examineTile(self, loc):
        objects=None
        if self[loc].cover==1:
            objects=[]
            if self[loc].memory:
                objects.append(self[loc].memory)
            if self[loc].was_seen:
                terrain=self[loc].tile.terrain
                if terrain not in objects:
                    objects.append(self[loc].tile.terrain)
        else:
            objects=self[loc].tile.contents()
        return [(id(obj), obj.getShortDescription(self[loc].cover), obj.getLongDescription(self[loc].cover)) for obj in objects]
