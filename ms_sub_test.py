import unittest
import os
from ms_sub import *


class TestSum(unittest.TestCase):
    def test_ms(self):
        test_file = "/tmp/ms.txt"
        with open(test_file, "w") as f:
            print("ms 2 1 -t 20", file=f)
            print("1389976535 449630748", file=f)
            print("", file=f)
            print("//", file=f)
            print("segsites: 4", file=f)
            print("positions: 0.016227 0.157615 0.169632 0.946270", file=f)
            print("0110", file=f)
            print("1010", file=f)

        my_ms = MS(test_file)
        self.assertEqual(my_ms.command, "ms 2 1 -t 20")
        self.assertEqual(
            my_ms.positions, "positions: 0.016227 0.157615 0.169632 0.946270"
        )
        self.assertEqual(my_ms.segs, "segsites: 4")
        hap_check = {0: "0110", 1: "1010"}
        self.assertEqual(my_ms.haps, hap_check)
        sub_hap1 = HAP(my_ms, [0, 1])
        sub_hap2 = HAP(my_ms, [0, 1])
        self.assertEqual(sub_hap1.haps, hap_check)
        self.assertEqual(sub_hap2.haps, hap_check)
        self.assertEqual(sub_hap1.variable_positions, [0, 1])
        self.assertEqual(sub_hap1.pos_str, "0.016227 0.157615")
        os.remove("/tmp/ms.txt")


if __name__ == "__main__":
    unittest.main()
