import random

class Bubble:
    def __init__(self, pos, img, speed, depth):
        self.pos = list(pos)
        self.img = img
        self.speed = speed
        self.depth = depth

    def update(self):
        self.pos[0] += self.speed

    def render(self, surf, offset=(0,0)):
        render_pos = (self.pos[0] - offset[0] * self.depth, self.pos[1] - offset[1] * self.depth)
        surf.blit(self.img, (render_pos[0] % (surf.get_width() + self.img.get_width()) - self.img.get_width(), render_pos[1] % (surf.get_height() + self.img.get_height() - self.img.get_height())))


class Bubbles:
    def __init__(self, bubble_images, count=30):
        self.bubbles = []

        for i in range(count):
            self.bubbles.append(Bubble((random.random() * 99999, random.random() * 99999), random.choice(bubble_images), random.random() * 0.05 + 0.05, random.random() * 0.6 + 0.2))


        self.bubbles.sort(key=lambda x: x.depth)


    def update(self):
        for bubble in self.bubbles:
            bubble.update()

    def render(self, surf, offset=(0,0)):
        for bubble in self.bubbles:
            bubble.render(surf, offset=offset)                        