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

