import subprocess
import os
import functools
import collections

import pytest

implementations = [
    'libmacaroons',
    'pymacaroons',
    'ruby-macaroons',
    'macaroons-js',
    'go-macaroon',
]

BasicMacaroonArgs = collections.namedtuple('BasicMacaroonArgs', 'location key id')


@functools.lru_cache(typed=True)
def execute_command(implementation, command, args):
    path = os.path.join(implementation, command)
    return subprocess.check_output([path] + list(args)) if os.path.isfile(path) else None


@pytest.mark.parametrize("implementation", implementations)
def test_basic_signature_equality(implementation):
    command = 'basic_macaroon_signature'
    args = BasicMacaroonArgs(location='loc', key='key', id='id')
    canonical = execute_command('libmacaroons', command, args)
    result = execute_command(implementation, command, args)
    assert(result == canonical)
