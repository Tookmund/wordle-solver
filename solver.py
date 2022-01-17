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

args = parser.parse_args()

if args.exclude is not None:
    reexclude = re.compile("[^"+"".join(args.exclude)+"]+")
    guesses = list(filter(reexclude.fullmatch, guesses))

if args.contains is not None:
    recontains = re.compile("["+"".join(args.contains)+"]+")
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
            print("Invalidate --locate location:", l)
    relocate = re.compile("".join(loclist))
    guesses = list(filter(relocate.fullmatch, guesses))

with open("guesses", "w") as g:
    g.write("\n".join(guesses))

if len(guesses) < 20:
    print("\n".join(guesses))
