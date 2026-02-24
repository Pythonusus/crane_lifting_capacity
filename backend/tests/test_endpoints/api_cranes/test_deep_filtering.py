from app.schemas.cranes import CraneFilterRequest, CraneListResponse


def test_valid_values(client):
    filter_request = CraneFilterRequest(radius=10, payload=12)

    response = client.post(
        "/api/cranes", json=filter_request.model_dump()
    )

    assert response.status_code == 200

    cranes_response = CraneListResponse.model_validate(response.json())

    assert [crane.name for crane in cranes_response.cranes] == [
        "Liebherr_LR1100.1",
        "Liebherr_LTM1250-5.1",
        "Takraf_РДК400",
        "Zoomlion_ZTC600V"
    ]
    assert cranes_response.cranes_count == 4
    assert cranes_response.has_more is False
    assert cranes_response.returned_count == 4


def test_invalid_radius(client):
    filter_request = CraneFilterRequest(radius=10000, payload=10)

    response = client.post(
        "/api/cranes", json=filter_request.model_dump()
    )

    assert response.status_code == 200

    cranes_response = CraneListResponse.model_validate(response.json())

    assert len(cranes_response.cranes) == 0
    assert cranes_response.cranes_count == 0
    assert cranes_response.has_more is False
    assert cranes_response.returned_count == 0


def test_invalid_payload(client):
    filter_request = CraneFilterRequest(radius=10, payload=100000)

    response = client.post(
        "/api/cranes", json=filter_request.model_dump()
    )

    assert response.status_code == 200

    cranes_response = CraneListResponse.model_validate(response.json())

    assert len(cranes_response.cranes) == 0
    assert cranes_response.cranes_count == 0
    assert cranes_response.has_more is False
    assert cranes_response.returned_count == 0
