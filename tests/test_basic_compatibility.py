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
    'php-macaroons',
    'rust-macaroons',
]

BasicMacaroonArgs = collections.namedtuple(
    'BasicMacaroonArgs', 'location key id'
)


@functools.lru_cache(typed=True)
def execute_command(implementation, command, args):
    path = os.path.join('implementations', implementation, command)
    if os.path.isfile(path):
        return subprocess.check_output([path] + list(args))
    else:
        pytest.skip(
            "Test not implemented for {impl}".format(impl=implementation)
        )
        return None


@pytest.mark.parametrize("implementation", implementations)
def test_basic_signature_equality(implementation):
    command = 'basic_macaroon_signature'
    args = BasicMacaroonArgs(location='loc', key='key', id='id')
    canonical = execute_command('libmacaroons', command, args)
    result = execute_command(implementation, command, args)
    assert(result == canonical)
