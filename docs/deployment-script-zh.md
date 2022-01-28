# [client-vpn-aio](../client-vpn-aio)

*其他语言版本： [English](./deployment-script.md)*

此页面介绍如何使用此项目包含的脚本来创建一个新的 OpenVPN 节点，并对其进行管理。

## 此页面包含

- [依赖的软件包](#依赖的软件包)
- [如何部署一下新的 OpenVPN 服务器](#如何部署一个新的-OpenVPN-服务器)
- [部署参数](#部署参数)
- [管理已创建的服务器部署](#管理已创建的服务器部署)
- [使用指南](#使用指南)
- [故障排除](#故障排除)

## 依赖的软件包

- git
- python-boto3
- aws-cli
- python3

使用部署脚本前，请确保 aws cli 已经在当前使用的操作系统上使用你的 AWS 账户正确安装和配置好了。 使用一下命令行来配置 aws cli ：

```shell
$ aws configure
```

## 如何部署一个新的 OpenVPN 服务器

- 将此项目克隆到你的文件系统中。
  ```shell
  $ git clone https://github.com/scottpedia/aws-client-vpn-setup.git
  ```
- 进入克隆的项目文件夹。
  ```shell
  $ cd aws-client-vpn-setup
  ```
- 运行脚本。
  ```shell
  ./client-vpn-aio
  ```
  > **注意事项:** 值得注意的是，此脚本在运行的过程中会在当前工作目录下生成一个临时的文件夹，并且次文件夹会在运行结束是被删除。若脚本运行成功，你将会在当前工作目录下收到两个输出的配置文件。所以请保证你目前使用的系统用户对当前工作目录有写权限。
- 交互式的一步一步的输入脚本需要的[部署参数](#部署参数)。
- 当部署完成以后，脚本自动在当前工作目录下生成两个配置文件。
  - `friendlyName.ovensetup` 包含部署信息，被脚本用来对一个以部署的节点进行操作。
  - `friendlyName.ovpn` 是标准的 OpenVPN 服务器连接配置文件，在部署完成以后使用此文件连接到 VPN 服务器。

  你需要首先激活部署过的节点，然后将生成的 `.ovpn` 配置文件载入任何支持 OpenVPN 的客户端软件，然后再连接到目标服务器。

## 部署参数

在部署过程中，脚本将会交互式的询问你想要的部署参数，见以下列表：

1. **部署名称**，此名称将会被多个 AWS 资源参考。此项若为空，一个随机生成的字符串将会被采用。

2. **是否使用[分裂隧道](https://docs.aws.amazon.com/vpn/latest/clientvpn-admin/split-tunnel-vpn.html)模式进行部署。** 如果你想要在连接到 VPN 节点的过程中同时能够访问到当前**本地局域网**内的资源的话，确保使用此特性。此项若为空，此特性将会被默认禁用。

3. **是否使用 AP 隔离**，若此项为是，连接到 VPN 节点的目标子网的客户端主机将无法互相在子网域内通信。若此项为空，此特性将会被默认禁用。

4. **VPN服务器使用的网络协议**，可选项为 `tcp` 或 `udp` 。 若想要一个更加稳定的连接，选择 `tcp` 。 若想要一个更快的连接，选择 `udp` 。 脚本默认会使用 `udp`。

5. **AWS 区域**，部署的目标区域。

6. **阅览并确定部署参数**。 键入 `Enter` 来确定参数。键入任何其他键 + `Enter` 来中止部署进程。

7. **脚本会在当前目录下下载一个 git 仓库前寻求许可**。 键入 `Enter` 来确认此操作。

## 管理已创建的服务器部署

当你已经完成一个节点的部署后，你可以使用脚本的命令对其进行管理。使用此脚本，你可以：
- 激活服务器
- 关闭服务器
- 显示当前服务器的状态
- 切换服务器状态（开或关）
- 终结已部署的节点

**脚本需要获得一个以部署的节点的信息以对此进行管理。** 所以说他需要获取指定部署在成功以后在当前文件目录下产生的配置文件（ `xxx.ovpnsetup` )。

若不给予任何参数，脚本将会自动在当前文件目录下寻找配置文件。若找到多个配置文件，脚本将会选择**最近创建的**一个。

**除此之外**，你也可以使用 `-f` 来指定配置文件的位置。

```shell
$ ./client-vpn-aio [command] -f /path/to/deployment/profile.ovpnsetup
```

更多关于此脚本的使用指南可在以下的 "Helper Text" 中找到。

## Helper Text

```
Usage: ./client-vpn-aio [command] -f [the_config_file]
The python script to deploy and manage the vpn service based on AWS Client VPN Endpoints.

NOTE: PLEASE HAVE YOUR AWS CLI SETUP WITH YOUR AWS ACCOUNT BEFORE YOU RUN THIS SCRIPT.
      THE SCRIPT WILL NOT RUN WITHOUT AN AWS ACCOUNT SETUP WITH THE CLI.

***TO DEPLOY A NEW VPN SERVICE, please run the script without any command.***

***TO MANAGE AN EXISTING ENDPOINT, please use the following commands:***
    status    :   Output the current status of the specified VPN Endpoint.
    on        :   Turn on the VPN
    off       :   Turn off the VPN
    toggle    :   Toggle the VPN
    terminate :   Terminate the selected OVPN setup on AWS.
   *help      :   Output the help

    -f [Filename] (Optional)
    You can use the optional -f flag to specify the file which contains the profile of a specific VPN deployment(*.ovpnsetup).
    Thus you can have multiple deployments active at the same time, and manage each of them with its profile.
    If the file is not speficied, the program will automatically look for one under the current working directory.
    If multiple profiles are found under the CWD, the most recent one will be used.
```

## 故障排除

  - `botocore.exceptions.ClientError: An error occurred (UnrecognizedClientException) when calling the ImportCertificate operation: The security token included in the request is invalid.` 
  如果说你遇到了以上问题，你可能就是试图在一个没有启用的 AWS 区域部署节点。打开你的 AWS 账户页面然后在 **”AWS Regions“** 的分栏内启用你想要使用的 AWS 区域。等几分钟后在试一次，然后你应该就能成功部署了。

  - `subprocess.CalledProcessError: Command '['git', 'clone', 'https://github.com/openvpn/easy-rsa.git', '.easy-rsa-XiJ7jjh11b']' returned non-zero exit status 128.`  
  如果说你遇到了以上的错误，脚本没有成功的获取 `open-rsa` 工具包。此错误发生可能是一下两种原因引起的：

    检查脚本的命令行输出，若其包含 `fatal: unable to access 'https://github.com/openvpn/easy-rsa.git/': Could not resolve host: github.com` , 则引起错误的原因便是你的网络问题。

    如果命令行输出包含 `git: command not found` ， 问题就应该是你的操作系统上没有安装 `git` 。
