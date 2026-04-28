from datetime import datetime
from typing import Any

from src.airplane import Airplane
from src.file_handler import JSONSaver


def filter_airplanes(json_saver, filter_words: str | list[str]) -> list[Airplane]:
    """Отбирает данные о самолетах по заданным странам регистрации."""
    criteria = {}
    if filter_words:
        criteria = {"country": filter_words}
    filtered_planes = json_saver.get_airplanes(criteria)
    result = [Airplane(**item) for item in filtered_planes]
    return result


def sort_airplanes(ranged_airplanes) -> Any:
    """Сортирует данные о самолетах по высоте полета (от большего к меньшему)."""
    if not ranged_airplanes:
        print("Нет данных для сортировки.")
        return []
    else:
        sorted_airplanes = sorted(ranged_airplanes, reverse=True)
        return sorted_airplanes


def get_top_airplanes(
    sorted_airplanes: list[dict[str, Any]], top_n: int
) -> list[dict[str, Any]]:
    """Отбирает топ N самолетов."""
    # находим, сколько попало в список, если меньше top_n
    count_planes = len(sorted_airplanes)
    actual_top = min(count_planes, top_n)
    top_airplanes = sorted_airplanes[:actual_top]
    if not top_airplanes:
        print("Нет данных для отображения.")
        return []
    elif count_planes < top_n:
        print(
            f"Найдено всего {count_planes} самолета(ов), что меньше запрошенных {top_n}. Выводим все найденные:"
        )
    else:
        print(f"Выводим топ-{top_n} самолетов:")
    return top_airplanes


def get_top_by_altitude(
    json_saver, alt_range: tuple, top_n: int
) -> list[dict[str, Any]]:
    """Отбирает данные о самолетах по заданному диапазону высоты полета и сортирует их с выводом топ N."""
    criteria = {}
    if alt_range:
        criteria = {"geo_altitude": alt_range}
    ranged_planes = json_saver.get_airplanes(criteria)
    planes = [Airplane(**item) for item in ranged_planes]

    sorted_planes = sort_airplanes(planes)
    result = get_top_airplanes(sorted_planes, top_n)
    return result


def print_airplanes(top_airplanes: list[Airplane]) -> None:
    """Печать данных о самолетах."""
    if not top_airplanes:
        return
    print(
        f"{'ID борта':<15} | {'Позывной рейса':<15} | "
        f"{'Страна регистрации ВС':<30} | {'Высота':<10} | {'Скорость':<10}"
    )
    print("-" * 92)
    for p in top_airplanes:
        print(
            f"{p.icao24:<15} | {p.callsign:<15} | {p.country:<30} | {p.geo_altitude:>10.2f} | {p.velocity:>10.2f}"
        )


def handle_results(planes: list[Airplane], title: str, default_name: str) -> None:
    """Печать таблицы с заголовком или сохранение в файл."""
    if not planes:
        return

    print("\n" + "=" * 75)
    print(f"ОТЧЕТ: {title.upper()}")
    print("=" * 75)

    print(
        "\n1. Показать таблицу | 2. Сохранить в JSON | 3. Оба варианта | 0. Пропустить"
    )
    choice = input("\nВыбор: ").strip()

    if choice in ("1", "3"):
        print_airplanes(planes)
        pass
    if choice in ("2", "3"):
        if not default_name:
            prefix = "results"
        elif isinstance(default_name, list):
            if len(default_name) > 2:  # если передан список стран
                prefix = "_".join(default_name[:2]) + "_and_others"
            else:
                prefix = "_".join(default_name)
        else:
            prefix = str(default_name)  # если передана строка

        prefix = prefix.replace(" ", "_").lower()

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        default_name = f"{prefix}_{timestamp}"

        filename = input(f"\nИмя файла [{default_name}.json]: ").strip() or default_name
        if not filename.endswith(".json"):
            filename += ".json"

        temp_store = JSONSaver(filename)
        # создаем словарь данных об отчете
        report_info = {
            "report_metadata": {
                "title": title,
                "created_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
                "total_count": len(planes),
            }
        }
        # записываем список со словарем, т.к. add_airplane читает файл
        temp_store._save_file([report_info])

        for plane in planes:
            temp_store.add_airplane(plane)
        print(f"\n✅ Отчет '{title}' сохранен в {filename}.")
