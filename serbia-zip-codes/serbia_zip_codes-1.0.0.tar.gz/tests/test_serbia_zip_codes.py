import serbia_zip_codes


def test_find_by_city_full_name():
    result = serbia_zip_codes.find_by_city("Loznica")
    assert len(result) == 1


def test_find_by_city_part_name():
    result = serbia_zip_codes.find_by_city("Lozni")
    assert len(result) == 1


def test_find_by_city_ignore_case():
    result = serbia_zip_codes.find_by_city("loznica")
    assert len(result) == 1


def test_find_by_city_no_result():
    result = serbia_zip_codes.find_by_city("qwerty")
    assert len(result) == 0


def test_find_by_city_multy_result():
    result = serbia_zip_codes.find_by_city("beograd")
    assert len(result) == 7


def test_find_by_zip_full_code():
    result = serbia_zip_codes.find_by_zip("15300")
    assert len(result) == 1
    assert result[0]['city'] == "Loznica"


def test_find_by_zip_partcode():
    result = serbia_zip_codes.find_by_zip("1530")
    assert len(result) == 9


def test_find_by_zip_number():
    result = serbia_zip_codes.find_by_zip(15300)
    assert len(result) == 1
    assert result[0]['city'] == "Loznica"


def test_get_all():
    result = serbia_zip_codes.get_all()
    assert len(result) == 1171
