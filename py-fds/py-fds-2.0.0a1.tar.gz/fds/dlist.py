class _Node:
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next


class DList:
    def __init__(self):
        self.__head = None
        self.__tail = None

    def __str__(self):
        l = "DList : ["
        tmp = self.__head
        while tmp is not None:
            l += str(tmp.data)
            if tmp.next is not None:
                l += " <=> "
            tmp = tmp.next
        return l + "]"

    def __len__(self, value):
        size = 0
        tmp = self.__head
        while tmp is not None:
            tmp = tmp.next
            size += 1
        return size

    def empty(self):
        return self.head == None

    def clear(self):
        while not self.empty():
            ptr = self.__head
            self.__head = self.__head.next
            del ptr
    
    def append(self, data):
        node = _Node(data)
        if self.empty():
            self.__head = self.__tail = node
        else:
            self.__tail.next = node
            self.__tail = node