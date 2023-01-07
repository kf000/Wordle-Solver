from timeit import default_timer as timer
from multiprocessing import Pool

NB_CPUS = 16
ENGLISH_WORDS_PATH = r"shorter_words_list.txt"
ENGLISH_WORDS_SET = [line.strip().lower() for line in open(ENGLISH_WORDS_PATH, 'r')]


class Wordle_grid:

    def __init__(self, attempts_list, colors_list):
        # 'x' is grey, 'g' is green, 'y' is yellow
        if len(attempts_list) != len(colors_list):
            raise ValueError
        colors_list = [list(colors) for colors in colors_list].copy()
        for colors in colors_list:
            if len(colors) != 5:
                raise ValueError
            for color in colors:
                if color not in ['x', 'g', 'y']:
                    raise ValueError
        for attempt in attempts_list:
            if len(attempt) != 5:
                raise ValueError
        self.attempts_list = attempts_list
        self.colors_list = colors_list

    def display_wordle_grid(self):
        display = '\033[90m' + '\n' + '-----' + '\n' + "display wordle grid:" + '\n'
        for attempt_index, attempt in enumerate(self.attempts_list):
            for letter_index, letter in enumerate(attempt):
                if self.colors_list[attempt_index][letter_index] == 'g':
                    display += '\033[92m' + letter
                elif self.colors_list[attempt_index][letter_index] == 'y':
                    display += '\033[93m' + letter
                else:
                    display += '\033[90m' + letter
            display += '\033[90m' + '\n'
        display += '-----'
        print(display)

    def analyse_wordle_grid(self):
        # all remaining letters, including confirmed ones
        remaining_letters = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd',
                             'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm']
        # green letters
        green_positions = []
        green_letters = []
        # yellow letters
        yellow_positions = []
        yellow_letters = []
        # potential multiple letters identified
        double_letters = []
        triple_letters = []
        quadruple_letters = []
        quintuple_letters = []
        # letters whose exact number of occurrences has been identified
        strictly_single_letters = []
        strictly_double_letters = []
        strictly_triple_letters = []
        strictly_quadruple_letters = []
        # already identified letters that cannot be place at certain positions
        misplaced_positions = []
        misplaced_letters = []
        for attempt_index, attempt in enumerate(self.attempts_list):
            for letter_index, letter in enumerate(attempt):
                duplicate_letter_index_list = [duplicate_index for duplicate_index, duplicate_letter in
                                               enumerate(attempt) if duplicate_letter == letter]
                duplicate_letter_color_list = [self.colors_list[attempt_index][duplicate_index] for duplicate_index in
                                               duplicate_letter_index_list]
                nb_grey = duplicate_letter_color_list.count('x')
                nb_green = duplicate_letter_color_list.count('g')
                nb_yellow = duplicate_letter_color_list.count('y')
                nb_colored = nb_green + nb_yellow
                if self.colors_list[attempt_index][letter_index] == 'x' and nb_colored == 0 and letter in remaining_letters:
                    remaining_letters.remove(letter)
                if self.colors_list[attempt_index][letter_index] == 'g':
                    green_positions.append(letter_index + 1)
                    green_letters.append(letter)
                if self.colors_list[attempt_index][letter_index] == 'y':
                    yellow_positions.append(letter_index + 1)
                    yellow_letters.append(letter)
                if nb_grey > 0:
                    if nb_colored == 1:
                        if letter not in strictly_single_letters:
                            strictly_single_letters.append(letter)
                    if nb_colored == 2:
                        if letter not in strictly_double_letters:
                            strictly_double_letters.append(letter)
                    if nb_colored == 3:
                        if letter not in strictly_triple_letters:
                            strictly_triple_letters.append(letter)
                    if nb_colored == 4:
                        if letter not in strictly_quadruple_letters:
                            strictly_quadruple_letters.append(letter)
                    if nb_colored > 0:
                        current_misplaced_positions = [misplaced_position + 1 for misplaced_position in
                                                       duplicate_letter_index_list if
                                                       self.colors_list[attempt_index][misplaced_position] == 'x']
                        misplaced_positions += current_misplaced_positions
                        misplaced_letters += [letter for misplaced_position in current_misplaced_positions]
                else:
                    if nb_colored == 2:
                        if letter not in double_letters:
                            double_letters.append(letter)
                    if nb_colored == 3:
                        if letter not in triple_letters:
                            triple_letters.append(letter)
                    if nb_colored == 4:
                        if letter not in quadruple_letters:
                            quadruple_letters.append(letter)
                    if nb_colored == 5:
                        if letter not in quintuple_letters:
                            quintuple_letters.append(letter)
        self.remaining_letters = remaining_letters
        self.green_positions = green_positions
        self.green_letters = green_letters
        self.yellow_positions = yellow_positions
        self.yellow_letters = yellow_letters
        self.double_letters = double_letters
        self.triple_letters = triple_letters
        self.quadruple_letters = quadruple_letters
        self.quintuple_letters = quintuple_letters
        self.strictly_single_letters = strictly_single_letters
        self.strictly_double_letters = strictly_double_letters
        self.strictly_triple_letters = strictly_triple_letters
        self.strictly_quadruple_letters = strictly_quadruple_letters
        self.misplaced_positions = misplaced_positions
        self.misplaced_letters = misplaced_letters

    def get_possible_solutions_wordle_grid(self):
        remaining_letters = self.remaining_letters
        green_positions = self.green_positions
        green_letters = self.green_letters
        yellow_positions = self.yellow_positions
        yellow_letters = self.yellow_letters
        double_letters = self.double_letters
        triple_letters = self.triple_letters
        quadruple_letters = self.quadruple_letters
        quintuple_letters = self.quintuple_letters
        strictly_single_letters = self.strictly_single_letters
        strictly_double_letters = self.strictly_double_letters
        strictly_triple_letters = self.strictly_triple_letters
        strictly_quadruple_letters = self.strictly_quadruple_letters
        misplaced_positions = self.misplaced_positions
        misplaced_letters = self.misplaced_letters
        confirmed_letters = green_letters + yellow_letters
        possible_solutions = []
        for word in ENGLISH_WORDS_SET:
            if any(letter not in word for letter in confirmed_letters):
                valid_solution = False
            elif any(letter not in remaining_letters for letter in word):
                valid_solution = False
            elif any(word[green_positions[green_index] - 1] != green_letter for green_index, green_letter in
                     enumerate(green_letters)):
                valid_solution = False
            elif any(word[yellow_positions[yellow_index] - 1] == yellow_letter for yellow_index, yellow_letter in
                     enumerate(yellow_letters)):
                valid_solution = False
            elif any(word.count(double_letter) < 2 for double_letter in double_letters):
                valid_solution = False
            elif any(word.count(triple_letter) < 3 for triple_letter in triple_letters):
                valid_solution = False
            elif any(word.count(quadruple_letter) < 4 for quadruple_letter in quadruple_letters):
                valid_solution = False
            elif any(word.count(quintuple_letter) < 5 for quintuple_letter in quintuple_letters):
                valid_solution = False
            elif any(word.count(strictly_single_letter) != 1 for strictly_single_letter in strictly_single_letters):
                valid_solution = False
            elif any(word.count(strictly_double_letter) != 2 for strictly_double_letter in strictly_double_letters):
                valid_solution = False
            elif any(word.count(strictly_triple_letter) != 3 for strictly_triple_letter in strictly_triple_letters):
                valid_solution = False
            elif any(word.count(strictly_quadruple_letter) != 4 for strictly_quadruple_letter in
                     strictly_quadruple_letters):
                valid_solution = False
            elif any(word[misplaced_positions[misplaced_index] - 1] == misplaced_letter for
                     misplaced_index, misplaced_letter in enumerate(misplaced_letters)):
                valid_solution = False
            else:
                valid_solution = True
            if valid_solution:
                possible_solutions.append(word)
        self.possible_solutions = possible_solutions

    def display_possible_solutions_wordle_grid(self):
        possible_solutions = self.possible_solutions
        result = '\n' + '-----' + '\n' + str(len(possible_solutions)) + " possible solution(s):"
        for word in possible_solutions:
            result += '\n' + word
        result += '\n' + '-----' + '\n'
        print(result)

    def get_optimal_attempts_wordle_grid(self):
        print('-----' + '\n' + "computing optimal attempt(s):" + '\n' + '-----')
        # alternative to a for loop to run on the 16 cores of the cpu
        with Pool(NB_CPUS) as p:
            tentative_attempt_scores = p.map(self.get_tentative_attempt_score, ENGLISH_WORDS_SET)
        optimal_attempts_indices = [index for index, score in enumerate(tentative_attempt_scores) if
                                    score == min(tentative_attempt_scores)]
        optimal_attempts = [solution for index, solution in enumerate(ENGLISH_WORDS_SET) if
                            index in optimal_attempts_indices]
        self.optimal_attempts = optimal_attempts

    def get_tentative_attempt_score(self, tentative_attempt):
        possible_solutions = self.possible_solutions
        score = 0
        for trial_winning_solution in possible_solutions:
            if tentative_attempt != trial_winning_solution:
                trial_wordle_grid = self.get_trial_wordle_grid(tentative_attempt, trial_winning_solution)
                trial_wordle_grid.analyse_wordle_grid()
                trial_wordle_grid.get_possible_solutions_wordle_grid()
                score += len(trial_wordle_grid.possible_solutions)
        return score

    def display_optimal_attempts_wordle_grid(self):
        optimal_attempts = self.optimal_attempts
        result = '-----' + '\n' + str(len(optimal_attempts)) + " optimal attempt(s):"
        for word in optimal_attempts:
            result += '\n' + word
        result += '\n' + '-----'
        print(result)

    def get_trial_wordle_grid(self, tentative_attempt, trial_winning_solution):
        new_attempts_list = self.attempts_list.copy()
        new_attempts_list.append(tentative_attempt)
        new_colors_list = self.colors_list.copy()
        colors = []
        for letter_index, letter in enumerate(tentative_attempt):
            if letter == trial_winning_solution[letter_index]:
                colors.append('g')
            elif letter in trial_winning_solution:
                colors.append('y')
            else:
                colors.append('x')
        for letter_index, letter in enumerate(tentative_attempt):
            if colors[letter_index] == 'y':
                count_previous_letter = len([previous_letter for previous_letter in tentative_attempt[:letter_index] if
                                             previous_letter == letter])
                count_forward_green_letter = len([forward_letter for forward_letter_index, forward_letter in
                                                  enumerate(tentative_attempt[letter_index:]) if
                                                  forward_letter == letter and colors[
                                                      letter_index + forward_letter_index] == 'g'])
                count_trial_winning_solution_letter = len(
                    [trial_winning_solution_letter for trial_winning_solution_letter in trial_winning_solution if
                     trial_winning_solution_letter == letter])
                if count_previous_letter + count_forward_green_letter >= count_trial_winning_solution_letter:
                    colors[letter_index] = 'x'
        new_colors_list.append(colors)
        trial_wordle_grid = Wordle_grid(new_attempts_list, new_colors_list)
        return trial_wordle_grid


def display_total_computation_time(start, end):
    print('\n' + '-----' + '\n' "total computation time:" + '\n' + str(round(end - start, 2)) + "s" + '\n' + '-----')


def run_wordle_solver(attempts_list, colors_list):
    start = timer()
    grid = Wordle_grid(attempts_list, colors_list)
    grid.display_wordle_grid()
    grid.analyse_wordle_grid()
    grid.get_possible_solutions_wordle_grid()
    grid.display_possible_solutions_wordle_grid()
    grid.get_optimal_attempts_wordle_grid()
    grid.display_optimal_attempts_wordle_grid()
    end = timer()
    display_total_computation_time(start, end)


if __name__ == "__main__":
    attempts_list = ['raise', 'would']
    colors_list = ['xxxxy', 'xyxyx']
    run_wordle_solver(attempts_list, colors_list)
