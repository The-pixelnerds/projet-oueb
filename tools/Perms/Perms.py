USER_MESSAGE_WRITE = 0b00001 #
USER_ROOM_READ = 0b00010 #
USER_ROOM_CREATE = 0b00100 #
USER_ROOM_DELETE = 0b01000 #
USER_ADMIN = 0b10000 #

ROOM_MESSAGE_WRITE = 0b0001 #
ROOM_READ = 0b0010 #
ROOM_DELETE = 0b0100 #
ROOM_ADMIN = 0b1000 #

class Perms:
    @staticmethod
    def test(permId,permValue):
        return (permId & permValue) > 0

    @staticmethod
    def create(**kwargs):
        id = 0
        for i in kwargs:
            id += i
        return id
    
    @staticmethod
    def gets(permId):
        id = permId
        li = []
        while id > 0:
            for i in range(len(li)):
                li[i] *= 2

            if id%2 == 1:
                li.append(1)
            id = id//2
        return li