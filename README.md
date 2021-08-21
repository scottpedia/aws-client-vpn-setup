# Create Your Private OpenVPN Service with AWS Client VPN Endpoint

Python script to rapidly deploy and manage a high-performance OpenVPN server on AWS, with AWS Client VPN Endpoint.

**To quickly deploy an OpenVPN server on AWS:**

```bash
git clone https://github.com/scottpedia/aws-client-vpn-setup.git && \
cd aws-client-vpn-setup && \
./client-vpn-aio
```

Then wait for the script to complete.

After that, you need to activate the endpoint before you can connect to it with client software. Please see [this page](docs/deployment-script.md) for how to use the script to manage a deployed OpenVPN endpoint, including how to activate it.

**Do not forget to turn the endpoint off after using it! Otherwise you will receive a huge bill over time.**

> **Note:** To deploy to newly-available AWS regions, you need to enable them first on AWS console. Follow this [link](https://console.aws.amazon.com/billing/home?#/account) to your account settings, and enable the region where you wish to deploy the OpenVPN server, under **"AWS Regions"** section. After that, the new region would be ready to use in a few minutes.

For a step-to-step tutorial on how to create an OpenVPN endpoint with Client VPN Endpoint on AWS, and how to configure the client, go to this [page](docs/manual-deployment.md).

# Overview

Traditionally, people build their own VPN servers with VMs on the cloud.(e.g. AWS EC2, Azure VMs, etc). In that context, we need to run installation and setup scripts directly on the server. And we are billed according to the hours the VM has been running, and the outbound internet traffic. The instance type determines the computing power(number of simultaneous users) and also the internet bandwidth(the bandwidth of the VPN).

This project, however, utilizes AWS Client VPN Endpoint, a service already integrated into AWS VPC. There are many advantages of that. First, we are billed for the outbound data usage the same way as the VM-based VPN Services while we enjoy almost unlimited bandwidth of AWS networking infrastructures. Also, the service has better reliability as it is managed by AWS. We are only billed for the connection time, not the active VM uptime as in the traditional method.

# Author and License

Copyright 2020-2021 [Scott X. Liang](https://github.com/scottpedia) \<scott.liang@pm.me\>   
[![GPL logo with text](img/gplv3-with-text-84x42.png)](https://www.gnu.org/licenses/gpl-3.0.txt)  
Unless otherwise noted, the work in this repository is licensed under [GNU General Public License Version 3](https://www.gnu.org/licenses/gpl-3.0.txt).

# See also

- [Setup IPsec VPN](https://github.com/hwdsl2/setup-ipsec-vpn)
- [OpenVPN Install](https://github.com/Nyr/openvpn-install)
- [Algo VPN](https://github.com/trailofbits/algo)
