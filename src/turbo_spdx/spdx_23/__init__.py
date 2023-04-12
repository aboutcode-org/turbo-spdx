#
# Copyright (c) nexB Inc. and others. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/turbo-spdx for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

from __future__ import annotations

from enum import Enum
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Extra
from pydantic import Field


class AnnotationType(str, Enum):
    OTHER = "OTHER"
    REVIEW = "REVIEW"


class Annotation(BaseModel):
    class Config:
        extra = Extra.forbid

    annotationDate: str = Field(
        ...,
        description=(
            "Identify when the comment was made. This is to be specified according to"
            " the combined date and time in the UTC format, as specified in the ISO"
            " 8601 standard."
        ),
    )
    annotationType: AnnotationType = Field(..., description="Type of the annotation.")
    annotator: str = Field(
        ...,
        description=(
            "This field identifies the person, organization, or tool that has commented"
            " on a file, package, snippet, or the entire document."
        ),
    )
    comment: str


class CreationInfo(BaseModel):
    class Config:
        extra = Extra.forbid

    comment: Optional[str]
    created: str = Field(
        ...,
        description=(
            "Identify when the SPDX document was originally created. The date is to be"
            " specified according to combined date and time in UTC format as specified"
            " in ISO 8601 standard."
        ),
    )
    creators: List[str] = Field(
        ...,
        description=(
            "Identify who (or what, in the case of a tool) created the SPDX document."
            " If the SPDX document was created by an individual, indicate the person's"
            " name. If the SPDX document was created on behalf of a company or"
            " organization, indicate the entity name. If the SPDX document was created"
            " using a software tool, indicate the name and version for that tool. If"
            " multiple participants or tools were involved, use multiple instances of"
            " this field. Person name or organization name may be designated as"
            " “anonymous” if appropriate."
        ),
        min_items=1,
    )
    licenseListVersion: Optional[str] = Field(
        default=None,
        description=(
            "An optional field for creators of the SPDX file to provide the version of"
            " the SPDX License List used when the SPDX file was created."
        ),
    )


class Algorithm(str, Enum):
    SHA1 = "SHA1"
    BLAKE3 = "BLAKE3"
    SHA3_384 = "SHA3-384"
    SHA256 = "SHA256"
    SHA384 = "SHA384"
    BLAKE2b_512 = "BLAKE2b-512"
    BLAKE2b_256 = "BLAKE2b-256"
    SHA3_512 = "SHA3-512"
    MD2 = "MD2"
    ADLER32 = "ADLER32"
    MD4 = "MD4"
    SHA3_256 = "SHA3-256"
    BLAKE2b_384 = "BLAKE2b-384"
    SHA512 = "SHA512"
    MD6 = "MD6"
    MD5 = "MD5"
    SHA224 = "SHA224"


class Checksum(BaseModel):
    class Config:
        extra = Extra.forbid

    algorithm: Algorithm = Field(
        ...,
        description=(
            "Identifies the algorithm used to produce the subject Checksum. Currently,"
            " SHA-1 is the only supported algorithm. It is anticipated that other"
            " algorithms will be supported at a later time."
        ),
    )
    checksumValue: str = Field(
        ...,
        description=(
            "The checksumValue property provides a lower case hexidecimal encoded"
            " digest value produced using a specific algorithm."
        ),
    )


class ExternalDocumentRef(BaseModel):
    class Config:
        extra = Extra.forbid

    checksum: Checksum = Field(
        ...,
        description=(
            "A Checksum is value that allows the contents of a file to be"
            " authenticated. Even small changes to the content of the file will change"
            " its checksum. This class allows the results of a variety of checksum and"
            " cryptographic message digest algorithms to be represented."
        ),
    )
    externalDocumentId: str = Field(
        ...,
        description=(
            "externalDocumentId is a string containing letters, numbers, ., - and/or +"
            " which uniquely identifies an external document within this document."
        ),
    )
    spdxDocument: str = Field(
        ...,
        description=("SPDX ID for SpdxDocument.  A property containing an SPDX document."),
    )


