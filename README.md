# AWS Client VPN Setup

This project helps you to quickly set up a working OpenVPN server on AWS, using [AWS Client VPN](https://aws.amazon.com/vpn/client-vpn/). 

## Overview

This project helps you deploy a working OpenVPN server by using AWS Client VPN. It is a built-in service of AWS VPC that is typically used by developers to securely connect to resources within the VPC network. But it can also be used to access the public internet, just like any typical VPN service. Deploying a VPN server this way has many advantages over the traditional way of deploying a VPN server on an ec2 instance. For example, the bandwidth is not limited by the networking performance of the instance type.

This project provides a python script that does the deployment automatically. Due to the distinct nature of this deployment method, it is recommended to understand how it works in detail before using the script. To do so, you can read through the manual deployment tutorial [here](docs/manual-deployment.md). Also, for more information on how to use the script, see this [page](docs/deployment-script.md).

## Comparison with Traditional VM-based Deployment Method

I personally came up with this idea of deploying a VPN server as a workabout of the traditional VM-based solution, in order to better fit my usage scenario. But this deployment method also has its own drawbacks. Below is a clear comparison between the two.

| | Traditional VM-based Deployment(on AWS and similar cloud platforms) | AWS Client VPN-based Deployment(this project) |
| --- | --- | --- |
| VPN protocol(s)[\*](#vpn-protocol-note) | not limited | OpenVPN |
| Billing Scheme  | instance uptime + outbound traffic | endpoint association time + connection time per user + outbound traffic |
| Deployment Time[\*\*](#deployment-time-note) | minutes depending on the instance type and other factors | 15 minutes maximum |
| Networking Performance | solely depending on the instance type used | automatically scalable | 
| Regions | all service regions where VM service is available | All AWS regions |

<a name="#vpn-protocol-note"></a>
\* hello

<details>

<a name="deployment-time-note"></a>
\*\* hello2

</details>

## Author and License

Copyright (C) 2020-2021 [Scott X. Liang](https://github.com/scottpedia) \<scott.liang@pm.me\>   
[![GPL logo with text](img/gplv3-with-text-84x42.png)](https://www.gnu.org/licenses/gpl-3.0.txt)  
Unless otherwise noted, the work in this repository is licensed under [GNU General Public License Version 3](https://www.gnu.org/licenses/gpl-3.0.txt).
