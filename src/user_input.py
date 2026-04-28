import re
from typing import Optional


def get_valid_countries(prompt: str, allow_empty: bool = False) -> str | list[str]:
    """
    Запрашивает страну (страны), проверяет на латиницу и форматирует регистр.

    Если allow_empty=True, Enter вернет пустой список.
    """
    while True:
        words_input = input(prompt)
        if not words_input and allow_empty:
            return []
        # разбиваем строку на список слов (запятая обязательный разделитель, чтобы учесть United States)
        countries = [word.strip() for word in words_input.split(",") if word.strip()]

        if not countries and not allow_empty:
            print("❌ Ошибка: список пуст. Введите названия стран через запятую.")
            continue
        # разрешаем буквы (A-Z) и пробелы внутри названий
        if all(re.fullmatch(r"[A-Za-z\s]+", c) for c in countries):
            return [c.title() for c in countries]

        print("❌ Ошибка: используйте только английские буквы.")


def get_valid_int(prompt: str, default: int = 5) -> int:
    """Запрашивает целое положительное число."""
    while True:
        value_input = input(f"{prompt} [Enter для {default}]: ").strip()
        if not value_input:
            return default
        try:
            value = int(value_input)
            if value < 0:
                print("❌ Ошибка: число должно быть положительным.")
                continue
            return value
        except ValueError:
            print("❌ Ошибка: введите целое число.")


def get_valid_altitude_range(
    prompt: str, allow_empty: bool = False
) -> Optional[tuple[float, float]]:
    """
    Запрашивает диапазон высот и возвращает кортеж (min_alt, max_alt).

    Enter вернет None (фильтр не применится).
    """
    while True:
        range_input = input(prompt).strip()
        if not range_input and allow_empty:
            return None
        parts = re.split(
            r"[-,\s]+", range_input
        )  # режем строку (пробелы, запятые, дефисы)
        parts = list(
            filter(None, parts)
        )  # чистим от пустых строк (если введено несколько разделителей подряд

        try:
            if len(parts) != 2:
                raise ValueError("❌ Ошибка: введите два числа через разделитель.")

            min_alt = float(parts[0])
            max_alt = float(parts[1])

            if min_alt > max_alt:
                print("❌ Ошибка: первое число должно быть меньше второго.")
                continue

            return min_alt, max_alt

        except ValueError:
            print(
                "❌ Ошибка: введите корректные числовые значения (например, 10000 - 15000)."
            )
