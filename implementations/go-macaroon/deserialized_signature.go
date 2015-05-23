// script arguments: serialized

package main

import (
  "os"
  "fmt"
  b64 "encoding/base64"
  "strings"

  "gopkg.in/macaroon.v1"
)


func main() {
    args := os.Args[1:]

    serialized := string([]byte(args[0]))


    if m := len(serialized) % 4; m != 0 {
      serialized += strings.Repeat("=", 4-m)
    }
    decoded, err := b64.URLEncoding.DecodeString(serialized)

    m := &macaroon.Macaroon{}
    err = m.UnmarshalBinary(decoded)

    if err == nil {
      fmt.Printf("%x\n", m.Signature())
    }
}
