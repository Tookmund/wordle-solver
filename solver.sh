#!/bin/sh

if [ ! -f guesses ]
then
	grep -E '^[a-z]{5}$' /usr/share/dict/american-english > guesses
fi

case $1 in
	x)
		grep -E -v "[$2]+" guesses > guesses.new
		mv guesses.new guesses
		;;
	c)
		grep -E "[$2]+" guesses > guesses.new
		mv guesses.new guesses
		;;
	g)
		grep -E "^$2\$" guesses
		;;
	l)
		grep -E "^$2\$" guesses > guesses.new
		mv guesses.new guesses
esac

LEN=$(wc -l guesses | cut -d ' ' -f 1)
if [ $LEN -le 20 ]
then
	cat guesses
else
	less guesses
fi
