def map_binary_to_pids(binary_string, start_pid):
    supported_pids = []

    for i, bit in enumerate(binary_string):
        if bit == '1':
            # Calculate the actual PID number without the 0x prefix
            pid = start_pid + i
            supported_pids.append(f"{pid:02X}")

    return supported_pids

# Given binary strings for PIDs
PIDS_A = "10111110001111101011100000010011"  # PIDs from 0x01 to 0x20
PIDS_B = "10000000000001011010000000000001"  # PIDs from 0x21 to 0x40
PIDS_C = "01101010110100000000000000000000"  # PIDs from 0x41 to 0x60

# Map each binary string to its corresponding PIDs
mapped_pids_A = map_binary_to_pids(PIDS_A, 0x01)
mapped_pids_B = map_binary_to_pids(PIDS_B, 0x21)
mapped_pids_C = map_binary_to_pids(PIDS_C, 0x41)

# Print the results
print(f"Supported PIDs (01 - 20): {mapped_pids_A}")
print(f"Supported PIDs (21 - 40): {mapped_pids_B}")
print(f"Supported PIDs (41 - 60): {mapped_pids_C}")
