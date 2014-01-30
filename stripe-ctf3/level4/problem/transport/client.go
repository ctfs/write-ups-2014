package transport

import (
	"bytes"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
)

type Client struct {
	client *http.Client
}

type RequestError struct {
	StatusCode int
	Message    []byte
}

func (r *RequestError) Error() string {
	return fmt.Sprintf("Status code %d: %s", r.StatusCode, r.Message)
}

func NewClient() *Client {
	return &Client{
		client: &http.Client{
			Transport: &http.Transport{
				Dial: UnixDialer,
			},
		},
	}
}

func (s *Client) SafePost(connectionString, path string, reqB io.Reader) (io.Reader, error) {
	url := connectionString + path
	resp, err := s.client.Post(url, "application/octet-stream", reqB)
	if err != nil {
		return nil, err
	}
	return handleResp(resp)
}

func (s *Client) SafeGet(connectionString, path string) (io.Reader, error) {
	url := connectionString + path
	resp, err := s.client.Get(url)
	if err != nil {
		return nil, err
	}
	return handleResp(resp)
}

func handleResp(resp *http.Response) (io.Reader, error) {
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	if resp.StatusCode != 200 {
		return nil, &RequestError{
			StatusCode: resp.StatusCode,
			Message:    body,
		}
	}

	return bytes.NewBuffer(body), nil
}
