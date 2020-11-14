#!/usr/bin/env python3
import time
from sys import stdout
import boto3
import sys
import traceback
import string
import random
import subprocess
from pathlib import Path
from json import dumps

client_ec2 = None
client_acm = None
client_cf = None

'''
So please leave these values below blank if you want to specify the ids with system environment variables.
Otherwise, the values specified here would override the environment variables.
'''
CLOUDFORMATION_STACK_ID = ""
CLIENT_VPN_ENDPOINT_ID = ""
SERVER_CERTIFICATE_ARN = ""
CLIENT_CERTIFICATE_ARN = ""
SUBNET_ID = ""
USER_SETTINGS = {}
TEMPLATE_CONTENT = ''
CLIENT_CERT = ''
CLIENT_KEY = ''
HELP_SCRIPT = '''
Usage: ./client-vpn-manager [command] -f [the_config_file]
The python script to deploy and manage the vpn service based on AWS Client VPN Endpoints.

NOTE: PLEASE HAVE YOUR AWS CLI SETUP WITH YOUR AWS ACCOUNT BEFORE YOU RUN THIS SCRIPT.
      THE SCRIPT WILL NOT RUN WITHOUT AN AWS ACCOUNT SETUP WITH THE CLI.

***TO DEPLOY A NEW VPN SERVICE, please run the script without any command or option.***

***TO MANAGE AN EXISTING ENDPOINT, please use the following commands:***
    status  :   Output the current status of the specified VPN Endpoint.
    on      :   Turn on the VPN
    off     :   Turn off the VPN
    toggle  :   Toggle the VPN
   *help    :   Output the help 

    -f [Filename] (Optional)
    You can use the optional -f flag to specify the file which contains the profile of a specific VPN deployment.
    Thus you can have multiple deployments active at the same time, and manage each of them with its profile.
    If the file is not speficied, the program will automatically look for one under the current working directory.
    If multiple profiles are found under the CWD, should the most recent one be used.
'''

# *** THE MANAGEMENT CODE SECTION STARTS ***


def get_association_state():
    response = client_ec2.describe_client_vpn_endpoints(
        ClientVpnEndpointIds=[
            CLIENT_VPN_ENDPOINT_ID,
        ]
    )
    if len(response['ClientVpnEndpoints']) > 0:
        return response['ClientVpnEndpoints'][0]['Status']['Code']
    else:
        raise Exception("No existing client vpn endpoint found.")


# This function returns True if the endpoint is associated with the target network, vice versa.
def is_associated():
    state = get_association_state()
    if state == "pending-associate":  # When the subnet is NOT associated
        return False
    elif state == "available":  # When the subnet is associated
        return True
    # the possibility of an endpoint neither assiciated nor available.(Unexpected state)
    else:
        raise Exception("An unexpected state detected.")


def associate_target_network() -> None:
    response = client_ec2.associate_client_vpn_target_network(
        ClientVpnEndpointId=CLIENT_VPN_ENDPOINT_ID,
        SubnetId=SUBNET_ID,
    )
    if response["Status"]["Code"] != 'associating':
        raise Exception("Unexpected association state detected : {}".format(
            response['Status']['Code']))


def create_internet_routing_rule() -> None:
    response = client_ec2.create_client_vpn_route(
        ClientVpnEndpointId=CLIENT_VPN_ENDPOINT_ID,
        # The CIDR block that allows the traffic in and out of the public internet.
        DestinationCidrBlock='0.0.0.0/0',
        TargetVpcSubnetId=SUBNET_ID,
    )
    if response['Status']['Code'] != 'creating':
        raise Exception("Unexpected state detected after creating the route : {}".format(
            response['Status']['Code']))


def get_current_association_id():
    response = client_ec2.describe_client_vpn_target_networks(
        ClientVpnEndpointId=CLIENT_VPN_ENDPOINT_ID
    )
    if len(response['ClientVpnTargetNetworks']) > 0:
        return response['ClientVpnTargetNetworks'][0]['AssociationId']
    else:
        raise Exception(
            "No association ID found, probably there is no terget network associated right now.")


def disassociate_target_network() -> None:
    associationId = get_current_association_id()
    response = client_ec2.response = client_ec2.disassociate_client_vpn_target_network(
        ClientVpnEndpointId=CLIENT_VPN_ENDPOINT_ID,
        AssociationId=associationId,
    )
    if response['Status']['Code'] != 'disassociating':
        raise Exception("Unexpected status detected after disassociation : {}".format(
            response['Status']['Code']))


