use regex::Regex;
use serialport::{self, SerialPort};
use std::io::{self, Read};
use std::thread;
use std::time::Duration;

fn read_gps_data(port: &mut Box<dyn SerialPort>) -> io::Result<String> {
    let mut serial_buf: Vec<u8> = vec![0; 1024];
    match port.read(serial_buf.as_mut_slice()) {
        Ok(bytes_read) if bytes_read > 0 => {
            // Convert bytes to string, ignoring invalid UTF-8 characters
            Ok(String::from_utf8_lossy(&serial_buf[..bytes_read])
                .trim()
                .to_string())
        }
        Ok(_) => Ok(String::new()),
        Err(ref e) if e.kind() == io::ErrorKind::TimedOut => Ok(String::new()),
        Err(e) => Err(e),
    }
}

fn main() -> io::Result<()> {
    // Configure the port name based on OS
    #[cfg(windows)]
    let port_name = "COM7";
    #[cfg(unix)]
    let port_name = "/dev/ttyUSB0";

    println!("Reading GPS data from NodeMCU...");

    // Open the serial port
    let mut port = serialport::new(port_name, 115_200)
        .timeout(Duration::from_millis(1000))
        .open()
        .map_err(|e| io::Error::new(io::ErrorKind::Other, e))?;

    // Compile the regex pattern
    let location_regex = Regex::new(r"Location:\s*([-\d.]+),\s*([-\d.]+)")
        .map_err(|e| io::Error::new(io::ErrorKind::Other, e))?;

    loop {
        // Read GPS data
        if let Ok(gps_raw_data) = read_gps_data(&mut port) {
            if !gps_raw_data.is_empty() {
                println!("{}", gps_raw_data); // Debug: print raw GPS data

                // Extract latitude and longitude using regex
                if let Some(captures) = location_regex.captures(&gps_raw_data) {
                    let lat = captures.get(1).map_or("", |m| m.as_str());
                    let lon = captures.get(2).map_or("", |m| m.as_str());
                    println!("http://maps.google.com/?q={},{}", lat, lon);
                } else {
                    println!("No valid location data received.");
                }
            }
        }

        // Sleep for 500ms
        thread::sleep(Duration::from_millis(500));
    }
}
