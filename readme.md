Please find below a portfolio with some of my projects/scripts.
This includes:
- Ansible Project (Linux Server): project with the scope of installing multiple roles, creating Linux group/users based on user input, modifying Apache homepage and activating ProxyPass towards Tomcat. Finally, all the services are checked and a Jenkins job is created via Ansible, along with installing the required dependencies. Made to work dynamically depending on Distro family (Redhat or Debian).
- Ansible Project (Router Cisco): project for getting familiarized with regular Cisco Router actions such as: configuration, facts gathering, backups, show commands. This was done in a hybrid environment which includes local physical routers and virtual routers in EVE-NG.
- College Final Project: Python GUI Packet Sniffer and flood DDoS preventer using OOP, Scapy, Graphs, FTP to a remote Windows Server machine (with Active Directory integration and policies), using Firewall rules to block risky traffic. More can be found in the pptx/UML included.
- Django Project: web project that gets input from Raspberry Pi sensors (temperature, humidity, fire presence, light intensity, parking distance) and renders different icons to the webpage, depending on the interval of said values. Also includes an about page and an account creation form.
- Docker Project: project which creates 3 Docker files and docker images based on mySQL, php and phpmyadmin. It then creates 4 containers using environment variables and exposing the needed ports. PHP index page is replaced with a file mapped to the containers using the volume feature. This has been done both with and without Docker Compose.
- Selenium Project: Script for navigating and logging in to a courses website and downloading/renaming all chapters and subchapters by iterating through the webpage DOM. More can be found in the script comments.
- Small Scripts: small Python scripts that I used for automation for personal need or for work.
- Terraform Project: AWS infrastracture set up and tear down which does the following:
    * Creates an S3 bucket and uses it as a backend to store the Terraform state
	* Creates a VPC, Subnets, Internet Gateway, Routing Tables and associates them
	* Creates a Security Group based on IP ranges from a data source
	* Creates private and public SSH key for authentication purposes
	* Creates an EC2 VM instance which is part of previously created VPC and SG
	* Creates an EBS volume for the VM and attaches it
	* Does initial configuration of the VM using 2 scripts, one for installing packages and the other for creating a logical volume and mounting it