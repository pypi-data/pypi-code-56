class Heap:

    def __init__(self, min_heap=True, key=None, comp_nodes=None):
        """
        Heap Constructor
        :param min_heap: boolean if its a min heap or not
        :param key: convert the value in the heap node to get a
        comparable(score) like in sorted function
        :param comp_nodes: a custom comparator fuction
        """
        self._heap_arr = []
        self.min = min_heap
        self.length = 0
        if key:
            self._get_node_score = key
        if comp_nodes:
            self.comp_nodes = comp_nodes

    def convert_node_to_representation(self, node):
        """
        A layered function to convert input node given by the user
        to actual heap node representation
        being used in OrderedHeap Currently
        :param node: Original Heap Node
        :return: Representation of Original Node
        """
        return node

    def convert_repr_to_node(self, node):
        """
        Converts the representation back to original node
        :param node: Representation node
        :return: Original Node
        """
        return node

    def comp_nodes(self, a, b):
        """
        This comp function is replace by the user if given
        Return 1 if a < b 0 if a== b else -1 a > b
        :param a: Score of Original Heap Node Given by User
        :param b: Score of Original Heap Node Given by User
        :return: [1,0,-1]

        NOTE : If key parameter in func is not given Score(node) = node
        """
        if a == b:
            return 0
        elif a < b:
            return 1
        return -1

    def _get_node_from_index(self, index):
        """
        Get Representation Node at index
        :param index:
        :return: Representation Node
        """
        if index < 0 or index >= len(self._heap_arr):
            return self.get_end_val()
        if self._heap_arr[index] == self.get_end_val():
            return self._heap_arr[index]
        return self._heap_arr[index]

    def _lte(self, a_index, b_index):
        """
        A comparator function to check if heap node a is less than or equal to
        node b
        :param a_index: Index of node a
        :param b_index: Index of node b
        :return: True,False
        """
        a_node = self._get_node_from_index(a_index)
        b_node = self._get_node_from_index(b_index)

        converted_a_node = self.convert_repr_to_node(a_node)
        converted_b_node = self.convert_repr_to_node(b_node)

        a_val = self._get_node_score(
            converted_a_node) if converted_a_node != self.get_end_val() \
            else self.get_end_val()
        b_val = self._get_node_score(
            converted_b_node) if converted_b_node != self.get_end_val() \
            else self.get_end_val()

        if a_val == self.get_end_val():
            return a_val < 0
        elif b_val == self.get_end_val():
            return 0 < b_val

        return_val = self.comp_nodes(a_val, b_val)
        return return_val == 1 or return_val == 0

    def _get_node_score(self, actual_node):
        """
        Get score from Original Heap Node
        :param actual_node: Original Heap Node
        :return: actual score
        """
        return actual_node

    def _swap(self, a, b):
        """
        swap node at indexes a and b
        :param a: integer
        :param b: integer
        :return: None
        """
        self._heap_arr[a], self._heap_arr[b] = \
            self._heap_arr[b], self._heap_arr[a]

    @classmethod
    def from_array(cls, arr, min_heap=True, key=None, comp_nodes=None):
        """
        Construct a heap from array of nodes. A node can be anything
        :param arr:  List of Nodes
        :param min_heap: whether a min_heap or max_heap to construct
        :param key: optional func to get score
        :param comp_nodes: optional func to get score
        :return:
        """
        heap = cls(min_heap, key, comp_nodes)
        heap.min = min_heap
        for i in arr:
            heap.insert(i)
        return heap

    def insert(self, a):
        """
        insert node in a heap
        :param a: Original Node
        :return:
        """
        a = self.convert_node_to_representation(a)
        # if self.length < len(self._heap_arr):
        #    self._heap_arr[self.length] = a
        # else:
        self._heap_arr.append(a)
        self.length += 1
        self.heapify_up(len(self._heap_arr) - 1)

    def heapify_up(self, node):
        """
        Heapify up a node starting from node
        :param node:
        :return:
        """
        if node <= 0:
            return
        if not self._comp((node - 1) // 2, node):
            self._swap((node - 1) // 2, node)
            self.heapify_up((node - 1) // 2)

    def get_end_val(self):
        """
        Get Maximum Values or Corner values for a heap
        :return:
        """
        if self.min:
            return float("infinity")
        return -float("infinity")

    def _comp(self, a_node_index, b_node_index):
        """
        Compare two heap Nodes and return True a<=b if
        min heap else return b<=a
        :param a_node_index:
        :param b_node_index:
        :return:
        """
        if self.min:
            return self._lte(a_node_index, b_node_index)
        else:
            return self._lte(b_node_index, a_node_index)

    def heapify_down(self, node):
        """
        heapify down a heap node
        :param node:
        :return:
        """
        if node > len(self._heap_arr) - 1:
            return
        self._heap_arr[node] = self.get_end_val()
        left = 2 * node + 1
        right = 2 * node + 2

        if self._comp(right, left):
            if right < len(self._heap_arr):
                self._heap_arr[node] = self._heap_arr[right]
            else:
                self._heap_arr[node] = self.get_end_val()
            self.heapify_down(right)
        else:
            if left < len(self._heap_arr):
                self._heap_arr[node] = self._heap_arr[left]
            else:
                self._heap_arr[node] = self.get_end_val()
            self.heapify_down(left)

    def pop(self):
        """
        pop a node from heap top
        :return: popped node
        """
        self.length -= 1
        temp = self._heap_arr[0]
        self.heapify_down(0)
        return self.convert_repr_to_node(temp)

    def top(self):
        """
        return the node from heap's top
        :return: top node
        """
        return self.convert_repr_to_node(self._heap_arr[0])


class OrderedHeap(Heap):
    """
    This heap is a variation of upper one and maintains the original order of
    insertion.
    """

    def convert_node_to_representation(self, node):
        return [self.length, node]

    def convert_repr_to_node(self, node):
        if node == self.get_end_val():
            return node
        return node[1]

    def _lte(self, a_index, b_index):
        """
        A comparator function to check if heap node a is less than or equal to
        node b
        NOTE : if key is given this function will be called for the calculated
        score calculated according to the key function
        :param a_index: Score of heap node a : if no key then Heap Node a
        :param b_index: Score of heap node b : if no key then Heap Node b
        :return: True,False
        """
        a_node = self._get_node_from_index(a_index)
        b_node = self._get_node_from_index(b_index)

        converted_a_node = self.convert_repr_to_node(a_node)
        converted_b_node = self.convert_repr_to_node(b_node)

        a_val = self._get_node_score(
            converted_a_node) if converted_a_node != self.get_end_val() \
            else self.get_end_val()
        b_val = self._get_node_score(
            converted_b_node) if converted_b_node != self.get_end_val() \
            else self.get_end_val()

        if a_val == self.get_end_val():
            return a_val < 0
        elif b_val == self.get_end_val():
            return 0 < b_val

        return_val = self.comp_nodes(a_val, b_val)
        if return_val == 0:
            if a_node != self.get_end_val() and b_node != self.get_end_val():
                return a_node[0] > b_node[0] if not self.min else a_node[0] < \
                                                                  b_node[0]
        return return_val == 1