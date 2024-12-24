from __future__ import annotations
from dataclasses import dataclass, field
from typing import overload, Self
from collections.abc import Generator


@dataclass 
class Node[T]:
    value: T 
    """The value"""

    next_: Node[T] | None = field(default=None, init=False, repr=True)
    """The Next Node"""

    prev: Node[T] | None = field(default=None, init=False, repr=True)
    """The Previous Node"""

    def __str__(self) -> str: 
        return str(self.value)
    
    def __eq__(self, other: Node) -> bool: 
        return self.value == other.value 
    
    def __ne__(self, other: Node[T]) -> bool:
        return self.value != other.value 
    
    def __gt__(self, other: Node) -> bool:
        return self.value > other.value 
    
    def __lt__(self, other: Node) -> bool:
        return self.value < other.value


class DLinkedList[T]:
    """Double Linked List Implemented at 3 AM"""

    head: Node[T] | None
    tail: Node[T] | None 

    def __init__(self, *values: T) -> None:
        self.tail = None 

        if not values: 
            self.head = None  
            return 
        
        self.head = Node(values[0])
        current = self.head 

        for value in values[1:]:
            node = Node(value)
            node.prev = current
            current.next_ = node 
            current = current.next_ 
        
        self.tail = current 
    
    def append(self, value: T) -> None: 
        """It appends a new element to the Linked List"""
        node = Node(value) 

        if self.head is None: 
            self.head = node 
            return 
        
        current = self.head 

        while current.next_: 
            current = current.next_ 
        
        current.next_ = node 
        node.prev = current
        self.tail = node 

    def remove(self, element: T, repeated: bool = False) -> None: 
        current = self.head 

        if not current: 
            return None 
        
        if current.value == element:

            self.head = current.next_

            if self.head:
                self.head.prev = None

            return None 
        
        while current: 
            if current.value == element: 
                current.prev.next_ = current.next_ # type: ignore
                
                if current.next_:
                    current.next_.prev = current.prev 
                
                if not repeated:
                    return None
            
            current = current.next_ 
    
    def delete(self, index: int) -> None: 
        """It deletes an elemen by Index
        Args:
            index: The index 
        
        Returns:
            It returns None if deletement successfully done,
            otherwise it will raise IndexError

        Raises:
            `IndexError`: The Index given was invalid
        """
        for pos, node in enumerate(self):
            if pos == self._parse_index(index): 
                self.remove(node.value)
                return None
        raise IndexError

    def reverse(self) -> None: 
        current = self.head 
        
        while current:
            temp = current.prev 
            
            current.prev = current.next_
            current.next_ = temp 
            
            
            if current.prev is None: 
                self.head = current 
            
            current = current.prev
        
        return None 
    
    def insert(self, element: T, index: int) -> None: 
        """It inserts an element at the given index, and all the elements are pushed ahead.
        
        Args: 
            element: The value
            index: The Index

        Returns:
            None 

        Examples: 
            l = DLinkedList(1, 2, 3)
            l.insert(1) 
            print(l) # [1, 1, 2, 3]
        """

        for pos, el in enumerate(self):
            if pos == index - 1: 
                new_node = Node(element)
                next_node = el.next_ 
                el.next_ = new_node 
                new_node.prev = el 
                new_node.next_ = next_node
        return None 
    
    def index(self, element: T) -> int:
        """Returns the index of the element given
        
        Arguments:
            element: The element we want to index
        Returns:
            `builtins.int`: The index
        Raises:
            `ValueError`: Element not in the DLinkedList
        
        """
        for pos, node in enumerate(self): 
            if node.value == element: 
                return pos 

        raise ValueError(f"{element!r} not in the DLinkedList")

    def __len__(self) -> int: 
        return sum(1 for _ in self)
    
    def __iter__(self) -> Generator[Node[T], None, None]: 
        current = self.head 
        while current:
            yield current
            current = current.next_ 
    
    def __iadd__(self, other: DLinkedList[T]) -> Self: 
        for node in other: 
            self.append(node.value)
        
        return self
    
    def __add__(self, other: DLinkedList[T]) -> DLinkedList[T]: 
        new_dll = DLinkedList() 

        for node in *self, *other:
            new_dll.append(node.value)

        return new_dll

    def __eq__(self, other: DLinkedList) -> bool: 
        for node1, node2 in zip(self, other):
            if node1 != node2: 
                return False 
            
        return True 
    
    def __reversed__(self) -> DLinkedList[T]: 
        new_dll = DLinkedList() 

        self.reverse() 

        for node in self: 
            new_dll.append(node.value)
        
        self.reverse() 
        return new_dll

    def get(self, index: int) -> Node[T]:
        """Gets an element from the Double Linked List by index (positive)
        
        Args:
            index (int): The Index
        
        Returns:
            T: The Value of the node 
        
        Raises:
            IndexError: Index out of range
        
        """
        parsed_index = self._parse_index(index)

        for pos, node in enumerate(self): 
            if pos == parsed_index: 
                return node
            
        raise IndexError
    
    def _parse_index(self, index: int) -> int | None: 
        """Parse the negative index to positive"""
        if index < -len(self) or index >= len(self): 
            return None

        return index % len(self)

    def _set_value(self, index: int, value: T) -> None: 
        for pos, node in enumerate(self):
            if pos == index:
                node.value = value
                return None

        raise IndexError 
    
    def _slice_handler(self, slice_obj: slice) -> tuple[int, int, int]:
        """It's a helper method to handle the slice object"""
        start, stop, step = slice_obj.start, slice_obj.stop, slice_obj.step 

        if step is None: 
            step = 1 
            
        if step < 0: 
            if start is None and stop is None: 
                start = len(self) - 1
                stop = -1
                
        else: 
            start = [start, 0][start is None]
            stop = [stop, len(self)][stop is None]
    
        return start, stop, step

    @overload 
    def __getitem__(self, index: int) -> Node[T]: ...

    @overload 
    def __getitem__(self, index: slice) -> DLinkedList[T]: ... 

    def __getitem__(self, index: int | slice) -> DLinkedList[T] | Node[T]: 
        if isinstance(index, int): 
            return self.get(index)

        new_dll = DLinkedList() 
        for pos in range(*self._slice_handler(index)):
            try: 
                new_dll.append(self.get(pos).value)
            except IndexError:
                pass 

        return new_dll

    @overload 
    def __setitem__(self, key: int, other: T) -> None: ... 

    @overload 
    def __setitem__(self, key: slice, other: DLinkedList[T]) -> None: ...

    def __setitem__(self, key, other): 
        if isinstance(key, int):
            return self._set_value(key, other)
        
        if isinstance(key, slice): 
            
            range_ = range(*self._slice_handler(key))

            for pos, node in zip(range_, other): 
                self[pos] = node.value
            
        return None 

    def __delitem__(self, key: int | slice) -> None:
        if isinstance(key, int):
            return self.delete(key)
        
        elif isinstance(key, slice): 
            track = {pos: node for pos, node in enumerate(self)}

            for pos in range(*(self._slice_handler(key))):
                try: 
                    if pos in track: 
                        self.remove(track[pos].value)
                except IndexError: 
                    pass 
            return None

    def __contains__(self, element: T) -> bool: 
        for node in self: 
            if node.value == element: 
                return True 
        return False 

    def clear(self) -> None: 
        self.head, self.tail = None, None
        return None 

    def extend(self, other: DLinkedList[T]) -> None: 
        self.__iadd__(other)
        return None 

    def copy(self) -> DLinkedList[T]: 
        """It copies the Doubly Linked List. It calls __copy__ which supports copy library"""
        return self.__copy__()

    def __copy__(self): 
        dll = DLinkedList()
        dll.extend(self)
        return dll 

    def __str__(self) -> str:
        return f"[{f', '.join(f"{node.value!r}" for node in self)}]"
    
    def __repr__(self) -> str: 
        return f"<DLinkedList={str(self)}>"
