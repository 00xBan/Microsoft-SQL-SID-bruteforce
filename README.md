# Windows SID Parser

A Python utility for parsing raw Windows Security Identifier (SID) bytes into their human-readable string representation.

## Overview

Windows SIDs are binary structures used to uniquely identify security principals (users, groups, computers) in Windows environments. This script takes a raw hex-encoded SID and breaks it down into its components, printing both the individual fields and the final canonical SID string.

This is useful during Active Directory enumeration, LDAP/LDIF analysis, forensics, and CTF/pentest scenarios where raw SID bytes appear in memory dumps, registry hives, or protocol captures.

## SID Structure

A SID is laid out in memory as follows:

```
Byte(s)   Field
-------   -----
0         Revision (always 0x01)
1         SubAuthority Count (number of 32-bit sub-authority values)
2–7       Identifier Authority (6 bytes, big-endian)
8–N       Sub-Authorities (4 bytes each, little-endian)
```

The resulting string form is:

```
S-<Revision>-<IdentifierAuthority>-<SubAuth1>-<SubAuth2>-...
```

## Usage

```python
sid = "0x<hex-encoded SID bytes>"
parse_sid(sid)
```

You need to change the code manually on line 38:

<img width="1333" height="627" alt="image" src="https://github.com/user-attachments/assets/a895312c-418f-4039-a4ba-d718aeded7bd" />

---

**Example:**

```python
sid = "0x0105000000000005150000000a185deefb22433798d8e847a00020000"
parse_sid(sid)
```

**Output:**

```
Revision: 1
SubAuthority Count: 5
Identifier Authority: 5
SubAuthorities: [21, 4000000010, 2570003451, 1206517144, 672]
String SID: S-1-5-21-4000000010-2570003451-1206517144-672
```

The final sub-authority (RID) identifies the specific account type:

| RID Range     | Meaning                        |
|---------------|--------------------------------|
| 500           | Built-in Administrator         |
| 501           | Guest                          |
| 502           | KRBTGT (Kerberos service)      |
| 512           | Domain Admins group            |
| 513           | Domain Users group             |
| 1000+         | User-created accounts / groups |

## Common Well-Known SIDs

| SID String    | Description               |
|---------------|---------------------------|
| S-1-1-0       | Everyone                  |
| S-1-5-18      | Local System              |
| S-1-5-19      | Local Service             |
| S-1-5-20      | Network Service           |
| S-1-5-32-544  | BUILTIN\Administrators    |
| S-1-5-32-545  | BUILTIN\Users             |

## Requirements

- Python 3.x
- Standard library only (`struct` module)

## Notes

- The hex string input should include the `0x` prefix.
- Sub-authorities are unpacked as unsigned 32-bit little-endian integers (`<I` format).
- The Identifier Authority is decoded as a 6-byte big-endian integer; for standard NT SIDs this will be `5` (NT Authority).
