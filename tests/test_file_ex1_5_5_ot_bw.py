"""
Test_1
"""

import filecmp
import subprocess


def test_1():
    """Test_1"""
    subprocess.run(["cwl-runner",
                    r"--outdir=./tests",
                    "./workflow/Retrieve_GC_workflow.cwl",
                    "./tests/test_file_ex1_5_5_ot_bw.yml"])
    subprocess.run(["./bigWigToWig", "./tests/ex1_5_5_ot_bw_test.bw", "./tests/ex1_5_5_ot_bw_test.wig"])
    assert filecmp.cmp("./tests/ex1_5_5_ot_bw_test.wig", "./tests/ex1_5_5_ot_bw.wig")


if __name__ == "__main__":
    test_1()
