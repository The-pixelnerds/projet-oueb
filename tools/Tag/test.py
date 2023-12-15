from TagManager import SimpleTag,DoubleTag

# on test les classes

if __name__ == "__main__":
    print("test de la classe SimpleTag")
    tag = SimpleTag("img")
    tag.addClassTag("test").addClassTag("test2")
    tag.addOther("onclick=\"alert('test')\"")
    print(tag.render())

    print("test de la classe DoubleTag")
    tag = DoubleTag("p")
    tag.addClassTag("test")
    tag.setIdTag("test")
    tag.setContent("test")
    print(tag.render())