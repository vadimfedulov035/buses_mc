#!/bin/python

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
    prob[unique] = {}
    for uniq in uniques:
        prob[unique][uniq] = buses[unique][uniq] / totalbuses[unique]

def bus_forecast(nbuses, bus):
    for i in range(nbuses):
        nextbus = np.random.choice( p=prob[bus])
