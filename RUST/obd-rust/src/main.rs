use serialport;
use std::time::Duration;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let port_name = "/dev/pts/4";
    let baud_rate = 9600;

    match serialport::new(port_name, baud_rate)
        .timeout(Duration::from_millis(10))
        .open()
    {
        Ok(_port) => {
            println!("Successfully connected to {}", port_name);
            // The port is automatically closed when it goes out of scope
        }
        Err(e) => {
            eprintln!("Failed to open port {}: {}", port_name, e);
            eprintln!("Make sure the port is available and not in use by another process.");
            return Err(e.into());
        }
    }

    Ok(())
}
