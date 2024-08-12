import os
import pytest
import tempfile
from pyls import get_descriptions_of_files_in_dir, display_results
import argparse

@pytest.fixture
def setup_test_directory():
    """Setup a temporary directory with some test files and directories."""
    test_dir = tempfile.TemporaryDirectory()
    os.mkdir(os.path.join(test_dir.name, "testdir"))
    with open(os.path.join(test_dir.name, "testfile.txt"), 'w') as f:
        f.write("This is a test file.")
    with open(os.path.join(test_dir.name, "testscript.sh"), 'w') as f:
        f.write("#!/bin/bash\necho Hello")
    os.chmod(os.path.join(test_dir.name, "testscript.sh"), 0o755)
    yield test_dir.name
    test_dir.cleanup()

def test_get_descriptions_of_files_in_dir_basic(setup_test_directory):
    """Test without any flags."""
    args = argparse.Namespace(dirname=setup_test_directory, long_format=False, filetype=False)
    results = get_descriptions_of_files_in_dir(args)
    assert len(results) == 3
    assert any(entry['filename'] == "testfile.txt" for entry in results)
    assert any(entry['filename'] == "testdir" for entry in results)
    assert any(entry['filename'] == "testscript.sh" for entry in results)