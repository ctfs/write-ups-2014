package sql

import (
	"bytes"
	"os/exec"
	"strings"
	"stripe-ctf.com/sqlcluster/log"
	"sync"
	"syscall"
)

type SQL struct {
	path           string
	sequenceNumber int
	mutex          sync.Mutex
}

type Output struct {
	Stdout         []byte
	Stderr         []byte
	SequenceNumber int
}

func NewSQL(path string) *SQL {
	sql := &SQL{
		path: path,
	}
	return sql
}

func getExitstatus(err error) int {
	exiterr, ok := err.(*exec.ExitError)
	if !ok {
		return -1
	}

	status, ok := exiterr.Sys().(syscall.WaitStatus)
	if !ok {
		return -1
	}

	return status.ExitStatus()
}

func (sql *SQL) Execute(tag string, command string) (*Output, error) {
	// TODO: make sure I can catch non-lock issuez
	sql.mutex.Lock()
	defer sql.mutex.Unlock()

	defer func() { sql.sequenceNumber += 1 }()
	if tag == "primary" || log.Verbose() {
		log.Printf("[%s] [%d] Executing %#v", tag, sql.sequenceNumber, command)
	}

	subprocess := exec.Command("sqlite3", sql.path)
	subprocess.Stdin = strings.NewReader(command + ";")

	var stdout, stderr bytes.Buffer
	subprocess.Stdout = &stdout
	subprocess.Stderr = &stderr

	if err := subprocess.Start(); err != nil {
		log.Panic(err)
	}

	var o, e []byte

	if err := subprocess.Wait(); err != nil {
		exitstatus := getExitstatus(err)
		switch true {
		case exitstatus < 0:
			log.Panic(err)
		case exitstatus == 1:
			fallthrough
		case exitstatus == 2:
			o = stderr.Bytes()
			e = nil
		}
	} else {
		o = stdout.Bytes()
		e = stderr.Bytes()
	}

	output := &Output{
		Stdout:         o,
		Stderr:         e,
		SequenceNumber: sql.sequenceNumber,
	}

	return output, nil
}
