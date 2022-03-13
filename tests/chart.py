import matplotlib.pyplot as plt
from tqdm import tqdm
import cv2 as cv
import os
import random

root = os.path.dirname(__file__)
main = os.path.join(root, "..")
folder = os.path.realpath("C:/Users/Pumpkin/Documents/TesisPotato/Imagenes/processed/processed/obj")
list = os.listdir(folder)
images = []
valid_images = [".jpg", ".png"] 
for f in tqdm(list):
  ext = os.path.splitext(f)[1]
  if ext.lower() not in valid_images:
      continue
  images.append(f)

fig = plt.figure(figsize=(8, 8))

random_images = random.choices(population = images, k=4)
for i in tqdm(range(len(random_images))):
  img = cv.imread(os.path.join(folder, random_images[i]))
  fig.add_subplot(1, 4, (i + 1))
  plt.imshow(img)
plt.show()
