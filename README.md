# Wordle-Solver
Python script to find all possible solutions and next optimal word to play\
After inputting the details of your current wordle grid, the script will display the above information\
The color convention is: g = green, y = yellow, x = grey\
By modifying ENGLISH_WORDS_PATH, you can chose between two sets of english words (scrabble_words_list.txt or reduced_words_list.txt) to run the script\
scrabble_words_list.txt is the most comprehensive set but takes longer to run\
reduced_words_list.txt is unfortuanetely missing some common names\
You need to import "multiprocessing" package to run the script\
For performance purpose, the script will run simulatenously on the number of CPU cores specified (NB_CPUS)
