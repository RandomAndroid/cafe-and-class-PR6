# cafe_system.py
from dataclasses import dataclass
from typing import List
import json
from pathlib import Path


@dataclass
class Dish:
    name: str
    price: float
    category: str
    prep_time: int  # в минутах


class CafeSystem:
    def __init__(self, menu_file: str = "menu.json"):
        self.menu_file = menu_file
        self.menu: List[Dish] = []
        self._load_menu()

    def _load_menu(self):
        path = Path(self.menu_file)
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            self.menu = [Dish(**item) for item in data]

    def _save_menu(self):
        data = [d.__dict__ for d in self.menu]
        Path(self.menu_file).write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def add_dish(self, name: str, price: float, category: str, prep_time: int) -> bool:
        """Добавляет блюдо в меню с проверкой входных данных."""
        if not name.strip():
            print(" Название блюда не может быть пустым.")
            return False
        if price <= 0:
            print(" Цена должна быть больше нуля.")
            return False
        if not category.strip():
            print(" Категория не может быть пустой.")
            return False
        if prep_time <= 0:
            print(" Время приготовления должно быть больше нуля (в минутах).")
            return False

        
        if any(d.name.lower() == name.lower() for d in self.menu):
            print(" Блюдо с таким названием уже существует.")
            return False

        self.menu.append(Dish(name.strip(), round(price, 2), category.strip(), int(prep_time)))
        self._save_menu()
        print(f" Блюдо '{name}' успешно добавлено в меню.")
        return True

    def show_menu(self):
        if not self.menu:
            print(" Меню пусто.")
            return
        print("\n Текущее меню:")
        print("-" * 65)
        print(f"{'Название':<20} {'Цена (₽)':<10} {'Категория':<15} {'Время (мин)':<10}")
        print("-" * 65)
        for dish in self.menu:
            print(f"{dish.name:<20} {dish.price:<10.2f} {dish.category:<15} {dish.prep_time:<10}")
        print("-" * 65)


def main():
    cafe = CafeSystem()
    while True:
        print("\n Система кафе:")
        print("1. Добавить блюдо в меню")
        print("2. Показать меню")
        print("3. Выход")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            try:
                name = input(" Название: ")
                price = float(input(" Цена (₽): "))
                category = input(" Категория (напитки, основные, десерты и т.д.): ")
                prep_time = int(input(" Время приготовления (мин): "))
                cafe.add_dish(name, price, category, prep_time)
            except ValueError:
                print(" Ошибка ввода: цена и время должны быть числами.")
        elif choice == "2":
            cafe.show_menu()
        elif choice == "3":
            print(" До свидания!")
            break
        else:
            print(" Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
