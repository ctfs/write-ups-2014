package server

import (
	"errors"
	"fmt"
	"github.com/gorilla/mux"
	"io/ioutil"
	"net/http"
	"path/filepath"
	"stripe-ctf.com/sqlcluster/log"
	"stripe-ctf.com/sqlcluster/sql"
	"stripe-ctf.com/sqlcluster/transport"
	"stripe-ctf.com/sqlcluster/util"
	"time"
)

type Server struct {
	name       string
	path       string
	listen     string
	router     *mux.Router
	httpServer *http.Server
	sql        *sql.SQL
	client     *transport.Client
	cluster    *Cluster
}

type Join struct {
	Self ServerAddress `json:"self"`
}

type JoinResponse struct {
	Self    ServerAddress   `json:"self"`
	Members []ServerAddress `json:"members"`
}

type Replicate struct {
	Self  ServerAddress `json:"self"`
	Query []byte        `json:"query"`
}

type ReplicateResponse struct {
	Self ServerAddress `json:"self"`
}

// Creates a new server.
func New(path, listen string) (*Server, error) {
	cs, err := transport.Encode(listen)
	if err != nil {
		return nil, err
	}

	sqlPath := filepath.Join(path, "storage.sql")
	util.EnsureAbsent(sqlPath)

	s := &Server{
		path:    path,
		listen:  listen,
		sql:     sql.NewSQL(sqlPath),
		router:  mux.NewRouter(),
		client:  transport.NewClient(),
		cluster: NewCluster(path, cs),
	}

	return s, nil
}

// Starts the server.
func (s *Server) ListenAndServe(primary string) error {
	var err error
	// Initialize and start HTTP server.
	s.httpServer = &http.Server{
		Handler: s.router,
	}

	if primary == "" {
		s.cluster.Init()
	} else {
		s.Join(primary)
		go func() {
			for {
				if s.healthcheckPrimary() {
					time.Sleep(10 * time.Millisecond)
					continue
				}

				s.cluster.PerformFailover()

				if s.cluster.State() == "primary" {
					break
				}
			}
		}()
	}

	s.router.HandleFunc("/sql", s.sqlHandler).Methods("POST")
	s.router.HandleFunc("/replicate", s.replicationHandler).Methods("POST")
	s.router.HandleFunc("/healthcheck", s.healthcheckHandler).Methods("GET")
	s.router.HandleFunc("/join", s.joinHandler).Methods("POST")

	// Start Unix transport
	l, err := transport.Listen(s.listen)
	if err != nil {
		log.Fatal(err)
	}
	return s.httpServer.Serve(l)
}

// Client operations

func (s *Server) healthcheckPrimary() bool {
	_, err := s.client.SafeGet(s.cluster.primary.ConnectionString, "/healthcheck")

	if err != nil {
		log.Printf("The primary appears to be down: %s", err)
		return false
	} else {
		return true
	}
}

// Join an existing cluster
func (s *Server) Join(primary string) error {
	join := &Join{Self: s.cluster.self}
	b := util.JSONEncode(join)

	cs, err := transport.Encode(primary)
	if err != nil {
		return err
	}

	for {
		body, err := s.client.SafePost(cs, "/join", b)
		if err != nil {
			log.Printf("Unable to join cluster: %s", err)
			time.Sleep(1 * time.Second)
			continue
		}

		resp := &JoinResponse{}
		if err = util.JSONDecode(body, &resp); err != nil {
			return err
		}

		s.cluster.Join(resp.Self, resp.Members)
		return nil
	}
}

// Server handlers
func (s *Server) joinHandler(w http.ResponseWriter, req *http.Request) {
	j := &Join{}
	if err := util.JSONDecode(req.Body, j); err != nil {
		log.Printf("Invalid join request: %s", err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	log.Printf("Handling join request: %#v", j)

	// Add node to the cluster
	if err := s.cluster.AddMember(j.Self); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}

	// Respond with the current cluster description
	resp := &JoinResponse{
		s.cluster.self,
		s.cluster.members,
	}
	b := util.JSONEncode(resp)
	w.Write(b.Bytes())
}

// This is the only user-facing function, and accordingly the body is
// a raw string rather than JSON.
func (s *Server) sqlHandler(w http.ResponseWriter, req *http.Request) {
	state := s.cluster.State()
	if state != "primary" {
		http.Error(w, "Only the primary can service queries, but this is a "+state, http.StatusBadRequest)
		return
	}

	query, err := ioutil.ReadAll(req.Body)
	if err != nil {
		log.Printf("Couldn't read body: %s", err)
		http.Error(w, err.Error(), http.StatusBadRequest)
	}

	log.Debugf("[%s] Received query: %#v", s.cluster.State(), string(query))
	resp, err := s.execute(query)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
	}

	r := &Replicate{
		Self:  s.cluster.self,
		Query: query,
	}
	for _, member := range s.cluster.members {
		b := util.JSONEncode(r)
		_, err := s.client.SafePost(member.ConnectionString, "/replicate", b)
		if err != nil {
			log.Printf("Couldn't replicate query to %v: %s", member, err)
		}
	}

	log.Debugf("[%s] Returning response to %#v: %#v", s.cluster.State(), string(query), string(resp))
	w.Write(resp)
}

func (s *Server) replicationHandler(w http.ResponseWriter, req *http.Request) {
	r := &Replicate{}
	if err := util.JSONDecode(req.Body, r); err != nil {
		log.Printf("Invalid replication request: %s", err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	log.Printf("Handling replication request from %v", r.Self)

	_, err := s.execute(r.Query)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
	}

	resp := &ReplicateResponse{
		s.cluster.self,
	}
	b := util.JSONEncode(resp)
	w.Write(b.Bytes())
}

func (s *Server) healthcheckHandler(w http.ResponseWriter, req *http.Request) {
	w.WriteHeader(http.StatusOK)
}

func (s *Server) execute(query []byte) ([]byte, error) {
	output, err := s.sql.Execute(s.cluster.State(), string(query))

	if err != nil {
		var msg string
		if output != nil && len(output.Stderr) > 0 {
			template := `Error executing %#v (%s)

SQLite error: %s`
			msg = fmt.Sprintf(template, query, err.Error(), util.FmtOutput(output.Stderr))
		} else {
			msg = err.Error()
		}

		return nil, errors.New(msg)
	}

	formatted := fmt.Sprintf("SequenceNumber: %d\n%s",
		output.SequenceNumber, output.Stdout)
	return []byte(formatted), nil
}
