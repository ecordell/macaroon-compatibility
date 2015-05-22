import subprocess
import os
import functools

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


def equal_to_canonical(implementation, command, args, canonical=None):
    canonical = canonical or execute_command('libmacaroons', command, args)
    result = execute_command(implementation, command, args)
    assert(result == canonical)


@pytest.mark.parametrize("implementation", implementations)
def test_basic_signature_equality(implementation):
    command = 'basic_macaroon_signature'
    args = ('loc', 'key', 'id')
    equal_to_canonical(implementation, command, args)


@pytest.mark.parametrize("implementation", implementations)
def test_first_party_caveat_signature(implementation):
    command = 'first_party_caveat_signature'
    args = ('loc', 'key', 'id', 'first_party')
    equal_to_canonical(implementation, command, args)
