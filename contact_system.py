"""
Contact Search System Using Data Structures
- Doubly linked list to store contacts (forward/backward traversal)
- Hash table (dict) for O(1) name lookup
- Substring search (naive) for keyword matching

Run:
  python contact_system.py        # interactive CLI
  python contact_system.py --demo # run demo flow
"""
from dataclasses import dataclass
from typing import Optional, Generator, List
import sys

# ===== Data structures =====

@dataclass
class Contact:
    name: str
    phone: str

class Node:
    def __init__(self, contact: Contact):
        self.contact = contact
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None

class DoublyLinkedList:
    def __init__(self):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self.size = 0

    def append(self, contact: Contact) -> Node:
        node = Node(contact)
        if self.tail is None:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self.size += 1
        return node

    def iter_forward(self) -> Generator[Contact, None, None]:
        cur = self.head
        while cur:
            yield cur.contact
            cur = cur.next

    def iter_backward(self) -> Generator[Contact, None, None]:
        cur = self.tail
        while cur:
            yield cur.contact
            cur = cur.prev

# ===== Utility functions =====

def naive_substring_search(text: str, pattern: str) -> bool:
    """Return True if pattern is a substring of text (case-insensitive)."""
    if pattern == "":
        return True
    t = text.lower()
    p = pattern.lower()
    return p in t

# ===== Contact manager combining structures =====

class ContactManager:
    def __init__(self):
        self.list = DoublyLinkedList()
        # Hash table: store by lowercase name for exact lookup
        self.table = {}  # type: dict[str, Contact]

    def add_contact(self, name: str, phone: str) -> None:
        name = name.strip()
        phone = phone.strip()
        contact = Contact(name=name, phone=phone)
        self.list.append(contact)
        # store exact name (lowercase) -> contact (last added for that name)
        self.table[name.lower()] = contact
        print("Contact added.")

    def find_by_name(self, name: str) -> Optional[Contact]:
        return self.table.get(name.lower())

    def search_by_keyword(self, keyword: str) -> List[Contact]:
        matches: List[Contact] = []
        for c in self.list.iter_forward():
            if naive_substring_search(c.name, keyword):
                matches.append(c)
        return matches

    def all_forward(self) -> List[Contact]:
        return list(self.list.iter_forward())

    def all_backward(self) -> List[Contact]:
        return list(self.list.iter_backward())

# ===== CLI =====

def print_menu():
    print('\nContact Search - Menu')
    print('1. Add Contact')
    print('2. Search by Keyword')
    print('3. Search by Exact Name')
    print('4. View All (Forward)')
    print('5. View All (Backward)')
    print('6. Exit')


def demo_flow(manager: ContactManager):
    print('Running demo...')
    manager.add_contact('Alice', '1234567890')
    manager.add_contact('Bob', '2345678901')
    manager.add_contact('Carol', '3456789012')
    manager.add_contact('Alfred', '4445556666')
    print('\nSearch keyword: Al')
    matches = manager.search_by_keyword('Al')
    for m in matches:
        print(f"Match found: {m.name} - {m.phone}")
    print('\nSearch exact name: Bob')
    exact = manager.find_by_name('Bob')
    if exact:
        print(f"Exact found: {exact.name} - {exact.phone}")
    else:
        print('Exact not found')
    print('\nAll forward:')
    for c in manager.all_forward():
        print(f"  {c.name} - {c.phone}")
    print('\nAll backward:')
    for c in manager.all_backward():
        print(f"  {c.name} - {c.phone}")


def interactive():
    manager = ContactManager()
    # main loop
    while True:
        print_menu()
        try:
            choice = input('\nEnter option: ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\nExiting...')
            break
        if not choice:
            continue
        if choice == '1':
            name = input('Name: ').strip()
            phone = input('Phone: ').strip()
            manager.add_contact(name, phone)
        elif choice == '2':
            kw = input('Search keyword: ').strip()
            matches = manager.search_by_keyword(kw)
            if matches:
                for m in matches:
                    print(f"Match found: {m.name} - {m.phone}")
            else:
                print('No matches found.')
        elif choice == '3':
            name = input('Name: ').strip()
            exact = manager.find_by_name(name)
            if exact:
                print(f"Exact found: {exact.name} - {exact.phone}")
            else:
                print('Not found.')
        elif choice == '4':
            print('\nAll contacts (forward):')
            for c in manager.all_forward():
                print(f"  {c.name} - {c.phone}")
        elif choice == '5':
            print('\nAll contacts (backward):')
            for c in manager.all_backward():
                print(f"  {c.name} - {c.phone}")
        elif choice == '6':
            print('Goodbye.')
            break
        else:
            print('Invalid option, try again.')

if __name__ == '__main__':
    if '--demo' in sys.argv:
        m = ContactManager()
        demo_flow(m)
    else:
        interactive()
