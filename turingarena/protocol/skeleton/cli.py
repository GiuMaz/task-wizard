"""TuringArena protocol skeleton generator.

Usage:
  skeleton [options]
"""

import docopt

from turingarena.protocol.skeleton import install_skeleton


def protocol_skeleton_cli(*, argv, protocol_id):
    args = docopt.docopt(__doc__, argv=argv)
    install_skeleton(protocol_id=protocol_id)
