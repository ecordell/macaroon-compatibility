// script arguments: location key id

package main

import (
  "os"
  "fmt"

  "gopkg.in/macaroon.v1"
)


func main() {
    args := os.Args[1:]

    key := []byte(args[1])

    m, err := macaroon.New(key, args[2], args[0])

    if err == nil {
      fmt.Printf("%x\n", m.Signature())
    }
}
