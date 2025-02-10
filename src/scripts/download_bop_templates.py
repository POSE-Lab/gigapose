import os
from pathlib import Path
import hydra
from omegaconf import DictConfig
from src.utils.logging import get_logger

logger = get_logger(__name__)


@hydra.main(
    version_base=None,
    config_path="../../configs",
    config_name="train",
)
def download(cfg: DictConfig) -> None:
    root_dir = Path(cfg.machine.root_dir)
    source_url = (
        "https://huggingface.co/datasets/nv-nguyen/gigaPose/resolve/main/templates.zip"
    )
    tmp_dir = root_dir / "datasets/tmp"
    templates_dir = root_dir / "datasets/templates"
    os.makedirs(tmp_dir, exist_ok=True)

    zip_file_path = tmp_dir / "templates.zip"
    download_cmd = f"wget -O {zip_file_path} {source_url}"
    logger.info(f"Running {download_cmd}")
    os.system(download_cmd)

    if not zip_file_path.exists():
        logger.error("Failed to download templates.zip. Exiting.")
        return

    unzip_cmd = f"unzip {zip_file_path} -d {tmp_dir}"
    logger.info(f"Running {unzip_cmd}")
    os.system(unzip_cmd)

    unzipped_templates_dir = tmp_dir / "templates"
    if not unzipped_templates_dir.exists():
        logger.error(
            f"The directory {unzipped_templates_dir} was not found after unzipping. "
            "Please check the structure of the zip file."
        )
        return
    os.makedirs(templates_dir.parent, exist_ok=True)
    os.rename(unzipped_templates_dir, templates_dir)
    logger.info(f"Templates successfully moved to {templates_dir}")

if __name__ == "__main__":
    download()
