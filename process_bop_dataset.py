# For Industrial

import os
from pathlib import Path
import argparse
import subprocess


def run_command(cmd: str) -> None:
    """
    Executes a shell command and raises an error if it fails.
    """
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed with return code {result.returncode}: {cmd}")


def process_bop_dataset(local_dir: str, dataset_name: str, nprocs: int = 10) -> None:
    """
    Processes a BOP-format dataset by:
    1. Converting from scenewise to imagewise format.
    2. Converting from imagewise to WebDataset format.
    
    Args:
        local_dir (str): Path to the root directory of the BOP-format dataset.
        dataset_name (str): Name of the dataset (e.g., "ours").
        nprocs (int): Number of processes to use for conversions.
    """
    local_dir = Path(local_dir)
    tmp_dir = local_dir / "tmp"

    local_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir.mkdir(parents=True, exist_ok=True)

    if dataset_name in ["tless", "hb"]:
        split = "test_primesense"
    else:
        split = "test"

    split_dir = local_dir / split
    tmp_imagewise_dir = tmp_dir / f"{dataset_name}_image_wise" / split
    tmp_imagewise_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Convert from scenewise to imagewise
    imagewise_cmd = (
        f"python -m src.scripts.convert_scenewise_to_imagewise "
        f"--input {split_dir} --output {tmp_imagewise_dir} --nprocs {nprocs}"
    )
    run_command(imagewise_cmd)

    # Step 2: Convert from imagewise to WebDataset
    webdataset_cmd = (
        f"python -m src.scripts.convert_imagewise_to_webdataset "
        f"--input {tmp_imagewise_dir} --output {split_dir}"
    )
    if dataset_name in ["tless", "ycbv", "tudl", "itodd"]:
        webdataset_cmd += f" --nprocs {nprocs}"

    run_command(webdataset_cmd)

    print(f"Processing complete. WebDataset output is in: {split_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a BOP-format dataset.")
    parser.add_argument("--local_dir", required=True, help="Path to the BOP-format dataset directory.")
    parser.add_argument("--dataset_name", required=True, help="Name of the dataset (e.g., 'ours').")
    parser.add_argument("--nprocs", type=int, default=10, help="Number of processes for conversion.")
    args = parser.parse_args()

    process_bop_dataset(args.local_dir, args.dataset_name, args.nprocs)
