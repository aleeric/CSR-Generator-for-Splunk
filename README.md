# CSR Generator

## Release history

| Date       | Version Notes |  
|------------|---------------|  
| 2024-10-04 | 0.0.1 Initial release |

---

## Overview
Generates a Certificate Signing Request (CSR) and a private key

---

## Syntax

```| gencsr common_name=<string> country=<string> state=<string> locality=<string> organization=<string> organizationalunit=<string> password=<string>```

---

## Example

```| gencsr common_name="support.example.com" country="US" state="MS" locality="Ridgeland" organization="Business Company" organizationalunit="Support" password="dummy"```

---

## Features

* The app generates Certificate Signing Requests (CSRs) for specified domains, following standard OpenSSL procedures.
* It allows customization of several certificate attributes such as Common Name (CN), Country (C), State (ST), Locality (L), Organization (O), and Organizational Unit (OU).
* No physical files are written to the disk. The private key and CSR are handled in memory, reducing the need for file management and enhancing security.
* It offers optional password protection for the generated private keys, which can be removed later as part of the key generation process.
* The app integrates smoothly with Splunk as a custom GeneratingCommand, making it accessible through Splunk’s Search Processing Language (SPL).
* It leverages the Splunk SDK for Python, allowing seamless integration into the Splunk ecosystem.
* Outputs the CSR and private key as strings directly in the search results, making it easy for the user to capture and use the generated data immediately.
* It provides default values for optional parameters (such as country and organization details) but also allows the user to override them through input options.


---

## Known limitations

* The app relies on OpenSSL and expects the Splunk environment to have specific file paths (e.g., /opt/splunk/bin/splunk cmd openssl). This could lead to compatibility issues on systems where OpenSSL or Splunk is installed differently, especially on non-Linux platforms.
* Although the password is passed securely to OpenSSL via memory, there may be concerns about the handling of sensitive information, such as the private key and password, as they are temporarily stored in variables within the app.
* The app does not perform any validation of user inputs, such as ensuring the common name is a valid domain or checking if the user-specified country is a valid two-letter code. This could result in CSR generation failures if invalid data is provided.
* The app is dependent on the external OpenSSL command-line tool. If OpenSSL is missing or not properly configured in the system environment, the app will fail to execute.
* The app runs commands synchronously, meaning it waits for each OpenSSL command to complete before proceeding. This could potentially lead to performance bottlenecks if generating multiple CSRs in parallel is required.

---

## Credits

* MS

---

## Source

Feel free to contribute via https://github.com/RictheRoot/CSR-Generator
