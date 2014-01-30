package main

import (
	"flag"
	"fmt"
	"io/ioutil"
	"os"
	"os/signal"
	"path/filepath"
	"stripe-ctf.com/sqlcluster/log"
	"stripe-ctf.com/sqlcluster/server"
	"syscall"
	"time"
)

func main() {
	var verbose bool
	var listen, join, directory string

	flag.BoolVar(&verbose, "v", false, "Enable debug output")
	flag.StringVar(&listen, "l", "127.0.0.1:4000", "Socket to listen on (Unix or TCP)")
	flag.StringVar(&join, "join", "", "Cluster to join")
	flag.StringVar(&directory, "d", "", "Storage directory")

	dir := filepath.Dir(os.Args[0])
	base := "./" + filepath.Base(os.Args[0])
	flag.Usage = func() {
		fmt.Fprintf(os.Stderr, `Usage: %s [options]

SQLCluster is a highly-available SQL store. It accepts commands over
HTTP, and returns the output of commands together with a
SequenceNumber which indicates the ordering in which requests are
being applied. (SequenceNumber is useful for validation, and can
otherwise be ignored.)

Run a cluster as follows:

  cd %s
  %s -d /tmp/sqlcluster/node0 &
  %s -d /tmp/sqlcluster/node1 -l 127.0.0.1:4001 --join 127.0.0.1:4000 &
  %s -d /tmp/sqlcluster/node2 -l 127.0.0.1:4002 --join 127.0.0.1:4000

You can then issue queries using your favorite HTTP client.

  curl 127.0.0.1:4000/sql -d 'CREATE TABLE hello (world int)'
  curl 127.0.0.1:4000/sql -d 'INSERT INTO hello (world) VALUES (1), (2)'
  curl 127.0.0.1:4000/sql -d 'SELECT * FROM hello'

This should return the following sequence of outputs:
  - SequenceNumber: 0

  - SequenceNumber: 1

  - SequenceNumber: 2
    1
    2

By default, SQLCluster will listen on a TCP port. However, if you
specify a listen address that begins with a / or ., that will be
interpeted as Unix path for SQLCluster to listen on. (Note that
Octopus runs using Unix sockets only, but it will probably be more
convient for you to develop using TCP.)

OPTIONS:
`, os.Args[0], dir, base, base, base)
		flag.PrintDefaults()
	}

	flag.Parse()

	if flag.NArg() != 0 {
		flag.Usage()
		os.Exit(1)
	}

	log.SetVerbose(verbose)

	if directory == "" {
		var err error
		directory, err = ioutil.TempDir("/tmp", "node")
		if err != nil {
			log.Fatalf("Could not create temporary base directory: %s", err)
		}
		defer os.RemoveAll(directory)

		log.Printf("Storing state in tmpdir %s", directory)
	} else {
		if err := os.MkdirAll(directory, os.ModeDir|0755); err != nil {
			log.Fatalf("Error while creating storage directory: %s", err)
		}
	}

	log.Printf("Changing directory to %s", directory)
	if err := os.Chdir(directory); err != nil {
		log.Fatalf("Error while changing to storage directory: %s", err)
	}

	// Make sure we don't leave stranded sqlclusters lying around
	go func() {
		for {
			time.Sleep(2 * time.Second)
			if os.Getppid() == 1 {
				log.Fatal("Parent process exited; terminating")
			}
		}
	}()

	// Start the server
	go func() {
		s, err := server.New(directory, listen)
		if err != nil {
			log.Fatal(err)
		}

		if err := s.ListenAndServe(join); err != nil {
			log.Fatal(err)
		}
	}()

	// Exit cleanly so we can remove the tmpdir
	sigchan := make(chan os.Signal)
	signal.Notify(sigchan, syscall.SIGINT, syscall.SIGTERM)
	<-sigchan
}
