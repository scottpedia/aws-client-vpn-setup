# AWS Client VPN Setup

*其他语言版本： [English](./README.md)*

此项目帮助你使用 [AWS Client VPN](https://aws.amazon.com/vpn/client-vpn/) 服务快速在 AWS 云平台上搭建一个 OpenVPN 服务器。

<a href="https://aws.amazon.com/vpn/"><img src="img/client-vpn.png" width="120" align="right"></a>

## 略览

此项目帮助你使用 AWS Client VPN 服务快速在 AWS 云平台上搭建一个 OpenVPN 服务器。 AWS Client VPN 服务是一个 AWS VPC 内置的附属服务，其用途是安全的访问到在指定 VPC 网域内的资源。但是此服务也可被用于来访问公网资源，类似于人们常用的 VPN 类型。利用以下方式部署一个 VPN 服务器相比基于 ec2 实例的传统部署方式有很多优点。比如， VPN 带宽不受指定实例类型的网络性能所限制。

此项目提供一个基于 python 的自动部署脚本。由于此项目所提供的 VPN 部署方式比较不同寻常，我建议大家在使用此脚本前首先了解其部署流程。详情可参见本项目提供的[手动部署教程](docs/manual-deployment.md)（英文）。除此之外，关于如何使用自动部署脚本，请参见其[使用指南](docs/deployment-script-zh.md)。

## 相比传统基于虚拟机的部署方式

此项目是我个人日常生活中开发出的一种相对更灵活高效的不使用虚拟机的 VPN 部署方式。但同时次方式也有自己的不足之处。一下是我列出的几项此项目和传统部署方式的比较。

| | 传统基于虚拟机的脚本部署（使用 AWS 或任意其他远程主机提供商） | 基于 AWS Client VPN 的部署方式（此项目） |
| --- | --- | --- |
| VPN 协议\* | 不限（取决于使用的脚本） | OpenVPN |
| 收费方式  | 实例开机时间 + 出站流量 | 节点对接时间\*\* + 连接时间/用户 + 出站流量 |
| 部署时间\*\*\* | 数分钟（取决于实例类型的性能以及额其他因素） | 最多15分钟 |
| 连接性能 | 取决于使用的实例类型的网络性能 | 自动根据用量缩放\*\*\*\* | 
| 部署地区 | 任意有可用虚拟机的区域 | 所有 AWS 区域 |
| 免费套餐\*\*\*\*\* | 在创建完账户后 12 个月内，每月 750 小时的免费 `t2.micro` 用量 | 免费套餐不可用 |

<details>
<summary>
展开以查看注释
</summary>

**\*** 你可以选择你想要在远程主机上安装的 VPN 类型，比如 IPsec 或 Shadowsocks 等等。但是若使用  Client VPN 服务，你就必须只能使用 OpenVPN 协议。

**\*\*** 不要将 “对接时间“ (association time) 与 ”用户连接时间“ (connection time per user) 混淆。”对接时间“是指 Client VPN 节点和指定 VPC 的指定子网对接 (association) 的时间。“用户对接时间”是指每用户连接节点的时间。

**\*\*\*** 在一个 ec2 实例上使用脚本安装 VPN 服务器软件需要等待操作系统下载和处理需要的软件包。（比如编译和生成证书的过程）所以说实际的部署时间不定，一般情况下配置越高的系统的等待时间越短。

**\*\*\*\*** 根据 AWS 提供的信息， Client VPN 的网络性能是弹性的，并且能够自动根据需要调整性能（收缩）。 根据我个人的经历， Client VPN 的网络带宽直接取决于你本地的网络环境的最高带宽限制。

**\*\*\*\*\*** 关于 AWS 的入门免费套餐，请参考[此页面](https://aws.amazon.com/free/)。

</details>

## 作者及发行许可

版权所有 (C) 2020-2022 [Scott X. Liang](https://github.com/scottpedia) \<scott.liang@pm.me\>   
[![GPL logo with text](img/gplv3-with-text-84x42.png)](https://www.gnu.org/licenses/gpl-3.0.txt)  
若不特殊声明， 此项目使用 [GNU General Public License Version 3](https://www.gnu.org/licenses/gpl-3.0.txt) 发行。
