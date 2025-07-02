FROM golang:1.22-alpine 
WORKDIR /app

COPY main.go .
COPY go.mod  . 

RUN go build -o server .

EXPOSE 8080

CMD ["./server"]
