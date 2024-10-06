pid_descriptions = {
    "00": "PIDS_A",
    "01": "STATUS",
    # ... (rest of the pid_descriptions dictionary)
}

mid_descriptions = {
    '00': 'MIDS_A',
    '01': 'MONITOR_O2_B1S1',
    # ... (rest of the mid_descriptions dictionary)
}

def map_binary_to_pids(binary_string, start_pid):
    return [f"{start_pid + i:02X}" for i, bit in enumerate(binary_string) if bit == '1']

def map_binary_to_mids(binary_string, mid_id):
    mid_ranges = {
        0x01: (0x00, 0x20),  # MID_A: 00 - 20
        0x02: (0x21, 0x40),  # MID_B: 21 - 40
        0x03: (0x41, 0x60),  # MID_C: 41 - 60
        0x04: (0x61, 0x80),  # MID_D: 61 - 80
        0x05: (0x81, 0xA0),  # MID_E: 81 - A0
        0x06: (0xA1, 0xC0)   # MID_F: A1 - C0
    }

    start, end = mid_ranges.get(mid_id, (None, None))
    if start is None:
        return []

    return [f"{start + i:02X}" for i, bit in enumerate(binary_string) if bit == '1' and start + i <= end]
