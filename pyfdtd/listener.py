class listener:
    def __init__(self, posX, posY):
        # save attribute
        self.pos = posX, posY

        # create value storage
        self.X, self.Y, self.Z = [], [], []
        self.values = self.X, self.Y, self.Z

    def update(self, field):
        # get value
        x, y, z = field[self.pos]

        # save value
        self.X.append(x)
        self.Y.append(y)
        self.Z.append(z)
