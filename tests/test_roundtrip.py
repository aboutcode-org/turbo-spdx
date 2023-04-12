import json

from turbo_spdx.model_23 import Document


class TestSPDXModel_2Dot3:
    def _validate_roundtrip(self, filename) -> None:
        """
        Roundtrip test: Json->SPDXBom Object->Json
        """
        with open(f"tests/data/fixtures/2.3/{filename}") as original:
            original_dict = json.load(original)

        parsed_json_from_model = Document(**original_dict).json(exclude_unset=True, by_alias=True)
        parsed_dict_from_model = json.loads(parsed_json_from_model)
        assert original_dict == parsed_dict_from_model

    def test_bom_SPDXJSONExample_v2_3(self) -> None:
        self._validate_roundtrip(filename="SPDXJSONExample-v2.3.spdx.json")
