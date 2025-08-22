from dataclasses import dataclass, field
from typing import List, Optional
import sys

@dataclass
class Product:
    id: int
    name: float
    price: float
    stock: int = field(default=0)

    def __post_init__(self):
        if not self.name or len(self.name.strip()) < 2:
            raise ValueError('The product name must be at least 2 characters long.')
        if self.price < 0:
            raise ValueError('The product price cannot be negative.')
        if self.stock < 0:
            raise ValueError('The product stock cannote be negative')

class ProductRepository:
    def __init__(self):
        self._items: List[Product] = []
        self._next_id = 1
    
    def _generate_id(self) -> int:
        nid = self._next_id
        self._next_id += 1
        return nid
    
    def create(self, name: str, price: float, stock: int = 0) -> Product:
        p = Product(id=self._generate_id(), name=name.strip(), price=price, stock=stock)
        self._items.append(p)
        return p
    
    def list_all(self) -> List[Product]:
        return list(self._items)
    
    def get_by_id(self, pid: int) -> Optional[Product]:
        return next((p for p in self._items if p.id == pid), None)
    
    def update(self, pid: int, name: Optional[str] = None,
               price: Optional[float] = None, stock: Optional[int] = None) -> Optional[Product]:
        p = self.get_by_id
        if not p:
            return None
        if name is not None:
            if len(name.strip()) < 2:
                raise ValueError('The product name must be at least 2 characters long.')
            p.name = name.strip()
        if price is not None:
            if price < 0:
                raise ValueError('The product price cannot be negative.')
            p.price = price
        if stock is not None:
            if stock <0:
                raise ValueError('The product stock cannote be negative')
            p.stock = stock
        return p
    
    def delete(self, pid: int) -> bool:
        p = self.get_by_id(pid)
        if not p:
            return False
        self._items.remove(p)
        return True
    
def prompt_int(msg:str) -> int:
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print('Enter a valid integer number')

def prompt_float(msg: str) -> float:
    while True:
        try:
            return float(input(msg).replace(',','.'))
        except ValueError:
            print('Enter a number (use docks or comma )')

def create_flow(repo: ProductRepository):
    print('\n== Create Product ==')
    name = input('Name: ').strip()
    price = prompt_float('Preço: ')
    stock = prompt_int ('Estoque: ')
    try:
        p = repo.create(name, price, stock)
        print(f'Create: {p}')
    except ValueError as e:
        print(f'Error: {e}')

def list_flow(repo: ProductRepository):
    print('\n== List products ==')
    items = repo.list_all()
    if not items:
        print('No products registered')
        return
    for p in items:
        print(f'[{p.id}] {p.name} | R$ {p.price:.2f} | estoque: {p.stock}')
    
def get_flow(repo: ProductRepository):
    print('\n== Product details ==')
    pid = prompt_int('ID: ')
    p = repo.get_by_id(pid)
    if p:
        print(p)
    else:
        print('Not found')
    
def update_flow(repo: ProductRepository):
    print('\n== Update Product ==')
    pid = prompt_int('ID: ')
    p = repo.get_by_id(pid)
    if not p:
        print('Not found')
    return

    name = input(f"Novo nome (Enter p/ manter '{p.name}'): ").strip()
    price_str = input(f"Novo preço (Enter p/ manter {p.price}): ").strip()
    stock_str = input(f"Novo estoque (Enter p/ manter {p.stock}): ").strip()

    name_val = p.name if name == "" else name
    price_val = p.price if price_str == "" else float(price_str.replace(",","."))
    stock_val = p.stock if stock_str == "" else int(stock_str)

    try:
        updated = repo.update(pid, name=name_val, price=price_val, stock=stock_val)
        print(f'Updated: {updated}')
    except ValueError as e:
        print(f'Error: {e}')
    
def delete_flow(repo: ProductRepository):
    print('\n== Delete product ==')
    pid = prompt_int('ID: ')
    ok = repo.delete(pid)
    print('Deleted' if ok else 'Not found')

def seed(repo: ProductRepository):
   repo.create('Teclado', 99.9, 10)
   repo.create('Mouse', 59.5, 25)

def main():
    repo = ProductRepository()
 #  seed(repo)
    menu = """
==== Product CRUD ====
1) Create
2) List
3) Show details by ID
4) Update
5) Delete
0) Exit
Choice: """
    actions = {
        "1": lambda: create_flow(repo),
        "2": lambda: list_flow(repo),
        "3": lambda: get_flow(repo),
        "4": lambda: update_flow(repo),
        "5": lambda: delete_flow(repo),
        "0": lambda: sys.exit(0),
    }
    while True:
        choice = input(menu).strip()
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()    