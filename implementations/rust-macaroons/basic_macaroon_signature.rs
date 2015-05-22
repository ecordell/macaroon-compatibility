// script arguments: location key id

extern crate macaroons;

use std::env;
use std::string::String;

use macaroons::token::{Token, Tag};

fn to_hex_string(bytes: Vec<u8>) -> String {
  let strs: Vec<String> = bytes.iter()
                               .map(|b| format!("{:x}", b))
                               .collect();
  strs.connect("")
}

fn main() {
  let args: Vec<_> = env::args().collect();
  let location = args[1].clone().into_bytes();
  let key = args[2].clone().into_bytes();
  let id = args[3].clone().into_bytes();


  let token = Token::new(key, id, location);
  let Tag(sig) = token.tag;

  let signature = to_hex_string(sig.to_vec());

  println!("{}", &signature);
}
