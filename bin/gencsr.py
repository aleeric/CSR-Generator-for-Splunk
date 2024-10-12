#!/usr/bin/env python

import sys
import time
import subprocess
import tempfile
from splunklib.searchcommands import (
    dispatch,
    GeneratingCommand,
    Configuration,
    Option
)

@Configuration()
class gencsrCommand(GeneratingCommand):
    common_name = Option(require=True)
    country = Option(require=False, default="US")
    state = Option(require=False, default="NA")
    locality = Option(require=False, default="NA")
    organization = Option(require=False, default="NA")
    organizationalunit = Option(require=False, default="NA")
    password = Option(require=False, default="dummypassword")
    subjectaltname = Option(require=False, default=None)

    def generate(self):
        domain = self.common_name.strip()
        country = self.country.strip() if self.country else "US"
        state = self.state.strip() if self.state else "NA"
        locality = self.locality.strip() if self.locality else "NA"
        organization = self.organization.strip() if self.organization else "NA"
        organizational_unit = self.organizationalunit.strip() if self.organizationalunit else "NA"
        password = self.password.strip() if self.password else "dummypassword"
        subject_alt_name = self.subjectaltname.strip() if self.subjectaltname else None

        try:
            key_output = subprocess.check_output([
                "/opt/splunk/bin/splunk", "cmd", "openssl", "genrsa", "-des3",
                "-passout", f"pass:{password}", "2048"
            ])
            key_content = key_output.decode('utf-8')

            key_output = subprocess.check_output([
                "/opt/splunk/bin/splunk", "cmd", "openssl", "rsa",
                "-passin", f"pass:{password}",
                "-outform", "PEM"
            ], input=key_content.encode('utf-8'))
            key_content = key_output.decode('utf-8')

            if subject_alt_name:
                san_entries = [san.strip() for san in subject_alt_name.split(',')]
                san_string = ",".join([f"DNS:{san}" for san in san_entries])

                openssl_config = f"""
[ req ]
default_bits       = 2048
distinguished_name = req_distinguished_name
req_extensions     = req_ext
prompt             = no

[ req_distinguished_name ]
C  = {country}
ST = {state}
L  = {locality}
O  = {organization}
OU = {organizational_unit}
CN = {domain}

[ req_ext ]
subjectAltName = {san_string}
"""

                with tempfile.NamedTemporaryFile(delete=True, mode='w+') as config_file:
                    config_file.write(openssl_config)
                    config_file.flush() 

                    csr_command = [
                        "/opt/splunk/bin/splunk", "cmd", "openssl", "req", "-new",
                        "-key", "/dev/stdin", "-passin", f"pass:{password}",
                        "-config", config_file.name
                    ]
                    print(f"Running command: {' '.join(csr_command)}")
                    csr_output = subprocess.check_output(csr_command, input=key_content.encode('utf-8'))
                    csr_content = csr_output.decode('utf-8')
            else:
                csr_command = [
                    "/opt/splunk/bin/splunk", "cmd", "openssl", "req", "-new",
                    "-key", "/dev/stdin", "-passin", f"pass:{password}",
                    "-subj", f"/C={country}/ST={state}/L={locality}/O={organization}/OU={organizational_unit}/CN={domain}"
                ]
                print(f"Running command: {' '.join(csr_command)}")
                csr_output = subprocess.check_output(csr_command, input=key_content.encode('utf-8'))
                csr_content = csr_output.decode('utf-8')

            yield {
                '_time': time.time(),
                'message': 'CSR generated successfully',
                'csr': csr_content,
                'key': key_content,
                'debug_info': {
                    'common_name': domain,
                    'country': country,
                    'state': state,
                    'locality': locality,
                    'organization': organization,
                    'organizational_unit': organizational_unit,
                    'password': password,
                    'subject_alt_name': subject_alt_name,
                }
            }

        except subprocess.CalledProcessError as e:
            yield {
                '_time': time.time(),
                'message': 'Error executing command',
                'error': str(e),
                'command_output': e.output.decode('utf-8') if e.output else ''
            }

dispatch(gencsrCommand, sys.argv, sys.stdin, sys.stdout, __name__)
