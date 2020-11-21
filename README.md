# Create Your Private OpenVPN Service with AWS Client VPN Endpoint

<a href="https://trackgit.com"><img src="https://sfy.cx/u/xqO" alt="trackgit-views" /></a>

An auto-deployment script to deploy and manage your own OpenVPN server with AWS Client VPN Endpoint.

**To quickly deploy an OpenVPN server:**

```bash
$ git clone https://github.com/scottpedia/aws-client-vpn-setup.git && cd aws-client-vpn-setup && python3 client-vpn-aio.py
```

- **For more information about the script, please go to [this page](docs/deployment-script.md).**

- **For detailed instructions on how to create the OpenVPN Server manually, please refer to [this page](/docs/manual-deployment.md).**

# Overview

Traditionally, people build their own VPN servers with VMs on the cloud.(e.g. AWS EC2, Azure VMs, etc). In that context, we need to run installation and setup scripts directly on the server. And we are billed according to the hours the VM has been running, and the outbound internet traffic. The instance type determines the computing power(number of simultaneous users) and also the internet bandwidth(the bandwidth of the VPN).

This project, however, utilizes AWS Client VPN Endpoint, a service already integrated into AWS VPC. There are many advantages of that. First, we are billed for the outbound data usage the same way as the VM-based VPN Services while we enjoy almost unlimited bandwidth of AWS networking infrastructures. Also, the service has better reliability as it is managed by AWS. We are only billed for the connection time, not the active VM uptime as in the traditional method.

# Author

Copyright (C) 2020 [Scott X. Liang](https://github.com/scottpedia)

# See also

- [Setup IPsec VPN](https://github.com/hwdsl2/setup-ipsec-vpn)
- [OpenVPN Install](https://github.com/Nyr/openvpn-install)
- [Algo VPN](https://github.com/trailofbits/algo)