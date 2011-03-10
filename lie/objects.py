import abc
import copy
import logging
from exceptions import NotImplementedError

__all__=['Actor', 'Floor', 'Terrain', 'Wall']

class BaseObject(object):
    """All in-game objects should derive from this or one of its children."""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        self.blocks_los=False

class Terrain(BaseObject):
    """A terrain feature."""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, passable_by):
        super(Terrain, self).__init__()
        self.passable_by=passable_by
        self.is_visible=False
        self.was_seen=False
    
    def isPassableBy(self, actor):
        if self.passable_by is None:
            return False
        return isinstance(actor,self.passable_by)

class Floor(Terrain):
    """A floor that can be walked on."""
    def __init__(self):
        super(Floor, self).__init__(Actor)
        self.symbol=u'\u00b7'

class Wall(Terrain):
    """An impassable wall."""
    def __init__(self):
        super(Wall, self).__init__(None)
        self.symbol='#'
        self.blocks_los=True

class Actor(BaseObject):
    """Any object that can act of its own volition."""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        super(Actor, self).__init__()

    def moveToTile(self, tile):
        if(tile.isPassableBy(self)):
            tile.actor=self
            self.parent.actor=None
            self.parent=tile
            return True
        else:
            self.moveBlocked(tile)
            return False
    
    @abc.abstractmethod
    def moveBlocked(self,tile):
        raise NotImplementedError()
    
    def moveN(self):
        return self.moveToOffset(0,-1)
    
    def moveNW(self):
        return self.moveToOffset(-1,-1)

    def moveNE(self):
        return self.moveToOffset(1,-1)
    
    def moveS(self):
        return self.moveToOffset(0,1)

    def moveSW(self):
        return self.moveToOffset(-1,1)

    def moveSE(self):
        return self.moveToOffset(1,1)

    def moveW(self):
        return self.moveToOffset(-1,0)

    def moveE(self):
        return self.moveToOffset(1,0)

    @abc.abstractmethod
    def moveToLocation(self,loc):
        raise NotImplementedError()
    
    def moveToOffset(self,x,y):
        src_tile=self.parent
        assert(src_tile)
        loc=copy.deepcopy(src_tile.location)
        loc.x+=x
        loc.y+=y
        return self.moveToLocation(loc)

    def idle(self):
        return False
