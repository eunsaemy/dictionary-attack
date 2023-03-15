# dictionary-based attack

## A dictionary-based password cracker for Linux (Fedora 36)

Write a dictionary-based password cracker for Fedora 36 that:
- decrypts passwords in the /etc/shadow
- supports:
  - MD5
  - SHA-256
  - SHA-512
  - yescrypt
 - does NOT support:
    - Blowfish
    - DES
 - writes results into a generated log file (password.log)
 - sets path to shadow file
 - sets path to dictionary file
 - exits the program on prompt

### To run dictionary.py:

```python dictionary.py```