def turn_on() -> None:
    print(
        f"Associating the target subnet({SUBNET_ID}) and creating the new route(0.0.0.0/0).")
    print("... ... ...")
    associate_target_network()
    print("... ... ...")
    create_internet_routing_rule()
    print("Done.")


def get_status() -> None:
    print("Getting the association state of the client vpn endpoint : \n{}".format(
        CLIENT_VPN_ENDPOINT_ID))
    print("... ... ...")
    print("Currently, and state of association is : \n{}".format(
        get_association_state()))
    print("Done.")


def disassociate() -> None:
    print(
        f"Disassociating the target subnet({SUBNET_ID})\nfrom the client vpn endpoint({CLIENT_VPN_ENDPOINT_ID}).")
    print("... ... ...")
    disassociate_target_network()
    print("Done.")


def manage():
    # The function is executed when the user wants to manage an existing VPN service.
    global CLIENT_VPN_ENDPOINT_ID
    global SUBNET_ID
    commandInput = sys.argv[1]
    if commandInput == "status":
        get_status()
    elif commandInput == "off":
        disassociate()
    elif commandInput == "on":
        turn_on()
    elif commandInput == "help":
        print(HELP_SCRIPT)
    else:
        raise Exception(
            f"No such command as \"{commandInput}\" is available. Please check you input and try again.\n{HELP_SCRIPT}")

# *** THE MANAGEMENT CODE SECTION ENDS ***
# *** THE DEPLOYMENT CODE SECTION STARTS ***


def get_user_settings():
    # The function gets the required deployment settings from the user.
    global USER_SETTINGS
    USER_SETTINGS = {
        'friendlyName': '',
        'isSplitTunneled': False,
        'region': ''
    }
    print("Getting user settings...")
    friendlyName = input(
        "Please give your new VPN Service a friendly name:\n[Default: auto-generated random characters]> ")
    if friendlyName == '':
        print("Empty string detected! Your VPN friendly name is now:")
        friendlyName = ''.join(random.SystemRandom().choice(
            string.ascii_letters + string.digits) for _ in range(10))
        print(friendlyName)
    else:
        print("Your current VPN friendly name is:\n{}".format(friendlyName))
    USER_SETTINGS['friendlyName'] = friendlyName

    isSplitTunneled = input(
        "Do you want to enable split tunnel for your VPN?\n[Default: Nn] <Yy or Nn> ").capitalize()
    while True:
        if isSplitTunneled == 'Y':
            USER_SETTINGS['isSplitTunneled'] = True
            print("The VPN will be split-tunnel enabled.")
            break
        elif isSplitTunneled == 'N':
            USER_SETTINGS['isSplitTunneled'] = False
            print("The VPN will be split-tunnel disabled.")
            break
        elif isSplitTunneled == '':
            USER_SETTINGS['isSplitTunneled'] = False
            print("The VPN will be split-tunnel disabled as default.")
            break
        else:
            print("Unrecognized input, please try again!")
            isSplitTunneled = input(
                "Do you want to enable split tunnel for your VPN?\n[Default: Nn] <Yy or Nn> ").capitalize()

    print("The following AWS regions support Client VPN Endpoint:")
    availableRegions = '''
    1. US East (N. Virginia)
    2. US East (Ohio)
    3. US West (N. California)
    4. US West (Oregon)
    5. Asia Pacific (Mumbai)
    6. Asia Pacific (Seoul)
    7. Aisa Pacific (Singapore)
    8. Aisa Pacific (Sydney)
    9. Asia Pacific (Tokyo)
    10. Canada (Central)
    11. Europe (Frankfurt)
    12. Europe (Ireland)
    13. Europe (London)
    14. Europe (Stockholm)
    '''
    regionsMapping = [
        "",
        "us-east-1",
        "us-east-2",
        "us-west-1",
        "us-west-2",
        "ap-south-1",
        "ap-northeast-2",
        "ap-southeast-1",
        "ap-southeast-2",
        "ap-northeast-1",
        "ca-central-1",
        "eu-central-1",
        "eu-west-1",
        "eu-west-2",
        "eu-north-1"
    ]
    print(availableRegions)
    while True:
        regionNumber = input(
            "Please select one from the list above. Enter the number only:\n[no Default] <1-14> ")
        try:
            regionNumberInteger = int(regionNumber)
            if regionNumberInteger <= 14 and regionNumberInteger >= 1:
                USER_SETTINGS['region'] = regionsMapping[regionNumberInteger]
            else:
                raise Exception(
                    "Value ({}) not found. Please re-enter your region number.".format(regionNumber))
        except Exception as e:
            print(e)
        else:
            print("Your choice is {}".format(USER_SETTINGS['region']))
            break

    print("Please review your settings:\n {}".format(USER_SETTINGS))
    if input("Please press ENTER to proceed, any other key to abort.\n> ").capitalize() != "":
        print("Abort.")
        sys.exit(1)


