# Create Your Private OpenVPN Service with AWS Client VPN Endpoint

> # An auto-deployment script is now available. It automatically deploys a ready-to-go OpenVPN endpoint on AWS. It also manages the deployed endpoints via the command line.(turn-on, turn-off...) Please check out [this page](docs/deployment-script.md) for more info!

<a href="https://trackgit.com"><img src="https://sfy.cx/u/xqO" alt="trackgit-views" /></a>
<a href="#to-create-the-vpn-endpoint-with-aws-cloudformation"><img src="https://img.shields.io/badge/deploy%20to-AWS-orange" /></a>

This repo introduces you a new way to build your own OpenVPN server on AWS, which is more powerful and cost-efficient than traditional VM-based solution. It also offers a auto-setup script to help you deploy the cloud resources and manage the VPN server. Go [**here**](docs/development-script.md) to know more about the auto-setup script.

If you want to know exactly how this works, please go ahead and expand the block below and read through the instruction manual.

# Overview

Traditionally, people build their own VPN servers with VMs on the cloud.(e.g. AWS EC2, Azure VMs, etc). In that context, we need to run installation and setup scripts directly on the server. And we are billed according to the hours the VM has been running, and the outbound internet traffic. The instance type determines the computing power(number of simultaneous users) and also the internet bandwidth(the bandwidth of the VPN).

This project, however, utilizes AWS Client VPN Endpoint, a service already integrated into AWS VPC. There are many advantages of that. First, we are billed for the outbound data usage the same way as the VM-based VPN Services while we enjoy almost unlimited bandwidth of AWS networking infrastructures. Also, the service has better reliability as it is managed by AWS. We are only billed for the connection time, not the active VM uptime as in the traditional method.

<details>
<summary>

^^^Table of Contents(Click the triangle above to expand the block)
=================

<a href="https://openvpn.net/"><img src="img/openvpn-icon.png" width="20%" align="right"></a>


