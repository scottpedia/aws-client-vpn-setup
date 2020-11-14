# [client-vpn-aio.py](../client-vpn-aio.py)

This is a python script that automatically deploys a ready-to-go OVPN endpoint in your desired AWS region. It also acts as a CLI tool to help you manage the Client VPN Endpoints.

## Requirements

Though it is a python script, there are bash commands called within the program, so it requires a Linux OS environment, with the following prerequisites installed:

- git
- python3
- pip
- aws cli
- boto3

Also please note that you need to have your aws account set up with the aws cli before you can run this program. To do so, run the following command:
```shell
$ aws configure
```

## To Setup a New OVPN Endpoint.

- Clone the repo and run the python script with ***no arguments***.
    
    ```shell
    $ cd /THE_DIR_YOU_WANT_TO_USE
    $ git clone https://github.com/scottpedia/aws-client-vpn-setup.git
    $ cd aws-client-vpn-setup
    $ python3 client-vpn-aio.py # no arguments
    ```

- You will be then prompted to enter some info about the endpoint. You can leave some of them blank and the default values will be used.

- After the endpoint is successfully created, you will see two new files under the `CWD`.

    - `xxxxx.ovpn` is the output file that you use with your OVPN client software to connect to the endpoint.

    - `xxxxx.ovpnsetup` is the file containing the properties of the deployed ovpn endpoint. This will be used to manage the OVPN endpoint it specifies.

- The endpoint is by default turned off right after the script is run. To activate the endpoint, use the management feature of the script. See this [section](#To-manage-an-existing-OVPN-endpoint) for more into about the management feature.

- After the endpoint is turned on, you can connect to the endpoint with your client software. See this [section](../README.md##how-to-set-up-the-client-for-the-vpn-server) from the main article for how to setup the client software on macOS.


