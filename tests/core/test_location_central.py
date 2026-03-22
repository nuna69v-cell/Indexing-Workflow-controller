from core.location_central import LocationCentral


def test_location_central_init():
    loc_central = LocationCentral()
    assert isinstance(loc_central, LocationCentral)