<!--ts-->
   * [Create Your Private OpenVPN Service with AWS Client VPN Endpoint](#create-your-private-openvpn-service-with-aws-client-vpn-endpoint)
   * [Overview](#overview)
   * [Table of Contents](#table-of-contents)
      * [What are AWS and AWS Client VPN Endpoint?](#what-are-aws-and-aws-client-vpn-endpoint)
      * [Step 1 : Create an AWS Account](#step-1--create-an-aws-account)
      * [Step 2 : Sign in to the Console with your AWS account](#step-2--sign-in-to-the-console-with-your-aws-account)
      * [Step 3 : Select the Region in which You Want to Set up Your Service](#step-3--select-the-region-in-which-you-want-to-set-up-your-service)
         * [The AWS Regions where Client VPN Endpoints are Available](#the-aws-regions-where-client-vpn-endpoints-are-available)
         * [<strong>How to select the region for your VPN Service?</strong>](#how-to-select-the-region-for-your-vpn-service)
      * [Step 4 : Create the server and client certificates for AWS Certificate Manager](#step-4--create-the-server-and-client-certificates-for-aws-certificate-manager)
      * [Step 5 : Create the Client VPN Endpoint](#step-5--create-the-client-vpn-endpoint)
         * [To Create the VPN endpoint manually.](#to-create-the-vpn-endpoint-manually)
      * [How to manage the Client VPN Endpoint](#how-to-manage-the-client-vpn-endpoint)
         * [<strong>To turn ON the VPN server</strong>](#to-turn-on-the-vpn-server)
         * [<strong>To turn OFF the VPN server</strong>](#to-turn-off-the-vpn-server)
      * [How to set up the client for the VPN server?](#how-to-set-up-the-client-for-the-vpn-server)
         * [Install Tunnelblick](#install-tunnelblick)
         * [Export the Configuration File](#export-the-configuration-file)
         * [Install the configuration](#install-the-configuration)
         * [Connect to the Endpoint](#connect-to-the-endpoint)
      * [The Pricing for AWS Client VPN Endpoint](#the-pricing-for-aws-client-vpn-endpoint)
      * [Conclusion](#conclusion)
      * [References](#references)

<!-- Added by: black, at: Wed Nov 11 14:25:05 EST 2020 -->

<!--te-->

</summary>

<a href="https://aws.amazon.com/vpn/"><img src="img/client-vpn.png" width="40" align="right"></a>

## What are AWS and AWS Client VPN Endpoint?

Amazon Web Service(AWS) is a cloud computing platform by Amazon founded in 2006. It is now one of the largest and most popular cloud computing platforms in the world. It provides a variety of services like Virtual Machine, Managed Database, etc.

<a href="https://aws.amazon.com/"><img src="img/aws-logo.png" width="120" align="right"></a>

One of the services being provided by AWS is Client VPN Endpoint. It helps to create an endpoint with which you can directly access the resources(like virtual machines) within a VPC via an OpenVPN connection to the designated subnet.

**However, with some modifications to the configuration, we can turn that service into a working VPN server that allows us to anonymously access the public internet with** <font color="red">**amazing performance!**</font> The figure below briefly explains how the client VPN endpoint intends to work.   

![how aws client vpn endpoint works](https://docs.aws.amazon.com/vpn/latest/clientvpn-admin/images/architecture.png)


## Step 1 : Create an AWS Account

> If you already have a working AWS account, you can skip to [Step 3](#step-3--select-the-region-in-which-you-want-to-set-up-your-service).

So the first step would be creating an AWS account. We need to have a working AWS account to create resources on the platform. Go to [the sign-up website](https://portal.aws.amazon.com/billing/signup#/start) to create a free account. Fill in the information forms as instructed.

![the sign-up website](img/aws-signup.png)

> Note that by creating a free AWS account, you are automatically granted free access to some of its services for the first year following the sign-up date. Go to [this page](https://aws.amazon.com/free) to get more information.  

## Step 2 : Sign in to the Console with your AWS account

Sign in to the AWS Management Console with the account you just created on [on this page](https://console.aws.amazon.com/). Select **"Root User"** and enter the email address, then click "Next". Enter the password on the following page and click "Sign in".

![the sign-in page](img/aws-signin.png)

You should be on this page after signing in. This is the main page of the AWS Management Console where you can find the index of all the services on this platform.

![AWS Management Console](img/aws-management-console.png)

## Step 3 : Select the Region in which You Want to Set up Your Service

Please notice that most of the AWS services are regional-independent. That means that two services of the same particular kind in two different regions are completely isolated. The same applies to the Client VPN Endpoints. So we need to decide which region you want you deploy your service to. 

> Note that not all AWS regions provide Client VPN Endpoints.

### The AWS Regions where Client VPN Endpoints are Available

<details>
<summary>Click to expand the list.</summary>

- US East (N. Virginia)
- US East (Ohio)
- US West (N. California)
- US West (Oregon)
- Asia Pacific (Mumbai)
- Asia Pacific (Seoul)
- Aisa Pacific (Singapore)
- Aisa Pacific (Sydney)
- Asia Pacific (Tokyo)
- Canada (Central)
- Europe (Frankfurt)
- Europe (Ireland)
- Europe (London)
- Europe (Stockholm)
</details>

And you can select the region from the list bar at the top right corner. Please do this **BEFORE** creating the endpoint.

![Select the region you prefer](img/region-selection.png)

### **How to select the region for your VPN Service?**

Usually, it highly depends on your current geolocation and that of the destination you want to access. For example, I am now living in Canada and wanting to access a Japanese video website that is exclusive to users in Japan. In that case, I would certainly select Asia Pacific (Tokyo) as my VPN region. 

Also, for a lot of Chinese users, the VPN is used to bypass the [GFW](https://en.wikipedia.org/wiki/Great_Firewall)(Great Firewall). So simply all the regions are suitable for this scenario, as the ones closer to China may have lower latencies. 

For simply encrypting the web traffic, the endpoint that is closest to you would be ideal as the latency is minimized.

**In this tutorial, we are going to create the VPN endpoint in the AWS region of Oregon. (US-West-2)**

## Step 4 : Create the server and client certificates for AWS Certificate Manager

We need to create the certificates for both the clients and the server. We are going to first generate the keys and the certificates locally on our computer and then uploading them to the Certificate Manager via either the web console or AWS CLI. 

> For now, this article only demonstrates how to create keys and certificates on computers running **Unix-like systems**. For how to create keys and certificates for AWS Certificate Manager on Windows, see **[this page](https://docs.aws.amazon.com/vpn/latest/clientvpn-admin/client-authentication.html#windows)**. 

**To generate the server and client certificates and keys and upload them to ACM(AWS Certificate Manager)**

1. Open your favorite terminal emulator and select a directory you want to use. Clone the OpenVPN `easy-rsa` repo to your local computer and navigate to the `easy-rsa/easyrsa3` folder. 

    `$ git clone https://github.com/OpenVPN/easy-rsa.git`

    `$ cd easy-rsa/easyrsa3`

2. Initialize a new PKI environment.

    `$ ./easyrsa init-pki`

3. Build a new certificate authority(CA).

    `$ ./easyrsa build-ca nopass`

    Follow the prompts to build the CA.

4. Generate the server certificate and key.

    `$  ./easyrsa build-server-full server nopass`

5. Generate the client certificate and key.

    > **Make sure to save the client certificate and key because you will need them [later](#export-the-configuration-file) to configure the client.**

    `$ ./easyrsa build-client-full client1.domain.tld nopass`

6. Copy the server certificate and key and the client certificate and key to a custom folder and then navigate into the custom folder.   

    Before you copy the certificates and keys, create the custom folder by using the `mkdir` command. The following example creates a custom folder in your home directory. 

    ```shell
    $ mkdir ~/custom_folder/
    $ cp pki/ca.crt ~/custom_folder/
    $ cp pki/issued/server.crt ~/custom_folder/
    $ cp pki/private/server.key ~/custom_folder/
    $ cp pki/issued/client1.domain.tld.crt ~/custom_folder
    $ cp pki/private/client1.domain.tld.key ~/custom_folder/
    $ cd ~/custom_folder/
	```
    You should be getting a directory layout like this:

    ```shell
    custom_folder
    ├── ca.crt
    ├── client1.domain.tld.crt
    ├── client1.domain.tld.key
    ├── server.crt
    └── server.key

    0 directories, 5 files
    ```

7. Go to **AWS Certificate Manager** on the web console.

    ![Find Certification Manager](img/find-certificate-manager.png)

    Click on **"Get Started"**.

    ![Click Get Started](img/get-started-acm.png)

8. Import the certificates for both the server and client.

    Click on **"Import a certificate"**.
    
    ![Click Import a certificate](img/import-a-certificate-acm.png)

    **To import the key and certificate for the server**

    > To view the content of these files, use your favorite text editor.
    > Simply use "TextEdit" if you are on macOS.

    - Copy the content of `server.crt` into the **1st** text field **"Certificate Body"**.

    - Copy the content of `server.key` into the **2nd** text field **"Certificate Private Key"**.

    - Copy the content of `ca.crt` into the **3rd** text field **"Certificate Chain"**

    - Click **"Next"** to proceed.

    ![import the key and certificate for the server](img/import-server-certificate.png)

    - Click **"Review and import"** on the next page.

    - And click **"Import"** to complete the process.

    **To do the same for the client**

    - Click **"Import a certificate"** on the next page.

    - Copy the content of `client1.domain.tld.crt` into the **1st** text field **"Certificate Body"**.

    - Copy the content of `client1.domain.tld.key` into the **2nd** text field **"Certificate Private Key"**.

    - Copy the content of `ca.crt` into the **3rd** text field **"Certificate Chain"**

    - Click **"Next"** to proceed.

    ![import the key and certificate for the client](img/import-client-certificate.png)

    - Click **"Review and import"** on the next page.

    - And click **"Import"** to complete the process.

    Now, you should be getting two available certificates after returning to ACM's main page.

    ![final ACM console](img/acm-console.png)

We now have the certificates ready for our Client VPN Endpoints.


## Step 5 : Create the Client VPN Endpoint

### To Create the VPN endpoint manually.

Scroll down the page to find **"VPC"** under the category of **"Networking & Content Delivery"** and open the link. 

![the VPC item](img/vpc.png)

![the VPC console](img/vpn-console.png)

Find and open **"Client VPN Endpoints"** from the side panel on the left.

![Client VPN Endpoint](img/client-vpn-endpoint.png)

You should be on this page following the last action. 

![Client VPN Endpoint page](img/client-vpn-endpoint-page.png)

**To create a Client VPN Endpoint**

1. Click **"Create Client VPN Endpoint"** on the top.

2. Enter the friendly name you choose into the **"Name Tag"**. (Optional)

3. Write a description for your endpoint into the **"Description"**. (Optional)

4. Enter the Client IPv4 CIDR into the **"Client IPv4 CIDR"**

    > **Note that the IP address range cannot overlap with the target network or any of the routes that will be associated with the Client VPN endpoint. The client CIDR range must have a block size that is between /12 and /22 and not overlap with VPC CIDR or any other route in the route table. You cannot change the IP address range after you create the Client VPN endpoint.**

    The sample values are shown in the image below.

    ![VPN endpoint 1](img/vpn-endpoint-creation-1.png)

5. Select the server certificate we just created for **"Server certificate ARN"**. In this case, the name of our certificate is **"server"**.

    ![VPN endpoint 2](img/endpoint-select-server-certificate.png)

6. Check **"Use mutual authentication"**.

7. Select the client certificate we just created for **"Client certificate ARN"**. In this case, the name of the certificate is **"client1.domain.tld"**.

    ![VPN endpoint 3](img/endpoint-select-client-certificate.png)

8. Select **"No"** for **"Do you want to log the details on client connections?"**.

9. Leave blank the DNS server addresses and go to the next step.

10. Select **"UDP"** as the default transporting protocol.

11. Enable [**"Split Tunnel"**](https://en.wikipedia.org/wiki/Split_tunneling) to allow access to the resources in your own Local Area Network(LAN) while connected to the VPN.

    > The split-tunnel connection pushes the route table of the VPN endpoint to the client so that only part of the traffic goes through the VPN endpoint. 

12. Select the VPC from which the subnets will be associating with the endpoint.

13. Select **443** for **"VPN port"**.

14. Click **"Create Client VPN Endpoint"** to proceed.

    You then should be able to see this page. Click **"Close"** to go back to the **"Client VPN Endpoints"** panel.

    ![creation successful](img/vpn-endpoint-creation-2.png)

15. Now we go to the **"Authorization"** tab.

    ![authorization](img/endpoint-authorization.png)

16. Click **"Authorize Ingress"** to make a new rule.

17. Enter **"0.0.0.0/0"** for **"Destination network to enable"**.

    > In doing so, we authorize all the users with the certificate to connect to the endpoint, regardless of their public IP addresses. You can also enter a specific IP range in CIDR citation to authorize the users within a specific networking environment. For example, you may enter the IP range of your house to only allow the connections from there.

    ![make a new authorization](img/add-authorization-rule.png)

18. Click **"Add authorization rule"** to add the rule.

Now you have created a Client VPN Endpoint that is ready to go in your desirable AWS region.

## How to manage the Client VPN Endpoint

Now we need to know how to use the Client VPN Endpoint that we have just created. The VPN endpoint that we just created is not intended for common uses(encrypting the web traffic, hide your IP address...) as [mentioned previously](#What-are-AWS-and-AWS-Client-VPN-Endpoint?), so it may not be as convenient to manage as for ordinary users. Extra steps are needed to turn on/off the server. Let's now go through how to turn it **ON** and **OFF**.

### **To turn ON the VPN server**

Because of the special nature of the Client VPN Endpoint, the server needs to be manually turned on and off. Though you can leave if on all the time, you will be billed more for the extra time when the endpoint is associated. We will be talking about the cost later in this article. 

To turn on the server, we need to first associate the target network with the endpoint and then create an extra route to enable Internet access when connected to the endpoint.

- First, we go to the Client VPN Endpoint control panel.

    ![The Control Panel](img/client-vpn-endpoint-control-panel.png)

- Then we go to the **"Association"** tab under the selected VPN endpoint. This is where we manage the subnets associated with the endpoint. There should be no Client VPN Target Networks here.

    ![The association tab](img/association-tab.png)

- Click **"Associate"** to associate the endpoint with a target network(a VPC subnet). 

    1. Select the VPC where the target network is from.

    2. Select the subnet to associate with.

    3. Click **"Associate"** to make the association.

        ![Associate target network](img/associate-target-network.png)

    4. Click **"Close"** to return to the control panel.

        It usually takes less than ten minutes for the server to finish the association. So the endpoint status will not change immediately following this action.

        ![association success](img/association-success.png)

- Go back to the control panel and go to the **"Route Table"** tab.

    1. We are now going to modify the endpoint's route table, adding an additional rule that defines the flow of the internet traffic within the target network. By doing this, we can later access the internet when connected to the VPN endpoint.

        ![create one additional route](img/create-additional-route.png)

    2. Click **"Create Route"** on the side panel. 

    3. Enter **"0.0.0.0/0"** for **"Route destination"**, and select the subnet that you want to associate with the VPN endpoint. The **"Description"** is optional, so we are going to leave it blank for now.

        ![create additional route](img/create-additional-route-2.png)

    4. Click **"Create Route"** to proceed.

        ![finish creating the route](img/create-additional-route-3.png)

        You should be able to see two routes being created now.

        ![routes being created](img/routes-being-created.png)

- Now the subnet is being associated. And the state of the endpoint remains **"Pending-associate"** until the endpoint is ready to accept incoming connections. It usually takes less than 10 minutes to complete the association.

    When the endpoint is fully associated or 'turned on' in our case, the state of the endpoint will become **"Available"** with a green indicator next to the caption.

    ![endpoint available](img/endpoint-available.png)

    By the time it becomes ready, the endpoint is ready to establish connections with the clients. 

### **To turn OFF the VPN server**

We now assume that the current state of the VPN endpoint is **"Available"**, which means that it is **"ON"** in our case. And the route table of the endpoint should contain two rules, one of which is an additional one that defines the flow of the internet traffic within the target network.

To **"turn off"** the server, we only need to disassociate the target subnet from the endpoint. The additional route that we created will be automatically deleted following the disassociation. However, that nature of the endpoint requires us to create the additional route every time when we try to turn on the server. 

The following section walks you through how to **"turn off"** of the server. **(disassociate the target subnet)**

- We first go to the control panel and navigate to the **"Association"** tab. 

    ![Association tab](img/to-disassociate-subnet.png)

- Select the one association that you see on the list by clicking the checkbox at the left of the row.

- And then click **"Disassociate"**.

    ![the Disassociation](img/to-disassociate-subnet-2.png)

- Click **"Yes, Disassociate"** to confirm the disassociation when being prompted. 
    
    ![Disassociation prompt](img/disassociation-prompt.png)

- By then we have just **"turned off"** the VPN service. You do not need to worry about the route we created as it is now being deleted automatically following the disassociation of the target network, as shown in the picture below. 

    ![Routes being deleted](img/deleting-routes.png)

## How to set up the client for the VPN server?

After the server is set up, we need to do some work to enable the client to connect to the server. In this case, we are going to use **TunnelBlick** as the client software.  Go to its [website](https://tunnelblick.net/) to get the latest release. If you are a Windows user who happened to be here, you can visit this [page](https://docs.aws.amazon.com/vpn/latest/clientvpn-user/windows.html) to get more information on VPN client softwares for Windows.

<a href="https://tunnelblick.net/"><img src="img/tunnelblick.png" height="80" align="right" ></img></a>

### Install Tunnelblick

> For a detailed walk-through of the installation process, see this [page](https://tunnelblick.net/cInstall.html) on `tunnelblick.net`. Get back to this page after completing the installation.

### Export the Configuration File

We need to have a configuration file in order to connect to the VPN endpoint with our client software. The following section focuses on how to export the OpenVPN configuration file of our VPN endpoint. 

- Go to the AWS Client VPN Endpoint control panel where your existing endpoint is located. Select the endpoint that we just created. And Click **"Download Client Configuration"**. 

    ![Download configuration](img/download-configuration.png)

- Click **"Download"** when prompted.

    ![Click Download](img/click-download.png)

- The downloaded file looks like this:

    > The configuration file downloaded from AWS will always have the same name(downloaded-client-config.ovpn) no matter what. So you can optionally change the name of the configuration file so it is recognized easier. 

    ![Downloaded file](img/downloaded-configuration.png)

- We need to make some edits to the raw configuration file downloaded from AWS before we can use it to connect to the endpoint. First, we need to **prepend a random string to the endpoint URL** in the configuration file. This is an effort by AWS to prevent DNS caching of the endpoint domains. Here is an example.

    1. Open the `.ovpn` configuration file with your favorite text editor.

    2. You should be able to find a line starting with **`remote`**, something like this.

        <code>
            remote cvpn-endpoint-0011abcabcabcabc1.prod.clientvpn.eu-west-2.amazonaws.com 443
        </code>

    3. Add a random string before the URL.

        <code>
            remote <font color="red">rad0mstr1nghere</font>.cvpn-endpoint-0011abcabcabcabc1.prod.clientvpn.eu-west-2.amazonaws.com 443
        </code>

- Now, we need the **CLIENT KEY AND CERTIFICATE** which we [previously](#step-4--create-the-server-and-client-certificates-for-aws-certificate-manager) created with easy-rsa, specifically, `client1.domain.tld.key` and `client1.domain.tld.crt`.

    1. Open the downloaded configuration file with your favorite text editor. In this case, I am using `nano`.

    2. Create `<cert></cert>` and `<key></key>` before the line `reneg-sec 0` in the configuration file. Here is an example:

        ```xml
        client
        dev tun
        proto udp
        remote asdf.cvpn-endpoint-0011abcabcabcabc1.prod.clientvpn.eu-west-2.amazonaws.com 443
        remote-random-hostname
        resolv-retry infinite
        nobind
        persist-key
        persist-tun
        remote-cert-tls server
        cipher AES-256-GCM
        verb 3

        <ca>
        ... ... ...
        </ca>

        <cert>
        
        </cert>

        <key>
        
        </key>

        reneg-sec 0
        ```
    
    3. Add the contents of the client certificate between `<cert></cert>` tags and the contents of the private key between `<key></key>` tags to the configuration file.

        ```xml
        <cert>
        Contents of client certificate (.crt) file
        </cert>

        <key>
        Contents of private key (.key) file
        </key>
        ```

    4. Save the configuration file. 

- We now have a working configuration file for the client.

### Install the configuration

> Make sure that you have your configuration file properly saved. To install the configuration, launch Tunnelblick if it is not already running, and drag the configuration file and drop it onto the Tunnelblick icon in the menu bar. And go to visit [this page](https://tunnelblick.net/cInstallConfigurations.html) on `tunnelblick.net` for more details on installing OVPN configurations.

### Connect to the Endpoint

- **Make sure that the Endpoint is "turned on".**

- Click the Tunnelblick icon on the menu bar and select your VPN profile to connect to the endpoint.

    <img src="img/menubar-connect.png" width="25%" height="25%">

- You should be able to see a status window at the right top corner of the screen when the client is connecting. Wait until it turns green.

    <img src="img/authorizing-status.png" width="25%" height="25%">
    <img src="img/connected-status.png" width="25%" height="25%">

- Now, we are connected to the endpoint. Let's do some tests.

    1. First let's see if our public IP address changed with `curl`.

        ```bash
        $ curl api.ipify.org
        ```

        This is our original public IP address.

        ![Original IP](img/ipify-original-cmd.png)

        This is our current public IP address.

        ![Current IP](img/ipify-cmd.png)

    2. Let's check the owner of this IP with `whois`.

        ```bash
        $ whois $(curl api.ipify.org) | less
        ```

        ![WHOIS](img/whois-cmd.png)

        We can now see that our current IP address belongs to Amazon.com, Inc. That means that we are properly connected.

        You may also see your **"Apparent Public IP Address"** on Tunnelblick's drop-down menu after connecting to the endpoint.

        ![Screenshot](img/connect-screen.png)

## The Pricing for AWS Client VPN Endpoint

We can find the pricing information of AWS Client VPN Endpoint on [this page](https://aws.amazon.com/vpn/pricing/). 

[![AWS VPN Pricing](img/aws-vpn-pricing.png)](https://aws.amazon.com/vpn/pricing/)

> **In AWS Client VPN you are charged for the number of active client connections per hour and the number of subnets that are associated to Client VPN per hour.** You start by creating a Client VPN endpoint and associating subnets to that endpoint. You can associate multiple subnets from within an Amazon Virtual Public Cloud (Amazon VPC) to a Client VPN endpoint as long as they are all part of the same AWS account. Each subnet associated with the Client VPN endpoint has to belong to a different Availability Zone and we will bill the Amazon VPC account owner. Billing starts once the subnet association is made and each partial hour consumed is pro-rated for the hour. The next step is to connect users to the Client VPN endpoint. **This can happen dynamically as users need the service and you are charged a second fee based on the number of active clients that are connected to the Client VPC endpoint, per hour. Any client connection that is less than an hour is also pro-rated for the hour.**

**Because we are accessing the Internet with the VPN for our purpose, we are also billed for the outbound data transfer made. You can check out data transfer pricings in different AWS regions [here](https://aws.amazon.com/ec2/pricing/on-demand/#Data_Transfer).**

[![Data Transfer](img/data-transfer-rate.png)](https://aws.amazon.com/ec2/pricing/on-demand/#Data_Transfer)

## Conclusion

**According to my own experience, the setup of VPN is very cost-efficient as you only pay as you go without any subscription.** It is also much cheaper than building a VPN server with an EC2 instance. But it is more complex than conventional VPN services. The long time it takes to boot up is a very bad trait. It is highly recommended to turn off the server every time you stop using it. You will be billed extensively if you leave the endpoint available for long durations without using it. 

**It is also a very high-performance solution.** The available bandwidth of the VPN directly depends on that of your internet connection. I have personally not experienced the bandwidth of the VPN being throttled, as it is being described on the AWS website:
<a href="https://aws.amazon.com/vpn/features/#AWS_Client_VPN_features">
> It is elastic, and automatically scales to meet your demand. </a>

<font color="red">**For the users in China who wish to bypass the GFW**</font>, this is a very good option as well, as there is absolutely no way the government can ban the DNS and IP addresses of public cloud platforms like AWS. So it is a very stable solution. Its performance, according to my experience using it in China, is not bad. Both downlink and uplink bandwidth can go up to **5MB/s** easily with a good Internet connection.

I will try to write a script to simplify the process to set up a VPN like this, and also to easily turn it on and off as well.

## References

* [AWS Client VPN User Guide](https://docs.aws.amazon.com/vpn/latest/clientvpn-user/index.html)
* [AWS Client VPN Administrator Guide](https://docs.aws.amazon.com/vpn/latest/clientvpn-admin/index.html)
* [AWS Client VPN features](https://aws.amazon.com/vpn/features/#AWS_Client_VPN_features)
* [AWS VPN pricing](https://aws.amazon.com/vpn/pricing/)
* [Tunnelblick Documentation](https://tunnelblick.net/documents.html)

</details>