class CrossRef(BaseModel):
    class Config:
        extra = Extra.forbid

    isLive: Optional[bool] = Field(
        default=None,
        description=("Indicate a URL is still a live accessible location on the public internet"),
    )
    isValid: Optional[bool] = Field(
        default=None, description="True if the URL is a valid well formed URL"
    )
    isWayBackLink: Optional[bool] = Field(
        default=None,
        description="True if the License SeeAlso URL points to a Wayback archive",
    )
    match: Optional[str] = Field(
        default=None,
        description=(
            "Status of a License List SeeAlso URL reference if it refers to a website"
            " that matches the license text."
        ),
    )
    order: Optional[int] = Field(
        default=None, description="The ordinal order of this element within a list"
    )
    timestamp: Optional[str] = Field(default=None, description="Timestamp")
    url: str = Field(..., description="URL Reference")


class HasExtractedLicensingInfo(BaseModel):
    class Config:
        extra = Extra.forbid

    comment: Optional[str]
    crossRefs: Optional[List[CrossRef]] = Field(
        default=None, description="Cross Reference Detail for a license SeeAlso URL"
    )
    extractedText: str = Field(
        ...,
        description=(
            "Provide a copy of the actual text of the license reference extracted from"
            " the package, file or snippet that is associated with the License"
            " Identifier to aid in future analysis."
        ),
    )
    licenseId: str = Field(
        ...,
        description=(
            "A human readable short form license identifier for a license. The license"
            " ID is either on the standard license list or the form"
            ' "LicenseRef-[idString]" where [idString] is a unique string containing'
            ' letters, numbers, "." or "-".  When used within a license expression, the'
            " license ID can optionally include a reference to an external document in"
            ' the form "DocumentRef-[docrefIdString]:LicenseRef-[idString]" where'
            " docRefIdString is an ID for an external document reference."
        ),
    )
    name: Optional[str] = Field(default=None, description="Identify name of this SpdxElement.")
    seeAlsos: Optional[List[str]]


class Reviewed(BaseModel):
    class Config:
        extra = Extra.forbid

    comment: Optional[str]
    reviewDate: str = Field(
        ...,
        description=(
            "The date and time at which the SpdxDocument was reviewed. This value must"
            " be in UTC and have 'Z' as its timezone indicator."
        ),
    )
    reviewer: Optional[str] = Field(
        default=None,
        description=(
            "The name and, optionally, contact information of the person who performed"
            " the review. Values of this property must conform to the agent and tool"
            " syntax.  The reviewer property is deprecated in favor of Annotation with"
            " an annotationType review."
        ),
    )


class Annotation1(Annotation):
    pass


class Checksum1(Checksum):
    pass


class ReferenceCategory(str, Enum):
    OTHER = "OTHER"
    PERSISTENT_ID = "PERSISTENT-ID"
    SECURITY = "SECURITY"
    PACKAGE_MANAGER = "PACKAGE-MANAGER"


class ExternalRef(BaseModel):
    class Config:
        extra = Extra.forbid

    comment: Optional[str]
    referenceCategory: ReferenceCategory = Field(
        ..., description="Category for the external reference"
    )
    referenceLocator: str = Field(
        ...,
        description=(
            "The unique string with no spaces necessary to access the package-specific"
            " information, metadata, or content within the target location. The format"
            " of the locator is subject to constraints defined by the <type>."
        ),
    )
    referenceType: str = Field(
        ...,
        description=(
            "Type of the external reference. These are definined in an appendix in the"
            " SPDX specification."
        ),
    )


class PackageVerificationCode(BaseModel):
    class Config:
        extra = Extra.forbid

    packageVerificationCodeExcludedFiles: Optional[List[str]] = Field(
        default=None,
        description=(
            "A file that was excluded when calculating the package verification code."
            " This is usually a file containing SPDX data regarding the package. If a"
            " package contains more than one SPDX file all SPDX files must be excluded"
            " from the package verification code. If this is not done it would be"
            " impossible to correctly calculate the verification codes in both files."
        ),
    )
    packageVerificationCodeValue: str = Field(
        ..., description="The actual package verification code as a hex encoded value."
    )


class PrimaryPackagePurpose(str, Enum):
    OTHER = "OTHER"
    INSTALL = "INSTALL"
    ARCHIVE = "ARCHIVE"
    FIRMWARE = "FIRMWARE"
    APPLICATION = "APPLICATION"
    FRAMEWORK = "FRAMEWORK"
    LIBRARY = "LIBRARY"
    CONTAINER = "CONTAINER"
    SOURCE = "SOURCE"
    DEVICE = "DEVICE"
    OPERATING_SYSTEM = "OPERATING_SYSTEM"
    FILE = "FILE"