def generate_credentials():
    # This function first clones https://github.com/openvpn/easy-rsa.git and generates certificates for both server and clients.
    # And saves it under the current directory.
    # After that, it uploads the credentials to ACM.
    global CLIENT_CERT
    global CLIENT_KEY
    print("Generating credentials...")
    input("In the process, you will be prompted to enter the DN for your CA. You can just leave it blank and press enter.\nPlease type enter to confirm > ")
    commandsToRun = [
        'git clone https://github.com/openvpn/easy-rsa.git .easy-rsa-{}'.format(
            USER_SETTINGS['friendlyName']),
        '.easy-rsa-{}/easyrsa3/easyrsa init-pki'.format(
            USER_SETTINGS['friendlyName']),
        '.easy-rsa-{}/easyrsa3/easyrsa build-ca nopass'.format(
            USER_SETTINGS['friendlyName']),
        '.easy-rsa-{}/easyrsa3/easyrsa build-server-full server-{} nopass'.format(
            USER_SETTINGS['friendlyName'], USER_SETTINGS['friendlyName']),
        '.easy-rsa-{}/easyrsa3/easyrsa build-client-full {}.domain.tld nopass'.format(
            USER_SETTINGS['friendlyName'], USER_SETTINGS['friendlyName']),
        'mkdir {}.ovpnsetup'.format(USER_SETTINGS['friendlyName']),
        'cp pki/ca.crt ./{}.ovpnsetup'.format(USER_SETTINGS['friendlyName']),
        'cp pki/issued/server-{}.crt ./{}.ovpnsetup'.format(
            USER_SETTINGS['friendlyName'], USER_SETTINGS['friendlyName']),
        'cp pki/private/server-{}.key ./{}.ovpnsetup'.format(
            USER_SETTINGS['friendlyName'], USER_SETTINGS['friendlyName']),
        'cp pki/issued/{}.domain.tld.crt ./{}.ovpnsetup'.format(
            USER_SETTINGS['friendlyName'], USER_SETTINGS['friendlyName']),
        'cp pki/private/{}.domain.tld.key ./{}.ovpnsetup'.format(
            USER_SETTINGS['friendlyName'], USER_SETTINGS['friendlyName']),
        'rm -rf .easy-rsa-{}'.format(USER_SETTINGS['friendlyName']),
        'rm -rf pki'
    ]
    for command in commandsToRun:
        subprocess.run(command.split(' '), stdout=sys.stdout, check=True)
    else:
        print("Done.\n")

    # pre-load the certificates into the memory.
    print("Retrieving the certificates...")
    CA_CERT = open(
        f"./{USER_SETTINGS['friendlyName']}.ovpnsetup/ca.crt", "r").read().encode('UTF-8')
    SERVER_CERT = open(
        f"./{USER_SETTINGS['friendlyName']}.ovpnsetup/server-{USER_SETTINGS['friendlyName']}.crt", "r").read().encode('UTF-8')
    SERVER_KEY = open(
        f"./{USER_SETTINGS['friendlyName']}.ovpnsetup/server-{USER_SETTINGS['friendlyName']}.key", "r").read().encode('UTF-8')
    CLIENT_CERT = open(
        f"./{USER_SETTINGS['friendlyName']}.ovpnsetup/{USER_SETTINGS['friendlyName']}.domain.tld.crt", "r").read().encode('UTF-8')
    CLIENT_KEY = open(
        f"./{USER_SETTINGS['friendlyName']}.ovpnsetup/{USER_SETTINGS['friendlyName']}.domain.tld.key", "r").read().encode('UTF-8')
    print("Done.\n")

    # Delete the temporary configuration folder. (This process is unnecessary and complicated. It should be later simplified.)
    subprocess.run(f"rm -rf {USER_SETTINGS['friendlyName']}-{}.ovpnsetup".split(' '), check=True)

    # Upload the certificates.
    # Import Server Certificate
    print("Uploading the certificates...")
    global SERVER_CERTIFICATE_ARN
    SERVER_CERTIFICATE_ARN = client_acm.import_certificate(
        Certificate=SERVER_CERT,
        PrivateKey=SERVER_KEY,
        CertificateChain=CA_CERT,
        Tags=[
            {
                "Key": "deploymentFriendlyName",
                "Value": USER_SETTINGS['friendlyName']
            }
        ]
    )['CertificateArn']
    # Import Client Certificate
    global CLIENT_CERTIFICATE_ARN
    CLIENT_CERTIFICATE_ARN = client_acm.import_certificate(
        Certificate=CLIENT_CERT,
        PrivateKey=CLIENT_KEY,
        CertificateChain=CA_CERT,
        Tags=[
            {
                "Key": "deploymentFriendlyName",
                "Value": USER_SETTINGS['friendlyName']
            }
        ]
    )['CertificateArn']
    print("Done.\n")


