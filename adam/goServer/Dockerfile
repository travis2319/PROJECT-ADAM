# Use the official Go image as the base image
FROM golang:latest

# Set the working directory inside the container
WORKDIR /app

# Copy the Go module files (go.mod and go.sum)
COPY go.mod go.sum ./

# Download and install dependencies
RUN go mod download

# Copy the rest of your application code into the container
COPY . .

# Build your Go application
RUN go build -o main .

# Expose the port your application listens on (change if needed)
EXPOSE 8080

# Command to run your application when the container starts
CMD ["./main"]