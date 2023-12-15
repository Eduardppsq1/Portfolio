Please find below a portfolio with some of my projects/scripts.
This includes:
- Ansible Project (Linux Server): installing multiple roles, creating Linux group/users based on user input, modifying Apache homepage and activating ProxyPass towards Tomcat. The services are checked and a Jenkins job is created via Ansible, along with installing the required dependencies. Made to work dynamically depending on Distro family (Redhat or Debian).
- Ansible Project (Router Cisco): Cisco ios/nxos configuration, facts gathering, backups, show commands. This was done in a hybrid environment which includes local physical routers and virtual routers in EVE-NG.
- College Final Project: Python GUI Packet Sniffer and flood DDoS preventer. The GUI includes parameters such as interface, packet type, number of packets, download path, IP/Username/Password of the FTP server.
	* Scapy for Packet sniffing and packet forging for tests
	* OOP and Functional Python programming notions to manipulate Scapy data
	* Graphs for evaluating the types of packets based on protocol or danger level
	* Local download of the packets data
	* FTP to a remote Windows Server machine with Active Directory integration and policies
	* Automated Firewall rules to block risky traffic
	* The project can be run manually or automatically and also has testing included in the GUI
	* More can be found in the pptx/UML diagram included
- Django Project: web project that gets input from Raspberry Pi sensors (temperature, humidity, fire presence, light intensity, parking distance) and renders them to the webpage along with different icons, depending on the interval of said values. Also includes an about page and an account creation form.
- Docker Project: creation of 3 Docker files and docker images based on mySQL, php and phpmyadmin; creation of 4 containers using environment variables and exposing the needed ports. PHP index page is replaced with a file mapped to the containers using the volume feature. This has been done both with and without Docker Compose.
- Kubernetes Project: Minikube cluster containing 2 deployments: a Python application that connects to a MySQL database and renders the success/failure to a website via Flask. This includes the following:
	* A Namespace which all the following resources will be a part of
	* A Dockerfile and the Python web app Deployment with 3 replicas
	* A ConfigMap for the web deployment to use as environment variables for connecting to the database
	* A Nodeport service for exposing the deployment externally
	* A MySQL Deployment with a test database already created
	* Secrets and a Persistent Volume/Persistent Volume Claim that the previous deployment will use
	* A ClusterIP service for exposing the deployment interally
	* There was a rolling update done on the web Deployment and extra labels added from dashboard
	* An Ingress service for routing HTTP traffic towards the web service
- Selenium Script: navigating and logging in to a courses website and downloading/renaming all chapters and subchapters by iterating through the webpage DOM. More can be found in the script comments.
- Small Scripts: small Python scripts that I used for automation for personal need or for work.
- Terraform Project: AWS infrastracture set up and tear down which does the following:
    * Creates an S3 bucket and uses it as a backend to store the Terraform state
	* Creates a VPC, Subnets, Internet Gateway, Routing Tables and associates them
	* Creates a Security Group based on IP ranges from a data source
	* Creates private and public SSH key for authentication purposes
	* Creates an EC2 VM instance which is part of previously created VPC and SG
	* Creates an EBS volume for the VM and attaches it
	* Does initial configuration of the VM using 2 scripts, one for installing packages and the other for creating a logical volume and mounting it