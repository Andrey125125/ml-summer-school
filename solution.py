
import os
import argparse

from PIL import Image, ImageStat


parser = argparse.ArgumentParser()
parser.add_argument('--path', type=str, required=True)
args = parser.parse_args()


class Picture:

    def __init__(self, image):

        self.image = image
        self.filename = image.filename

        stat = ImageStat.Stat(image)
        self.mean = stat.mean
        self.stddev = stat.stddev

    def __eq__(self, other):

        return self.image == other.image

    def is_similar_to(self, other):

        mean_difference = map(lambda x, y: abs(x - y), self.mean, other.mean)
        if all(item < 4.5 for item in mean_difference):
            return True
        std_difference = map(lambda x, y: abs(x - y), self.stddev, other.stddev)
        if all(item < 6.5 for item in mean_difference) and all(item < 5 for item in std_difference):
            return True
        else:
            return False


images = []  # store objects of class Picture here

print('duplicates:')

for file in os.listdir(args.path):
    if file.endswith('.jpg'):
        img = Image.open(args.path + '/' + file)
        img.filename = file
        curr_image = Picture(img)
        if curr_image not in images:
            images.append(curr_image)
        else:
            print(images[images.index(curr_image)].filename + '   ' + curr_image.filename)

print('\n' + 'similar pictures:')

for i in range(len(images)):
    for j in range(i + 1, len(images)):
        if images[i].is_similar_to(images[j]):
            print(images[i].filename + '   ' + images[j].filename)
