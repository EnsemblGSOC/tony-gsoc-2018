"""
test_error_ex3.py
Test if a TypeError is correctly raised when a non-fasta file is given to the GC program.
"""

import subprocess


def test_error_ex3():
    """test_error_ex3"""
    subprocess.run(["echo", ])

    result = subprocess.run(["python3", "./GC_analysis/GC_analysis.py",
                             "-i", "./tests/ex3.fasta",
                             "-o", "./tests/ex3.fasta.wig",
                             "-w", "5",
                             "-s", "5"], stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    assert result.stderr.split(b"\n")[-2] == b"TypeError"

    assert result.returncode == 1

    assert result.stdout[-28:] == b" contains no sequence data.\n"


if __name__ == "__main__":
    test_error_ex3()
