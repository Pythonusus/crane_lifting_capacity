from app.schemas.calc_requests import PayloadCalcRequest
from app.schemas.calc_responses import PayloadCalcResponse


class TestSinglePayloadRequest:
    def test_radius_not_in_lc_table(self, client, calc_accuracy):
        payload_request = PayloadCalcRequest(
            crane_name="Liebherr_LR1200.1",
            boom_len="50м",
            radius="10.32",
            equipment_weight=0,
            safety_factor=1.5,
        )

        response = client.post(
            "/process", json={"payload_request": payload_request.model_dump()}
        )

        assert response.status_code == 200

        # Parse response data using Pydantic model
        payload_response = PayloadCalcResponse.model_validate(response.json())

        # Assert request data in response
        assert payload_response.request.crane_name == "Liebherr_LR1200.1"
        assert payload_response.request.boom_len == "50м"
        assert float(payload_response.request.radius) == 10.32
        assert payload_response.request.equipment_weight == 0
        assert payload_response.request.safety_factor == 1.5

        # Expected values
        expected_lifting_capacity = 73.27
        expected_payload = (
            expected_lifting_capacity / payload_response.request.safety_factor
            - payload_response.request.equipment_weight
        )

        # Assert calculated values
        assert (
            abs(payload_response.lifting_capacity - expected_lifting_capacity)
            < calc_accuracy
        )
        assert abs(payload_response.payload - expected_payload) < calc_accuracy

    def test_radius_in_lc_table(self, client, calc_accuracy):
        payload_request = PayloadCalcRequest(
            crane_name="Takraf_РДК400",
            boom_len="36.0м",
            radius="16",
            equipment_weight=2,
            safety_factor=1.8,
        )

        response = client.post(
            "/process", json={"payload_request": payload_request.model_dump()}
        )

        assert response.status_code == 200

        # Parse response data using Pydantic model
        payload_response = PayloadCalcResponse.model_validate(response.json())

        # Assert request data in response
        assert payload_response.request.crane_name == "Takraf_РДК400"
        assert payload_response.request.boom_len == "36.0м"
        assert float(payload_response.request.radius) == 16
        assert payload_response.request.equipment_weight == 2
        assert payload_response.request.safety_factor == 1.8

        # Expected values
        expected_lifting_capacity = 5.2
        expected_payload = (
            expected_lifting_capacity / payload_response.request.safety_factor
            - payload_response.request.equipment_weight
        )

        # Assert calculated values
        assert (
            abs(payload_response.lifting_capacity - expected_lifting_capacity)
            < calc_accuracy
        )
        assert abs(payload_response.payload - expected_payload) < calc_accuracy
