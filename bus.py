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

# append every unique name to uniques
uniques = []
for name in names:
    if name not in uniques:
        uniques.append(name)

# create dict of dicts for counting occurences
buses = {}
for unique in uniques:
    buses[unique] = {}
    for uniq in uniques:
        buses[unique][uniq] = 0

# count every bus occurence after every bus
for i in range(len(names)):
    if i < len(names) - 1:
        buses[names[i]][names[i+1]] += 1
    else:
        buses[names[i]][names[-1]] += 1

# count total number of buses after every bus
totalbuses = {}
for unique in uniques:
    totalbuses[unique] = 0
    for uniq in uniques:
        totalbuses[unique] += buses[unique][uniq]

# calculate probability of every bus occurence after every bus
prob = {}
for unique in uniques:
    prob[unique] = []
    for uniq in uniques:
        prob[unique].append(buses[unique][uniq] / totalbuses[unique])

# create generator for forecasting buses
def bus_forecast(bus):
    while True:
        bus = np.random.choice(uniques, p=prob[bus])
        yield bus

busgen = bus_forecast(np.random.choice(uniques))

while True:
    bus = next(busgen)
    print(f"Подошел автобус {bus}")
    answ = input("Сесть в него? (y/n): ")
    if answ == "y":
        print(f"Вы успешно сели в автобус {bus}!")
        break
    elif answ == "n":
        print("Продолжаем ожидать автобус...")
    else:
        print("Вы не успели сесть в автобус...")
    for i in trange(100):
        sleep(0.1)
