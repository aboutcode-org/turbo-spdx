=========
TurboSPDX
=========

TurboSPDX is a fast and lightweight Python library for parsing and writing SPDX JSON documents correctly. With its precise implementation of the SPDX schema, library can accurately handle even the most complex SPDX documents.

|license| |version| |build| 

.. |license| image:: https://img.shields.io/badge/License-Apache--2.0-blue.svg?style=for-the-badge
    :target: https://opensource.org/licenses/Apache-2.0

.. |version| image:: https://img.shields.io/badge/Version-v1.0.0-brightgreen.svg?style=for-the-badge
    :alt: Version: v1.0.0

.. |build| image:: https://img.shields.io/badge/Build-passing-brightgreen.svg?style=for-the-badge
    :alt: Build: passing


How to use ?
=============

To use TurboSPDX in your project, you can simply install it using pip:


.. code-block:: bash

    $ pip install turbo-spdx

After installation, you can import the ``turbo_spdx`` module and start using it:

Examples
---------

1. Parse an existing SPDX document:

   .. code-block:: python

      >>> from turbo_spdx.spdx_23 import Document
      >>> 
      >>> your_existing_spdx_document = {
      ...   "SPDXID": "SPDXRef-DOCUMENT",
      ...   "spdxVersion": "SPDX-2.3",
      ...   "name": "TurboSPDX-v1.0",
      ...   "dataLicense": "Apache-2.0",
      ...   "creationInfo": {
      ...     "created": "2023-04-05T18:30:22Z",
      ...     "creators": [
      ...       "Organization: nexB"
      ...     ]
      ...   },
      ...   "packages": [
      ...     {
      ...       "name": "lxml",
      ...       "SPDXID": "SPDXRef-package-demo",
      ...       "downloadLocation": "NOASSERTION",
      ...       "versionInfo": "3.3.5",
      ...       "releaseDate": "2000-01-01T00:00:00Z",
      ...       "externalRefs": [
      ...         {
      ...           "referenceCategory": "PACKAGE-MANAGER",
      ...           "referenceType": "purl",
      ...           "referenceLocator": "pkg:pypi/lxml@3.3.5"
      ...         }
      ...       ]
      ...     }
      ...   ]
      ... }
      >>> 
      >>> parsed_sbom = Document(**your_existing_spdx_document)
      >>>
      >>> parsed_sbom.name
      'TurboSPDX-v1.0'
      >>>
      >>> parsed_sbom.packages
      [Package(SPDXID='SPDXRef-package-demo', annotations=None, attributionTexts=None, builtDate=None, checksums=None, comment=None, copyrightText=None, description=None, downloadLocation='NOASSERTION', externalRefs=[ExternalRef(comment=None, referenceCategory=<ReferenceCategory.PACKAGE_MANAGER: 'PACKAGE-MANAGER'>, referenceLocator='pkg:pypi/lxml@3.3.5', referenceType='purl')], filesAnalyzed=None, hasFiles=None, homepage=None, licenseComments=None, licenseConcluded=None, licenseDeclared=None, licenseInfoFromFiles=None, name='lxml', originator=None, packageFileName=None, packageVerificationCode=None, primaryPackagePurpose=None, releaseDate='2000-01-01T00:00:00Z', sourceInfo=None, summary=None, supplier=None, validUntilDate=None, versionInfo='3.3.5')]

2. Create one from scratch:

   .. code-block:: python

        >>> from turbo_spdx.spdx_23 import Document, CreationInfo
        >>> 
        >>> creation_info = CreationInfo(
        ...     created="2023-04-05T18:30:22Z",
        ...     creators=["Organization: nexB"]
        ... )
        >>>
        >>> sbom = Document(
        ...     SPDXID="SPDXRef-DOCUMENT",
        ...     name="TurboSPDX-v1.0",
        ...     spdxVersion="SPDX-2.3",
        ...     dataLicense="Apache-2.0",
        ...     creationInfo=creation_info
        ... )
        >>> sbom
        Document(SPDXID='SPDXRef-DOCUMENT', annotations=None, comment=None, creationInfo=CreationInfo(comment=None, created='2023-04-05T18:30:22Z', creators=['Organization: nexB'], licenseListVersion=None), dataLicense='Apache-2.0', externalDocumentRefs=None, hasExtractedLicensingInfos=None, name='TurboSPDX-v1.0', revieweds=None, spdxVersion='SPDX-2.3', documentNamespace=None, documentDescribes=None, packages=None, files=None, snippets=None, relationships=None)

3. Easily convert SPDX Document to JSON:

   .. code-block:: python

        >>> sbom.json(exclude_unset=True, by_alias=True)
        '{"SPDXID": "SPDXRef-DOCUMENT", "creationInfo": {"created": "2023-04-05T18:30:22Z", "creators": ["Organization: nexB"]}, "dataLicense": "Apache-2.0", "name": "TurboSPDX-v1.0", "spdxVersion": "SPDX-2.3"}'

 

How it works ?
=================

| TurboSPDX is a `Pydantic <https://docs.pydantic.dev/>`_ model generated from the SPDX schema.
|
| TurboSPDX utilizes Pydantic's data validation and parsing capabilities to ensure that the generated model conforms to the SPDX schema. The model is type-safe and can easily serialize and deserialize data to and from JSON. The generated model is a precise manifestation of the SPDX schema,  it's as good as the SPDX schema.

How to contribute ?
=====================

We welcome contributions from the community! If you find a bug or have an idea for a new feature, please open an issue on the GitHub repository. If you want to contribute code, you can fork the repository, make your changes, and submit a pull request.

- Please try to write a good commit message, see `good commit message wiki. <https://aboutcode.readthedocs.io/en/latest/contributing/writing_good_commit_messages.html>`_
- Add DCO Sign Off to your commits.

Development setup
------------------
Run these commands, starting from a git clone of https://github.com/nexB/turbo-spdx.git

.. code-block:: bash
    
    $ ./configure --dev
    $ source venv/bin/active

- Generate/ regenerate model:

  .. code-block:: bash

     $ make model version=2.3

- Run tests:

  .. code-block:: bash

     $ make test

License
====================

SPDX-License-Identifier: Apache-2.0

The TurboSPDX software is licensed under the Apache License version 2.0.

You may not use this software except in compliance with the License. You may obtain a copy of the License at: http://apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
