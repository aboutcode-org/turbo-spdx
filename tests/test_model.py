#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/scancode-toolkit for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

import json
import pathlib
from unittest import TestCase

import jsonschema

from turbo_spdx import model_23 as spdx


class TestSPDXModel(TestCase):
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

    checksum_sha1_spdx_data = {
        "algorithm": "SHA1",
        "checksumValue": "10c72b88de4c5f3095ebe20b4d8afbedb32b8f",
    }

    external_ref_purl_spdx_data = {
        "referenceCategory": "PACKAGE-MANAGER",
        "referenceType": "purl",
        "referenceLocator": "pkg:pypi/lxml@3.3.5",
    }

    licensing_info_spdx_data = {
        "licenseId": "LicenseRef-1",
        "extractedText": "License Text",
        "name": "License 1",
        "seeAlsos": [
            "https://license1.text",
            "https://license1.homepage",
        ],
    }

    package_spdx_data = {
        "name": "lxml",
        "SPDXID": "SPDXRef-package1",
        "downloadLocation": "NOASSERTION",
        "licenseConcluded": "LicenseRef-1",
        "copyrightText": "NOASSERTION",
        "filesAnalyzed": False,
        "versionInfo": "3.3.5",
        "licenseDeclared": "NOASSERTION",
        "releaseDate": "2000-01-01T00:00:00Z",
        "checksums": [
            {
                "algorithm": "SHA1",
                "checksumValue": "10c72b88de4c5f3095ebe20b4d8afbedb32b8f",
            },
            {
                "algorithm": "MD5",
                "checksumValue": "56770c1a2df6e0dc51c491f0a5b9d865",
            },
        ],
        "externalRefs": [
            {
                "referenceCategory": "PACKAGE-MANAGER",
                "referenceType": "purl",
                "referenceLocator": "pkg:pypi/lxml@3.3.5",
            }
        ],
    }

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

    relationship_spdx_data = {
        "spdxElementId": "SPDXRef-package1",
        "relatedSpdxElement": "SPDXRef-file1",
        "relationshipType": "CONTAINS",
    }

    document_spdx_data = {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": "SPDXRef-DOCUMENT",
        "name": "document_name",
        "documentNamespace": "https://[CreatorWebsite]/[DocumentName]-[UUID]",
        "creationInfo": {
            "created": "2022-09-21T13:50:20Z",
            "creators": [
                "Person: John Doe (john@starship.space)",
                "Organization: Starship ()",
                "Tool: SPDXCode-1.0",
            ],
            "licenseListVersion": "3.18",
            "comment": "Generated with SPDXCode",
        },
        "packages": [
            {
                "name": "lxml",
                "SPDXID": "SPDXRef-package1",
                "downloadLocation": "NOASSERTION",
                "licenseConcluded": "LicenseRef-1",
                "copyrightText": "NOASSERTION",
                "filesAnalyzed": False,
                "versionInfo": "3.3.5",
                "licenseDeclared": "NOASSERTION",
                "releaseDate": "2000-01-01T00:00:00Z",
                "checksums": [
                    {
                        "algorithm": "SHA1",
                        "checksumValue": "10c72b88de4c5f3095ebe20b4d8afbedb32b8f",
                    },
                    {
                        "algorithm": "MD5",
                        "checksumValue": "56770c1a2df6e0dc51c491f0a5b9d865",
                    },
                ],
                "externalRefs": [
                    {
                        "referenceCategory": "PACKAGE-MANAGER",
                        "referenceType": "purl",
                        "referenceLocator": "pkg:pypi/lxml@3.3.5",
                    }
                ],
            }
        ],
        "files": [
            {
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
        ],
        "documentDescribes": ["SPDXRef-package1"],
        "hasExtractedLicensingInfos": [
            {
                "licenseId": "LicenseRef-1",
                "extractedText": "License Text",
                "name": "License 1",
                "seeAlsos": ["https://license1.text", "https://license1.homepage"],
            }
        ],
        "relationships": [
            {
                "spdxElementId": "SPDXRef-package1",
                "relatedSpdxElement": "SPDXRef-file1",
                "relationshipType": "CONTAINS",
            }
        ],
        "comment": "This document was created using SPDXCode-1.0",
    }

    def get_dict(self, attributes):
        json_attributes = attributes.json(exclude_unset=True, by_alias=True)
        return json.loads(json_attributes)

    def test_spdx_creation_info_from_data(self):
        creation_info = spdx.CreationInfo(**self.creation_info_spdx_data)
        assert self.creation_info_spdx_data == self.get_dict(creation_info)

    def test_spdx_checksum_from_data(self):
        checksum = spdx.Checksum(**self.checksum_sha1_spdx_data)
        assert self.checksum_sha1_spdx_data == self.get_dict(checksum)

    def test_spdx_external_ref_from_data(self):
        external_ref = spdx.ExternalRef(**self.external_ref_purl_spdx_data)
        assert self.external_ref_purl_spdx_data == self.get_dict(external_ref)

    def test_spdx_extracted_licensing_info_from_data(self):
        licensing_info = spdx.HasExtractedLicensingInfo(**self.licensing_info_spdx_data)
        assert self.licensing_info_spdx_data == self.get_dict(licensing_info)

    def test_spdx_package_from_data(self):
        package = spdx.Package(**self.package_spdx_data)
        assert self.package_spdx_data == self.get_dict(package)

    def test_spdx_file_from_data(self):
        file = spdx.File(**self.file_spdx_data)
        assert self.file_spdx_data == self.get_dict(file)

    def test_spdx_relationship_from_data(self):
        relationship = spdx.Relationship(**self.relationship_spdx_data)
        assert self.relationship_spdx_data == self.get_dict(relationship)

    def test_spdx_document_from_data(self):
        document = spdx.Document(**self.document_spdx_data)
        assert self.document_spdx_data == self.get_dict(document)

    def test_spdx_document_validate(self):
        schema = pathlib.Path(__file__).parent / "data" / "schema" / "2.3" / "spdx-schema.json"
        schema = schema.read_text()
        schema = json.loads(schema)

        document_object = spdx.Document(**self.document_spdx_data)
        document = self.get_dict(document_object)
        jsonschema.validate(instance=document, schema=schema)
