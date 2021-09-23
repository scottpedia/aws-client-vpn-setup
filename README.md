# AWS Client VPN Setup

This project helps you to quickly set up a working OpenVPN server on AWS, using [AWS Client VPN](https://aws.amazon.com/vpn/client-vpn/). 

## Overview

This project helps you deploy a working OpenVPN server by using AWS Client VPN. It is a built-in service of AWS VPC that is typically used by developers to securely connect to resources within the VPC network. But it can also be used to access the public internet, just like any typical VPN service. Deploying a VPN server this way has many advantages over the traditional way of deploying a VPN server on an ec2 instance. For example, the bandwidth is not limited by the networking performance of the instance type.

This project provides a python script that does the deployment automatically. Due to the distinct nature of this deployment method, it is recommended to understand how it works in detail before using the script. To do so, you can read through the manual deployment tutorial [here](docs/manual-deployment.md). Also, for more information on how to use the script, see this [page](docs/deployment-script.md).

This project aims to mainly help the people in China, People's Republic of, to gain free(as in freedom) access to the World Wide Web without being censored by the GFW(Great Fire Wall). In the name of Freedom, I wish this project makes itself useful to those in countries where Internet is censored. 

# Author and License

Copyright (C) 2020-2021 [Scott X. Liang](https://github.com/scottpedia) \<scott.liang@pm.me\>   
[![GPL logo with text](img/gplv3-with-text-84x42.png)](https://www.gnu.org/licenses/gpl-3.0.txt)  
Unless otherwise noted, the work in this repository is licensed under [GNU General Public License Version 3](https://www.gnu.org/licenses/gpl-3.0.txt).
