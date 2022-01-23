#!/usr/bin/env python3
import re
import argparse
import sys

try:
    guesses = open("guesses")
except FileNotFoundError:
    five = re.compile("^[a-z]{5}$")
    guesses = filter(five.match, open("/usr/share/dict/american-english"))

# Remove last char
guesses = list(map(lambda x: x[:-1], guesses))

parser = argparse.ArgumentParser(description="Solve Wordle for you")
parser.add_argument("-x", "--exclude", action="append")
parser.add_argument("-c", "--contains", action="append")

parser.add_argument("-l", "--locate", nargs=2, action="append")
parser.add_argument("-n", "--not-located", dest="notloc", nargs=2, action="append")

parser.add_argument("-r", "--regex")

args = parser.parse_args()

if args.exclude is not None:
    reexclude = re.compile("[^"+"".join(args.exclude)+"]+")
    guesses = list(filter(reexclude.fullmatch, guesses))

def contains(cl, guesses):
    recstr = ""
    for c in cl:
        recstr += "(?=.*"+c+")"
    recontains = re.compile(recstr)
    return list(filter(recontains.match, guesses))

if args.contains is not None:
    guesses = contains("".join(args.contains), guesses)

def locate(larg, guesses):
    loclist = ["."] * 5
    for l in larg:
        try:
            loc = int(l[0])
            char = l[1]
            loclist[loc-1] = char
        except TypeError:
            print("Invalid locate argument:", l)
        except IndexError:
            print("Invalid locate location:", l)
    relocate = re.compile("".join(loclist))
    return list(filter(relocate.fullmatch, guesses))

if args.locate is not None:
    guesses = locate(args.locate, guesses)

if args.notloc is not None:
    guesses = locate(map(lambda t: (t[0], "[^"+t[1]+"]"), args.notloc), guesses)
    cl = ""
    for l in args.notloc:
        cl += l[1]
    guesses = contains(cl, guesses)

if args.regex is not None:
    reregex = re.compile(args.regex)
    guesses = list(filter(reregex.fullmatch, guesses))

with open("guesses", "w") as g:
    g.write("\n".join(guesses))
    g.write("\n")

freq = []
if len(guesses) == 0:
    print("NO GUESSES???")
    sys.exit(1)
elif len(guesses) == 1:
    print("CERTAIN:", guesses[0])
    sys.exit(0)

for i in range(len(guesses[0])):
    d = {}
    for w in guesses:
        l = w[i]
        if l in d:
            d[l] += 1
        else:
            d[l] = 1
    freq.append(d)

def wordfreq(word):
    score = 0
    existing = []
    for i in range(len(word)):
        l = word[i]
        if l not in existing:
            score += freq[i][l]
            existing.append(l)
    return score

guess = (None, 0)
for g in guesses:
    score = wordfreq(g)
    if score > guess[1]:
        guess = (g, score)

print("GUESS:", guess[0])
