from typing import List, Dict
from dataclasses import dataclass
from colorama import Fore, Style, init

# Ініціалізація Colorama
init(autoreset=True)

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

    Args:
        print_jobs: Список завдань на друк
        constraints: Обмеження принтера

    Returns:
        Dict з порядком друку та загальним часом
    """
    jobs = [PrintJob(**job) for job in print_jobs]
    jobs.sort(key=lambda x: (x.priority, print_jobs.index({"id": x.id, "volume": x.volume, "priority": x.priority, "print_time": x.print_time})))

    print_order = []
    total_time = 0
    current_volume = 0
    current_items = 0
    max_time_in_group = 0

    for job in jobs:
        if (current_volume + job.volume <= constraints["max_volume"] and
            current_items + 1 <= constraints["max_items"]):
            print_order.append(job.id)
            current_volume += job.volume
            current_items += 1
            max_time_in_group = max(max_time_in_group, job.print_time)
        else:
            total_time += max_time_in_group
            current_volume = job.volume
            current_items = 1
            max_time_in_group = job.print_time
            print_order.append(job.id)

    total_time += max_time_in_group

    return {
        "print_order": print_order,
        "total_time": total_time
    }

def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print(Fore.BLUE + "Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(Fore.GREEN + f"Порядок друку: {result1['print_order']}")
    print(Fore.YELLOW + f"Загальний час: {result1['total_time']} хвилин\n")

    print(Fore.BLUE + "Тест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(Fore.GREEN + f"Порядок друку: {result2['print_order']}")
    print(Fore.YELLOW + f"Загальний час: {result2['total_time']} хвилин\n")

    print(Fore.BLUE + "Тест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(Fore.GREEN + f"Порядок друку: {result3['print_order']}")
    print(Fore.YELLOW + f"Загальний час: {result3['total_time']} хвилин")

if __name__ == "__main__":
    test_printing_optimization()
