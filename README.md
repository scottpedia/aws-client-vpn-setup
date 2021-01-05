# Create Your Private OpenVPN Service with AWS Client VPN Endpoint

> **Any help to improve this project is welcomed!**  
> **Update:** AWS recently made Client VPN Endpoint available across **ALL 18 Regions.** Newly added regions include HongKong(ap-east-1), Milan(eu-south-1), Paris(eu-west-3) and Bahrain(me-south-1). **However**, these regions are disabled by AWS by default, so you need to enable them on [this page](https://console.aws.amazon.com/billing/home?#/account) before deployment.

An auto-deployment script to deploy and manage your own OpenVPN server with AWS Client VPN Endpoint.

**To quickly deploy an OpenVPN server:**

```bash
git clone https://github.com/scottpedia/aws-client-vpn-setup.git && \
cd aws-client-vpn-setup && \
./client-vpn-aio
```

Then wait for the script to complete. If it is successful, you can now connect to the endpoint with your client software. **Do not forget to turn the endpoint off after using it! Otherwise you will receive a huge bill over time.**

- **For more information about the script(including how to turn off the endpoint with it), please go to [this page](docs/deployment-script.md).**

- **For detailed instructions on how to create the OpenVPN Server manually, please refer to [this page](/docs/manual-deployment.md).**

# Overview

Traditionally, people build their own VPN servers with VMs on the cloud.(e.g. AWS EC2, Azure VMs, etc). In that context, we need to run installation and setup scripts directly on the server. And we are billed according to the hours the VM has been running, and the outbound internet traffic. The instance type determines the computing power(number of simultaneous users) and also the internet bandwidth(the bandwidth of the VPN).

This project, however, utilizes AWS Client VPN Endpoint, a service already integrated into AWS VPC. There are many advantages of that. First, we are billed for the outbound data usage the same way as the VM-based VPN Services while we enjoy almost unlimited bandwidth of AWS networking infrastructures. Also, the service has better reliability as it is managed by AWS. We are only billed for the connection time, not the active VM uptime as in the traditional method.

# Author and License

Copyright 2020-2021 [Scott X. Liang](https://github.com/scottpedia) me@theanonymity.de   
[![GPL logo with text](img/gplv3-with-text-84x42.png)](https://www.gnu.org/licenses/gpl-3.0.txt)  
Unless otherwise noted, the work in this repository is licensed under [GNU General Public License Version 3](https://www.gnu.org/licenses/gpl-3.0.txt).

# See also

- [Setup IPsec VPN](https://github.com/hwdsl2/setup-ipsec-vpn)
- [OpenVPN Install](https://github.com/Nyr/openvpn-install)
- [Algo VPN](https://github.com/trailofbits/algo)
