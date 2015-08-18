// script arguments: location key id
//                   first_party_caveat
//                   third_party_location third_party_key third_party_id
//                   discharge_macaroon
// script output: macaroon bound_discharge
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

    location := args[0]
    key := []byte(args[1])
    id := args[2];
    first_party_caveat := args[3]
    third_party_location := args[4]
    third_party_key := []byte(args[5])
    third_party_id := args[6]
    discharge_macaroon := args[7]

    if m := len(discharge_macaroon) % 4; m != 0 {
      discharge_macaroon += strings.Repeat("=", 4-m)
    }
    decoded_discharge, err := b64.URLEncoding.DecodeString(discharge_macaroon)

    discharge := &macaroon.Macaroon{}
    err = discharge.UnmarshalBinary(decoded_discharge)

    m, err := macaroon.New(key, id, location)

    m.AddFirstPartyCaveat(first_party_caveat)
    m.AddThirdPartyCaveat(third_party_key, third_party_id, third_party_location)

    discharge.Bind(m.Signature())

    serialized, err := m.MarshalBinary()
    encoded := strings.TrimRight(b64.URLEncoding.EncodeToString(serialized), "=")

    serialized_discharge, err := discharge.MarshalBinary()
    encoded_discharge := strings.TrimRight(b64.URLEncoding.EncodeToString(serialized_discharge), "=")

    if err == nil {
      fmt.Printf("%s\n%s\n", encoded, encoded_discharge)
    }
}
