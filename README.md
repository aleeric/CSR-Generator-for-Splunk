# CSR Generator

## Release history

| Date       | Version | Notes                                                             | 
|------------|---------|-------------------------------------------------------------------|
| 2024-10-04 | 0.0.1   | Initial release                                                   |
| 2024-10-12 | 0.0.2   | Added `subjectAltName` support, improved input handling, and bug fixes |

---

## Overview
This app generates a Certificate Signing Request (CSR) and a private key directly within Splunk using OpenSSL.

---

## Syntax


```| gencsr common_name=<string> country=<string> state=<string> locality=<string> organization=<string> organizationalunit=<string> password=<string> subjectaltname=<string>```


---

## Example

```| gencsr common_name="example.com" country="US" state="CA" locality="San Francisco" organization="Example Inc." organizationalunit="IT" password="securepassword" subjectaltname="www.example.com,mail.example.com"```

---

## Features

* Generates CSRs using OpenSSL standards.
* Customizable fields: Common Name (CN), Country (C), State (ST), Locality (L), Organization (O), Organizational Unit (OU), and subjectAltName.
* Handles CSRs and private keys securely in-memory; no files are written to disk.
* Option to password-protect the generated private key.
* Outputs the CSR and private key directly in search results for easy access.
* Seamless integration with Splunk’s SPL via a custom GeneratingCommand.
* Default values provided for optional parameters, but users can override them.

---

## New in Version 0.0.2

* Added support for subjectAltName in CSRs.
* Improved handling of optional input fields with defaults.
* Enhanced input validation to prevent empty fields.
* Minor bug fixes and performance improvements.

---

## Known limitations

* OpenSSL must be installed and properly configured in the Splunk environment.
* Limited input validation — invalid fields, like incorrect country codes, may cause CSR generation to fail.
* Dependence on external OpenSSL tools, so the app won't work if OpenSSL is missing or misconfigured.
* Commands are executed synchronously, which could slow performance if multiple CSRs are generated in parallel.

---

## Credits

* MS

---

## Source

Feel free to contribute via https://github.com/RictheRoot/CSR-Generator
