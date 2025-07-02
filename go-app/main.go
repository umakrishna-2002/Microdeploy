package main

import (
	"fmt"
	"net/http"
)

func main() {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		fmt.Fprintf(w, `{"service": "go-app", "status": "running"}`)
	})

	fmt.Println("Starting Go server on :8080...")
	http.ListenAndServe(":8080", nil)
}
