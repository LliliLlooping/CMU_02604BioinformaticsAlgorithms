from typing import Dict, Tuple, List
import numpy as np
from ProfileHMMConstructing import ProfileHMMConstructing


class ProfileHMMDecoding:

    def __init__(self):
        """
        Initializes the ProfileHMM instance. 
        """
        self.profileHmmConstructing = ProfileHMMConstructing()

    def _initialize_states(self, transition_matrix):
        return list(transition_matrix.keys())

    def _initialize_matrices(self, s, transition_matrix, emission_matrix, path):
        """
        Initializes and returns two matrices: a score matrix and a backtrack matrix for dynamic programming.

        This function sets up the initial conditions for dynamic programming by calculating the starting 
        log probabilities for transitions from the start state ('S') to other states ('I0', 'M1', 'D1', etc.) 
        and by initializing the backtrack matrix for path reconstruction. The matrices are populated based on 
        the given transition and emission matrices for a sequence ('path').

        Parameters:
        - s (int): The number of states in the model.
        - transition_matrix (dict): A dictionary representing the transition probabilities between states.
        - emission_matrix (dict): A dictionary representing the emission probabilities from states to sequence characters.
        - path (str): The sequence of observed characters.

        Returns:
        - tuple: A tuple containing the initialized score matrix (numpy array) and backtrack matrix (list of lists).
        """

        # Helper function to calculate log of transition and add emission if provided
        def calc_log(transition_from, transition_to, emission_char=None):
            transition_prob = np.log(
                transition_matrix[transition_from][transition_to])
            if emission_char is not None:
                emission_prob = np.log(
                    emission_matrix[transition_to][emission_char])
                return transition_prob + emission_prob
            return transition_prob

        # Initialize matrix and backtrack structure
        matrix = np.zeros((s * 3 + 1, len(path) + 1), dtype=float)
        backtrack = [[[0, 0]
                      for _ in range(len(path) + 1)] for _ in range(s * 3 + 1)]

        # Initial values for the start state
        matrix[0, 1] = calc_log('S', 'I0', path[0])
        matrix[2, 0] = calc_log('S', 'D1')
        matrix[1, 1] = calc_log('S', 'M1', path[0])

        # Fill in the initial values for the deletion states
        for i in range(1, s):
            matrix[3 * i + 2, 0] = matrix[3 * i - 1, 0] + \
                calc_log(f'D{i}', f'D{i+1}')
            backtrack[3 * i + 2][0] = [3 * i - 1, 0]

        # Set initial transition from I0 and D1
        matrix[2, 1] = matrix[0, 1] + calc_log('I0', 'D1')
        backtrack[2][1] = [0, 1]

        # Loop through states to initialize the rest of the matrix
        for i in range(s):
            if i > 0:
                matrix[i * 3 + 1, 1] = matrix[i * 3 - 1, 0] + \
                    calc_log(f'D{i}', f'M{i+1}', path[0])
                backtrack[i * 3 + 1][1] = [i * 3 - 1, 0]

            matrix[i * 3 + 3, 1] = matrix[i * 3 + 2, 0] + \
                calc_log(f'D{i+1}', f'I{i+1}', path[0])
            backtrack[i * 3 + 3][1] = [i * 3 + 2, 0]

            if i > 0:
                tmp = [calc_log(f'M{i}', f'D{i+1}') + matrix[i * 3 - 2, 1],
                       calc_log(f'D{i}', f'D{i+1}') + matrix[i * 3 - 1, 1],
                       calc_log(f'I{i}', f'D{i+1}') + matrix[i * 3, 1]]
                max_index = np.argmax(tmp)
                matrix[i * 3 + 2, 1] = max(tmp)
                backtrack[i * 3 + 2][1] = [i * 3 - 2 + max_index, 1]

        # Continue with transition probabilities
        for j in range(2, len(path) + 1):
            matrix[0, j] = matrix[0, j - 1] + calc_log('I0', 'I0', path[j - 1])
            backtrack[0][j] = [0, j-1]

        return matrix, backtrack

    def _fill_matrices(self, matrix, backtrack, s, path, transition_matrix, emission_matrix):
        """
        Fills the provided matrices with scores and backtracking pointers based on dynamic programming.

        This function iteratively computes the scores for each cell in the matrix based on the transition and 
        emission probabilities, considering the best path from previous states ('M', 'D', 'I') for each position 
        in the sequence ('path'). It also updates the backtrack matrix to enable path reconstruction.

        Parameters:
        - matrix (np.ndarray): The score matrix to be filled, initially containing zeros.
        - backtrack (list of lists): The backtrack matrix for tracing the optimal path, initially containing zeros.
        - s (int): The number of states in the model.
        - path (str): The sequence of observed characters.
        - transition_matrix (dict): A dictionary representing the transition probabilities between states.
        - emission_matrix (dict): A dictionary representing the emission probabilities from states to sequence characters.

        Returns:
        - None: The function updates the matrix and backtrack in place.
        """

        # Helper function to calculate log probabilities for transitions and emissions
        def calc_log(transition_from, transition_to, emission_char=None):
            transition_prob = np.log(
                transition_matrix[transition_from][transition_to])
            if emission_char is not None:
                emission_prob = np.log(
                    emission_matrix[transition_to][emission_char])
                return transition_prob + emission_prob
            return transition_prob

        # Dynamic programming to fill matrices
        for j in range(2, len(path) + 1):
            # Initial transitions from I0
            matrix[1, j] = matrix[0, j - 1] + \
                calc_log('I0', 'M1', path[j - 1])
            backtrack[1][j] = [0, j - 1]
            matrix[2, j] = matrix[0, j] + calc_log('I0', 'D1')
            backtrack[2][j] = [0, j]

            # Iterate through states to fill in the rest of the matrix
            for i in range(s):
                # Calculate probabilities for transitioning to I states
                tmp = [
                    calc_log(
                        f'M{i+1}', f'I{i+1}', path[j - 1]) + matrix[i * 3 + 1, j - 1],
                    calc_log(
                        f'D{i+1}', f'I{i+1}', path[j - 1]) + matrix[i * 3 + 2, j - 1],
                    calc_log(f'I{i+1}', f'I{i+1}',
                             path[j - 1]) + matrix[i * 3 + 3, j - 1]
                ]
                max_index = np.argmax(tmp)
                matrix[i * 3 + 3, j] = max(tmp)
                backtrack[i * 3 + 3][j] = [i * 3 + 1 + max_index, j - 1]

                if i > 0:
                    # Calculate probabilities for transitioning to M states
                    tmp_m = [
                        calc_log(
                            f'M{i}', f'M{i+1}', path[j - 1]) + matrix[i * 3 - 2, j - 1],
                        calc_log(
                            f'D{i}', f'M{i+1}', path[j - 1]) + matrix[i * 3 - 1, j - 1] + 1e-15,
                        calc_log(
                            f'I{i}', f'M{i+1}', path[j - 1]) + matrix[i * 3, j - 1]
                    ]
                    max_index_m = np.argmax(tmp_m)
                    matrix[i * 3 + 1, j] = max(tmp_m)
                    backtrack[i * 3 + 1][j] = [i * 3 - 2 + max_index_m, j - 1]

                    # Calculate probabilities for transitioning to D states
                    tmp_d = [
                        calc_log(f'M{i}', f'D{i+1}') + matrix[i * 3 - 2, j],
                        calc_log(f'D{i}', f'D{i+1}') +
                        matrix[i * 3 - 1, j],
                        calc_log(f'I{i}', f'D{i+1}') + matrix[i * 3, j]
                    ]
                    max_index_d = np.argmax(tmp_d)
                    matrix[i * 3 + 2, j] = max(tmp_d)
                    backtrack[i * 3 + 2][j] = [i * 3 - 2 + max_index_d, j]

    def _traceback(self, backtrack, states_list, matrix, transition_matrix, s, path):
        """
        Reconstructs the most likely path of states through the matrix using backtracking.

        Starting from the final state determined by the highest probability of transitioning to the end state ('E'),
        this function traces back through the backtrack matrix to reconstruct the sequence of states that led to the 
        most probable path given the observed sequence ('path'). The states list excludes the start and end states 
        for clarity in the output path.

        Parameters:
        - backtrack (list of lists): The backtrack matrix containing pointers for tracing the optimal path.
        - states_list (list): A list of state labels, including the start ('S') and end ('E') states.
        - matrix (np.ndarray): The score matrix containing the dynamic programming scores.
        - transition_matrix (dict): A dictionary representing the transition probabilities between states.
        - s (int): The number of states in the model, not including 'S' and 'E'.
        - path (str): The sequence of observed characters.

        Returns:
        - list: A list of state labels representing the most likely path through the sequence.
        """

        # Helper function to calculate log probabilities for transitions to 'E'
        def calc_log_to_end(state_prefix, state_number):
            return np.log(transition_matrix[f'{state_prefix}{state_number}']['E'])

        # Exclude start 'S' and end 'E' from states list for output construction
        states_list_ = states_list[1:-1]

        # Determine the final state index based on the maximum probability transition to 'E'
        final_state_probs = [
            matrix[s * 3 - 2, len(path)] + calc_log_to_end('M', s),
            matrix[s * 3 - 1, len(path)] + calc_log_to_end('D', s),
            matrix[s * 3, len(path)] + calc_log_to_end('I', s)
        ]
        final_state_idx = s * 3 - 2 + np.argmax(final_state_probs)

        # Initialize traceback from the final state
        bt = [final_state_idx, len(path)]
        output = []

        # Perform traceback until the start of the sequence
        while bt[0] != 0 or bt[1] != 0:
            output.append(states_list_[bt[0]])
            bt = backtrack[bt[0]][bt[1]]

        # Reverse the output to get the correct order of states
        return output[::-1]

    def profile_decoding(self, transition_matrix, emission_matrix, path):

        states_list = self._initialize_states(
            transition_matrix)

        s = (len(states_list) - 3) // 3

        matrix, backtrack = self._initialize_matrices(
            s, transition_matrix, emission_matrix, path)

        self._fill_matrices(matrix, backtrack, s, path,
                            transition_matrix, emission_matrix)
        output = self._traceback(
            backtrack, states_list, matrix, transition_matrix, s, path)

        return output

    def test(self):

        alphabets = ['A', 'B', 'C', 'D', 'E']
        path = 'CCBACCBDEAACEDCAABEDDACACBDCDECAADAEDCCCACBAAAEDB'
        threshold = 0.351
        delta = 0.01
        with open('alignments.txt', 'r') as file:
            alignments = file.read().split('\n')

        _, transition_matrix, emission_matrix = self.profileHmmConstructing.construct_profile_hmm(
            threshold, alphabets, alignments, delta)

        hidden_path = self.profile_decoding(
            transition_matrix, emission_matrix, path)

        output_string = ''
        for h in hidden_path:
            output_string += h + ' '
        print(output_string[:-1])
