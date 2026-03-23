import os
import sys
from unittest.mock import mock_open, patch

# Add the directory containing LibsXMLGenerator.py to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import LibsXMLGenerator


@patch("builtins.open", new_callable=mock_open)
def test_write_file(mock_file):
    name = "TestLib"
    version = "1.0.0"

    LibsXMLGenerator.writeFile(name, version)

    mock_file.assert_called_once_with("library_testlib_strings.xml", "w")

    handle = mock_file()

    expected_writes = [
        '<?xml version="1.0" encoding="utf-8"?>\n',
        '<resources> \n',
        '	<string name="define_int_TestLib"></string>\n',
        '	<!-- Author section -->\n',
        '	<string name="library_TestLib_author"></string>\n',
        '	<string name="library_TestLib_authorWebsite"></string>\n',
        '	<!-- Library section -->\n',
        '	<string name="library_TestLib_libraryName">TestLib</string>\n',
        '	<string name="library_TestLib_libraryDescription"></string>\n',
        '	<string name="library_TestLib_libraryWebsite"></string>\n',
        '	<string name="library_TestLib_libraryVersion">1.0.0</string>\n',
        '	<!-- OpenSource section -->\n',
        '	<string name="library_TestLib_isOpenSource">true</string>\n',
        '	<string name="library_TestLib_repositoryLink"></string>\n',
        '	<!-- License section -->\n',
        '	<string name="library_TestLib_licenseId"></string>\n',
        '</resources> \n'
    ]

    for write_call in expected_writes:
        handle.write.assert_any_call(write_call)

    assert handle.write.call_count == len(expected_writes)
