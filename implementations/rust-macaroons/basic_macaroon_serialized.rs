// script arguments: location key id

extern crate macaroons;

use std::env;
use std::string::String;

use macaroons::token::{Token};

fn main() {
  let args: Vec<_> = env::args().collect();
  let location = args[1].clone().into_bytes();
  let key = args[2].clone().into_bytes();
  let id = args[3].clone().into_bytes();

  let token = Token::new(&key, id, location);
  let serialized = String::from_utf8(token.serialize()).unwrap();

  println!("{}", &serialized);
}
