# Wordle-Solver

## Description

A Python script to find the next optimal word to play + all the potential solutions of your wordle grid.

## Installation

Download the .py and the two .txt files in a single directory.

_You would need to import "multiprocessing" and "timeit" python packages to run the script._

## About the script

* ENGLISH_WORDS_FILE

By modifying this global variable (ENGLISH_WORDS_FILE), you can choose between two sets of english words (word_list.txt or comprehensive_word_list.txt).

I would recommend you to start with word_list.txt, if results are not satisfactory, you can re-run the script with comprehensive_word_list.txt.

_word_list.txt is a list of english words, unfortunately missing a few common ones, computation will be faster._

_comprehensive_word_list.txt is a more comprehensive list, the script will take longer to run._

```sh
ENGLISH_WORDS_FILE = r"word_list.txt"
```

* NB_CPUS

For performance purpose, the script will run simultaneously on several CPU cores.

The number of CPU cores use to run the program is defined with the global variable NB_CPUS.

```sh
NB_CPUS = 16
```
* attempts_list and colors_list 

Simply input your wordle grid details using these two lists.

```sh
 attempts_list = ['train', 'cleat']
 colors_list = ['yxyxx', 'xxggy']
 ```

_The color convention is g for green, y for yellow and x for grey._

Please note that the code will take a long time (potentially hours) to run on empty attempts and colors lists. That being said, doing so, will provide you the optimal opening word of any Wordle grid.

I would recommend you to run the code only after playing (and inputting) your opening word.

## How does it work

The next optimal word to play is the one that will minimize the number of remaining potential solutions after playing it.

The next optimal word to play is chosen among all english words, not only among the potential solutions. 

## Output

In this example (run with above inputs), you may notice that the optimal next words are all the words containing at least 2 letters among d, k and m.
Indeed, after playing one of these words, the number of remaining solutions will always be exactly 1 (given that the current remaining solutions are stead, steak and steam).
On the other hand, if you randomly play one of the current remaining solution (stead, steak or steam), you will have 1/3 chance to win (therefore reducing the number of remaining solutions to 0) and 2/3 chance to end up with exactly 2 remaining solutions after playing..
In average, you are therefore left with in average 4/3 remaining solutions after playing one of the 3 current remaining solutions (stead, steak or steam), which is not optimal.

```sh

-----
display wordle grid:
train
cleat
-----

-----
3 possible solution(s):
steam
stead
steak
-----

-----
computing optimal attempt(s)...
-----

-----
56 optimal attempt(s):
moody
mould
admix
moldy
kodak
dumpy
smack
amend
modal
dusky
smoke
milky
demon
kudzu
odium
drake
demur
murky
medic
monad
knead
media
mound
embed
dream
humid
kombu
model
dummy
midst
datum
idiom
muddy
smoky
drank
vodka
smirk
naked
bedim
dogma
modem
skimp
musky
madam
drama
drunk
karma
amide
demit
drink
admit
midge
medal
nomad
degum
timid
-----

-----
total computation time:
1.62s
-----

Process finished with exit code 0
```

_Please note that on your terminal, the Wordle grid colors should be displayed._
