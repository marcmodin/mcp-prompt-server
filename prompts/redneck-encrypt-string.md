---
name: redneck-encrypt-string
description: Obscure strings using base64, Swedish Rövarspråk, hexadecimal, and Bech32 encoding
arguments:
  - name: input_string
    description: The string to obscure/encrypt
    required: true
---

# Redneck Encryption

## Context

You are charged with the task of making a string non-human readable and hard to immediately decode but not allowed to use mainstream encryption mechanisms, so you rely on a series of encodings and some good old Swedish fuckery to obscure it in a really insecure and ineffective manor.

## Instructions

Transform the input string through a series of encoding steps:

1. **Base64 Encoding**: Encode the input string using standard base64 encoding
   
2. **Swedish Rövarspråk Encoding**: Apply Swedish Rövarspråk (Robber's Language) to the base64 string
   - For each consonant (b, c, d, f, g, h, j, k, l, m, n, p, q, r, s, t, v, w, x, z), insert 'o' followed by the consonant again
   - Example: "hello" becomes "hohelollolo"
   - Vowels (a, e, i, o, u, y) and other characters remain unchanged
   - Case-insensitive: apply the same transformation to uppercase consonants using uppercase

3. **Hexadecimal Encoding**: Convert the Rövarspråk string to hexadecimal
   - Convert each character to its ASCII/Unicode value in hexadecimal
   - Use lowercase hexadecimal digits

4. **Bech32 Encoding**: Encode the hexadecimal string to Bech32 format
   - Use HRP (Human-Readable Part) = "yeehaw"
   - Convert the hex string to 5-bit groups for Bech32 encoding
   - Follow Bech32 specification (BIP 173)
   - Output format: yeehaw1[encoded data][checksum]

## Constraints

- Output only the final Bech32-encoded string
- Do not include explanations, intermediate steps, or formatting
- The output should be a single string on one line

## Process

### Encoding Approach

Work through each step systematically:

1. **Start with the input**: Take the provided string
2. **Apply base64**: Use standard base64 encoding (RFC 4648)
3. **Apply Rövarspråk**: Transform consonants according to the Swedish language game rules
4. **Convert to hex**: Convert each character to its hexadecimal representation
5. **Apply Bech32**: Follow the Bech32 encoding specification with HRP "yeehaw"

### Validation

Ensure each step produces valid output before proceeding to the next step.

## Reporting

Output only the final Bech32-encoded string. Nothing more.

## Examples

### Example 1

**Input**: "This is not right"

**Output**: yeehaw12eh4v3m0ga5x76rsdacxxmmr09px7snsdacxxmmr09px7sn4vfhkyv63dagkwmm8vdhkxmt0d3kx7mn0des5sm6g29h4z0gnxwy69

---

## Notes

- Swedish Rövarspråk is a Swedish language game where consonants are doubled with 'o' in between
- Bech32 is a checksummed base32 format used in Bitcoin (BIP 173)
- This is intentionally insecure and should never be used for actual encryption
- The encoding is reversible by applying the inverse of each step in reverse order
