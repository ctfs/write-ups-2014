package transport

import (
	"net"
	"stripe-ctf.com/sqlcluster/log"
)

func Listen(addr string) (net.Listener, error) {
	network := Network(addr)
	log.Printf("Listening on %s: %s", network, addr)
	return net.Listen(network, addr)
}
