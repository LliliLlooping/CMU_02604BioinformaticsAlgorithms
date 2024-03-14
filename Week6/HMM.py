from typing import Dict, Tuple, List
import numpy as np


from typing import Dict


class HMM:
    """
    A class representing a Hidden Markov Model (HMM).
    HMMs are statistical models that assume there is an unobserved (hidden) Markov process that generates an observed sequence of symbols.
    """

    def __init__(self):
        """
        Initializes the HMM instance. Currently, this constructor doesn't initialize any properties.
        """
        pass

    def calculate_path_prob(self, path: str, transition_prob: Dict[str, Dict[str, float]]) -> float:
        """
        Calculates the probability of a given path of states based on the transition probabilities.

        Parameters:
        - path (str): A sequence of states.
        - transition_prob (Dict[str, Dict[str, float]]): A dictionary representing the transition probabilities 
          between states where transition_prob[state1][state2] is the probability of transitioning from state1 to state2.

        Returns:
        - float: The probability of the given path.
        """
        # Initialize with two states of equal probabilities: H, T
        prob = 0.5
        for i in range(1, len(path)):
            # Multiply the current probability by the transition probability from the current state to the next.
            prob *= transition_prob[path[i-1]][path[i]]
        return prob

    def calculate_conditional_prob(self, observed_sequence: str, path: str, emission_prob: Dict[str, Dict[str, float]]) -> float:
        """
        Calculates the probability of an observed sequence given a path of states, based on the emission probabilities.

        Parameters:
        - observed_sequence (str): The observed sequence of symbols.
        - path (str): A sequence of states.
        - emission_prob (Dict[str, Dict[str, float]]): A dictionary representing the emission probabilities where 
          emission_prob[state][symbol] is the probability of emitting a symbol when in a given state.

        Returns:
        - float: The conditional probability of the observed sequence given the path.
        """
        # Initialize the probability with a neutral value.
        prob = 1
        for i in range(len(path)):
            # Multiply the current probability by the emission probability of the observed symbol given the current state.
            prob *= emission_prob[path[i]][observed_sequence[i]]
        return prob

    def _decoding_initialize_matrices(self, num_states: int, len_string: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Initialize the probability and backtrack matrices.

        Parameters:
        - num_states (int): The number of states in the HMM.
        - len_string (int): The length of the observed string.

        Returns:
        - Tuple containing the initialized probability and backtrack matrices.
        """
        prob_matrix = np.zeros((num_states, len_string), dtype=float)
        backtrack_matrix = np.zeros((num_states, len_string), dtype=int)
        return prob_matrix, backtrack_matrix

    def _decoding_initialize_first_column(self, prob_matrix: np.ndarray, emission_prob: Dict[str, Dict[str, float]], string: str, state_list: List[str], num_states: int):
        """
        Initializes the first column of the probability matrix based on the initial emission probabilities.
        """
        for i in range(num_states):
            prob_matrix[i, 0] = emission_prob[state_list[i]
                                              ][string[0]] / num_states

    def _decoding_fill_matrices(self, prob_matrix: np.ndarray, backtrack_matrix: np.ndarray, string: str, emission_prob: Dict[str, Dict[str, float]], transmission_prob: Dict[str, Dict[str, float]], state_list: List[str], num_states: int):
        """
        Fills the probability and backtrack matrices with values according to the Viterbi algorithm.
        """
        len_string = len(string)
        for j in range(1, len_string):
            for i in range(num_states):
                potential_values = [prob_matrix[i_, j-1] * transmission_prob[state_list[i_]]
                                    [state_list[i]] * emission_prob[state_list[i]][string[j]] for i_ in range(num_states)]
                prob_matrix[i, j] = max(potential_values)
                backtrack_matrix[i, j] = np.argmax(potential_values)

    def _decoding_traceback(self, backtrack_matrix: np.ndarray, last_state: int, len_string: int, state_list: List[str]) -> str:
        """
        Performs the traceback through the backtrack matrix to determine the most likely sequence of states.
        """
        hidden_state_idx = [last_state]
        for j in reversed(range(len_string - 1)):
            hidden_state_idx.append(
                backtrack_matrix[hidden_state_idx[-1], j+1])
        hidden_states = ''.join([state_list[idx]
                                for idx in hidden_state_idx[::-1]])
        return hidden_states

    def decoding(self, string: str, emission_prob: Dict[str, Dict[str, float]], transmission_prob: Dict[str, Dict[str, float]]) -> str:
        """
        Decodes the most likely sequence of states for a given observed string using the Viterbi algorithm.
        """
        num_states, len_string = len(transmission_prob), len(string)
        state_list = list(transmission_prob.keys())

        prob_matrix, backtrack_matrix = self._decoding_initialize_matrices(
            num_states, len_string)
        self._decoding_initialize_first_column(
            prob_matrix, emission_prob, string, state_list, num_states)
        self._decoding_fill_matrices(
            prob_matrix, backtrack_matrix, string, emission_prob, transmission_prob, state_list, num_states)

        last_state = np.argmax(prob_matrix[:, len_string - 1])
        return self._decoding_traceback(backtrack_matrix, last_state, len_string, state_list)

    def test(self):
        pass

        # path = 'ABBABAABBABABABBBBBBABABAABBBAABBBBABBABBABAAAABBA'
        # transition_prob = {
        #     'A': {'A': 0.102,
        #           'B': 0.898},
        #     'B': {'A': 0.304,
        #           'B': 0.696}
        # }
        # path_prob = self.calculate_path_prob(path, transition_prob)
        # print(path_prob)

        # path = 'BBAAABBABBBBAABBAABABABAAAABAAAABBBBABABABAABBABBB'
        # emission_prob = {
        #     'A': {'x': 0.399,
        #           'y': 0.161,
        #           'z': 0.44},
        #     'B': {'x': 0.669,
        #           'y': 0.244,
        #           'z': 0.087},
        # }
        # string = 'zyxxzxzyzzzyzyzzyyyyxzyxxxzxyxxxxzxyyzzzxzxzxxyzyy'
        # conditional_prob = self.calculate_conditional_prob(
        #     string, path, emission_prob)
        # print(conditional_prob)

        string = '712666'
        emission_prob = {
            'S': {'1': 0.0,
                  '2': 0.0,
                  '3': 0.0,
                  '4': 0.0,
                  '5': 0.0,
                  '6': 0.0,
                  '7': 1},
            'F': {'1': 1/6,
                  '2': 1/6,
                  '3': 1/6,
                  '4': 1/6,
                  '5': 1/6,
                  '6': 1/6,
                  '7': 0},
            'H': {'1': 1/12,
                  '2': 1/12,
                  '3': 1/12,
                  '4': 1/12,
                  '5': 1/3,
                  '6': 1/3,
                  '7': 0},
            'L': {'1': 1/3,
                  '2': 1/3,
                  '3': 1/12,
                  '4': 1/12,
                  '5': 1/12,
                  '6': 1/12,
                  '7': 0}

        }
        transition_prob = {
            'F': {
                'F': 0.4,
                'H': 0.1,
                'L': 0.5,
                'S': 0
            },
            'H': {
                'F': 0.2,
                'H': 0.6,
                'L': 0.2,
                'S': 0
            },
            'L': {
                'F': 1.0,
                'H': 0.0,
                'L': 0.0,
                'S': 0
            },
            'S': {
                'F': 1.0,
                'H': 0.0,
                'L': 0.0,
                'S': 0.0
            }
        }
        hidden_states = self.decoding(
            string, emission_prob, transition_prob)
        print(hidden_states)
