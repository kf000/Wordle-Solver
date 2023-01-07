# Wordle-Solver
Python script to find all possible solutions and next optimal word to play.\
After inputting your wordle grid details, the script will display the above information.\
The color convention is g for green, y for yellow, x for grey.\
By modifying ENGLISH_WORDS_PATH, you can choose between two sets of english words (scrabble_words_list.txt or reduced_words_list.txt).\
scrabble_words_list.txt is the most comprehensive list, the script will take longer to run.\
reduced_words_list.txt is a shorter list (unfortunately missing a few common names), computation will be faster.\
If results are not satisfactory with the shorter list, you can re-run the script with the comprehensive one.
You need to import "multiprocessing" package to run the script.\
For performance purpose, the script will run simultaneously on the number of CPU cores specified (NB_CPUS).