# This function downloads the cloudformation template if one is not found under the CWD.
def download_cloudformation_template():
    cfTemplate = Path('cloudformation-template')
    global TEMPLATE_CONTENT
    for count in range(3):
        if cfTemplate.exists():
            TEMPLATE_CONTENT = cfTemplate.open('r').read()
            break
        else:
            subprocess.run("wget \'https://raw.githubusercontent.com/Scottpedia/vpn-toggle-utility/setup-script/cloudformation-template\' -O cloudformation-template".split(
                ' '), check=True, stdout=sys.stdout)
    else:
        raise Exception(
            "Failed to find and download the cloudformation template.")


def deploy_cloudformation_template():
    print("Now we start to deploy the actual thing on AWS.")
    print("Deploying...")
    response = client_cf.create_stack(
        StackName='ovpn-{}'.format(USER_SETTINGS['friendlyName']),
        TemplateBody=TEMPLATE_CONTENT,
        Parameters=[
            {
                'ParameterKey': 'ClientCertificateArn',
                'ParameterValue': CLIENT_CERTIFICATE_ARN
            },
            {
                'ParameterKey': 'ServerCertificateArn',
                'ParameterValue': SERVER_CERTIFICATE_ARN
            },
            {
                'ParameterKey': 'isSplitTunnelled',
                'ParameterValue': str(USER_SETTINGS['isSplitTunneled']).lower()
            },
            {
                'ParameterKey': 'FriendlyName',
                'ParameterValue': USER_SETTINGS['friendlyName']
            }
        ],
        TimeoutInMinutes=15,
        Tags=[
            {
                "Key": "deploymentFriendlyName",
                "Value": USER_SETTINGS['friendlyName']
            }
        ]
    )
    global CLOUDFORMATION_STACK_ID
    global CLIENT_VPN_ENDPOINT_ID
    global SUBNET_ID
    CLOUDFORMATION_STACK_ID = response['StackId']
    print("Deployment initiated. The program will refresh every 3 seconds to check the progress of deployment. The timeout is 5 mimutes.")
    for i in range(100):
        time.sleep(3)
        response = client_cf.describe_stacks(
            StackName='ovpn-{}'.format(USER_SETTINGS['friendlyName'])
        )
        if response["Stacks"][0]['StackStatus'] == 'CREATE_COMPLETE':
            print("Stack is successfully created!")
            outputs = response["Stacks"][0]['Outputs']
            outputs.sort(key=lambda x : x['OutputKey'])
            CLIENT_VPN_ENDPOINT_ID = outputs[0]['OutputValue']
            SUBNET_ID = outputs[1]['OutputValue']
            break
        elif response["Stacks"][0]['StackStatus'] == ('CREATE_FAILED' or 'ROLLBACK_IN_PROGRESS'):
            print("The stack deployment failed.")
            raise Exception("The stack deployment failed.")
        elif response["Stacks"][0]['StackStatus'] == 'CREATE_IN_PROGRESS':
            pass
        else:
            raise Exception("Unexpected stack status detected.")
    else:
        raise Exception("Deployment timed out.")


