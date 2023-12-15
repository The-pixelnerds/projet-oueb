import Tag

class SimpleTag(Tag.Tag):
    def __init__(self, name: str) -> None:
        """
        Initializes a SimpleTag object.

        Parameters:
        name (str): The name of the tag.
        """
        super().__init__()
        self.name: str = name

    def render(self) -> str:
        """
        Renders the SimpleTag object.

        Returns:
        str: The rendered HTML tag.
        """
        return "<" + self.name + self.renderAttributes() + " />"

class DoubleTag(Tag.Tag):
    def __init__(self, name: str) -> None:
        """
        Initializes a DoubleTag object.

        Parameters:
        name (str): The name of the tag.
        """
        super().__init__()
        self.name: str = name
        self.content: str = ""

    def setContent(self, content: str) -> 'DoubleTag':
        """
        Sets the content of the DoubleTag object.

        Parameters:
        content (str): The content of the tag.

        Returns:
        DoubleTag: The DoubleTag object itself.
        """
        self.content = content
        return self

    def render(self) -> str:
        """
        Renders the DoubleTag object.

        Returns:
        str: The rendered HTML tag.
        """
        return "<" + self.name + self.renderAttributes() + ">" + self.content + "</" + self.name + ">"