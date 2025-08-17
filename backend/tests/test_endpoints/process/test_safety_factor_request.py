from app.schemas.calc_requests import SafetyFactorCalcRequest
from app.schemas.calc_responses import SafetyFactorCalcResponse


class TestSingleSafetyFactorRequest:
    def test_radius_not_in_lc_table(self, client, calc_accuracy):
        safety_request = SafetyFactorCalcRequest(
            crane_name="Liebherr_LR1100",
            boom_len="14.0м",
            radius="5.5",
            equipment_weight=0,
            payload=40.1,
        )

        response = client.post(
            "/process", json={"safety_request": safety_request.model_dump()}
        )

        assert response.status_code == 200

        # Parse response data using Pydantic model
        safety_response = SafetyFactorCalcResponse.model_validate(
            response.json()
        )

        # Assert request data in response
        assert safety_response.request.crane_name == "Liebherr_LR1100"
        assert safety_response.request.boom_len == "14.0м"
        assert float(safety_response.request.radius) == 5.5
        assert safety_response.request.equipment_weight == 0
        assert safety_response.request.payload == 40.1

        # Expected values
        expected_lifting_capacity = 77.15
        expected_safety_factor = expected_lifting_capacity / (
            safety_response.request.payload
            + safety_response.request.equipment_weight
        )

        # Assert calculated values
        assert (
            abs(safety_response.lifting_capacity - expected_lifting_capacity)
            < calc_accuracy
        )
        assert (
            abs(safety_response.safety_factor - expected_safety_factor)
            < calc_accuracy
        )

    def test_radius_in_lc_table(self, client, calc_accuracy):
        safety_request = SafetyFactorCalcRequest(
            crane_name="Liebherr_LTM1300-6.2",
            boom_len="43.9м",
            radius="12",
            equipment_weight=5,
            payload=50.33,
        )

        response = client.post(
            "/process", json={"safety_request": safety_request.model_dump()}
        )

        assert response.status_code == 200

        # Parse response data using Pydantic model
        safety_response = SafetyFactorCalcResponse.model_validate(
            response.json()
        )

        # Assert request data in response
        assert safety_response.request.crane_name == "Liebherr_LTM1300-6.2"
        assert safety_response.request.boom_len == "43.9м"
        assert float(safety_response.request.radius) == 12
        assert safety_response.request.equipment_weight == 5
        assert safety_response.request.payload == 50.33

        # Expected values
        expected_lifting_capacity = 56.4
        expected_safety_factor = expected_lifting_capacity / (
            safety_response.request.payload
            + safety_response.request.equipment_weight
        )

        # Assert calculated values
        assert (
            abs(safety_response.lifting_capacity - expected_lifting_capacity)
            < calc_accuracy
        )
        assert (
            abs(safety_response.safety_factor - expected_safety_factor)
            < calc_accuracy
        )
