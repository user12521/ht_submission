from wrap_app.serializers import SepticSerializer


def test_valid_septic_serializer():
    valid_serializer_data = {
        "address": "123 Main St",
        "zipcode": "12345"
    }
    serializer = SepticSerializer(data=valid_serializer_data)
    assert serializer.is_valid()
    assert serializer.validated_data == valid_serializer_data
    assert serializer.data == valid_serializer_data
    assert serializer.errors == {}


def test_invalid_septic_serializer():
    invalid_serializer_data = {
        "zipcode": "12045",
        "uses_septic": True
    }
    serializer = SepticSerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == invalid_serializer_data
    assert serializer.errors == {"address": ["This field is required."]}
