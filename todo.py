import json
from typing import Dict, List, Any
import os
import uuid

data_file: str = "tasks.json"

Task = Dict[str, Any]

prioritty_map: Dict[int, str] = {1: "Низкий", 2: "Средний", 3: "Высокий"}
status_map: Dict[int, str] = {1: "Новая", 2: "В процессе", 3: "Завершена"}

priority_order: Dict[str, int] = {"Низкий": 1, "Средний": 2, "Высокий": 3}
status_order: Dict[str, int] = {"Новая": 1, "В процессе": 2, "Завершена": 3}


def load_tasks() -> Dict[str, Task]:
    if not os.path.exists(data_file):
        return {}
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            data: Dict[str, Task] = json.load(f)
            return {str(k): v for k, v in data.items()}
    except Exception:
        print("Не получилось прочитать tasks.json. Начинаем с пустого")
        return {}


def save_tasks(tasks: Dict[str, Task]) -> None:
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def next_id(tasks: Dict[str, Task]) -> str:
    while True:
        tid = str(uuid.uuid4())[:3]
        if tid not in tasks:
            return tid


def ask_int(message: str, allowed: List[int]) -> int:
    while True:
        raw: str = input(message)
        if raw.isdigit():
            val: int = int(raw)
            if val in allowed:
                return val
        print(f"Ошибка ввода. Введите одно из: {allowed}")


def ask_bool(message: str) -> bool:
    raw: str = input(message + " (y/N):")
    return raw == "y"


def create_task(tasks: Dict[str, Task]) -> None:
    print("\n===Создание задачи===")

    title: str = input("Название: ")
    desc: str = input("Описание: ")

    print("Приоритет: 1 — низкий, 2 — средний, 3 — высокий")
    p: int = ask_int("Ваш выбор: ", [1, 2, 3])

    print("Статус: 1 — новая, 2 — в процессе, 3 — завершена")
    s: int = ask_int("Ваш выбор: ", [1, 2, 3])

    important: bool = ask_bool("Сделать важной?")

    tid: str = next_id(tasks)
    tasks[tid] = {
        "title": title or "(no name)",
        "desc": desc,
        "priority": prioritty_map[p],
        "status": status_map[s],
        "important": important,
    }
    save_tasks(tasks)
    print(f"Готово! Задача создана с id={tid}")


def print_task(task_id: str, task: Task) -> None:
    mark = " ⚠️" if task.get("important") else ""
    print(f"[{task_id}] {task.get('title','')}{mark}")
    print(f"Описание: {task.get('desc','')}")
    print(f"Приоритет: {task.get('priority','')} | Статус: {task.get('status','')}\n")


def show_tasks(tasks: Dict[str, Task]) -> None:
    print("\n===Список задач===")
    if not tasks:
        print("Пусто")
        return
    for tid, t in tasks.items():
        print_task(tid, t)


def show_sorted_status(tasks: Dict[str, Task]) -> None:
    print("\n=== Сортировка по статусу ===")
    if not tasks:
        print("Пока пусто")
        return
    items = sorted(
        tasks.items(), key=lambda kv: status_order.get(kv[1].get("status", ""), 999)
    )
    for tid, t in items:
        print_task(tid, t)


def show_sorted_priority(tasks: Dict[str, Task]) -> None:
    print("\n=== Сортировка по приоритету ===")
    if not tasks:
        print("Пусто")
        return
    items = sorted(
        tasks.items(), key=lambda kv: priority_order.get(kv[1].get("priority", ""), 999)
    )
    for tid, t in items:
        print_task(tid, t)


def show_important(tasks: Dict[str, Task]) -> None:
    print("\n=== Важные задачи ===")
    if not tasks:
        print("Пока пусто")
        return
    found = [(tid, t) for tid, t in tasks.items() if t.get("important")]
    if not found:
        print("Важных задач нет")
    else:
        for tid, t in found:
            print_task(tid, t)


def search_tasks(tasks: Dict[str, Task]) -> None:
    print("\n=== Поиск ===")
    if not tasks:
        print("Пока пусто")
        return
    q = input("Введите слово или фразу: ")
    found = []

    for tid, t in tasks.items():
        title = str(t.get("title", ""))
        desc = str(t.get("desc", ""))
        if q in title or q in desc:
            found.append((tid, t))

    if not found:
        print("Ничего не нашли")
    else:
        for tid, t in found:
            print_task(tid, t)


def update_task(tasks: Dict[str, Task]) -> None:
    print("\n=== Обновление задачи ===")
    if not tasks:
        print("Пусто")
        return
    tid = input("ID задачи: ")
    if tid not in tasks:
        print("Такой задачи нет.")
        return
    while True:
        print("\nЧто поменять?")
        print("1 — Название")
        print("2 — Описание")
        print("3 — Приоритет")
        print("4 — Статус")
        print("0 — Назад")
        choice = ask_int("Ваш выбор: ", [0, 1, 2, 3, 4])
        if choice == 0:
            break
        elif choice == 1:
            tasks[tid]["title"] = input("Новое название: ") or tasks[tid]["title"]
        elif choice == 2:
            tasks[tid]["desc"] = input("Новое описание: ")
        elif choice == 3:
            print("Приоритет: 1 — низкий, 2 — средний, 3 — высокий")
            p = ask_int("Ваш выбор: ", [1, 2, 3])
            tasks[tid]["priority"] = prioritty_map[p]
        elif choice == 4:
            print("Статус: 1 — новая, 2 — в процессе, 3 — завершена")
            s = ask_int("Ваш выбор: ", [1, 2, 3])
            tasks[tid]["status"] = status_map[s]

        save_tasks(tasks)
        print("Сохранено")


def delete_task(tasks: Dict[str, Task]) -> None:
    print("\n=== Удаление задачи ===")
    if not tasks:
        print("Пока пусто")
        return
    tid = input("ID задачи: ")
    if tid not in tasks:
        print("Такой задачи нет")
        return
    ok = input(f"Точно удалить [{tid}]? (y/N): ")

    if ok == "y":
        del tasks[tid]
        save_tasks(tasks)
        print("Удаленно")
    else:
        print("Отмена")


def main() -> None:
    print("=== Мой лист! ===")
    tasks: Dict[str, Task] = load_tasks()

    while True:
        print("\nГлавное меню:")
        print("1 — Создать задачу")
        print("2 — Просмотреть задачи")
        print("3 — Обновить задачу")
        print("4 — Удалить задачу")
        print("0 — Выйти")

        choice = ask_int("Ваш выбор: ", [0, 1, 2, 3, 4])

        if choice == 0:
            print("До встречи на танцполе!")
            break
        elif choice == 1:
            create_task(tasks)
        elif choice == 2:
            while True:
                print("\nПросмотр:")
                print("1 — все")
                print("2 — по статусу")
                print("3 — по приоритету")
                print("4 — поиск")
                print("5 — только важные")
                print("0 — назад")
                c2 = ask_int("Ваш выбор: ", [0, 1, 2, 3, 4, 5])
                if c2 == 0:
                    break
                if c2 == 1:
                    show_tasks(tasks)
                if c2 == 2:
                    show_sorted_status(tasks)
                if c2 == 3:
                    show_sorted_priority(tasks)
                if c2 == 4:
                    search_tasks(tasks)
                if c2 == 5:
                    show_important(tasks)
        elif choice == 3:
            update_task(tasks)
        elif choice == 4:
            delete_task(tasks)


if __name__ == "__main__":
    main()
