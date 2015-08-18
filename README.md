# Macaroon Compatibility Tests

This contains tests that compare different macaroon libraries for compatibility. 

The tests are written in Python, and create subprocesses that communicate with various language's implementations of macaroons.

Eventually this will generate some nice reports that will be hosted on Github Pages - until then, here's a quick overview:

Tested Implementations:

 - [libmacaroons](https://github.com/rescrv/libmacaroons) (considered the 'reference' in most situations)
 - [go-macaroon](https://github.com/go-macaroon/macaroon)
 - [macaroons.js](https://github.com/nitram509/macaroons.js)
 - [php-macaroons](https://github.com/immense/php-macaroons)
 - [pymacaroons](https://github.com/ecordell/pymacaroons)
 - [ruby-macaroons](https://github.com/localmed/ruby-macaroons)
 - [rust-macaroons](https://github.com/cryptosphere/rust-macaroons)

Compatibility Results:

 - **Basic Signatures Matching** *Given a location, key, and identifier, all libraries should output the same signature for a macaroon.*
    + ✔ All Passing
 - **First Party Caveat Signatures Matching** *Given a location, key, identifier, and one predicate, all libraries should output the same signature for a macaroon with a single first party caveat.*
    + ✔ All Passing
 - **Basic Binary Serialization** *Given a simple macaroon with a location, key, and id, all libraries should output the same serialized form.*
     + ✔ All Passing
 - **Deserialization of Serialized Macaroon (Signature)** *A macaroon serialized with one library should be deserialized without error by all other macaroon libraries, and the signature should be unchanged*
     + ✔ All Passing
 - **Verifying a Macaroon with a First Party Caveat** *A macaroon with a first party caveat serialized with one library should be deserialized and verified by all other macaroon libraries.*
     + ✔ All Passing
 - **Verifying a Macaroon with a Third Party Caveat** *A macaroon with a third party caveat created with one library and a discharge macaroon issued by another library, should be deserialized and verified by all other macaroon libraries.*
     + ✔ Passing
         * libmacaroons
         * pymacaroons
         * ruby-macaroons
         * macaroons-js
         * php-macaroons
     + - Skipped (tests not yet implemented)
         * go-macaroons
     + ✘ Failing
         * rust-macaroons (Third Party Caveats and Verification unimplemented)

You can also view the [raw test report](https://rawgit.com/ecordell/macaroon-compatibility/master/report.html) (may take some time to grok).

# Details

Each implementation has its own folder containing executable files - one per test. Each test file accepts arguments and should write the result to stdout. The test runner pipes the same arguments to each test in each implementation and compares the results.

# Contributing

Contributions very welcome! There are three main things to help with:

 - Adding tests for a new Macaroon implementation. This may involve adding a new language to the Dockerfile, adding dependencies, and setting up an environment for tests to run.
 - Adding new tests. It's always better to have more coverage. Ideally, every implementation will have a full set of tests.
 - Improving test implementations. I'm not an expert in all of the languages that are being tested - it would be good if these tests were also good, canonical examples of Macaroon libarary usage in their respective languages.
