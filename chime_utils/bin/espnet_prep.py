import logging

import click

from chime_utils.bin.base import cli
from chime_utils.dprep.espnet import prepare_chime6, prepare_dipco, prepare_mixer6

logging.basicConfig(
    format=(
        "%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d]" " %(message)s"
    ),
    datefmt="%Y-%m-%d:%H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


@cli.group(name="espnet-prep")
def espnet_prep():
    """General utilities for creating and manipulating ESPNet/Kaldi manifests."""
    pass


@espnet_prep.command(name="chime6")
@click.argument("corpus-dir", type=click.Path(exists=True))
@click.argument("output-dir", type=click.Path(exists=False))
@click.option(
    "--dset-part",
    "-d",
    type=str,
    default="train,dev",
    required=False,
    show_default=True,
    help=(
        "For which part of the dataset you want to prepare speechbrain JSON manifests.\n"
        "Choose between 'train','dev' and 'eval'."
        "You can choose multiple by using commas e.g. 'train,dev,eval'."
    ),
)
@click.option(
    "--mic",
    "-m",
    type=str,
    default="mdm",
    required=False,
    show_default=True,
    help=(
        "the microphone type to use, choose from "
        '"ihm" (close-talk) or "mdm" (multi-microphone array) or "all" for both. '
        "For MDM, there are 6 array devices with 4 channels each, "
        "so the resulting recordings will have 24 channels."
    ),
)
@click.option(
    "--json-dir",
    "-j",
    type=click.Path(exists=False),
    required=False,
    default=None,
    show_default=True,
    help=(
        "Override the JSON annotation directory"
        "of the current dataset partition (e.g. dev)"
        "this allows for example to create a manifest from for example a JSON"
        "created with forced alignment available at"
        "https://github.com/chimechallenge/CHiME7_DASR_falign."
    ),
)
@click.option(
    "--use-problematic",
    "-u",
    type=str,
    default=True,
    required=False,
    is_flag=True,
    help=(
        "Whether or not use problematic devices in the manifests creation.\nSee"
        " https://www.chimechallenge.org/challenges/chime6/track1_data, there"
        " are some devices that had recording problems in some sessions."
    ),
)
@click.option(
    "--txt-norm",
    "-t",
    type=str,
    required=False,
    default="chime8",
    show_default=True,
    help=(
        "Which text normalization to use."
        "Choose between 'None', 'chime6', 'chime7' and 'chime8'"
    ),
)
def chime6(
    corpus_dir: str,
    output_dir: str,
    dset_part: str,
    mic: str,
    json_dir=None,
    use_problematic: bool = False,
    txt_norm: str = "chime8",
):
    """
    This function prepares CHiME-6 data to ESPNet/Kaldi manifest format.\n
    CORPUS_DIR: Path to the CHiME-6 root directory.\n
    OUTPUT_DIR: Path to the output directory where the lhotse manifests will be stored.
    """
    dset_part = dset_part.split(",")
    mic = mic.split(",")
    for d in dset_part:
        for m in mic:
            prepare_chime6(
                corpus_dir,
                output_dir,
                d,
                m,
                json_dir,
                use_problematic,
                txt_norm,
            )


@espnet_prep.command(name="dipco")
@click.argument("corpus-dir", type=click.Path(exists=True))
@click.argument("output-dir", type=click.Path(exists=False))
@click.option(
    "--dset-part",
    "-d",
    type=str,
    default="dev",
    required=False,
    show_default=True,
    help=(
        "For which part of the dataset you want to prepare lhotse manifests.\n"
        "Choose between 'dev' and 'eval'."
        "You can choose multiple by using commas e.g. 'dev,eval'."
    ),
)
@click.option(
    "--mic",
    "-m",
    type=str,
    default="mdm",
    required=False,
    show_default=True,
    help=(
        "the microphone type to use, choose from "
        '"ihm" (close-talk) or "mdm" (multi-microphone array) settings. '
        "For MDM, there are 5 array devices with 7 channels each, "
        "so the resulting recordings will have 35 channels."
    ),
)
@click.option(
    "--json-dir",
    "-j",
    type=click.Path(exists=False),
    required=False,
    default=None,
    show_default=True,
    help=(
        "Override the JSON annotation directory"
        "of the current dataset partition (e.g. dev)"
        "this allows for example to create a manifest from for example a JSON"
        "created with forced alignment available at"
        "https://github.com/chimechallenge/CHiME7_DASR_falign."
    ),
)
@click.option(
    "--txt-norm",
    "-t",
    type=str,
    required=False,
    default="chime8",
    show_default=True,
    help=(
        "Which text normalization to use."
        "Choose between 'None', 'chime6', 'chime7' and 'chime8'"
    ),
)
def dipco(
    corpus_dir: str,
    output_dir: str,
    dset_part: str,
    mic: str,
    json_dir=None,
    txt_norm: str = "chime8",
):
    """
    This function prepares DiPCo data to Kaldi manifest format.\n
    CORPUS_DIR: Path to the DiPCo root directory.\n
    OUTPUT_DIR: Path to the output directory where the lhotse manifests will be stored.
    """
    dset_part = dset_part.split(",")
    mic = mic.split(",")
    for d in dset_part:
        for m in mic:
            prepare_dipco(corpus_dir, output_dir, d, m, json_dir, txt_norm)


@espnet_prep.command(name="mixer6")
@click.argument("corpus-dir", type=click.Path(exists=True))
@click.argument("output-dir", type=click.Path(exists=False))
@click.option(
    "--dset-part",
    "-d",
    type=str,
    default="dev",
    required=False,
    show_default=True,
    help=(
        "For which part of the dataset you want to prepare lhotse manifests.\n"
        "Choose between 'train_weak_intv','train_weak_call', 'dev' and 'eval'."
        "You can choose multiple by using commas e.g. 'dev,eval'."
    ),
)
@click.option(
    "--mic",
    "-m",
    type=str,
    default="mdm",
    required=False,
    show_default=True,
    help=(
        "the microphone type to use, choose from "
        '"ihm" (close-talk) or "mdm" (multi-microphone array) settings. '
        "For MDM, there are 11 heterogeneous devices."
    ),
)
@click.option(
    "--json-dir",
    "-j",
    type=click.Path(exists=False),
    required=False,
    default=None,
    show_default=True,
    help=(
        "Override the JSON annotation directory"
        "of the current dataset partition (e.g. dev)"
        "this allows for example to create a manifest from for example a JSON"
        "created with forced alignment available at"
        "https://github.com/chimechallenge/CHiME7_DASR_falign."
    ),
)
@click.option(
    "--txt-norm",
    "-t",
    type=str,
    required=False,
    default="chime8",
    show_default=True,
    help=(
        "Which text normalization to use."
        "Choose between 'None', 'chime6', 'chime7' and 'chime8'"
    ),
)
def mixer6(
    corpus_dir: str,
    output_dir: str,
    dset_part: str,
    mic: str,
    json_dir=None,
    txt_norm: str = "chime8",
):
    """
    This function prepares Mixer 6 Speech data to Kaldi manifest format.\n
    CORPUS_DIR: Path to the Mixer 6 Speech root directory.\n
    OUTPUT_DIR: Path to the output directory where the lhotse manifests will be stored.
    """
    dset_part = dset_part.split(",")
    mic = mic.split(",")
    for d in dset_part:
        for m in mic:
            prepare_mixer6(corpus_dir, output_dir, d, m, json_dir, txt_norm)
