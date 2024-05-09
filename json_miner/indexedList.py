class IndexedSubsetList(list):
    '''
    A modified list class to keep track of original indexes after selecting a subset of elements.

    self.original_indices: Shows the initial indexes of the elements mapped. A subset of these elements
                           can be selected using the turn_on method.
    self.binary_flags: Indicates whether an element is selected (1) or not selected (0). This is used to
                       retrieve the subset of the list while retaining the original indexes.
    '''
    def __init__(self, *args, **kwargs):
        # Get arguments if defined. If a string is passed, it is transformed into a list of characters,
        # which is the behavior inherited from the superclass list.
        if args:
            # If actual indexes are passed, they are retained from kwargs; otherwise, index values are
            # initialized based on the length of the sequence provided.
            self.original_indices = kwargs.get('original_indices', list(range(len(args[0]))))

            # binary_flags are used to indicate whether an element is selected (1) or not (0).
            # This helps in retrieving the subset of the list while maintaining the original indexes.
            self.binary_flags = [0] * len(args[0])
        else:
            # Initializing empty lists for original indexes and binary flags when the class is initialized
            # without any input arguments.
            self.original_indices = []
            self.binary_flags = []
        super().__init__(*args)

    def turn_on(self, index):
        '''
        Turn on the binary_flag at the given index, marking the element as selected.
        This flag will be used by other methods to retrieve the subset.
        '''
        self.binary_flags[index] = 1

    def turn_off(self, index):
        '''
        Turn off the binary_flag at the given index, unselecting the element.
        This flag will be used by other methods to retrieve the subset.
        '''
        self.binary_flags[index] = 0

    def get_subset(self):
        '''
        Retrieve the selected elements as a new IndexedSubsetList, preserving their actual indexes.
        '''
        subset = [self[i] for i in range(len(self)) if self.binary_flags[i] == 1]
        original_indices = [self.original_indices[i] for i in range(len(self)) if self.binary_flags[i] == 1]
        return IndexedSubsetList(subset, original_indices=original_indices)

    def get_original_indexes(self, start, end):
        '''
        Get the original indexes that was traced.
        '''
        return self.original_indices[start], self.original_indices[end]