class Package(BaseModel):
    class Config:
        extra = Extra.forbid

    SPDXID: str = Field(
        ...,
        description=(
            "Uniquely identify any element in an SPDX document which may be referenced"
            " by other elements."
        ),
    )
    annotations: Optional[List[Annotation1]] = Field(
        default=None, description="Provide additional information about an SpdxElement."
    )
    attributionTexts: Optional[List[str]] = Field(
        default=None,
        description=(
            "This field provides a place for the SPDX data creator to record"
            " acknowledgements that may be required to be communicated in some"
            " contexts. This is not meant to include the actual complete license text"
            " (see licenseConculded and licenseDeclared), and may or may not include"
            " copyright notices (see also copyrightText). The SPDX data creator may use"
            " this field to record other acknowledgements, such as particular clauses"
            " from license texts, which may be necessary or desirable to reproduce."
        ),
    )
    builtDate: Optional[str] = Field(
        default=None,
        description=(
            "This field provides a place for recording the actual date the package was" " built."
        ),
    )
    checksums: Optional[List[Checksum1]] = Field(
        default=None,
        description=(
            "The checksum property provides a mechanism that can be used to verify that"
            " the contents of a File or Package have not changed."
        ),
    )
    comment: Optional[str]
    copyrightText: Optional[str] = Field(
        default=None,
        description=(
            "The text of copyright declarations recited in the package, file or"
            " snippet.\n\nIf the copyrightText field is not present, it implies an"
            " equivalent meaning to NOASSERTION."
        ),
    )
    description: Optional[str] = Field(
        default=None, description="Provides a detailed description of the package."
    )
    downloadLocation: str = Field(
        ...,
        description=(
            "The URI at which this package is available for download. Private (i.e.,"
            " not publicly reachable) URIs are acceptable as values of this property."
            " The values http://spdx.org/rdf/terms#none and"
            " http://spdx.org/rdf/terms#noassertion may be used to specify that the"
            " package is not downloadable or that no attempt was made to determine its"
            " download location, respectively."
        ),
    )
    externalRefs: Optional[List[ExternalRef]] = Field(
        default=None,
        description=(
            "An External Reference allows a Package to reference an external source of"
            " additional information, metadata, enumerations, asset identifiers, or"
            " downloadable content believed to be relevant to the Package."
        ),
    )
    filesAnalyzed: Optional[bool] = Field(
        default=None,
        description=(
            "Indicates whether the file content of this package has been available for"
            " or subjected to analysis when creating the SPDX document. If false"
            " indicates packages that represent metadata or URI references to a"
            " project, product, artifact, distribution or a component. If set to false,"
            " the package must not contain any files."
        ),
    )
    hasFiles: Optional[List[str]] = Field(
        default=None,
        description="Indicates that a particular file belongs to a package.",
    )
    homepage: Optional[str]
    licenseComments: Optional[str] = Field(
        default=None,
        description=(
            "The licenseComments property allows the preparer of the SPDX document to"
            " describe why the licensing in spdx:licenseConcluded was chosen."
        ),
    )
    licenseConcluded: Optional[str] = Field(
        default=None,
        description=(
            "License expression for licenseConcluded. See SPDX Annex D for the license"
            " expression syntax.  The licensing that the preparer of this SPDX document"
            " has concluded, based on the evidence, actually applies to the SPDX"
            " Item.\n\nIf the licenseConcluded field is not present for an SPDX Item,"
            " it implies an equivalent meaning to NOASSERTION."
        ),
    )
    licenseDeclared: Optional[str] = Field(
        default=None,
        description=(
            "License expression for licenseDeclared. See SPDX Annex D for the license"
            " expression syntax.  The licensing that the creators of the software in"
            " the package, or the packager, have declared. Declarations by the original"
            " software creator should be preferred, if they exist."
        ),
    )
    licenseInfoFromFiles: Optional[List[str]] = Field(
        default=None,
        description=(
            "The licensing information that was discovered directly within the package."
            " There will be an instance of this property for each distinct value of"
            " alllicenseInfoInFile properties of all files contained in the"
            " package.\n\nIf the licenseInfoFromFiles field is not present for a"
            " package and filesAnalyzed property for that same pacakge is true or"
            " omitted, it implies an equivalent meaning to NOASSERTION."
        ),
    )
    name: str = Field(..., description="Identify name of this SpdxElement.")
    originator: Optional[str] = Field(
        default=None,
        description=(
            "The name and, optionally, contact information of the person or"
            " organization that originally created the package. Values of this property"
            " must conform to the agent and tool syntax."
        ),
    )
    packageFileName: Optional[str] = Field(
        default=None,
        description=("The base name of the package file name. For example, zlib-1.2.5.tar.gz."),
    )
    packageVerificationCode: Optional[PackageVerificationCode] = Field(
        default=None,
        description=(
            "A manifest based verification code (the algorithm is defined in section"
            " 4.7 of the full specification) of the SPDX Item. This allows consumers of"
            " this data and/or database to determine if an SPDX item they have in hand"
            " is identical to the SPDX item from which the data was produced. This"
            " algorithm works even if the SPDX document is included in the SPDX item."
        ),
    )
    primaryPackagePurpose: Optional[PrimaryPackagePurpose] = Field(
        default=None,
        description=(
            "This field provides information about the primary purpose of the"
            " identified package. Package Purpose is intrinsic to how the package is"
            " being used rather than the content of the package."
        ),
    )
    releaseDate: Optional[str] = Field(
        default=None,
        description=(
            "This field provides a place for recording the date the package was" " released."
        ),
    )
    sourceInfo: Optional[str] = Field(
        default=None,
        description=(
            "Allows the producer(s) of the SPDX document to describe how the package"
            " was acquired and/or changed from the original source."
        ),
    )
    summary: Optional[str] = Field(
        default=None, description="Provides a short description of the package."
    )
    supplier: Optional[str] = Field(
        default=None,
        description=(
            "The name and, optionally, contact information of the person or"
            " organization who was the immediate supplier of this package to the"
            " recipient. The supplier may be different than originator when the"
            " software has been repackaged. Values of this property must conform to the"
            " agent and tool syntax."
        ),
    )
    validUntilDate: Optional[str] = Field(
        default=None,
        description=(
            "This field provides a place for recording the end of the support period"
            " for a package from the supplier."
        ),
    )
    versionInfo: Optional[str] = Field(
        default=None,
        description=(
            "Provides an indication of the version of the package that is described by"
            " this SpdxDocument."
        ),
    )


