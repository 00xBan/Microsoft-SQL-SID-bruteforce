import struct

def parse_sid(hex_sid):
    sid_bytes = bytes.fromhex(hex_sid)

    # Revision
    revision = sid_bytes[0]

    # Number of sub authorities
    subauth_count = sid_bytes[1]

    # Identifier Authority (6 bytes, big-endian)
    identifier_authority = int.from_bytes(sid_bytes[2:8], byteorder='big')

    print(f"Revision: {revision}")
    print(f"SubAuthority Count: {subauth_count}")
    print(f"Identifier Authority: {identifier_authority}")

    # SubAuthorities (4 bytes each, little-endian)
    offset = 8
    subauthorities = []

    for i in range(subauth_count):
        subauth = struct.unpack("<I", sid_bytes[offset:offset+4])[0]
        subauthorities.append(subauth)
        offset += 4

    print("SubAuthorities:", subauthorities)

    # Build string SID
    sid_string = f"S-{revision}-{identifier_authority}"
    for sub in subauthorities:
        sid_string += f"-{sub}"

    print("String SID:", sid_string)


sid = "0x010500000000000515000000a185deefb22433798d8e847a00020000"
parse_sid(sid)
