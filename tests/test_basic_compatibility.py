import subprocess
import os
import functools
import itertools

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


def impl_permutations():
    return itertools.permutations(implementations, 2)


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
    canonical_result = execute_command(canonical or 'libmacaroons', command, args)
    result = execute_command(implementation, command, args)
    assert(result == canonical_result)


def are_interoperable(source_impl, source_command, source_args, dest_impl, dest_command, canonical=None):
    canonical_result = piped_result(
        canonical or 'libmacaroons', source_command, source_args,
        canonical or 'libmacaroons', dest_command
    )
    dest_result = piped_result(source_impl, source_command, source_args, dest_impl, dest_command)
    assert(dest_result == canonical_result)


def piped_result(source_impl, source_command, source_args, dest_impl, dest_command):
    source_result = execute_command(source_impl, source_command, source_args)
    dest_args = tuple(source_result.decode('ascii').split('\n'))
    dest_result = execute_command(dest_impl, dest_command, dest_args)
    return dest_result


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


@pytest.mark.parametrize("implementation", implementations)
def test_basic_serialization_equality(implementation):
    command = 'basic_macaroon_serialized'
    args = ('loc', 'key', 'id')
    equal_to_canonical(implementation, command, args)


@pytest.mark.parametrize("source_impl,dest_impl", impl_permutations())
def test_basic_deserialization_interoperability(source_impl, dest_impl):
    source_command = 'basic_macaroon_serialized'
    source_args = ('loc', 'key', 'id')
    dest_command = 'deserialized_signature'
    are_interoperable(
        source_impl, source_command, source_args,
        dest_impl, dest_command
    )


@pytest.mark.parametrize("source_impl,dest_impl", impl_permutations())
def test_basic_first_party_caveat_verification(source_impl, dest_impl):
    source_command = 'first_party_macaroon_serialized'
    source_args = ('loc', 'key', 'id', 'first_party')
    dest_command = 'verify_first_party_macaroon'
    are_interoperable(
        source_impl, source_command, source_args,
        dest_impl, dest_command
    )


@pytest.mark.parametrize("discharge_impl,macaroon_impl,verify_impl",
                         itertools.combinations_with_replacement(implementations, 3))
def test_third_party_caveat_verification(discharge_impl,
                                         macaroon_impl,
                                         verify_impl):
    discharge_location = 'discharge_loc'
    discharge_key = 'discharge_key'
    discharge_id = 'discharge_id'
    discharge_first_party = 'discharge_first_party'
    first_party = 'first_party'
    key = 'key'

    discharge_command = 'first_party_macaroon_serialized'
    discharge_args = (
        discharge_location, discharge_key, discharge_id, discharge_first_party
    )
    discharge_macaroon, _, _, _ = execute_command(
        discharge_impl, discharge_command, discharge_args
    ).decode('ascii').split('\n')

    macaroon_command = 'third_party_macaroon_serialized'
    macaroon_args = (
        'loc', key, 'id', first_party,
        discharge_location, discharge_key, discharge_id, discharge_macaroon
    )
    serialized_macaroon, bound_discharge, _ = execute_command(
        macaroon_impl, macaroon_command, macaroon_args
    ).decode('ascii').split('\n')

    verify_command = 'verify_third_party_macaroon'
    verify_args = (
        serialized_macaroon, bound_discharge, key,
        first_party, discharge_first_party
    )
    verified, _ = execute_command(
        verify_impl, verify_command, verify_args
    ).decode('ascii').split('\n')

    assert(verified == "True")
