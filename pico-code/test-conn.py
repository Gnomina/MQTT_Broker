def mqtt_conn(client_id: str, keep_alive: int) -> bytes:
    header = bytes([0x10])  # CONNECT packet

    # Protocol length and name
    protocol_name = "MQTT"
    protocol_name_len = len(protocol_name).to_bytes(2, byteorder='big')
    protocol_name_bytes = protocol_name.encode('ascii')

    # Protocol version (MQTT 3.1.1)
    protocol_level = bytes([0x04])

    # Connection flags (Clean Session)
    connect_flags = bytes([0x02])

    # Keep Alive
    keep_alive_bytes = keep_alive.to_bytes(2, byteorder='big')

    # Client ID
    client_id_len = len(client_id).to_bytes(2, byteorder='big')
    client_id_bytes = client_id.encode('ascii')

    # Calculate remaining packet lenght
    remaining_length = len(protocol_name_len + protocol_name_bytes + protocol_level +
                           connect_flags + keep_alive_bytes + client_id_len + client_id_bytes)
    remaining_length_bytes = bytes([remaining_length])

    # Putting it all together
    packet = header + remaining_length_bytes + protocol_name_len + protocol_name_bytes + \
        protocol_level + connect_flags + keep_alive_bytes + client_id_len + client_id_bytes

    return packet


# Usage example
packet = mqtt_conn("Admin", 100)
print(packet.hex())
