// script arguments: location key id caveat_id

extern crate macaroons;

use std::env;
use std::string::String;

use macaroons::token::Token;
use macaroons::caveat::{Caveat, Predicate};


fn main() {
  let args: Vec<_> = env::args().collect();
  let location = args[1].clone().into_bytes();
  let key = args[2].clone().into_bytes();
  let id = args[3].clone().into_bytes();
  let caveat_id = args[4].clone().into_bytes();

  let mut token = Token::new(&key, id, location);
  token = token.add_caveat(Caveat::new(Predicate(caveat_id)));
  let serialized = String::from_utf8(token.serialize()).unwrap();

  println!("{}", &serialized);
  println!("{}", args[2].clone());
  println!("{}", args[4].clone());

}
