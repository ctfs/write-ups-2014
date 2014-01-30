package server

import (
	"errors"
	"fmt"
	"stripe-ctf.com/sqlcluster/log"
)

type ServerAddress struct {
	Name             string `json:"name"`
	ConnectionString string `json:"address"`
}

func (sa ServerAddress) String() string {
	return fmt.Sprintf("Server<%s>", sa.Name)
}

type Cluster struct {
	self    ServerAddress
	primary ServerAddress
	members []ServerAddress
}

func NewCluster(name, connectionString string) *Cluster {
	c := &Cluster{}
	c.self = ServerAddress{
		Name:             name,
		ConnectionString: connectionString,
	}
	return c
}

func (c *Cluster) Init() {
	log.Printf("Initializing cluster and promoting self to primary")
	c.primary = c.self
	c.members = make([]ServerAddress, 0)
}

func (c *Cluster) Join(primary ServerAddress, members []ServerAddress) {
	log.Printf("Joining existing cluster: primary %v, members %v", primary, members)
	c.primary = primary
	c.members = members
}

func (c *Cluster) AddMember(identity ServerAddress) error {
	state := c.State()
	if state != "primary" {
		return errors.New("Can only join to a primary, but you're talking to a " + state)
	}

	log.Printf("Adding new cluster member %v", identity)
	c.members = append(c.members, identity)

	return nil
}

func (c *Cluster) State() string {
	switch true {
	case c.members == nil:
		return "startup"
	case c.self.Name == c.primary.Name:
		return "primary"
	default:
		return "secondary"
	}
}

func (c *Cluster) PerformFailover() {
	state := c.State()
	if state != "secondary" {
		log.Fatalf("Trying to fail over even though my state is %s", state)
	}

	c.primary = c.members[0]
	c.members = c.members[1:]

	if c.State() == "primary" {
		log.Printf("I am the the primary now.")
	} else {
		log.Printf("Promoted %s to primary. My time will come one day.", c.primary.Name)
	}
}
