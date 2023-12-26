USER_MESSAGE_WRITE = 0b00001 #
USER_ROOM_READ = 0b00010 #
USER_ROOM_CREATE = 0b00100 #
USER_ROOM_DELETE = 0b01000 #
USER_ADMIN = 0b10000 #

ROOM_MESSAGE_WRITE = 0b00001 #
ROOM_READ = 0b00010 #
ROOM_DELETE = 0b00100 #
ROOM_ADMIN = 0b01000 #
ROOM_MESSAGE_DELETE = 0b10000

class Perms:
    """
    Utility class for handling permissions.
    """

    @staticmethod
    def test(permId: int, permValue: int) -> bool:
        """
        Check if the given permission ID is present in the permission value.

        Args:
            permId (int): The permission ID to check.
            permValue (int): The permission value to check against.

        Returns:
            bool: True if the permission ID is present in the permission value, False otherwise.
        """
        return (permId & permValue) > 0

    @staticmethod
    def create(**kwargs: int) -> int:
        """
        Create a permission value based on the given permission IDs.

        Args:
            **kwargs: Variable number of keyword arguments representing permission IDs.

        Returns:
            int: The permission value created from the given permission IDs.
        """
        id = 0
        for i in kwargs:
            id += i
        return id
    
    @staticmethod
    def gets(permId: int) -> list:
        """
        Get a list of permission IDs from the given permission value.

        Args:
            permId (int): The permission value to extract permission IDs from.

        Returns:
            list: A list of permission IDs extracted from the given permission value.
        """
        id = permId
        li = []
        while id > 0:
            for i in range(len(li)):
                li[i] *= 2

            if id%2 == 1:
                li.append(1)
            id = id//2
        return li