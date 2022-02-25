from random import randint


def randomize_coords(x1, x2, y1, y2):
    return randint(x1, x2), randint(y1, y2)


class AuctionButtons:
    def search_filter_button_coords(self):
        x1, x2, y1, y2 = 1825, 1901, 134, 158
        return randomize_coords(x1, x2, y1, y2)

    def accept_button_coords(self):
        x1, x2, y1, y2 = 1131, 1222, 472, 498
        return randomize_coords(x1, x2, y1, y2)

    def search_button_coords(self):
        x1, x2, y1, y2 = 1236, 1328, 762, 789
        return randomize_coords(x1, x2, y1, y2)

    def item_one(self):
        x1, x2, y1, y2 = 1040, 1885, 224, 257
        return randomize_coords(x1, x2, y1, y2)

    def bid_buy(self):
        x1, x2, y1, y2 = 1781, 1899, 816, 840
        return randomize_coords(x1, x2, y1, y2)

    def confirm_buy(self):
        x1, x2, y1, y2 = 1359, 1446, 596, 619
        return randomize_coords(x1, x2, y1, y2)

    def T2_coords(self):
        x1, x2, y1, y2 = 1547, 1699, 303, 337
        return randomize_coords(x1, x2, y1, y2)

    def T3_coords(self):
        x1, x2, y1, y2 = 1547, 1699, 214, 245
        return randomize_coords(x1, x2, y1, y2)
