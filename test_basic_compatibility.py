import subprocess
import os
import functools

implementations = [
    'libmacaroons',
    'pymacaroons',
    'ruby-macaroons',
    'macaroons-js',
]


class NonCanonicalMacaroonException(Exception):
    pass


def all_results_equal(command, args):
    paths = {
        impl: os.path.join(impl, command)
        for impl in implementations
    }
    results = {
        impl: subprocess.check_output([path] + args)
        if os.path.isfile(path) else None
        for impl, path in paths.items()
    }
    canonical = results['libmacaroons']
    for impl, r in results.items():
        if r and r != canonical:
            raise NonCanonicalMacaroonException(
                '{impl} {command} differs from canonical.'
                '\nExpected: {ex}\nGot: {got}'.format(
                    impl=impl, command=command, ex=canonical, got=r
                )
            )
    return True


def test_basic_macaroon_equality():
    command = 'create_basic_macaroon'
    args = ['loc', 'key', 'id']
    assert(all_results_equal(command, args))
