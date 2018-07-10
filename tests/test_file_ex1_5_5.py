"""
Test_1
"""

import filecmp
import subprocess


def test_1():
    """Test_1"""
    subprocess.run(["cwl-runner",
                    "../workflow/Retrieve_GC_workflow.cwl",
                    "./test_file_ex1_5_5.yml"])
    assert filecmp.cmp("./tests/ex1_5_5_test.wig", "./tests/ex1_5_5.wig")



if __name__ == "__main__":
    test_1()
