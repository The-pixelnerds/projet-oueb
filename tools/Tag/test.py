import Tag
from SimpleTag import SimpleTag 
from DoubleTag import DoubleTag

# on test les classes

tag = SimpleTag("img")
tag.addClassTag("test")
tag.addOther("onclick=\"alert('test')\"")
print(tag.render())

tag = DoubleTag("p")
tag.addClassTag("test")
tag.setIdTag("test")
tag.setContent("test")
print(tag.render())

