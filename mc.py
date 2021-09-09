#!/bin/python

import numpy as np
from time import sleep
from tqdm import trange

file = open("schedule.txt", "r")

# PARSE ORIGINAL DATASET

# loop through lines, words, chars
name = []
names = []
for line in file:
    words = line.split(', ')
    for word in words:
        for char in word:
            # skip the '\n' on the last line
            if char != '\n':
                # assemble the name char by char
                name.append(char)
        # append joined name to names
        names.append(''.join(name))
        name = []

# TRAIN MARKOV CHAIN

# append every unique name to uniques
uniques = []
for name in names:
    if name not in uniques:
        uniques.append(name)

# create dict of dicts for counting occurences
items = {}
for unique in uniques:
    items[unique] = {}
    for uniq in uniques:
        items[unique][uniq] = 0

# count item occurence after every item
for i in range(len(names)):
    if i < len(names) - 1:
        items[names[i]][names[i+1]] += 1
    else:
        items[names[i]][names[-1]] += 1

# count total number of items after every item
totalitems = {}
for unique in uniques:
    totalitems[unique] = 0
    for uniq in uniques:
        totalitems[unique] += items[unique][uniq]

# calculate probability of item occurence after every item
prob = {}
for unique in uniques:
    prob[unique] = []
    for uniq in uniques:
        prob[unique].append(items[unique][uniq] / totalitems[unique])

# create generator for forecasting items
def item_forecast(item):
    while True:
        item = np.random.choice(uniques, p=prob[item])
        yield item

# FORECAST ITEMS

# initialize generator
itemgen = item_forecast(np.random.choice(uniques))

while True:
    item = next(itemgen)
    print(f"Подошел автобус {item}")
    answ = input("Сесть в него? (y/n): ")
    if answ == "y":
        print(f"Вы успешно сели в автобус {item}!")
        break
    elif answ == "n":
        print("Продолжаем ожидать автобус...")
    else:
        print("Вы не успели сесть в автобус...")
    for i in trange(100):
        sleep(0.1)
