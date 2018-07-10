"""
Test_1
"""

import filecmp
import subprocess


def test_1():
    """Test_1"""
    subprocess.run(["cwl-runner",
                    "../workflow/Retrieve_GC_workflow.cwl",
                    "./test_file_ex1_5_5_gz_ot.yml"])
    subprocess.run(["gzip", "-d", "-f", "./tests/ex2_5_5_gz_ot_test.wig.gz"])
    assert filecmp.cmp("./tests/ex2_5_5_gz_ot_test.wig", "./tests/ex2_5_5.wig")


if __name__ == "__main__":
    test_1()