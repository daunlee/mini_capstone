"""
This is not meant to be used directly
as an object, but serves as a abstract parent object for various
state-search-problem representations.

Your search algorithms will use StateNode objects, making them generalizable
for all kinds of problems.
"""
class StateNode:

    """
    A 'static' method that reads data from a text file and returns
    a StateNode which is an initial state.
     """
    def readFromFile(filename):
        raise NotImplementedError

    """
    Creates an state node.
    Takes:
    parent: the preceding StateNode along the path taken to reach the state
            (the initial state's parent should be None)
    path_length: the number of actions taken in the path to reach the state
    path_cost (optional: the cost of the entire path to reach the state

    In any subclass of StateNode, the __init__() should take and store
    additional parameters that define its state.
    Use super.__init__() to call this
    function and set up parent and path_cost
    """
    def __init__(self, parent, path_length, path_cost = 0) :
        self.parent = parent
        self.path_length = path_length
        self.path_cost = path_cost

    """
    Returns a full feature representation of the environment's current state.
    This should be an immutable type - only primitives, strings, and tuples.
    (no lists or objects).
    If two StateNode objects represent the same state,
    get_features() should return the same for both objects.
    Note, however, that two states with identical features
    may have different paths.
    """
    def get_all_features(self) :
        raise NotImplementedError

    """
    Returns True if a goal state.
    """
    def is_goal_state(self) :
        raise NotImplementedError

    """
    Generate and return an iterable (e.g. a list) of all possible neighbor
    states (StateNode objects).
    """
    def generate_next_states(self) :
        raise NotImplementedError

    """
    Return a string representation of the State
    This gets called when str() is used on an Object.
    """
    def __str__(self) :
        raise NotImplementedError


    """
    Returns a string describing the action taken from the parent StateNode
    that results in transitioning to this StateNode
    along the path taken to reach this state.
    (None if the initial state)
    """
    def describe_previous_action(self) :
        raise NotImplementedError


    """
    Returns the parent StateNode, the preceding StateNode
    along the path taken to reach this state.
    (None if the initial state)
    """
    def get_parent(self) :
        return self.parent

    """
    Returns a list of StateNodes on the path from
    the initial state to this state,
    """
    def get_path(self) :
        path = [self]
        s = self.get_parent()
        while s is not None :
            path.append(s)
            s = s.get_parent()
        path.reverse()
        return path

    """
    Returns the length of the entire path (number of
    actions) to reach this state
    """
    def get_path_length(self) :
        return self.path_length

    """
    Returns the cost of the entire path (total cost
    of actions) to reach this state
    """
    def get_path_cost(self) :
        return self.path_cost


    """
    Leave this function alone.
    This is needed to make tuple comparison work with heapq
    (PriorityQueue). However, it doesn't actually
    describe ordering.
    """
    def __lt__(self, other):
        return True

    """
    Leave this function alone;
    This is needed to make StateNode immutable and usable in Sets/Dicts;
    it compares types and get_all_features().
    """
    def __eq__(self, other):
        return (isinstance(other, type(self)) and (self.get_all_features() == other.get_all_features()))

    """
    Leave this function alone;
    This is important to make StateNode hashable and usable in Sets/Dicts;
    it hashes get_all_features().
    """
    def __hash__(self):
        return hash(self.get_all_features())
