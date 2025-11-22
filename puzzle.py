from search import SearchSpace, bfs

class BlockPuzzleSearchSpace(SearchSpace):

    def __init__(self, intervals, cube_width):
        super().__init__()
        self.intervals = intervals
        self.cube_width = cube_width
        self.start_state = ('E',)

    def get_start_state(self):
        """Returns the start state.

        A state of this search space is a sequence of directions. The start state
        contains a single arbitrary initial direction ('E').

        Returns
        -------
        tuple[str]
            The start state
        """
        return self.start_state

    def is_final_state(self, state):
        """Checks whether a given state is a final state.

        To qualify as a final state, the state trajectory should visit all
        positions in a 3x3 cube (without visiting the same position twice).

        Parameters
        ----------
        state : tuple[str]
            A state of the search space, i.e. a sequence of directions

        Returns
        -------
        bool
            True iff the state is a final state
        """
        x = 0
        y = 0
        z = 0
        coordinates = [(x, y, z)]
        map = { "E": (1, 0, 0), "W": (-1, 0, 0), "N": (0, 1, 0), "S": (0, -1, 0), "U": (0, 0, 1), "D": (0, 0, -1) }

        for move in state:
            dx, dy, dz = map[move]
            x, y, z = x + dx, y + dy, z + dz
            coordinates.append((x, y, z))

        if len(coordinates) != len(self.intervals) + 1:  # making sure length matches
            return False

        if len(coordinates) != len(set(coordinates)):  # making sure no coords revisit
            return False

        for (x, y, z) in coordinates:  # making sure within cube bounds
            if not (0 <= x < self.cube_width and 0 <= y < self.cube_width and 0 <= z <
                    self.cube_width):
                return False

        return True


    def get_successors(self, state):
        """Determines the possible successors of a state.

        A state is a sequence of directions. To generate its successor, we append a direction
        that forces the "snake" to make a 90-degree turn along some axis. In other words,
        one cannot append the direction in which the snake is already heading, nor can one
        append the completely opposite direction.

        For instance, if the state is (U, N, W), then we cannot append directions "W" (the
        direction in which the snake is currently going) or "E" (the opposite direction)
        to derive a successor.

        This method also filters out successors that lead to "invalid" states, as determined
        by the .is_valid_state() method.

        Parameters
        ----------
        state : tuple[str]
            A state of the search space, i.e. a sequence of directions

        Returns
        -------
        list[tuple[str]]
            The list of valid successor states.
        """
        if not isinstance(state, tuple):  # check for all tuples (otherwise error happens)
            state = tuple(state)

        map = { "E": (1, 0, 0), "W": (-1, 0, 0), "N": (0, 1, 0), "S": (0, -1, 0), "U": (0, 0, 1), "D": (0, 0, -1) }

        directions = {
            "E": ["U", "N", "S", "D"], "W": ["U", "N", "S", "D"],
            "N": ["E", "W", "U", "D"], "S": ["E", "W", "U", "D"],
            "U": ["E", "W", "N", "S"], "D": ["E", "W", "N", "S"],
        }

        current_structure = []
        prev_direction = state[0]
        count = 1
        for i in range(1, len(state)):
            if state[i] == prev_direction:
                count += 1
            else:
                current_structure.append(count)
                prev_direction = state[i]
                count = 1
        current_structure.append(count)
        curr_piece_len = current_structure[-1]

        if curr_piece_len < self.intervals[len(current_structure)-1]:  # check point
            return [state + (state[-1],)]  # straight

        new_successors = []
        for turn in directions[state[-1]]:
            candidate = state + (turn,)
            x, y, z = 0, 0, 0
            coordinates = [(x, y, z)]
            for move in candidate:
                dx, dy, dz = map[move]
                x, y, z = x + dx, y + dy, z + dz
                coordinates.append((x, y, z))

            if len(coordinates) != len(set(coordinates)):
                continue

            x_vals = [p[0] for p in coordinates]
            y_vals = [p[1] for p in coordinates]
            z_vals = [p[2] for p in coordinates]

            # make sure within cube bounds
            if (max(x_vals) - min(x_vals) < self.cube_width and max(y_vals) - min(
                    y_vals) < self.cube_width and max(z_vals) - min(z_vals) <
                    self.cube_width):
                new_successors.append(candidate)

        return new_successors
 
       

def construct_search_space_for_2x2x2_puzzle():
    return BlockPuzzleSearchSpace(intervals=(1, 1, 1, 1, 1, 1, 1), cube_width=2)


def construct_search_space_for_3x3x3_puzzle():
    return BlockPuzzleSearchSpace(intervals=(2, 2, 2, 2, 1, 1, 1, 2, 2, 1, 1, 2, 1, 2, 1, 1, 2), cube_width=3)


def small_solution():
    space = construct_search_space_for_2x2x2_puzzle()
    return bfs(space)


def puzzle_solution():
    space = construct_search_space_for_3x3x3_puzzle()
    return bfs(space)