def download_connection_profile():
    print('Exporting the connection profile...')
    connConfig = client_ec2.export_client_vpn_client_configuration(
        ClientVpnEndpointId=CLIENT_VPN_ENDPOINT_ID
    )
    print('Done.\n')

    print('Inserting client-side credentials...')
    print('Processing...')
    conn_fragments = connConfig['ClientConfiguration'].split('\n')

    conn_fragments[3] = 'remote ' + ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits)
                                            for _ in range(20)).lower() + '.' + conn_fragments[3].split(' ')[1] + ' 443'

    conn_fragments.insert(-2, '<key>')
    for _i in CLIENT_KEY.decode('UTF-8').split('\n'):
        conn_fragments.insert(-2, _i)
    conn_fragments.insert(-2, '</key>')

    conn_fragments.insert(-2, '<cert>')
    for _i in CLIENT_CERT.decode('UTF-8').split('\n'):
        conn_fragments.insert(-2, _i)
    conn_fragments.insert(-2, '</cert>')

    ovpnConfig = '\n'.join(conn_fragments)

    ovpnFile = open(
        f"{USER_SETTINGS['region']}-{USER_SETTINGS['friendlyName']}.ovpn", "w+")
    ovpnFile.write(ovpnConfig)
    ovpnFile.close()
    print('Done.\n')
    print('Your .ovpn file is: ' + f"{USER_SETTINGS['region']}-{USER_SETTINGS['friendlyName']}.ovpn")


# In the following function, we save the setup result as a file under the CWD for later use, 
# that is, to identify the existing VPN endpoint that the user wants to manage.
# Here is the list of attributes one profile has:
# - Region
# - Client VPN Endpoint ID
# - Client VPN Subnet ID
# - Date of Creation
# - Friendly Name of the Deployment
# These data should be stored in Json format.
def save_the_setup_results():
    print("Gathering Deployment attributes...")
    saveTime = int(time.time())
    DATA_TO_STORE={
        "AWS_REGION": USER_SETTINGS['region'],
        "ENDPOINT_ID": CLIENT_VPN_ENDPOINT_ID,
        "SUBNET_ID": SUBNET_ID,
        "DATE_OF_CREATION": saveTime,
        "FRIENDLY_NAME": USER_SETTINGS['friendlyName']
    }
    print('Done.\n')
    print(DATA_TO_STORE)
    print(f"Saving the file as \'{USER_SETTINGS['friendlyName']}-{saveTime}.ovpnsetup\' ...")
    _f = open(f"{USER_SETTINGS['friendlyName']}-{saveTime}.ovpnsetup",'w+')
    _f.write(dumps(DATA_TO_STORE))
    _f.close()
    print('Done.\n')
    

    # *** THE DEPLOYMENT CODE SECTION ENDS ***
if __name__ == "__main__":
    if len(sys.argv) > 1:  # To see if the command is present.
        try:
            # get_configuration()
            manage()
        except Exception as e:
            print("Errors occured.", file=sys.stderr)
            traceback.print_exc()
    else:  # manage the vpn when there is no commands or options.
        print("No commands or options detected in the command line. Let's setup a brand-new VPN service!")
        input("Please note that this program will create several temporary & non-temporary files and directories under the current working direcory. \
            Be sure that you have the proper permission to write to the CWD and it is okay for such purposes!\nPlease press any key to proceed. > ")
        # Before we initiate the deployment sequence, we need to know the following parameters:
        # - the AWS region where the endpoint will be created. (no Default, mandatory)
        # - the friendly name of this vpn service. (Default: timestampt/UUID)
        # - if the vpn service should be split-tunnelled. (Default: non-split-tunnel)
        # The user will be prompted to speficy these parameters. The job is done within the following function:
        get_user_settings()
        try:
            client_ec2 = boto3.client(
                "ec2", region_name=USER_SETTINGS['region'])
            client_acm = boto3.client(
                "acm", region_name=USER_SETTINGS['region'])
            client_cf = boto3.client(
                "cloudformation", region_name=USER_SETTINGS['region'])
            generate_credentials()
            download_cloudformation_template(),
            # save the aws-generated private keys at the same time.
            deploy_cloudformation_template()
            download_connection_profile()
            # # Insert the generated credential into the .ovpn file.
            save_the_setup_results()
        except Exception as e:
            print(
                "Errors occured during the deployment process.\n Program Exits.", file=sys.stderr)
            traceback.print_exc()
