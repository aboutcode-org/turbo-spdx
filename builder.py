#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

PYTHON_TARGET_VERSION = "3.8"


def get_version(arg):
    version = arg[1:] if arg.startswith(("v", "V")) else arg
    return version


def download_schema(version):
    schema_url = (
        f"https://raw.githubusercontent.com/spdx/spdx-spec/v{version}/schemas/spdx-schema.json"
    )

    snake_version = version.replace(".", "_")
    download_directory = f"./spdx_schema_{snake_version}"

    response = requests.get(schema_url)
    schema_location = os.path.join(download_directory, "spdx-schema.json")

    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"No schema found for v{version}.")

    # create download directory if not exists
    if not os.path.isdir(download_directory):
        os.mkdir(download_directory)

    with open(schema_location, "wb") as f:
        f.write(response.content)

    return schema_location


def pre_generation(version):
    snake_version = version.replace(".", "_")
    schema_directory = f"./src/spdx_{snake_version}"
    if not os.path.isdir(schema_directory):
        os.mkdir(schema_directory)

    return f"{schema_directory}/__init__.py"


def generate_data_model(schema_location, output_location):
    command = [
        "datamodel-codegen",
        "--field-include-all-keys",
        "--input-file-type",
        "jsonschema",
        "--reuse-model",
        "--snake-case-field",
        "--target-python-version",
        PYTHON_TARGET_VERSION,
        "--use-double-quotes",
        "--use-standard-collections",
        "--use-subclass-enum",
        "--wrap-string-literal",
        "--use-default-kwarg",
        "--strip-default-none",
        "--class-name",
        "SPDXBom",
        "--input",
        schema_location,
        "--output",
        output_location,
    ]

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Print the stdout and stderr outputs
    print(result.stdout.decode())
    print(result.stderr.decode())


def handler():
    usages = """
Usage: builder [OPTIONS] [VERSION]

  Generate SPDX SBOM model for given schema VERSION.

Options:
  -h, --help   Show this message and exit.
"""

    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(usages)
        return
    version = get_version(sys.argv[1])
    schema_location = download_schema(version)
    output_location = pre_generation(version)
    generate_data_model(schema_location, output_location)


if __name__ == "__main__":
    handler()
