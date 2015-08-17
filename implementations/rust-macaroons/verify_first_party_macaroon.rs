// script arguments: serialized key first_party_caveat

extern crate macaroons;

use std::env;

use macaroons::token::Token;
use macaroons::verifier::Verifier;
use macaroons::caveat::Predicate;

fn main() {
  let args: Vec<_> = env::args().collect();
  let serialized = args[1].clone().into_bytes();
  let key = args[2].clone().into_bytes();
  let first_party = args[3].clone().into_bytes();

  let token = Token::deserialize(serialized).unwrap();

  let verifier = Verifier::new(|_predicate| {
    let predicate = _predicate.clone();
    let Predicate(predicate_value) = predicate;
    predicate_value == first_party
  });

  if verifier.verify(&key, &token) {
      println!("True");
  } else {
      println!("False");
  }
}
