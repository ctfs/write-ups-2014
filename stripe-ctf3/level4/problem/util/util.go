package util

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"strings"
	"stripe-ctf.com/sqlcluster/log"
)

func EnsureAbsent(path string) {
	err := os.Remove(path)
	if err != nil && !os.IsNotExist(err) {
		log.Fatal(err)
	}
}

func FmtOutput(out []byte) string {
	o := string(out)
	if strings.ContainsAny(o, "\n") {
		return fmt.Sprintf(`"""
%s"""`, o)
	} else {
		return fmt.Sprintf("%#v", o)
	}
}

func JSONEncode(s interface{}) *bytes.Buffer {
	var b bytes.Buffer
	json.NewEncoder(&b).Encode(s)
	return &b
}

func JSONDecode(body io.Reader, s interface{}) error {
	return json.NewDecoder(body).Decode(s)
}
