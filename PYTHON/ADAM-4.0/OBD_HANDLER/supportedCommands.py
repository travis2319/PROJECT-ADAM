
def get_supported_commands(conn,sensor_file):
    sensor_names = [cmd.name for cmd in conn.supported_commands]
    print(f"Retrieved {len(sensor_names)} sensor names.")
    sensor_names.sort()
    print("Command names sorted.")
    
    with open(sensor_file, 'w') as file:
        for name in sensor_names:
            file.write(name + '\n')
    print(f"Sorted sensor names have been saved to {sensor_file}")

    return sensor_names

