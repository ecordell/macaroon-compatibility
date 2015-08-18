// script arguments: serialized_macaroon discharge_macaroon key
//                   first_party_caveat discharge_first_party

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

    serialized_macaroon := string([]byte(args[0]))
    discharge_macaroon := string([]byte(args[1]))
    key := []byte(args[2])
    first_party_caveat := args[3]
    discharge_first_party := args[4]


    if m := len(serialized_macaroon) % 4; m != 0 {
      serialized_macaroon += strings.Repeat("=", 4-m)
    }
    decoded, err := b64.URLEncoding.DecodeString(serialized_macaroon)

    if m := len(discharge_macaroon) % 4; m != 0 {
      discharge_macaroon += strings.Repeat("=", 4-m)
    }
    decoded_discharge, err := b64.URLEncoding.DecodeString(discharge_macaroon)

    m := &macaroon.Macaroon{}
    err = m.UnmarshalBinary(decoded)

    discharge := &macaroon.Macaroon{}
    err = discharge.UnmarshalBinary(decoded_discharge)

    check := func(cav string) error {
      if cav == first_party_caveat || cav == discharge_first_party {
        return nil
      }
      return fmt.Errorf("Caveat Unmet")
    }

    if err == nil {
      err := m.Verify(key, check, []*macaroon.Macaroon{discharge})
      if err == nil {
        fmt.Printf("True\n")
      } else {
        fmt.Println(err)
      }
    }
}
