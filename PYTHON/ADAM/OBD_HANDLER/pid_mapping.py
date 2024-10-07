import obd
from .utils import supported_pids, supported_mids, pid_responses, mid_responses, pid_descriptions

def map_binary_to_pids(binary_string, start_pid):
    pids = []
    for i, bit in enumerate(binary_string):
        if bit == '1':
            pid = start_pid + i
            pids.append(f"{pid:02X}")
    return pids

def map_binary_to_mids(binary_string, mid_id):
    print(f"Mapping MIDs for {mid_id:02X}: {binary_string}")
    mid_ranges = {
        0x01: (0x00, 0x20), 0x02: (0x21, 0x40), 0x03: (0x41, 0x60),
        0x04: (0x61, 0x80), 0x05: (0x81, 0xA0), 0x06: (0xA1, 0xC0)
    }
    start, end = mid_ranges.get(mid_id, (None, None))
    if start is None:
        return []
    return [f"{start+i:02X}" for i, bit in enumerate(binary_string) if bit == '1' and start+i <= end]

def initialize_supported_pids(connection):
    global supported_pids, supported_mids
    for cmd_name in ['PIDS_A', 'PIDS_B', 'PIDS_C', 'MIDS_A', 'MIDS_B', 'MIDS_C', 'MIDS_D', 'MIDS_E', 'MIDS_F']:
        response = connection.query(getattr(obd.commands, cmd_name))
        if not response.is_null():
            if cmd_name.startswith('P'):
                pid_responses[cmd_name] = response.value.bits
                print(f"{cmd_name}: {pid_responses[cmd_name]}")
            elif cmd_name.startswith('M'):
                mid_responses[cmd_name] = response.value.bits
                print(f"{cmd_name}: {mid_responses[cmd_name]}")

    if pid_responses['PIDS_A']:
        supported_pids.extend(map_binary_to_pids(pid_responses['PIDS_A'], 0x01))
    if pid_responses['PIDS_B']:
        supported_pids.extend(map_binary_to_pids(pid_responses['PIDS_B'], 0x21))
    if pid_responses['PIDS_C']:
        supported_pids.extend(map_binary_to_pids(pid_responses['PIDS_C'], 0x41))
    print(f"All supported PIDs: {supported_pids}")

    for mid_id, mid_name in enumerate(['MIDS_A', 'MIDS_B', 'MIDS_C', 'MIDS_D', 'MIDS_E', 'MIDS_F'], start=1):
        if mid_responses[mid_name]:
            supported_mids.extend(map_binary_to_mids(mid_responses[mid_name], mid_id))
    print(f"All supported MIDs: {supported_mids}")

def get_pid_names(supported_pids):
    pid_names = [pid_descriptions.get(pid, "Unknown") for pid in supported_pids]
    print(pid_names)
    return pid_names