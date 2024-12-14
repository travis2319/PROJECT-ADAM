# Use the official Go image as the base image
FROM golang:latest

# Set the working directory inside the container
WORKDIR /app

# Copy the Go module files (go.mod and go.sum)
COPY go.mod go.sum ./

# Download and install dependencies
RUN go mod download

# Download dependencies
RUN go mod tidy

# Copy the rest of your application code into the container
COPY . .

# Build your Go application
RUN go build -o test ./main.go

# Expose the port your application listens on (default is 8080 here)
EXPOSE 3000

# Command to run your application when the container starts
CMD ["./test"]
