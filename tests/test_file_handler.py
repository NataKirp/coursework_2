from src.airplane import Airplane


def test_add_airplanes(temp_saver):
    """Тестирование обновления существующих данных (один ICAO24, разные позывной, скорость и высота)."""
    plane_1 = Airplane(
        icao24="a1", callsign="OLD", country="France", geo_altitude=10000, velocity=200
    )
    plane_2 = Airplane(
        icao24="a1", callsign="NEW", country="France", geo_altitude=15000, velocity=400
    )

    temp_saver.add_airplane(plane_1)
    temp_saver.add_airplane(plane_2)

    data = temp_saver.get_airplanes({})
    assert len(data) == 1
    assert data[0]["callsign"] == "NEW"
    assert data[0]["geo_altitude"] == 15000


def test_get_airplanes(temp_saver, sample_planes):
    """Тестирование поиска в файле по критериям."""
    for plane in sample_planes:
        temp_saver.add_airplane(plane)  # добавляем тестовые данные в тестовый файл

    criteria = {"country": ["Russia", "France"]}
    results = temp_saver.get_airplanes(criteria)
    assert len(results) == 2
    assert results[0]["country"] in ["Russia", "France"]

    criteria = {"geo_altitude": (5000, 6000)}
    results = temp_saver.get_airplanes(criteria)
    assert len(results) == 1
    assert results[0]["geo_altitude"] == 5000

    assert len(temp_saver.get_airplanes({})) == 3


def test_delete_airplanes(temp_saver, sample_planes):
    """Тестирование удаления самолета по icao24."""
    for plane in sample_planes:
        temp_saver.add_airplane(plane)

    initial_len = len(sample_planes)
    result = temp_saver.delete_airplane(icao24="a2")
    assert result < initial_len


def test_clear_airplane(temp_saver, sample_planes):
    """Тестирование удаления всех данных из файла."""
    for plane in sample_planes:
        temp_saver.add_airplane(plane)

    result = temp_saver.clear_airplanes()
    assert result is None