class Annotation2(Annotation):
    pass


class Checksum2(Checksum):
    pass


class FileType(str, Enum):
    OTHER = "OTHER"
    DOCUMENTATION = "DOCUMENTATION"
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    ARCHIVE = "ARCHIVE"
    SPDX = "SPDX"
    APPLICATION = "APPLICATION"
    SOURCE = "SOURCE"
    BINARY = "BINARY"
    TEXT = "TEXT"
    AUDIO = "AUDIO"


class File(BaseModel):
    class Config:
        extra = Extra.forbid

    SPDXID: str = Field(
        ...,
        description=(
            "Uniquely identify any element in an SPDX document which may be referenced"
            " by other elements."
        ),
    )
    annotations: Optional[List[Annotation2]] = Field(
        default=None, description="Provide additional information about an SpdxElement."
    )
    artifactOfs: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description=(
            "Indicates the project in which the SpdxElement originated. Tools must"
            " preserve doap:homepage and doap:name properties and the URI (if one is"
            " known) of doap:Project resources that are values of this property. All"
            " other properties of doap:Projects are not directly supported by SPDX and"
            " may be dropped when translating to or from some SPDX formats."
        ),
    )
    attributionTexts: Optional[List[str]] = Field(
        default=None,
        description=(
            "This field provides a place for the SPDX data creator to record"
            " acknowledgements that may be required to be communicated in some"
            " contexts. This is not meant to include the actual complete license text"
            " (see licenseConculded and licenseDeclared), and may or may not include"
            " copyright notices (see also copyrightText). The SPDX data creator may use"
            " this field to record other acknowledgements, such as particular clauses"
            " from license texts, which may be necessary or desirable to reproduce."
        ),
    )
    checksums: List[Checksum2] = Field(
        ...,
        description=(
            "The checksum property provides a mechanism that can be used to verify that"
            " the contents of a File or Package have not changed."
        ),
        min_items=1,
    )
    comment: Optional[str]
    copyrightText: Optional[str] = Field(
        default=None,
        description=(
            "The text of copyright declarations recited in the package, file or"
            " snippet.\n\nIf the copyrightText field is not present, it implies an"
            " equivalent meaning to NOASSERTION."
        ),
    )
    fileContributors: Optional[List[str]] = Field(
        default=None,
        description=(
            "This field provides a place for the SPDX file creator to record file"
            " contributors. Contributors could include names of copyright holders"
            " and/or authors who may not be copyright holders yet contributed to the"
            " file content."
        ),
    )
    fileDependencies: Optional[List[str]] = Field(
        default=None,
        description=(
            "This field is deprecated since SPDX 2.0 in favor of using Section 7 which"
            " provides more granularity about relationships."
        ),
    )
    fileName: str = Field(
        ..., description="The name of the file relative to the root of the package."
    )
    fileTypes: Optional[List[FileType]] = Field(default=None, description="The type of the file.")
    licenseComments: Optional[str] = Field(
        default=None,
        description=(
            "The licenseComments property allows the preparer of the SPDX document to"
            " describe why the licensing in spdx:licenseConcluded was chosen."
        ),
    )
    licenseConcluded: Optional[str] = Field(
        default=None,
        description=(
            "License expression for licenseConcluded. See SPDX Annex D for the license"
            " expression syntax.  The licensing that the preparer of this SPDX document"
            " has concluded, based on the evidence, actually applies to the SPDX"
            " Item.\n\nIf the licenseConcluded field is not present for an SPDX Item,"
            " it implies an equivalent meaning to NOASSERTION."
        ),
    )
    licenseInfoInFiles: Optional[List[str]] = Field(
        default=None,
        description=(
            "Licensing information that was discovered directly in the subject file."
            " This is also considered a declared license for the file.\n\nIf the"
            " licenseInfoInFile field is not present for a file, it implies an"
            " equivalent meaning to NOASSERTION."
        ),
    )
    noticeText: Optional[str] = Field(
        default=None,
        description=(
            "This field provides a place for the SPDX file creator to record potential"
            " legal notices found in the file. This may or may not include copyright"
            " statements."
        ),
    )


