# ---- Build Stage ----
FROM golang:alpine AS builder

# Install necessary packages
RUN apk add --no-cache git

# Set the working directory
WORKDIR /app

# Copy the Go module files and download dependencies
COPY go.mod go.sum ./
RUN go mod download && go mod tidy

# Copy the rest of the application
COPY . .

# Build the Go application
RUN go build -o server ./main.go

# ---- Run Stage ----
FROM alpine:latest

# Set the working directory
WORKDIR /root/

# Copy the built binary from the builder stage
COPY --from=builder /app/server .

# Expose the port your application listens on
EXPOSE 3000

# Command to run your application
CMD ["./server"]

# # Use the official Go image as the base image
# FROM golang:latest

# # Set the working directory inside the container
# WORKDIR /app

# # Copy the Go module files (go.mod and go.sum)
# COPY go.mod go.sum ./

# # Download and install dependencies
# RUN go mod download

# # Download dependencies
# RUN go mod tidy

# # Copy the rest of your application code into the container
# COPY . .

# # Build your Go application
# RUN go build -o test ./main.go

# # Expose the port your application listens on (default is 8080 here)
# EXPOSE 3000

# # Command to run your application when the container starts
# CMD ["./test"]