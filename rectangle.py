class Rectangle:
    """
    Represents a rectangle with an integer length and width.

    Requirement 1: needs length:int and width:int to be initialized.
    Requirement 2: instances are iterable.
    Requirement 3: iterating yields the length first, in the form
        {'length': <VALUE_OF_LENGTH>}
    followed by the width, in the form
        {'width': <VALUE_OF_WIDTH>}
    """

    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width

    def __iter__(self):
        yield {'length': self.length}
        yield {'width': self.width}


if __name__ == '__main__':
    rect = Rectangle(length=10, width=5)
    for item in rect:
        print(item)
    # Output:
    # {'length': 10}
    # {'width': 5}
