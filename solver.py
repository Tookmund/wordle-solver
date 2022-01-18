#!/usr/bin/env python3
import re
import argparse

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

if args.contains is not None:
    cl = "".join(args.contains)
    recstr = ""
    for c in cl:
        recstr += "(?=.*"+c+")"
    recontains = re.compile(recstr)
    guesses = list(filter(recontains.match, guesses))

if args.locate is not None:
    loclist = ["."] * 5
    for l in args.locate:
        try:
            loc = int(l[0])
            char = l[1]
            loclist[loc-1] = char
        except TypeError:
            print("Invalid --locate argument:", l)
        except IndexError:
            print("Invalid --locate location:", l)
    relocate = re.compile("".join(loclist))
    guesses = list(filter(relocate.fullmatch, guesses))

if args.notloc is not None:
    loclist = ["."] * 5
    for l in args.notloc:
        try:
            loc = int(l[0])
            char = l[1]
            loclist[loc-1] = "[^"+char+"]"
        except TypeError:
            print("Invalid --not-located argument:", l)
        except IndexError:
            print("Invalid --not-located location:", l)
    renotlocate = re.compile("".join(loclist))
    guesses = list(filter(renotlocate.fullmatch, guesses))

if args.regex is not None:
    reregex = re.compile(args.regex)
    guesses = list(filter(reregex.fullmatch, guesses))

with open("guesses", "w") as g:
    g.write("\n".join(guesses))
    g.write("\n")

# Dictionary Frequency Table from Wikipedia
# https://en.wikipedia.org/wiki/Letter_frequency
freq = {
        "a": 	7.8,
        "b":    2,
        "c":    4,
        "d": 	3.8,
        "e": 	11,
        "f": 	1.4,
        "g": 	3,
        "h":    2.3,
        "i":    8.2,
        "j":    0.21,
        "k":    2.5,
        "l":    5.3,
        "m":    2.7,
        "n":    7.2,
        "o":    6.1,
        "p": 	2.8,
        "q":    0.24,
        "r":    7.3,
        "s":    8.7,
        "t":    6.7,
        "u": 	3.3,
        "v":    1,
        "w":    0.91,
        "x":    0.27,
        "y":    1.6,
        "z": 	0.44,
}

def wordfreq(word):
    score = 1
    existing = []
    for l in word:
        if l not in existing:
            score *= freq[l]
            existing.append(l)
    return score

guess = (None, 0)
for g in guesses:
    score = wordfreq(g)
    if score > guess[1]:
        guess = (g, score)

print("GUESS: ", guess[0])
