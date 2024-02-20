from typing import Dict, Tuple, List
import numpy as np


class ProfileHMMConstructing:

    def __init__(self):
        """
        Initializes the ProfileHMM instance. Currently, this constructor doesn't initialize any properties.
        """
        pass

    def _profile_constructing_find_removal_cols(self, alignments: List[str], threshold: float) -> List[int]:
        """
        Identifies columns in the alignment that should be removed based on a given threshold.

        Parameters:
        - alignments (List[str]): The list of aligned sequences.
        - threshold (float): The threshold for determining if a column should be removed. 
        A column is reserved if the fraction of non-gap characters is at least this threshold.

        Returns:
        - List[int]: A list of indices for columns that are reserved (not removed).
        """
        num_seq, len_seq = len(alignments), len(alignments[0])
        reserved_cols = [i for i in range(
            len_seq) if [seq[i] for seq in alignments].count('-') < threshold * num_seq]
        return reserved_cols

    def _profile_constructing_initialize_matrices(self, state_list, alphabets):
        """
        Initializes the transition and emission matrices for the HMM with all values set to zero.

        Parameters:
        - state_list: A list of the states in the HMM.
        - alphabets: The set of all possible emissions (alphabet).

        Returns:
        - A tuple containing the initialized transition and emission matrices.
        """
        transition_matrix = {last_state: {
            next_state: 0 for next_state in state_list} for last_state in state_list}
        emission_matrix = {
            state: {alphabet: 0 for alphabet in alphabets} for state in state_list}
        return transition_matrix, emission_matrix

    def _profile_constructing_handle_insertions(self, seq, j, reserved_cols, transition_matrix, emission_matrix, last_state, alphabets):
        """
        Handle insertions for a specific position in a sequence.

        Parameters:
        - seq: The sequence being processed.
        - j: The current index in reserved_cols indicating the position to check for insertions.
        - reserved_cols: List of columns reserved based on a threshold, indicating non-gap majority positions.
        - transition_matrix: The HMM transition matrix being updated.
        - emission_matrix: The HMM emission matrix being updated.
        - last_state: The last state in the HMM before processing the current insertion.
        - alphabets: The set of possible alphabets (symbols) in the sequences.

        Returns:
        - last_state: Updated last state after processing insertions.
        """
        start = 0 if j == 0 else reserved_cols[j-1] + 1
        end = reserved_cols[j]
        insertion = list(seq[start:end])
        if len(insertion) - insertion.count('-') > 0:
            transition_matrix[last_state][f'I{j}'] += 1
            transition_matrix[f'I{j}'][f'I{j}'] += len(
                insertion) - insertion.count('-') - 1
            for alphabet in insertion:
                if alphabet != '-':
                    emission_matrix[f'I{j}'][alphabet] += 1
            last_state = f'I{j}'
        return last_state

    def _profile_constructing_update_match_or_deletion(self, seq, col, j, transition_matrix, emission_matrix, last_state):
        """
        Update the matrices for match or deletion states based on the current column.

        Parameters:
        - seq: The sequence being processed.
        - col: The current column index in the sequence.
        - j: The position index used to label the states.
        - transition_matrix: The HMM transition matrix being updated.
        - emission_matrix: The HMM emission matrix being updated.
        - last_state: The last state in the HMM before processing the current column.

        Returns:
        - last_state: Updated last state after processing the current column.
        """
        if seq[col] == '-':
            transition_matrix[last_state][f'D{j+1}'] += 1
            last_state = f'D{j+1}'
        else:
            transition_matrix[last_state][f'M{j+1}'] += 1
            emission_matrix[f'M{j+1}'][seq[col]] += 1
            last_state = f'M{j+1}'
        return last_state

    def _profile_constructing_apply_delta_adjustments(self, transition_matrix, emission_matrix, reserved_cols, delta, alphabets):
        """
        Apply delta adjustments to transition and emission matrices to avoid zero probabilities.

        Parameters:
        - transition_matrix: The HMM transition matrix to adjust.
        - emission_matrix: The HMM emission matrix to adjust.
        - reserved_cols: List of reserved column indices based on a threshold.
        - delta: The adjustment value to be added to probabilities.
        - alphabets: The set of possible alphabets (symbols) in the sequences.
        """
        # Adjust transitions from the start state
        transition_matrix['S']['I0'] += delta
        transition_matrix['S']['M1'] += delta
        transition_matrix['S']['D1'] += delta

        # Adjust transitions for middle states based on reserved columns
        states = {'I': 0, 'M': 1, 'D': 1}
        for j in range(len(reserved_cols)):
            for state, offset in states.items():
                transition_matrix['I' + str(j)][state + str(j+offset)] += delta
        for j in range(1, len(reserved_cols)):
            for state, offset in states.items():
                transition_matrix['M' +
                                  str(j)][state + str(j+offset)] += delta
                transition_matrix['D' +
                                  str(j)][state + str(j+offset)] += delta

        # Adjust transitions for end states
        j = len(reserved_cols)
        transition_matrix['I' + str(j)]['I' + str(j)] += delta
        transition_matrix['I' + str(j)]['E'] += delta
        transition_matrix['M' + str(j)]['I' + str(j)] += delta
        transition_matrix['M' + str(j)]['E'] += delta
        transition_matrix['D' + str(j)]['I' + str(j)] += delta
        transition_matrix['D' + str(j)]['E'] += delta

        # Adjust emission
        for alphabet in alphabets:
            emission_matrix['I0'][alphabet] += delta
        for j in range(len(reserved_cols)):
            for alphabet in alphabets:
                emission_matrix['M' + str(j+1)][alphabet] += delta
                emission_matrix['I' + str(j+1)][alphabet] += delta

    def _profile_constructing_update_matrices(self, seq, reserved_cols, transition_matrix, emission_matrix, alphabets, delta):
        """
        Updates the transition and emission matrices based on a single sequence.

        Parameters:
        - seq: The sequence to update the matrices with.
        - reserved_cols: Columns in the alignment that have been reserved.
        - transition_matrix: The HMM's transition matrix.
        - emission_matrix: The HMM's emission matrix.
        - alphabets: The set of all possible emissions.
        - delta: The pseudo-count to be added for smoothing purposes.

        Returns:
        - None. The function updates the matrices in place.
        """

        last_state = 'S'

        for j, col in enumerate(reserved_cols):
            # Handle insertions before the current column
            last_state = self._profile_constructing_handle_insertions(
                seq, j, reserved_cols, transition_matrix, emission_matrix, last_state, alphabets)
            # Update for match or deletion
            last_state = self._profile_constructing_update_match_or_deletion(
                seq, col, j, transition_matrix, emission_matrix, last_state)

        # Handle transitions to the end state
        transition_matrix[last_state]['E'] += 1

    def _profile_constructing_normalize_matrices(self, transition_matrix, emission_matrix, state_list, alphabets, is_round=False):
        """
        Normalizes the transition and emission matrices so that the sum of probabilities from any state equals 1.

        Parameters:
        - transition_matrix: The HMM's transition matrix to normalize.
        - emission_matrix: The HMM's emission matrix to normalize.
        - state_list: A list of the HMM's states.
        - alphabets: The set of all possible emissions.

        Returns:
        - None. The function updates the matrices in place.
        """
        # Normalize transition matrix
        for state in state_list:
            total = sum(transition_matrix[state].values())
            if total > 0:
                for next_state in state_list:
                    if is_round:
                        transition_matrix[state][next_state] = round(
                            transition_matrix[state][next_state] / total, 3)
                    else:
                        transition_matrix[state][next_state] /= total
        # Normalize emission matrix
        for state in state_list:
            total = sum(emission_matrix[state].values())
            if total > 0:
                for alphabet in alphabets:
                    if is_round:
                        emission_matrix[state][alphabet] = round(
                            emission_matrix[state][alphabet] / total, 3)
                    else:
                        emission_matrix[state][alphabet] /= total

    def construct_profile_hmm(self, threshold, alphabets, alignments, delta):
        """
        Constructs a Profile Hidden Markov Model (HMM) based on input alignments, a threshold for column removal,
        an alphabet of emissions, and a delta for smoothing.

        Parameters:
        - threshold: The threshold used to decide which columns to keep in the alignments.
        - alphabets: The set of all possible emissions.
        - alignments: A list of aligned sequences.
        - delta: The pseudo-count added to transitions and emissions for smoothing.

        Returns:
        - A tuple containing the list of HMM states, and the normalized transition and emission matrices.
        """

        reserved_cols = self._profile_constructing_find_removal_cols(
            alignments, threshold)

        state_list = ['S', 'I0'] + [f'{x}{i}' for i in range(
            1, len(reserved_cols)+1) for x in ['M', 'D', 'I']] + ['E']

        transition_matrix, emission_matrix = self._profile_constructing_initialize_matrices(
            state_list, alphabets)

        for seq in alignments:
            self._profile_constructing_update_matrices(
                seq, reserved_cols, transition_matrix, emission_matrix, alphabets, delta)

        if delta > 0:
            self._profile_constructing_normalize_matrices(
                transition_matrix, emission_matrix, state_list, alphabets)

            # Apply delta adjustments
            self._profile_constructing_apply_delta_adjustments(
                transition_matrix, emission_matrix, reserved_cols, delta, alphabets)

        self._profile_constructing_normalize_matrices(
            transition_matrix, emission_matrix, state_list, alphabets)

        return state_list, transition_matrix, emission_matrix

    def test(self):
        pass

        threshold = 0.304
        delta = 0.01
        alphabets = ['A', 'B', 'C', 'D', 'E']
        with open('alignments.txt', 'r') as file:
            alignments = file.read().split('\n')

        states_list, transition_matrix, emission_matrix = self.construct_profile_hmm(
            threshold, alphabets, alignments, delta)

        with open('output.txt', 'w') as file:
            file.write('\t')
            for i in range(len(states_list) - 1):
                file.write(states_list[i] + '\t')
            file.write(states_list[-1] + '\n')
            for state in states_list:
                file.write(state + '\t')
                for i in range(len(states_list) - 1):
                    next_state = states_list[i]
                    file.write(
                        str(transition_matrix[state][next_state]) + '\t')
                file.write(
                    str(transition_matrix[state][states_list[-1]]) + '\n')

            file.write('--------' + '\n')

            file.write('\t')
            for i in range(len(alphabets) - 1):
                file.write(alphabets[i] + '\t')
            file.write(alphabets[-1] + '\n')
            for state in states_list:
                file.write(state + '\t')
                for i in range(len(alphabets) - 1):
                    alphabet = alphabets[i]
                    file.write(
                        str(emission_matrix[state][alphabet]) + '\t')
                file.write(
                    str(emission_matrix[state][alphabets[-1]]) + '\n')
