use std::fs::OpenOptions;
use std::io::{Read, Write};
use std::os::unix::fs::OpenOptionsExt;

fn main() {
    let port_name = "/dev/pts/2";

    let mut port = OpenOptions::new()
        .read(true)
        .write(true)
        .custom_flags(libc::O_NOCTTY) // Prevent the port from becoming the controlling terminal
        .open(port_name)
        .expect("Failed to open port");

    println!("Connected: {}", port_name);

    // Optionally, you can read and write data here
    let mut buffer = [0; 1024];
    let bytes_read = port.read(&mut buffer).expect("Read failed");
    println!("Read {} bytes: {:?}", bytes_read, &buffer[..bytes_read]);

    let message = "Hello from Rust!\n";
    port.write_all(message.as_bytes()).expect("Write failed");
}

