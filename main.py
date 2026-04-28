import sys

from src.api import AirplanesAPI

from src.airplane import Airplane
from src.file_handler import JSONSaver
from src.user_input import get_valid_int, get_valid_altitude_range, get_valid_countries
from src.utils import handle_results, filter_airplanes, get_top_by_altitude


def user_interaction():
    """Главная функция: управление выполнением программы."""
    json_saver = JSONSaver()  # инициализируем хранилище
    api = AirplanesAPI()  # Создание экземпляра класса для работы с API сайтов с самолетами
    print("Привет! Добро пожаловать в программу 'Трекер самолетов'.")

    try:
        while True:
            print("\n1. Загрузить новые данные из API")
            print("2. Просмотр / фильтрация данных из базы (JSON)")
            print("3. Удалить самолет из базы по ID борта (ICAO24)")
            print("4. Очистить базу")
            print("0. Выход из программы")

            try:
                choice = input("\nВыберите действие (0-4): ").strip()

                if choice == "0":
                    print("Завершение работы.")
                    break

                elif choice == "1":
                    country_list = get_valid_countries(
                        "Введите название страны, в чьем воздушном пространстве будет производиться поиск: ")
                    if len(country_list) > 1:
                        print(f"Внимание: поиск будет выполнен только по первой стране: {country_list[0]}")
                    country = country_list[0]

                    api.get_airplanes(country)  # Получение информации о самолетах с opensky-network.org
                    planes = Airplane.cast_to_object_list(
                        api.airplanes)  # Преобразование набора данных в список объектов

                    for plane in planes:
                        json_saver.add_airplane(plane)
                    print(f"Все найденные самолеты ({len(planes)} шт.) сохранены в файл.")

                elif choice == "2":
                    load_data = json_saver.get_airplanes({})
                    if not load_data:
                        print("База пуста. Загрузите данные из API.")
                        continue

                    while True:
                        print("\n[Настройка фильтров. Выберите действие (1-2), Enter = пропустить]")
                        print("\n1. По странам регистрации")
                        print("2. По высоте полета (Топ-N)")
                        sub_choice = input("\nВыберите тип: ").strip()

                        if sub_choice == "1":
                            filter_words = get_valid_countries(
                                "\nВведите через запятую названия стран для фильтрации по стране регистрации [Все]: ",
                                True)
                            filtered_planes = filter_airplanes(json_saver, filter_words)
                            title = f"Список самолетов ({', '.join(filter_words) if filter_words else 'Все страны'})"
                            suggested_name = filter_words if filter_words else "all_countries"
                            handle_results(filtered_planes, title, suggested_name)

                        if sub_choice == "2":
                            alt_range = get_valid_altitude_range(
                                "Введите диапазон высот полета (мин - макс) [Все]: ", True)
                            top_n = get_valid_int("Введите количество самолетов для вывода в топ N")

                            top_planes = get_top_by_altitude(json_saver, alt_range, top_n)
                            title = f"Топ-{top_n} по высоте (Диапазон: {alt_range if alt_range else 'Любой'})"
                            suggested_name = f"top_{top_n}_altitude"
                            handle_results(top_planes, title, suggested_name)
                        break

                elif choice == "3":
                    icao_to_delete = input("Введите ID (ICAO24) самолета для удаления: ").strip()
                    if json_saver.delete_airplane(icao_to_delete):
                        print(f"Самолет с ID {icao_to_delete} успешно удален из базы.")
                    else:
                        print(f"Самолет с ID {icao_to_delete} не найден.")
                    continue

                elif choice == "4":
                    confirm = input("Вы уверены, что хотите очистить всю базу? (Да/Нет): ")
                    if confirm.lower() == "да":
                        json_saver.clear_airplanes()
                        print("✅ База данных успешно очищена.")
                    else:
                        print("Отмена очистки.")
                    continue

            except Exception as e:
                print(f"⚠️ Ошибка: {e}\nВозврат в меню...")

    except KeyboardInterrupt:
        print("\nПрограмма остановлена пользователем.")
        sys.exit(0)


if __name__ == "__main__":
    user_interaction()
