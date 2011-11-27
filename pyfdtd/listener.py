from field import field

class listener:
    def __init__(self, posX, posY):
        # save attribute
        self.pos = posX, posY

        # create value storage
        self.values = []

    def update(self, field):
        # save value
        self.values.append(field[self.pos])
