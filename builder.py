#
# Copyright (c) nexB Inc. and others. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/turbo-spdx for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

import os
import subprocess
import sys

import requests

SPDX_SCHEMA_URL = (
    "https://raw.githubusercontent.com/spdx/spdx-spec/v{version}/schemas/spdx-schema.json"
)
TEMP_SCHEMA_DIR = "./spdx_schema_{version}"

MODEL_DIR = "./src/turbo_spdx/spdx_{version}"
MODEL_PYTHON_TARGET_VERSION = "3.8"
MODEL_CLASS_NAME = "Document"


def download_schema(version: str) -> str:
    """
    Download the SPDX schema file of a specific version from SPDX_SCHEMA_URL,
    and save it to a temporary directory. If the schema file already exists,
    return the path of the existing file.

    Parameters:
        version (str): The version of the SPDX schema to download.

    Returns:
        str: The path to the downloaded SPDX schema.

    Raises:
        requests.exceptions.HTTPError: If the request to the
            SPDX_SCHEMA_URL returns a non-200 status code.
    """
    schema_url = SPDX_SCHEMA_URL.format(version=version)

    snake_version = version.replace(".", "_")
    download_directory = TEMP_SCHEMA_DIR.format(version=snake_version)

    response = requests.get(schema_url)
    schema_location = os.path.join(download_directory, "spdx-schema.json")

    if os.path.isfile(schema_location):
        return schema_location

    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"No schema found for v{version}.")

    # Create download directory if not exists
    if not os.path.isdir(download_directory):
        os.mkdir(download_directory)

    with open(schema_location, "wb") as f:
        f.write(response.content)

    return schema_location


def pre_generation(version: str) -> str:
    """
    Create directory for the SPDX schema model corresponding to the given version.

    Parameters:
        version (str): Version of the SPDX schema model.

    Returns:
        str: The path to the '__init__.py' file in the created directory.
    """
    model_version = version.replace(".", "")
    schema_directory = MODEL_DIR.format(version=model_version)

    if not os.path.isdir(schema_directory):
        os.mkdir(schema_directory)

    return f"{schema_directory}/__init__.py"


def generate_data_model(schema_location: str, output_location: str) -> None:
    """
    Generate a data model from the SPDX schema file, and save the output at
    output_location.

    Parameters:
        schema_location (str): Path to the SPDX schema.
        output_location (str): Path to save the generated data model.

    Returns:
        None
    """
    command = [
        "datamodel-codegen",
        "--field-include-all-keys",
        "--input-file-type",
        "jsonschema",
        "--reuse-model",
        # "--snake-case-field",
        "--target-python-version",
        MODEL_PYTHON_TARGET_VERSION,
        "--use-double-quotes",
        # "--use-standard-collections",
        "--use-subclass-enum",
        "--wrap-string-literal",
        "--use-default-kwarg",
        "--strip-default-none",
        "--disable-timestamp",
        "--class-name",
        MODEL_CLASS_NAME,
        "--input",
        schema_location,
        "--output",
        output_location,
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Print the stdout and stderr outputs
    print(result.stdout.decode())
    print(result.stderr.decode())


def add_copyright(file: str) -> None:
    """
    Prepend copyright to a file.

    Parameters:
        file (str): The file to prepend to.

    Returns:
        None
    """
    with open(__file__, "r") as f:
        copyright = "".join([next(f) for x in range(7)])

    with open(file, "r") as f:
        # Skip the header
        for i in range(2):
            next(f)
        # Read the remaining contents of the file
        model_code = f.read()

        with open("tempFile", "w") as f2:
            f2.write(copyright)
            f2.write(model_code)

    os.remove(file)
    os.rename("tempFile", file)


def post_generation(output_location: str) -> None:
    """
    Run post-generation tasks on the generated data model.

    Parameters:
        output_location (str): Path to the generated data model file.

    Returns:
        None
    """

    # Add copyright
    add_copyright(output_location)

    # Fix code style
    run_black = subprocess.run(
        ["venv/bin/black", "-l", "100", output_location],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    print(run_black.stdout.decode())
    print(run_black.stderr.decode())

    run_isort = subprocess.run(
        ["venv/bin/isort", "--profile", "black", "--sl", "-l", "100", output_location],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    print(run_isort.stdout.decode())
    print(run_isort.stderr.decode())


def strip_leading_v(version: str) -> str:
    """
    Strip leading "v" or "V" character from version.

    Parameters:
        version (str): A string representing version.

    Returns:
        str: Version with any leading "v" or "V" character removed.
    """
    striped_version = version[1:] if version.startswith(("v", "V")) else version
    return striped_version


def help():
    return """
Usage: builder [OPTIONS] [VERSION]

  Generate SPDX SBOM model for given schema VERSION.

Options:
  -h, --help   Show this message and exit.
"""


def handler():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(help())
        return
    version = strip_leading_v(sys.argv[1])
    schema_location = download_schema(version)
    output_location = pre_generation(version)
    generate_data_model(schema_location, output_location)
    post_generation(output_location)


if __name__ == "__main__":
    handler()
