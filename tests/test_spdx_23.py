#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/aboutcode-org/scancode-toolkit for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

import json
import pathlib
from unittest import TestCase

import jsonschema

from turbo_spdx.spdx_23 import Checksum
from turbo_spdx.spdx_23 import CreationInfo
from turbo_spdx.spdx_23 import Document
from turbo_spdx.spdx_23 import ExternalRef
from turbo_spdx.spdx_23 import File
from turbo_spdx.spdx_23 import HasExtractedLicensingInfo
from turbo_spdx.spdx_23 import Package
from turbo_spdx.spdx_23 import Relationship


class TestSPDXModel_23(TestCase):
    def test_spdx_creation_info(self):
        creation_info_spdx_data = {
            "created": "2022-09-21T13:50:20Z",
            "creators": [
                "Person: John Doe (john@starship.space)",
                "Organization: Starship ()",
                "Tool: SPDXCode-1.0",
            ],
            "licenseListVersion": "3.18",
            "comment": "Generated with SPDXCode",
        }
        creation_info = CreationInfo(**creation_info_spdx_data)
        assert creation_info_spdx_data == spdx_to_dict(creation_info)

    def test_spdx_checksum(self):
        checksum_sha1_spdx_data = {
            "algorithm": "SHA1",
            "checksumValue": "10c72b88de4c5f3095ebe20b4d8afbedb32b8f",
        }
        checksum = Checksum(**checksum_sha1_spdx_data)
        assert checksum_sha1_spdx_data == spdx_to_dict(checksum)

    def test_spdx_external_ref(self):
        external_ref_purl_spdx_data = {
            "referenceCategory": "PACKAGE-MANAGER",
            "referenceType": "purl",
            "referenceLocator": "pkg:pypi/lxml@3.3.5",
        }
        external_ref = ExternalRef(**external_ref_purl_spdx_data)
        assert external_ref_purl_spdx_data == spdx_to_dict(external_ref)

    def test_spdx_extracted_licensing_info(self):
        licensing_info_spdx_data = {
            "licenseId": "LicenseRef-1",
            "extractedText": "License Text",
            "name": "License 1",
            "seeAlsos": [
                "https://license1.text",
                "https://license1.homepage",
            ],
        }
        licensing_info = HasExtractedLicensingInfo(**licensing_info_spdx_data)
        assert licensing_info_spdx_data == spdx_to_dict(licensing_info)

    def test_spdx_file(self):
        file_spdx_data = {
            "SPDXID": "SPDXRef-file1",
            "fileName": "file.txt",
            "checksums": [
                {
                    "algorithm": "SHA1",
                    "checksumValue": "10c72b88de4c5f3095ebe20b4d8afbedb32b8f",
                }
            ],
            "fileTypes": ["TEXT"],
            "copyrightText": "NOASSERTION",
            "licenseConcluded": "LicenseRef-1",
            "comment": "comment",
            "licenseComments": "license_comments",
        }
        file = File(**file_spdx_data)
        assert file_spdx_data == spdx_to_dict(file)

    def test_spdx_relationship(self):
        relationship_spdx_data = {
            "spdxElementId": "SPDXRef-package1",
            "relatedSpdxElement": "SPDXRef-file1",
            "relationshipType": "CONTAINS",
        }
        relationship = Relationship(**relationship_spdx_data)
        assert relationship_spdx_data == spdx_to_dict(relationship)

    def test_spdx_package(self):
        package_spdx_data = (
            pathlib.Path(__file__).parent / "data" / "fixtures" /
            "2.3" / "package_spdx_data.json"
        )
        package_spdx_data = package_spdx_data.read_text()
        package_spdx_data = json.loads(package_spdx_data)

        package = Package(**package_spdx_data)
        assert package_spdx_data == spdx_to_dict(package)

    def test_spdx_document(self):
        document_spdx_data = (
            pathlib.Path(__file__).parent / "data" / "fixtures" /
            "2.3" / "document_spdx_data.json"
        )
        document_spdx_data = document_spdx_data.read_text()
        document_spdx_data = json.loads(document_spdx_data)

        document = Document(**document_spdx_data)
        assert document_spdx_data == spdx_to_dict(document)

    def test_spdx_document_validate(self):
        schema = pathlib.Path(__file__).parent / "data" / \
            "schema" / "2.3" / "spdx-schema.json"
        schema = schema.read_text(encoding="utf-8")
        schema = json.loads(schema)

        document_spdx_data = (
            pathlib.Path(__file__).parent / "data" / "fixtures" /
            "2.3" / "document_spdx_data.json"
        )
        document_spdx_data = document_spdx_data.read_text()
        document_spdx_data = json.loads(document_spdx_data)

        document_object = Document(**document_spdx_data)
        document = spdx_to_dict(document_object)
        jsonschema.validate(instance=document, schema=schema)


class TestRoundTripSPDXModel_23:
    def _validate_roundtrip(self, filename) -> None:
        """
        Roundtrip test: Json->SPDXBom Object->Json
        """
        document_path = pathlib.Path(
            __file__).parent / "data" / "fixtures" / "2.3" / filename
        original_document = document_path.read_text()
        original_document = json.loads(original_document)

        parsed_json_from_model = Document(**original_document).json(
            exclude_unset=True, by_alias=True
        )
        parsed_dict_from_model = json.loads(parsed_json_from_model)
        assert original_document == parsed_dict_from_model

    def test_SPDXJSONExample_v2_3(self) -> None:
        self._validate_roundtrip(filename="SPDXJSONExample-v2.3.spdx.json")

    def test_asgiref_spdx(self) -> None:
        self._validate_roundtrip(filename="asgiref-3.3.0.spdx.json")

    def test_toml_spdx(self) -> None:
        self._validate_roundtrip(filename="toml.spdx.json")


def spdx_to_dict(attributes):
    return attributes.dict(exclude_unset=True, by_alias=True)
