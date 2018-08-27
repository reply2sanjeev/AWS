#--------------------------------------------------#
To Create a VPC:
#--------------------------------------------------#
# aws ec2 create-vpc --cidr-block 10.0.0.0/16

#--------------------------------------------------#
To Create Internet Gateway:
#--------------------------------------------------#
# aws ec2 create-internet-gateway

#--------------------------------------------------#
Attach Internet Gateway with VPC:
#--------------------------------------------------#

# aws ec2 attach-internet-gateway --vpc-id "vpc-036813beb28be0710" --internet-gateway-id "igw-084a3b4b5a4113dd4" --region us-east-1

#--------------------------------------------------#
To Create Subnet :
#--------------------------------------------------#
# aws ec2 create-subnet --vpc-id vpc-036813beb28be0710 --cidr-block 10.0.1.0/24

# aws ec2 create-subnet --vpc-id vpc-036813beb28be0710 --cidr-block 10.0.2.0/24 --availability-zone "us-east-1b"


# aws ec2 create-subnet --vpc-id vpc-036813beb28be0710 --cidr-block 10.0.3.0/24 --availability-zone "us-east-1a"

# aws ec2 create-subnet --vpc-id vpc-036813beb28be0710 --cidr-block 10.0.4.0/24 --availability-zone "us-east-1b"

#--------------------------------------------------#
Create a custom route table for your VPC.
#--------------------------------------------------#

# RouteTable-1 [Public]

# aws ec2 create-route-table --vpc-id vpc-036813beb28be0710


#--------------------------------------------------#
# RouteTable-2 [Private]
#--------------------------------------------------#

# aws ec2 create-route-table --vpc-id vpc-036813beb28be0710

#--------------------------------------------------#
Create a route in the route table that points all traffic (0.0.0.0/0) to the Internet gateway.
#--------------------------------------------------#

# aws ec2 create-route --route-table-id "rtb-07715d57c56bd94f2" --destination-cidr-block 0.0.0.0/0 --gateway-id "igw-084a3b4b5a4113dd4"

#--------------------------------------------------#
To check list of subnets part of a specific VPC :
#--------------------------------------------------#

# aws ec2 describe-subnets --filters "Name=vpc-id,Values=vpc-036813beb28be0710" --query 'Subnets[*].{ID:SubnetId,CIDR:CidrBlock}'
#----------------------------------------------------------#
Subnet Association with RouteTable i.e. Public RouteTable:
#----------------------------------------------------------#

# aws ec2 associate-route-table  --subnet-id "subnet-0ade9f8d7d4c6f62e" --route-table-id rtb-07715d57c56bd94f2

#----------------------------------------------------------#
Subnet Association with RouteTable i.e. Private RouteTable:
#----------------------------------------------------------#

# aws ec2 associate-route-table  --subnet-id "subnet-04346daa909540389" --route-table-id rtb-098e36ef350476777

#----------------------------------------------------------#
Auto AssignIPV4 Public IP on Subnets :
#----------------------------------------------------------#

# aws ec2 modify-subnet-attribute --subnet-id "subnet-0ade9f8d7d4c6f62e" --map-public-ip-on-launch

# aws ec2 modify-subnet-attribute --subnet-id "subnet-035c5ce122305657d" --map-public-ip-on-launch

#----------------------------------------------------------#
Launch an Instance into Your Subnet
#----------------------------------------------------------#
To launch and connect to an instance in your public subnet

Create a key pair and use the --query option and the --output text option to pipe your private key directly into a file with the .pem extension.

# aws ec2 create-key-pair --key-name nn_01 --query 'KeyMaterial' --output text > nn_01.pem


#----------------------------------------------------------#
Create Security Group on Public Subnet :
#----------------------------------------------------------#
Create a security group in your VPC, and add a rule that allows SSH access from anywhere.

# aws ec2 create-security-group --group-name SSHAccess --description "Security group for SSH access" --vpc-id "vpc-036813beb28be0710"

# aws ec2 authorize-security-group-ingress --group-id sg-082ae04b7cfae10ff --protocol tcp --port 22 --cidr 0.0.0.0/0


#----------------------------------------------------------#
Creates a network ACL for the specified VPC
#----------------------------------------------------------#
# aws ec2 describe-network-acls

# aws ec2 create-network-acl --vpc-id "vpc-036813beb28be0710"

#----------------------------------------------------------#
To create a network ACL entry
#----------------------------------------------------------#
The rule allows ingress traffic from any IPv4 address (0.0.0.0/0) on UDP port 53 (DNS) into any associated subnet.

# aws ec2 create-network-acl-entry --network-acl-id "acl-069cd03e31aa3d070" --ingress --rule-number 100 --protocol udp --port-range From=53,To=53 --cidr-block 0.0.0.0/0 --rule-action allow

This example creates a rule for the specified network ACL that allows ingress traffic from any IPv6 address (::/0) on TCP port 80 (HTTP).

# aws ec2 create-network-acl-entry --network-acl-id "acl-069cd03e31aa3d070" --ingress --rule-number 120 --protocol tcp --port-range From=80,To=80 --ipv6-cidr-block ::/0 --rule-action allow

#----------------------------------------------------------#


#----------------------------------------------------------#
Launch an instance into your public subnet, using the security group and key pair you've created.
#----------------------------------------------------------#
# aws ec2 run-instances --image-id ami-6871a115 --count 1 --instance-type t2.micro --key-name nn_01 --security-group-ids sg-082ae04b7cfae10ff --subnet-id "subnet-0ade9f8d7d4c6f62e"



#----------------------------------------------------------#
Do SSH to EC2 instance from Base machine:
#----------------------------------------------------------#

$ ssh -i "nn_01.pem" ec2-user@X.X.X.X
The authenticity of host 'X.x.x.x (X.x.x.x)' can't be established.
ECDSA key fingerprint is SHA256:f000xe1HwDZ9v/Gd4kt7h/CBuRkXLtGtZFhtXtqmM8A.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'X.x.x.x' (ECDSA) to the list of known hosts.
-bash: warning: setlocale: LC_CTYPE: cannot change locale (UTF-8): No such file or directory
[ec2-user@ip-10-0-1-143 ~]$

#----------------- Check the Instance Details--------------#
# aws ec2 describe-instances --instance-id "i-0980c7d910410ef37"
#----------------------------------------------------------#

#----------------------------------------------------------#
Clean Up :
#----------------------------------------------------------#
Delete your security group:

# aws ec2 delete-security-group --group-id sg-082ae04b7cfae10ff

Delete your subnets:

# aws ec2 delete-subnet --subnet-id "subnet-0ade9f8d7d4c6f62e"
# aws ec2 delete-subnet --subnet-id "subnet-0cb2a499bfd075c70"
# aws ec2 delete-subnet --subnet-id "subnet-04346daa909540389"
# aws ec2 delete-subnet --subnet-id "subnet-035c5ce122305657d"

Delete your custom route table:

# aws ec2 delete-route-table --route-table-id "rtb-07715d57c56bd94f2"
# aws ec2 delete-route-table --route-table-id "rtb-098e36ef350476777"

Detach your Internet gateway from your VPC:

# aws ec2 detach-internet-gateway --internet-gateway-id "igw-084a3b4b5a4113dd4" --vpc-id "vpc-036813beb28be0710"

Delete your Internet gateway:

# aws ec2 delete-internet-gateway --internet-gateway-id "igw-084a3b4b5a4113dd4"

Delete your VPC:

# aws ec2 delete-vpc --vpc-id "vpc-036813beb28be0710"
#----------------------------------------------------------#