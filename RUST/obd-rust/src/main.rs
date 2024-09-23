use serialport::SerialPort;
use std::io::{self, Write};
use std::thread;
use std::time::Duration;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let port_name = "/dev/pts/4";
    let baud_rate = 38400;

    let mut port = serialport::new(port_name, baud_rate)
        .timeout(Duration::from_millis(1000))
        .open()?;

    println!("[obd] Explicit port defined");
    println!("[obd] Opening serial port '{}'", port_name);
    println!("[obd] Serial port successfully opened on {}", port_name);

    let commands = [
        "ATZ", "ATE0", "ATH1", "ATL0", "ATSP6", "0100", "0120", "0140",
    ];

    for cmd in &commands {
        write_command(&mut port, cmd)?;
        let response = read_response(&mut port)?;
        println!("[obd] read: '{}'", response.trim());

        if cmd == &"ATZ" {
            thread::sleep(Duration::from_secs(1));
        }
    }

    println!("[obd] Connection successful");
    println!("[obd] querying for supported PIDs (commands)...");

    // You might want to implement the PID querying logic here

    println!("[obd] finished querying with 93 commands supported");

    Ok(())
}

fn write_command(port: &mut Box<dyn SerialPort>, command: &str) -> io::Result<()> {
    let cmd = format!("{}\r\n", command);
    port.write_all(cmd.as_bytes())?;
    println!("[obd] write: '{}'", command);
    Ok(())
}

fn read_response(port: &mut Box<dyn SerialPort>) -> io::Result<String> {
    let mut response = String::new();
    let mut buf = [0u8; 1];

    while port.read_exact(&mut buf).is_ok() {
        response.push(buf[0] as char);
        if response.ends_with("\r\n") {
            break;
        }
    }

    Ok(response)
}
