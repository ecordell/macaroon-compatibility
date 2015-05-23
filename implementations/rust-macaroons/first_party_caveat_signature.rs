// script arguments: location key id caveat_id

extern crate macaroons;

use std::env;
use std::string::String;

use macaroons::token::{Token, Tag};
use macaroons::caveat::{Caveat, Predicate};

fn to_hex_string(bytes: Vec<u8>) -> String {
  let strs: Vec<String> = bytes.iter()
                               .map(|b| format!("{:01$x}", b, 2))
                               .collect();
  strs.connect("")
}

fn main() {
  let args: Vec<_> = env::args().collect();
  let location = args[1].clone().into_bytes();
  let key = args[2].clone().into_bytes();
  let id = args[3].clone().into_bytes();
  let caveat_id = args[4].clone().into_bytes();

  let mut token = Token::new(key, id, location);
  token = token.add_caveat(Caveat::new(Predicate(caveat_id)));

  let Tag(sig) = token.tag;

  let signature = to_hex_string(sig.to_vec());

  println!("{}", &signature);
}
