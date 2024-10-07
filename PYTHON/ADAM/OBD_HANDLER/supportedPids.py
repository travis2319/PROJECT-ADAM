import obd
def initialize_supported_pids(connection,supported_pids,supported_mids):
    # Query for supported PIDs and MIDs
    for cmd_name in ['PIDS_A', 'PIDS_B', 'PIDS_C', 'MIDS_A', 'MIDS_B', 'MIDS_C', 'MIDS_D', 'MIDS_E', 'MIDS_F']:
        response = connection.query(getattr(obd.commands, cmd_name))
        if not response.is_null():
            if cmd_name.startswith('PIDS_'):
                pid_responses[cmd_name] = response.value.bits
                print(f"{cmd_name}: {pid_responses[cmd_name]}")
            elif cmd_name.startswith('MIDS_'):
                mid_responses[cmd_name] = response.value.bits
                print(f"{cmd_name}: {mid_responses[cmd_name]}")

    # Map binary responses to PIDs
    if pid_responses['PIDS_A']:
        supported_pids.extend(map_binary_to_pids(pid_responses['PIDS_A'], 0x01))
        print(f"Added PIDs (01 - 20)")
    if pid_responses['PIDS_B']:
        supported_pids.extend(map_binary_to_pids(pid_responses['PIDS_B'], 0x21))
        print(f"Added PIDs (21 - 40)")
    if pid_responses['PIDS_C']:
        supported_pids.extend(map_binary_to_pids(pid_responses['PIDS_C'], 0x41))
        print(f"Added PIDs (41 - 60)")
    print(f"All supported PIDs: {supported_pids}")

    # Map binary responses to MIDs
    if mid_responses['MIDS_A']:
        supported_mids.extend(map_binary_to_mids(mid_responses['MIDS_A'], 0x01))
        print(f"Added MIDs (01 - 10): {supported_mids}")
    if mid_responses['MIDS_B']:
        supported_mids.extend(map_binary_to_mids(mid_responses['MIDS_B'], 0x02))
        print(f"Added MIDs (21 - 3D)")
    if mid_responses['MIDS_C']:
        supported_mids.extend(map_binary_to_mids(mid_responses['MIDS_C'], 0x03))
        print(f"Added MIDs (41 - 50)")
    if mid_responses['MIDS_D']:
        supported_mids.extend(map_binary_to_mids(mid_responses['MIDS_D'], 0x04))
        print(f"Added MIDs (61 - 74)")
    if mid_responses['MIDS_E']:
        supported_mids.extend(map_binary_to_mids(mid_responses['MIDS_E'], 0x05))
        print(f"Added MIDs (81 - 99)")
    if mid_responses['MIDS_F']:
        supported_mids.extend(map_binary_to_mids(mid_responses['MIDS_F'], 0x06))
        print(f"Added MIDs (A1 - B1)")
    print(f"All supported MIDs: {supported_mids}")
    
    return supported_pids,supported_mids

