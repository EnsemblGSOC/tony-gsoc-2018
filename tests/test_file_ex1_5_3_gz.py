"""
.. See the NOTICE file distributed with this work for additional information
   regarding copyright ownership.
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
       http://www.apache.org/licenses/LICENSE-2.0
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

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
                    "./tests/test_file_ex1_5_3_gz.yml"])
    subprocess.run(["gzip", "-d", "-f", "./tests/ex1_5_3_gz_test.wig.gz"])
    assert filecmp.cmp("./tests/ex1_5_3_gz_test.wig", "./tests/ex1_5_3.wig")


if __name__ == "__main__":
    test_1()