class Annotation3(Annotation):
    pass


class EndPointer(BaseModel):
    class Config:
        extra = Extra.forbid

    reference: str = Field(..., description="SPDX ID for File")
    offset: Optional[int] = Field(default=None, description="Byte offset in the file")
    lineNumber: Optional[int] = Field(default=None, description="line number offset in the file")


class StartPointer(EndPointer):
    pass


class Range(BaseModel):
    class Config:
        extra = Extra.forbid

    endPointer: EndPointer
    startPointer: StartPointer


class Snippet(BaseModel):
    class Config:
        extra = Extra.forbid

    SPDXID: str = Field(
        ...,
        description=(
            "Uniquely identify any element in an SPDX document which may be referenced"
            " by other elements."
        ),
    )
    annotations: Optional[List[Annotation3]] = Field(
        default=None, description="Provide additional information about an SpdxElement."
    )
    attributionTexts: Optional[List[str]] = Field(
        default=None,
        description=(
            "This field provides a place for the SPDX data creator to record"
            " acknowledgements that may be required to be communicated in some"
            " contexts. This is not meant to include the actual complete license text"
            " (see licenseConculded and licenseDeclared), and may or may not include"
            " copyright notices (see also copyrightText). The SPDX data creator may use"
            " this field to record other acknowledgements, such as particular clauses"
            " from license texts, which may be necessary or desirable to reproduce."
        ),
    )
    comment: Optional[str]
    copyrightText: Optional[str] = Field(
        default=None,
        description=(
            "The text of copyright declarations recited in the package, file or"
            " snippet.\n\nIf the copyrightText field is not present, it implies an"
            " equivalent meaning to NOASSERTION."
        ),
    )
    licenseComments: Optional[str] = Field(
        default=None,
        description=(
            "The licenseComments property allows the preparer of the SPDX document to"
            " describe why the licensing in spdx:licenseConcluded was chosen."
        ),
    )
    licenseConcluded: Optional[str] = Field(
        default=None,
        description=(
            "License expression for licenseConcluded. See SPDX Annex D for the license"
            " expression syntax.  The licensing that the preparer of this SPDX document"
            " has concluded, based on the evidence, actually applies to the SPDX"
            " Item.\n\nIf the licenseConcluded field is not present for an SPDX Item,"
            " it implies an equivalent meaning to NOASSERTION."
        ),
    )
    licenseInfoInSnippets: Optional[List[str]] = Field(
        default=None,
        description=(
            "Licensing information that was discovered directly in the subject snippet."
            " This is also considered a declared license for the snippet.\n\nIf the"
            " licenseInfoInSnippet field is not present for a snippet, it implies an"
            " equivalent meaning to NOASSERTION."
        ),
    )
    name: str = Field(..., description="Identify name of this SpdxElement.")
    ranges: List[Range] = Field(
        ...,
        description=(
            "This field defines the byte range in the original host file (in X.2) that"
            " the snippet information applies to"
        ),
        min_items=1,
    )
    snippetFromFile: str = Field(
        ...,
        description=(
            "SPDX ID for File.  File containing the SPDX element (e.g. the file"
            " contaning a snippet)."
        ),
    )


