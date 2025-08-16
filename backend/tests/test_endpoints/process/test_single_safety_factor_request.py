from app.schemas.calc_requests import (
    PayloadCalcRequest,
    PayloadCalcRequestBase,
    SafetyFactorCalcRequest,
    SafetyFactorCalcRequestBase,
)
from app.schemas.calc_responses import (
    PayloadCalcResponse,
    PayloadCalcResponseBase,
    SafetyFactorCalcResponse,
    SafetyFactorCalcResponseBase,
)


class TestSingleSafetyFactorRequest:
    def test_radius_not_in_lc_table(self, client, calc_accuracy):
        base_request = SafetyFactorCalcRequestBase(
            crane_name="Liebherr_LR1100",
            boom_len="14.0м",
            radius="5.5",
            equipment_weight=0,
            payload=40.1,
        )
        safety_request = SafetyFactorCalcRequest(base_requests=[base_request])

        response = client.post(
            "/process", json={"safety_request": safety_request.model_dump()}
        )

        assert response.status_code == 200

        # Parse response data using Pydantic model
        safety_response = SafetyFactorCalcResponse.model_validate(
            response.json()
        )

        assert len(safety_response.base_responses) == 1
        base_response = safety_response.base_responses[0]
        assert isinstance(base_response, SafetyFactorCalcResponseBase)

        # Assert request data in response
        assert base_response.request.crane_name == "Liebherr_LR1100"
        assert base_response.request.boom_len == "14.0м"
        assert float(base_response.request.radius) == 5.5
        assert base_response.request.equipment_weight == 0
        assert base_response.request.payload == 40.1

        # Expected values
        expected_lifting_capacity = 77.15
        expected_safety_factor = expected_lifting_capacity / (
            base_response.request.payload
            + base_response.request.equipment_weight
        )

        # Assert calculated values
        assert (
            abs(base_response.lifting_capacity - expected_lifting_capacity)
            < calc_accuracy
        )
        assert (
            abs(base_response.safety_factor - expected_safety_factor)
            < calc_accuracy
        )

    def test_radius_in_lc_table(self, client, calc_accuracy):
        base_request = SafetyFactorCalcRequestBase(
            crane_name="Liebherr_LTM1300-6.2",
            boom_len="43.9м",
            radius="12",
            equipment_weight=5,
            payload=50.33,
        )
        safety_request = SafetyFactorCalcRequest(base_requests=[base_request])

        response = client.post(
            "/process", json={"safety_request": safety_request.model_dump()}
        )

        assert response.status_code == 200

        # Parse response data using Pydantic model
        safety_response = SafetyFactorCalcResponse.model_validate(
            response.json()
        )

        assert len(safety_response.base_responses) == 1
        base_response = safety_response.base_responses[0]
        assert isinstance(base_response, SafetyFactorCalcResponseBase)

        # Assert request data in response
        assert base_response.request.crane_name == "Liebherr_LTM1300-6.2"
        assert base_response.request.boom_len == "43.9м"
        assert float(base_response.request.radius) == 12
        assert base_response.request.equipment_weight == 5
        assert base_response.request.payload == 50.33

        # Expected values
        expected_lifting_capacity = 56.4
        expected_safety_factor = expected_lifting_capacity / (
            base_response.request.payload
            + base_response.request.equipment_weight
        )

        # Assert calculated values
        assert (
            abs(base_response.lifting_capacity - expected_lifting_capacity)
            < calc_accuracy
        )
        assert (
            abs(base_response.safety_factor - expected_safety_factor)
            < calc_accuracy
        )


class TestSinglePayloadRequest:
    def test_radius_not_in_lc_table(self, client, calc_accuracy):
        base_request = PayloadCalcRequestBase(
            crane_name="Liebherr_LR1200.1",
            boom_len="50м",
            radius="10.32",
            equipment_weight=0,
            safety_factor=1.5,
        )
        payload_request = PayloadCalcRequest(base_requests=[base_request])

        response = client.post(
            "/process", json={"payload_request": payload_request.model_dump()}
        )

        assert response.status_code == 200

        # Parse response data using Pydantic model
        payload_response = PayloadCalcResponse.model_validate(response.json())

        assert len(payload_response.base_responses) == 1
        base_response = payload_response.base_responses[0]
        assert isinstance(base_response, PayloadCalcResponseBase)

        # Assert request data in response
        assert base_response.request.crane_name == "Liebherr_LR1200.1"
        assert base_response.request.boom_len == "50м"
        assert float(base_response.request.radius) == 10.32
        assert base_response.request.equipment_weight == 0
        assert base_response.request.safety_factor == 1.5

        # Expected values
        expected_lifting_capacity = 73.27
        expected_payload = (
            expected_lifting_capacity / base_response.request.safety_factor
            - base_response.request.equipment_weight
        )

        # Assert calculated values
        assert (
            abs(base_response.lifting_capacity - expected_lifting_capacity)
            < calc_accuracy
        )
        assert abs(base_response.payload - expected_payload) < calc_accuracy

    def test_radius_in_lc_table(self, client, calc_accuracy):
        base_request = PayloadCalcRequestBase(
            crane_name="Takraf_РДК400",
            boom_len="36.0м",
            radius="16",
            equipment_weight=2,
            safety_factor=1.8,
        )
        payload_request = PayloadCalcRequest(base_requests=[base_request])

        response = client.post(
            "/process", json={"payload_request": payload_request.model_dump()}
        )

        assert response.status_code == 200

        # Parse response data using Pydantic model
        payload_response = PayloadCalcResponse.model_validate(response.json())

        assert len(payload_response.base_responses) == 1
        base_response = payload_response.base_responses[0]
        assert isinstance(base_response, PayloadCalcResponseBase)

        # Assert request data in response
        assert base_response.request.crane_name == "Takraf_РДК400"
        assert base_response.request.boom_len == "36.0м"
        assert float(base_response.request.radius) == 16
        assert base_response.request.equipment_weight == 2
        assert base_response.request.safety_factor == 1.8

        # Expected values
        expected_lifting_capacity = 5.2
        expected_payload = (
            expected_lifting_capacity / base_response.request.safety_factor
            - base_response.request.equipment_weight
        )

        # Assert calculated values
        assert (
            abs(base_response.lifting_capacity - expected_lifting_capacity)
            < calc_accuracy
        )
        assert abs(base_response.payload - expected_payload) < calc_accuracy
