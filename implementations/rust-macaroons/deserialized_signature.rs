// script arguments: serialized

extern crate macaroons;

use std::env;
use std::string::String;

use macaroons::token::{Token, Tag};

fn to_hex_string(bytes: Vec<u8>) -> String {
  let strs: Vec<String> = bytes.iter()
                               .map(|b| format!("{:01$x}", b, 2))
                               .collect();
  strs.connect("")
}

fn main() {
  let args: Vec<_> = env::args().collect();
  let serialized = args[1].clone().into_bytes();

  let token = Token::deserialize(serialized).unwrap();

  let Tag(sig) = token.tag;

  let signature = to_hex_string(sig.to_vec());

  println!("{}", &signature);
}
