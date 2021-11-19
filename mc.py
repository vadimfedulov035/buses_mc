#!/bin/python

import numpy as np
from time import sleep

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

# find uniques
uniques = set(names)

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
        items[names[i]][names[0]] += 1

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
        item = np.random.choice(tuple(uniques), p=prob[item])
        yield item

# FORECAST ITEMS

forecast = True
while forecast:
    itemgen = item_forecast(np.random.choice(tuple(uniques)))
    while True:
        item = next(itemgen)
        print(f"Подош(ел/ла) автобус/троллейбус/маршрутка {item}?")
        answ = input("Предсказание верно? (y/n/q): ")
        if answ == "y":
            print(f"Предсказываю дальше!\n")
        elif answ == "n":
            print("Предсказываю снова...\n")
            break
        elif answ == "q":
            forecast = False
            print("Оканчиваю работу...")
            break
        else:
            print("Не понял вашего ответа\n")
