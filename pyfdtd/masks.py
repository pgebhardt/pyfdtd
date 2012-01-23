def ellipse(posx, posy, rx, ry=None):
    """Creates a mask function with circle shape"""
    # set default for ry
    if ry == None:
        ry = rx

    def mask(x, y):
        if (x - posx) ** 2 / rx ** 2 + (y - posy) ** 2 / ry ** 2 <= 1.0:
            return 1.0

        return 0.0

    # return mask function
    return mask
