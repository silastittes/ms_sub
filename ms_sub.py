from dataclasses import dataclass
from typing import Dict, List, Tuple, Set
import argparse
import sys


class MS:
    """
    Structure to represent ms simulator's output format
    """

    def __init__(self, file: str):
        with open(file) as d:
            self.command = d.readline().strip()
            self.seeds = d.readline().strip()
            _ = d.readline().strip()
            _ = d.readline().strip()
            self.segs = d.readline().strip()
            if not self.segs.startswith("segsites:"):
                raise ValueError(
                    "ms input file does not contains segsites on line 5. Verify input file format."
                )
            self.positions = d.readline().strip()
            if not self.positions.startswith("positions:"):
                raise ValueError(
                    "ms input file does not contains positions on line 6. Verify input file format"
                )
            self.haps: Dict[int, str] = dict()
            hap_idx = 0
            for line in d:
                if line.strip():
                    ln = line.strip()
                    self.haps[hap_idx] = ln
                    hap_idx += 1

    def sub_haps(self, hap_idx: List[int]) -> Dict[int, str]:
        """
        subset the dictionary of haplotypes
        """
        item_list = list(self.haps.items())
        return dict([item_list[i] for i in hap_idx])


class HAP:
    """
    Generate a ms object with a subset of haplotypes
    """

    def __init__(self, ms: MS, hap_idx: List[int]):
        self.haps = ms.sub_haps(hap_idx)
        self.pos_list = ms.positions.split(":")[1:][0].split()
        self.command = ms.command.split()[0]
        self.seeds = ms.seeds
        # get the index of where along haplotype variables sites occur
        self.variable_positions: List[int] = []
        for (idx, _) in enumerate(self.pos_list):
            pos_set: Set[str] = set()
            for (_, hap) in self.haps.items():
                pos_set.add(hap[idx])  # add 0 or 1 at current locus to SET (not list)
            if len(pos_set) > 1:
                self.variable_positions.append(idx)
        self.pos_str = " ".join([self.pos_list[i] for i in self.variable_positions])

    def write_sub(self, ms: MS, file_name: str):
        with open(file_name, "w") as f:
            size = len(self.haps.keys())
            print(f"{self.command} {size} 1", file=f)
            print(f"{self.seeds}", file=f)
            print("", file=f)
            print("//", file=f)
            print(f"segsites: {len(self.variable_positions)}", file=f)
            print(f"positions: {self.pos_str}", file=f)
            for seq in self.haps.values():
                print("".join([seq[i] for i in self.variable_positions]), file=f)


def parse_args(args):
    """
    argument parsing
    """
    # Instantiate the parser
    parser = argparse.ArgumentParser(description="Split ms output in two!")
    # ms file input
    parser.add_argument(
        "ms_file",
        type=str,
        help="File containing ms output -- assumes no line for a tree string.",
    )
    # prefix
    parser.add_argument(
        "--prefix",
        "-p",
        type=str,
        required=True,
        help="""The output prefix to using when generating the output files""",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    my_ms = MS(args.ms_file)
    hap_ids = list(my_ms.haps.keys())
    myhap = HAP(my_ms, hap_ids[: len(hap_ids) // 2])
    myhap.write_sub(my_ms, f"{args.prefix}_1.txt")
    myhap2 = HAP(my_ms, hap_ids[len(hap_ids) // 2 :])
    myhap2.write_sub(my_ms, f"{args.prefix}_2.txt")
