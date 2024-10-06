#!/usr/bin/env python

import sys
import os
import time
import subprocess
import io
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
    state = Option(require=False, default="N/A")
    locality = Option(require=False, default="N/A")
    organization = Option(require=False, default="N/A")
    organizationalunit = Option(require=False, default="N/A")
    password = Option(require=False, default="dummypassword")

    def generate(self):
        domain = self.common_name
        country = self.country
        state = self.state
        locality = self.locality
        organization = self.organization
        organizational_unit = self.organizationalunit
        password = self.password

        try:

            key_output = subprocess.check_output([
                "/opt/splunk/bin/splunk", "cmd", "openssl", "genrsa", "-des3",
                "-passout", f"pass:{password}", "2048"
            ])
            key_content = key_output.decode('utf-8')

            key_output = subprocess.check_output([
                "/opt/splunk/bin/splunk", "cmd", "openssl", "rsa", 
                "-in", "/dev/stdin", "-passin", f"pass:{password}", 
                "-outform", "PEM"
            ], input=key_content.encode('utf-8'))
            key_content = key_output.decode('utf-8')

            csr_output = subprocess.check_output([
                "/opt/splunk/bin/splunk", "cmd", "openssl", "req", "-new",
                "-key", "/dev/stdin", "-passin", f"pass:{password}",
                "-subj", f"/C={country}/ST={state}/L={locality}/O={organization}/OU={organizational_unit}/CN={domain}"
            ], input=key_content.encode('utf-8'))
            csr_content = csr_output.decode('utf-8')

            yield {
                '_time': time.time(),
                'message': 'CSR generated successfully',
                'csr': csr_content,
                'key': key_content
            }

        except subprocess.CalledProcessError as e:
            yield {'_time': time.time(), 'message': 'Error executing command', 'error': str(e)}

dispatch(gencsrCommand, sys.argv, sys.stdin, sys.stdout, __name__)