class RelationshipType(str, Enum):
    VARIANT_OF = "VARIANT_OF"
    COPY_OF = "COPY_OF"
    PATCH_FOR = "PATCH_FOR"
    TEST_DEPENDENCY_OF = "TEST_DEPENDENCY_OF"
    CONTAINED_BY = "CONTAINED_BY"
    DATA_FILE_OF = "DATA_FILE_OF"
    OPTIONAL_COMPONENT_OF = "OPTIONAL_COMPONENT_OF"
    ANCESTOR_OF = "ANCESTOR_OF"
    GENERATES = "GENERATES"
    CONTAINS = "CONTAINS"
    OPTIONAL_DEPENDENCY_OF = "OPTIONAL_DEPENDENCY_OF"
    FILE_ADDED = "FILE_ADDED"
    REQUIREMENT_DESCRIPTION_FOR = "REQUIREMENT_DESCRIPTION_FOR"
    DEV_DEPENDENCY_OF = "DEV_DEPENDENCY_OF"
    DEPENDENCY_OF = "DEPENDENCY_OF"
    BUILD_DEPENDENCY_OF = "BUILD_DEPENDENCY_OF"
    DESCRIBES = "DESCRIBES"
    PREREQUISITE_FOR = "PREREQUISITE_FOR"
    HAS_PREREQUISITE = "HAS_PREREQUISITE"
    PROVIDED_DEPENDENCY_OF = "PROVIDED_DEPENDENCY_OF"
    DYNAMIC_LINK = "DYNAMIC_LINK"
    DESCRIBED_BY = "DESCRIBED_BY"
    METAFILE_OF = "METAFILE_OF"
    DEPENDENCY_MANIFEST_OF = "DEPENDENCY_MANIFEST_OF"
    PATCH_APPLIED = "PATCH_APPLIED"
    RUNTIME_DEPENDENCY_OF = "RUNTIME_DEPENDENCY_OF"
    TEST_OF = "TEST_OF"
    TEST_TOOL_OF = "TEST_TOOL_OF"
    DEPENDS_ON = "DEPENDS_ON"
    SPECIFICATION_FOR = "SPECIFICATION_FOR"
    FILE_MODIFIED = "FILE_MODIFIED"
    DISTRIBUTION_ARTIFACT = "DISTRIBUTION_ARTIFACT"
    AMENDS = "AMENDS"
    DOCUMENTATION_OF = "DOCUMENTATION_OF"
    GENERATED_FROM = "GENERATED_FROM"
    STATIC_LINK = "STATIC_LINK"
    OTHER = "OTHER"
    BUILD_TOOL_OF = "BUILD_TOOL_OF"
    TEST_CASE_OF = "TEST_CASE_OF"
    PACKAGE_OF = "PACKAGE_OF"
    DESCENDANT_OF = "DESCENDANT_OF"
    FILE_DELETED = "FILE_DELETED"
    EXPANDED_FROM_ARCHIVE = "EXPANDED_FROM_ARCHIVE"
    DEV_TOOL_OF = "DEV_TOOL_OF"
    EXAMPLE_OF = "EXAMPLE_OF"


