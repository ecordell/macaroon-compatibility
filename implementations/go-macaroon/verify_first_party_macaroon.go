// script arguments: serialized key caveat

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
    key := []byte(args[1])
    caveat := args[2]

    if m := len(serialized) % 4; m != 0 {
      serialized += strings.Repeat("=", 4-m)
    }
    decoded, err := b64.URLEncoding.DecodeString(serialized)

    m := &macaroon.Macaroon{}
    err = m.UnmarshalBinary(decoded)

    check := func(cav string) error {
      if cav == caveat {
        return nil
      }
      return fmt.Errorf("Caveat Unmet")
    }

    if err == nil {
      err := m.Verify(key, check, nil)
      if err == nil {
        fmt.Printf("True\n")
      } else {
        fmt.Printf("False\n")
      }
    }
}
