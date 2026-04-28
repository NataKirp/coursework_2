from src.user_input import (get_valid_altitude_range, get_valid_countries,
                            get_valid_int)


def test_get_valid_countries_empty(monkeypatch):
    """Тестирование поведения функции при пустом вводе."""
    monkeypatch.setattr("builtins.input", lambda _: "")
    assert get_valid_countries("Prompt", allow_empty=True) == []


def test_get_valid_countries_format(monkeypatch):
    """Тестирование поведения функции при вводе с пробелами и в разном регистре."""
    monkeypatch.setattr("builtins.input", lambda _: "  russia,  fRaNcE  ")
    assert get_valid_countries("Prompt") == ["Russia", "France"]


def test_get_valid_int_correct_input(monkeypatch):
    """Тестирование поведения функции при корректном вводе."""
    monkeypatch.setattr("builtins.input", lambda _: "2")
    assert get_valid_int("Prompt") == 2


def test_get_valid_int_default_input(monkeypatch):
    """Тестирование поведения функции при пустом вводе (выбор по умолчанию)."""
    monkeypatch.setattr("builtins.input", lambda _: "")
    assert get_valid_int("Prompt") == 5


def test_get_valid_int_incorrect_input(monkeypatch, capsys):
    """Тестирование поведения функции при некорректном вводе (строка, отрицательное число)."""
    inputs = iter(
        ["one", "-1", "1"]
    )  # из-за while true передаем плохие вводы, а в конце хороший, чтобы выйти
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    get_valid_int("Prompt")

    captured = capsys.readouterr()
    assert (
        "❌ Ошибка: введите целое число.\n"
        "❌ Ошибка: число должно быть положительным.\n"
    ) in captured.out


def test_get_valid_altitude_range_empty(monkeypatch):
    """Тестирование поведения функции при пустом вводе."""
    monkeypatch.setattr("builtins.input", lambda _: "")
    assert get_valid_altitude_range("Prompt", allow_empty=True) is None


def test_get_valid_altitude_range_correct_input(monkeypatch):
    """Тестирование поведения функции при корректном вводе."""
    monkeypatch.setattr("builtins.input", lambda _: "5000 - 10000")
    assert get_valid_altitude_range("Prompt", allow_empty=True) == (5000.0, 10000.0)


def test_get_valid_altitude_range_incorrect_input(monkeypatch, capsys):
    """Тестирование поведения функции при некорректном вводе (строка, одно число, первое больше второго)."""
    inputs = iter(
        ["abc", "1000", "5000-1000", "1000-5000"]
    )  # из-за while true передаем плохие вводы, а в конце хороший, чтобы выйти
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    get_valid_altitude_range("Prompt")

    captured = capsys.readouterr()
    assert (
        "❌ Ошибка: введите корректные числовые значения (например, 10000 - 15000).\n"
        "❌ Ошибка: введите корректные числовые значения (например, 10000 - 15000).\n"
        "❌ Ошибка: первое число должно быть меньше второго.\n"
    ) in captured.out