class Relationship(BaseModel):
    class Config:
        extra = Extra.forbid

    spdxElementId: str = Field(..., description="Id to which the SPDX element is related")
    comment: Optional[str]
    relatedSpdxElement: str = Field(
        ..., description="SPDX ID for SpdxElement.  A related SpdxElement."
    )
    relationshipType: RelationshipType = Field(
        ..., description="Describes the type of relationship between two SPDX elements."
    )


class Document(BaseModel):
    class Config:
        extra = Extra.forbid

    SPDXID: str = Field(
        ...,
        description=(
            "Uniquely identify any element in an SPDX document which may be referenced"
            " by other elements."
        ),
    )
    annotations: Optional[List[Annotation]] = Field(
        default=None, description="Provide additional information about an SpdxElement."
    )
    comment: Optional[str]
    creationInfo: CreationInfo = Field(
        ...,
        description=(
            "One instance is required for each SPDX file produced. It provides the"
            " necessary information for forward and backward compatibility for"
            " processing tools."
        ),
    )
    dataLicense: str = Field(
        ...,
        description=(
            "License expression for dataLicense. See SPDX Annex D for the license"
            " expression syntax.  Compliance with the SPDX specification includes"
            " populating the SPDX fields therein with data related to such fields"
            ' ("SPDX-Metadata"). The SPDX specification contains numerous fields where'
            " an SPDX document creator may provide relevant explanatory text in"
            ' SPDX-Metadata. Without opining on the lawfulness of "database rights" (in'
            " jurisdictions where applicable), such explanatory text is copyrightable"
            " subject matter in most Berne Convention countries. By using the SPDX"
            " specification, or any portion hereof, you hereby agree that any copyright"
            " rights (as determined by your jurisdiction) in any SPDX-Metadata,"
            " including without limitation explanatory text, shall be subject to the"
            " terms of the Creative Commons CC0 1.0 Universal license. For"
            " SPDX-Metadata not containing any copyright rights, you hereby agree and"
            ' acknowledge that the SPDX-Metadata is provided to you "as-is" and without'
            " any representations or warranties of any kind concerning the"
            " SPDX-Metadata, express, implied, statutory or otherwise, including"
            " without limitation warranties of title, merchantability, fitness for a"
            " particular purpose, non-infringement, or the absence of latent or other"
            " defects, accuracy, or the presence or absence of errors, whether or not"
            " discoverable, all to the greatest extent permissible under applicable"
            " law."
        ),
    )
    externalDocumentRefs: Optional[List[ExternalDocumentRef]] = Field(
        default=None,
        description=("Identify any external SPDX documents referenced within this SPDX document."),
    )
    hasExtractedLicensingInfos: Optional[List[HasExtractedLicensingInfo]] = Field(
        default=None,
        description=(
            "Indicates that a particular ExtractedLicensingInfo was defined in the"
            " subject SpdxDocument."
        ),
    )
    name: str = Field(..., description="Identify name of this SpdxElement.")
    revieweds: Optional[List[Reviewed]] = Field(default=None, description="Reviewed")
    spdxVersion: str = Field(
        ...,
        description=(
            "Provide a reference number that can be used to understand how to parse and"
            " interpret the rest of the file. It will enable both future changes to the"
            " specification and to support backward compatibility. The version number"
            " consists of a major and minor version indicator. The major field will be"
            " incremented when incompatible changes between versions are made (one or"
            " more sections are created, modified or deleted). The minor field will be"
            " incremented when backwards compatible changes are made."
        ),
    )
    documentNamespace: Optional[str] = Field(
        default=None,
        description=(
            "The URI provides an unambiguous mechanism for other SPDX documents to"
            " reference SPDX elements within this SPDX document."
        ),
    )
    documentDescribes: Optional[List[str]] = Field(
        default=None,
        description="Packages, files and/or Snippets described by this SPDX document",
    )
    packages: Optional[List[Package]] = Field(
        default=None, description="Packages referenced in the SPDX document"
    )
    files: Optional[List[File]] = Field(
        default=None, description="Files referenced in the SPDX document"
    )
    snippets: Optional[List[Snippet]] = Field(
        default=None, description="Snippets referenced in the SPDX document"
    )
    relationships: Optional[List[Relationship]] = Field(
        default=None, description="Relationships referenced in the SPDX document"
    )
