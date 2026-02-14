# 📓 NetAIMCP Manual

![Latest Release](https://img.shields.io/badge/version-1.0.0-blue.svg)

## 📖 **Table of Contents**
- 📜 **Lab Manual for NetAIMCP**
  - [🔭 Overview](#-overview)
  - [📦 GitHub Repository](#-github-repository)
  - [♻️ Document Lifecycle](#%EF%B8%8F-document-lifecycle)
  - [⚒️ Tech Stack](#%EF%B8%8F-tech-stack)
  - [📋 Included Vendors](#-included-vendors)
  - [🎓 Networking Topics](#-networking-topics)
  - [🛠️ Environment Setup](#%EF%B8%8F-environment-setup)
  - [📂 Router OS Images](#-router-os-images)
  - [🖥️ Terminal Management](#%EF%B8%8F-terminal-management)
  - [🔄 Network Topology](#-network-topology)
  - [💻 MCP Server Code](#-mcp-server-code)
  - [🔥 Automation and Troubleshooting](#-automation-and-troubleshooting)
  - [⬆️ Planned Upgrades](#%EF%B8%8F-planned-upgrades)
  - [⚠️ Disclaimer](#%EF%B8%8F-disclaimer)
  - [📜 License](#-license)

## 🔭 Overview
The purpose of this project is to showcase the capabilities of **Claude** and **MCP**, combined with **Python** and **Scrapli**, in regards to network automation and troubleshooting.

By design, the project is **multi-vendor**, **multi-protocol**, **multi-area/multi-AS**, **OSI L3-focused**, in order to automate and troubleshoot various scenarios in a diverse and complex network.

What you'll find in this manual:
- [x] How to **setup this lab** from scratch
- [x] The current **topology diagram** PNG
- [x] The **startup config** of each router
- [x] The **Containerlab YAML** lab file
- [x] The **NETWORK.json** inventory file
- [x] The latest **MCPServer.py** code

⚠️ **NOTE**: This project assumes at least **CCNA**-level knowledge (**CCNP** preferred), as well as familiarity with **Linux** terminal commands, **Python** syntax, and multi-vendor **CLIs**.

## 📦 GitHub Repository
The GitHub repo for this Lab Manual:
- [x] [**NetAIMCP GitHub Repository**](https://github.com/pdudotdev/netaimcp)

## ♻️ Document Lifecycle
This document is **NOT** static. I will periodically add **new features** (devices, vendors, protocols, configs) to the network topology below.

**Each update is announced via**:
- [x] Udemy email announcement
- [x] The PNA Discord server

**New version updates are marked as**:
- [x] **UPDATE#vX.Y**
- [x] Should match the release no. of the **NetAIMCP** GitHub repo.

**Current version**:
- [x] The current version of this document is **v1.0**

## ⚒️ Tech Stack
The main tools and technologies used for building the project:
- [x] Claude AI (Claude Code)
- [x] MCP Server (FastMCP)
- [x] ContainerLab
- [x] Docker
- [x] Python
- [x] Scrapli
- [x] Ubuntu
- [x] VS Code
- [x] VirtualBox/VMware

## 📋 Included Vendors
- [x] **Arista**: EOS (cEOS)
- [x] **Cisco**: IOS/IOS-XE (IOL)

## 🎓 Networking Topics
Networking topics in this topology:
- [x] **OSPF multi-area**:
  - Basic protocol config
    - Reference bandwidth
    - Point-to-point links
    - Passive interfaces
    - MD5 authentication
    - External type 1 routes
  - Route redistribution
  - Route summarization (ABR)
  - Route filtering with prefix lists
  - Route filtering with distribute lists
  - Area types: normal, totally stubby, totally nssa

- [x] **EIGRP**:
  - Basic protocol config
    - Passive interfaces
    - MD5 authentication
    - Stub connected/summary
  - Local summarization
  - Route redistribution
  - Default metric via route map

- [x] **Others**:
  - Policy-Based Routing
  - IP SLA icmp-echo

## 🛠️ Environment Setup
The environment setup mimics the steps we've discussed in Sections 1-2 (and partially, Section 3) of the course.
However, I'm including a checklist for you to verify before moving to the network topology section.

⚠️ **NOTE**: You should create a separate project directory, different than the one you used for the course. You can even choose to quickly deploy a new Ubuntu VM from scratch for this lab, in order to keep everything clean.

⚠️ **NOTE**: You will need to bump up your VM resources a bit since this lab is more complex, and also to accomodate any future expansions.

**My VM resources for this lab**:
- [x] VirtualBox or VMware
- [x] 12 processor cores
- [x] 32 GB RAM memory
- [x] 50 GB hard disk

**Summary checklist**:
- [x] Initial config:
```
sudo apt update && sudo apt upgrade -y
sudo apt install vim curl python3.12-venv python3-pip
```
- [x] Install VS Code.
- [x] Directory setup:
```
mkdir mcp-project
cd mcp-project
python3 -m venv mcp
source mcp/bin/activate
pip install --upgrade pip
pip install fastmcp scrapli asyncssh python-dotenv
```
- [x] Docker engine:
```
sudo apt update
sudo apt install ca-certificates
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl status docker
sudo docker run hello-world
```
- [x] Containerlab:
```
curl -sL https://containerlab.dev/setup | sudo -E bash -s "all"
newgrp docker
clab --help
clab version
```
- [x] Containerlab commands:
```
containerlab deploy -t lab.yml
containerlab save -t lab.yml
containerlab inspect -t lab.yml
containerlab redeploy -t lab.yml
docker exec -it <container-name/id> Cli     (-i interactive, -t pseudo-tty/terminal)

containerlab graph -t lab.yml
containerlab destroy -t lab.yml
```
- [x] The .env file:
```
ROUTER_USERNAME=admin
ROUTER_PASSWORD=admin
```
```
ROUTER_USERNAME=claude_mcp
SSH_KEY_PATH=/home/mcp/.ssh/id_rsa
```
- [x] Claude Code:
```
curl -fsSL https://claude.ai/install.sh | bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
claude doctor
```
- [x] Claude auth:
```
claude auth login
```
- [x] Claude <-> MCP server:
```
claude mcp add mcp_automation -s user -- ./mcp/bin/python MCPServer.py
claude mcp list
```

⚠️ **NOTE**: See all the detailed installation steps in the course.

## 📂 Router OS Images
### Arista EOS
To download the **Arista cEOS** file, see the **Full Guide** in Section 2 of the course.
- [x] Then, you need to import it into Docker using:
```
sudo docker import ~/cEOS64-lab-4.35.0F.tar.xz ceos:4.35.0F
docker images
```
- [x] Containerlab's docs for Arista cEOS: [here](https://containerlab.dev/manual/kinds/ceos/)

### Cisco IOS
You are responsible of getting your own Cisco IOL file, however here's a starting point:
- [x] Containerlab's [**documentation for IOL**](https://containerlab.dev/manual/kinds/cisco_iol/)

**Quick note**:
- [x] You'll notice something new in the **lab.yml** below:
`CLAB_MGMT_PASSTHROUGH: "true"`
- [x] This setting enables **TRANSPARENT MANAGEMENT**, details [here](https://containerlab.dev/manual/vrnetlab/#management-interface)

## 🖥️ Terminal Management
Since we're dealing with a complex topology containing many devices, we need to make our lives easier when it comes to the SSH connections.
For this reason, I'm using **Tabby**:
- [x] Download link [**here**](https://tabby.sh/)
- [x] The installer is **tabby-1.0.230-linux-x64.deb** (version no. might differ)
- [x] Installation: `sudo dpkg -i tabby-1.0.230-linux-x64.deb`
- [x] Start it with `tabby` and pin it to the Dash
- [x] Go to **Settings - Profiles & connections - New - New Profile Group**
- [x] Go to **New - New profile - SSH connection**, name it **R1A**, assign it to your Group
- [x] Scroll down to **Connection**, Host 172.20.20.201 (see **lab.yml** below ), Port 22
- [x] Set **Username** to **admin**. Set a **Password** in the keychain, also **admin**.
- [x] Hit **Save**. Do this for each router after you create your topology.
- [x] Connect to each device using the ▶︎ button. You may be prompted for the password again.
- [x] To quickly create the same connection type for each router, **Duplicate** R1A, then just change the name and IP address.

⚠️ **NOTE**: You don't have to use **Tabby** if you already like using a similar tool. They're all basically doing the same thing, just the UI slightly differs.

## 🔄 Network Topology
- [x] Current network topology
  - *Subject to periodic upgrades*

![topology](TOPOLOGY.png)

- [x] Containerlab **lab.yml** file:
```
name: mcp-lab

topology:
  defaults:
    env:
      CLAB_MGMT_PASSTHROUGH: "true"
  nodes:
    R1A:
      kind: arista_ceos
      image: ceos:4.35.0F
      mgmt-ipv4: 172.20.20.201
    R2A:
      kind: arista_ceos
      image: ceos:4.35.0F
      mgmt-ipv4: 172.20.20.202
    R3C:
      kind: cisco_iol
      image: vrnetlab/cisco_iol:17.16.01a
      mgmt-ipv4: 172.20.20.203
    R4C:
      kind: cisco_iol
      image: vrnetlab/cisco_iol:17.16.01a
      mgmt-ipv4: 172.20.20.204
    R5C:
      kind: cisco_iol
      image: vrnetlab/cisco_iol:17.16.01a
      mgmt-ipv4: 172.20.20.205
    R6A:
      kind: arista_ceos
      image: ceos:4.35.0F
      mgmt-ipv4: 172.20.20.206
    R7A:
      kind: arista_ceos
      image: ceos:4.35.0F
      mgmt-ipv4: 172.20.20.207
    R8C:
      kind: cisco_iol
      image: vrnetlab/cisco_iol:17.16.01a
      mgmt-ipv4: 172.20.20.208
    R9C:
      kind: cisco_iol
      image: vrnetlab/cisco_iol:17.16.01a
      mgmt-ipv4: 172.20.20.209
    R10C:
      kind: cisco_iol
      image: vrnetlab/cisco_iol:17.16.01a
      mgmt-ipv4: 172.20.20.210
    R11C:
      kind: cisco_iol
      image: vrnetlab/cisco_iol:17.16.01a
      mgmt-ipv4: 172.20.20.211
  links:
    - endpoints: ["R1A:eth1", "R10C:Ethernet0/1"]
    - endpoints: ["R1A:eth2", "R11C:Ethernet0/1"]
    - endpoints: ["R10C:Ethernet0/2", "R11C:Ethernet0/2"]
    - endpoints: ["R1A:eth3", "R3C:Ethernet0/3"]
    - endpoints: ["R1A:eth4", "R2A:eth3"]
    - endpoints: ["R3C:Ethernet0/2", "R4C:Ethernet0/1"]
    - endpoints: ["R3C:Ethernet0/1", "R5C:Ethernet0/1"]
    - endpoints: ["R4C:Ethernet0/2", "R5C:Ethernet0/2"]
    - endpoints: ["R2A:eth4", "R3C:Ethernet1/0"]
    - endpoints: ["R2A:eth2", "R7A:eth1"]
    - endpoints: ["R2A:eth1", "R6A:eth1"]
    - endpoints: ["R7A:eth2", "R8C:Ethernet0/2"]
    - endpoints: ["R6A:eth2", "R8C:Ethernet0/1"]
    - endpoints: ["R8C:Ethernet0/3", "R9C:Ethernet0/1"]
```

- [x] **NETWORK.json** inventory file:
```
{
"R1A": {"host": "172.20.20.201", "platform": "arista_eos", "transport": "asyncssh", "cli_style": "eos"},
"R2A": {"host": "172.20.20.202", "platform": "arista_eos", "transport": "asyncssh", "cli_style": "eos"},
"R3C": {"host": "172.20.20.203", "platform": "cisco_iosxe", "transport": "asyncssh", "cli_style": "ios"},
"R4C": {"host": "172.20.20.204", "platform": "cisco_iosxe", "transport": "asyncssh", "cli_style": "ios"},
"R5C": {"host": "172.20.20.205", "platform": "cisco_iosxe", "transport": "asyncssh", "cli_style": "ios"},
"R6A": {"host": "172.20.20.206", "platform": "arista_eos", "transport": "asyncssh", "cli_style": "eos"},
"R7A": {"host": "172.20.20.207", "platform": "arista_eos", "transport": "asyncssh", "cli_style": "eos"},
"R8C": {"host": "172.20.20.208", "platform": "cisco_iosxe", "transport": "asyncssh", "cli_style": "ios"},
"R9C": {"host": "172.20.20.209", "platform": "cisco_iosxe", "transport": "asyncssh", "cli_style": "ios"},
"R10C": {"host": "172.20.20.210", "platform": "cisco_iosxe", "transport": "asyncssh", "cli_style": "ios"},
"R11C": {"host": "172.20.20.211", "platform": "cisco_iosxe", "transport": "asyncssh", "cli_style": "ios"}
}
```
⚠️ **NOTE**: Adding `"cli_style": "eos"` or `"cli_style": "ios"` to the **NETWORK.json** inventory file provides additional context to Claude when executing commands on one type of device or another.

- [x] Router naming convention:
  - **RXY** where:
    - **R**: device type (router)
    - **X**: device number id
    - **Y**: vendor (A-Arista, C-Cisco, etc.)

- [x] Interface naming convention:
  - Interface **0/1** in the diagram:
    - Corresponds to **Eth1** on Arista
    - Corresponds to **Eth0/1** on Cisco

- [x] Default SSH credentials:
  - Arista: `admin:admin`
  - Cisco: `admin:admin`

- [x] **.env** credentials file:
```
ROUTER_USERNAME=admin
ROUTER_PASSWORD=admin
```

- [x] Router configurations:
  - Each config below refers to only the most important commands, not the entire startup-config files

💾 **Router R1A**:
```
interface Ethernet1
   description TO-R10C
   no switchport
   ip address 172.16.0.5/30
   ip ospf network point-to-point
   ip ospf authentication message-digest
   ip ospf message-digest-key 1 md5 7 cPJDR7WarHSE8UOIp1vPEw==
!
interface Ethernet2
   description TO-R11C
   no switchport
   ip address 172.16.0.9/30
   ip ospf network point-to-point
   ip ospf authentication message-digest
   ip ospf message-digest-key 1 md5 7 n9WRlnPw52vTZSOwrukUTQ==
!
interface Ethernet3
   description TO-R3C
   no switchport
   ip address 10.0.0.5/30
   ip ospf network point-to-point
   ip ospf authentication message-digest
   ip ospf message-digest-key 1 md5 7 n9WRlnPw52vz969Bs+VvOg==
!
interface Ethernet4
   description TO-R2A
   no switchport
   ip address 10.0.0.1/30
   ip ospf network point-to-point
   ip ospf authentication message-digest
   ip ospf message-digest-key 1 md5 7 ZQHQDAcRIt5F5/tAXUShpQ==
!
ip routing
!
router ospf 1
   router-id 1.1.1.1
   auto-cost reference-bandwidth 100000
   area 0.0.0.2 stub no-summary
   area 0.0.0.2 range 172.16.0.0/24
   network 10.0.0.0/30 area 0.0.0.0
   network 10.0.0.4/30 area 0.0.0.0
   network 172.16.0.4/30 area 0.0.0.2
   network 172.16.0.8/30 area 0.0.0.2
   max-lsa 12000
!
```
💾 **Router R2A**:
```
interface Ethernet1
   description TO-R6A
   no switchport
   ip address 10.1.1.14/30
   ip ospf network point-to-point
   ip ospf authentication message-digest
   ip ospf message-digest-key 1 md5 7 cPJDR7WarHTWLNmizABMlQ==
!
interface Ethernet2
   description TO-R7A
   no switchport
   ip address 10.1.1.10/30
   ip ospf network point-to-point
   ip ospf authentication message-digest
   ip ospf message-digest-key 1 md5 7 n9WRlnPw52vFGviUBTwgxw==
!
interface Ethernet3
   description TO-R1A
   no switchport
   ip address 10.0.0.2/30
   ip ospf network point-to-point
   ip ospf authentication message-digest
   ip ospf message-digest-key 1 md5 7 n9WRlnPw52vz969Bs+VvOg==
!
interface Ethernet4
   description TO-R3C
   no switchport
   ip address 10.0.0.9/30
   ip ospf network point-to-point
   ip ospf authentication message-digest
   ip ospf message-digest-key 1 md5 7 ZQHQDAcRIt5F5/tAXUShpQ==
!
interface Loopback1
   ip address 2.2.2.66/32
!
ip routing
!
ip prefix-list FILTER_3333LO_LOCAL seq 10 deny 3.3.3.3/32
ip prefix-list FILTER_3333LO_LOCAL seq 20 permit 0.0.0.0/0 le 32
ip prefix-list NO-2222LO seq 10 deny 2.2.2.66/32
ip prefix-list NO-2222LO seq 20 permit 0.0.0.0/0 le 32
!
router ospf 1
   router-id 2.2.2.2
   auto-cost reference-bandwidth 100000
   passive-interface Loopback1
   distribute-list prefix-list FILTER_3333LO_LOCAL in
   area 0.0.0.0 filter prefix-list NO-2222LO
   area 0.0.0.1 nssa no-summary
   area 0.0.0.1 nssa default-information-originate
   network 2.2.2.66/32 area 0.0.0.1
   network 10.0.0.0/30 area 0.0.0.0
   network 10.0.0.8/30 area 0.0.0.0
   network 10.1.1.8/30 area 0.0.0.1
   network 10.1.1.12/30 area 0.0.0.1
   max-lsa 12000
!
```

💾 **Router R3C**:
```
key chain MCP
 key 1
  key-string MCPLAB10
!
interface Loopback1
 ip address 3.3.3.3 255.255.255.0
!
interface Ethernet0/0
 description clab-mgmt
 vrf forwarding clab-mgmt
 ip address 172.20.20.203 255.255.255.0
 ipv6 address 3FFF:172:20:20::3/64
!
interface Ethernet0/1
 description TO-R5C
 ip address 192.168.10.5 255.255.255.252
 ip authentication mode eigrp 10 md5
 ip authentication key-chain eigrp 10 MCP
!
interface Ethernet0/2
 description TO-R4C
 ip address 192.168.10.1 255.255.255.252
 ip authentication mode eigrp 10 md5
 ip authentication key-chain eigrp 10 MCP
!
interface Ethernet0/3
 description TO-R1A
 ip address 10.0.0.6 255.255.255.252
 ip ospf authentication message-digest
 ip ospf message-digest-key 1 md5 AREA0
 ip ospf network point-to-point
!
interface Ethernet1/0
 description TO-R2A
 ip address 10.0.0.10 255.255.255.252
 ip ospf authentication message-digest
 ip ospf message-digest-key 1 md5 AREA0
 ip ospf network point-to-point
!
interface Ethernet1/1
 no ip address
 shutdown
!
interface Ethernet1/2
 no ip address
 shutdown
!
interface Ethernet1/3
 no ip address
 shutdown
!
!
router eigrp 10
 network 192.168.10.0 0.0.0.3
 network 192.168.10.4 0.0.0.3
 redistribute ospf 1 route-map OSPF-TO-EIGRP
!
router ospf 1
 router-id 3.3.3.3
 auto-cost reference-bandwidth 100000
 redistribute eigrp 10 metric-type 1
 passive-interface Loopback1
 network 3.3.3.0 0.0.0.255 area 0
 network 10.0.0.4 0.0.0.3 area 0
 network 10.0.0.8 0.0.0.3 area 0
!
route-map OSPF-TO-EIGRP permit 10 
 set metric 1000000 1 255 1 1500
!
```

💾 **Router R4C**:
```
key chain MCP
 key 1
  key-string MCPLAB10
!
interface Loopback1
 ip address 4.4.1.1 255.255.255.0
!
interface Loopback2
 ip address 4.4.2.1 255.255.255.0
!
interface Ethernet0/0
 description clab-mgmt
 vrf forwarding clab-mgmt
 ip address 172.20.20.204 255.255.255.0
 ipv6 address 3FFF:172:20:20::2/64
!
interface Ethernet0/1
 description TO-R3C
 ip address 192.168.10.2 255.255.255.252
 ip authentication mode eigrp 10 md5
 ip authentication key-chain eigrp 10 MCP
 ip summary-address eigrp 10 4.4.0.0 255.255.252.0
!
interface Ethernet0/2
 description TO-R5C
 ip address 192.168.10.9 255.255.255.252
 ip authentication mode eigrp 10 md5
 ip authentication key-chain eigrp 10 MCP
 ip summary-address eigrp 10 4.4.0.0 255.255.252.0
!
interface Ethernet0/3
 no ip address
 shutdown
!
!
router eigrp 10
 network 4.4.1.0 0.0.0.255
 network 4.4.2.0 0.0.0.255
 network 192.168.10.0 0.0.0.3
 network 192.168.10.8 0.0.0.3
 passive-interface Loopback1
 passive-interface Loopback2
!
```

💾 **Router R5C**:
```
key chain MCP
 key 1
  key-string MCPLAB10
!
interface Loopback1
 ip address 5.5.1.1 255.255.255.0
!
interface Loopback2
 ip address 5.5.2.1 255.255.255.0
!
interface Ethernet0/0
 description clab-mgmt
 vrf forwarding clab-mgmt
 ip address 172.20.20.205 255.255.255.0
 ipv6 address 3FFF:172:20:20::2/64
!
interface Ethernet0/1
 description TO-R3C
 ip address 192.168.10.6 255.255.255.252
 ip authentication mode eigrp 10 md5
 ip authentication key-chain eigrp 10 MCP
 ip summary-address eigrp 10 5.5.0.0 255.255.252.0
!
interface Ethernet0/2
 description TO-R4C
 ip address 192.168.10.10 255.255.255.252
 ip authentication mode eigrp 10 md5
 ip authentication key-chain eigrp 10 MCP
 ip summary-address eigrp 10 5.5.0.0 255.255.252.0
 !
interface Ethernet0/3
 no ip address
 shutdown
!
!
router eigrp 10
 network 5.5.1.0 0.0.0.255
 network 5.5.2.0 0.0.0.255
 network 192.168.10.4 0.0.0.3
 network 192.168.10.8 0.0.0.3
 passive-interface Loopback1
 passive-interface Loopback2
!
ip sla responder
ip sla 1
 icmp-echo 10.10.10.10 source-ip 5.5.1.1
ip sla schedule 1 life forever start-time now
```

💾 **Router R6A**:
```
interface Ethernet1
   description TO-R2A
   no switchport
   ip address 10.1.1.13/30
   ip ospf network point-to-point
   ip ospf authentication message-digest
   ip ospf message-digest-key 1 md5 7 cPJDR7WarHTWLNmizABMlQ==
!
interface Ethernet2
   description TO-R8C
   no switchport
   ip address 10.1.1.2/30
   ip ospf network point-to-point
   ip ospf authentication message-digest
   ip ospf message-digest-key 1 md5 7 n9WRlnPw52vFGviUBTwgxw==
!
interface Loopback1
   ip address 6.6.6.6/32
!
ip routing
!
router ospf 1
   router-id 6.6.6.6
   auto-cost reference-bandwidth 100000
   passive-interface Loopback1
   area 0.0.0.1 nssa
   network 6.6.6.6/32 area 0.0.0.1
   network 10.1.1.0/30 area 0.0.0.1
   network 10.1.1.12/30 area 0.0.0.1
   max-lsa 12000
!
```

💾 **Router R7A**:
```
interface Ethernet1
   description TO-R2A
   no switchport
   ip address 10.1.1.9/30
   ip ospf network point-to-point
   ip ospf authentication message-digest
   ip ospf message-digest-key 1 md5 7 cPJDR7WarHTWLNmizABMlQ==
!
interface Ethernet2
   description TO-R8C
   no switchport
   ip address 10.1.1.6/30
   ip ospf network point-to-point
   ip ospf authentication message-digest
   ip ospf message-digest-key 1 md5 7 n9WRlnPw52vFGviUBTwgxw==
!
interface Loopback1
   ip address 7.7.7.7/32
!
ip routing
!
router ospf 1
   router-id 7.7.7.7
   auto-cost reference-bandwidth 100000
   passive-interface Loopback1
   area 0.0.0.1 nssa
   network 7.7.7.7/32 area 0.0.0.1
   network 10.1.1.4/30 area 0.0.0.1
   network 10.1.1.8/30 area 0.0.0.1
   max-lsa 12000
!
```

💾 **Router R8C**:
```
key chain MCP
 key 1
  key-string MCPLAB20
!
interface Loopback1
 ip address 8.8.8.8 255.255.255.255
!
interface Ethernet0/0
 description clab-mgmt
 vrf forwarding clab-mgmt
 ip address 172.20.20.208 255.255.255.0
 ipv6 address 3FFF:172:20:20::A/64
!
interface Ethernet0/1
 description TO-R6A
 ip address 10.1.1.1 255.255.255.252
 ip ospf authentication message-digest
 ip ospf message-digest-key 1 md5 AREA1
 ip ospf network point-to-point
!
interface Ethernet0/2
 description TO-R7A
 ip address 10.1.1.5 255.255.255.252
 ip ospf authentication message-digest
 ip ospf message-digest-key 1 md5 AREA1
 ip ospf network point-to-point
!
interface Ethernet0/3
 description TO-R9C
 ip address 192.168.20.1 255.255.255.252
 ip authentication mode eigrp 20 md5
 ip authentication key-chain eigrp 20 MCP
 ip policy route-map ACCESS-R2-LO
!
!
router eigrp 20
 network 8.8.8.8 0.0.0.0
 network 192.168.20.0 0.0.0.3
 redistribute ospf 1 route-map OSPF-TO-EIGRP
 passive-interface Loopback1
!
router ospf 1
 router-id 8.8.8.8
 auto-cost reference-bandwidth 100000
 area 1 nssa
 redistribute eigrp 20 metric-type 1
 network 10.1.1.0 0.0.0.3 area 1
 network 10.1.1.4 0.0.0.3 area 1
!
ip access-list extended 100
 10 permit ip host 192.168.20.2 host 2.2.2.66
ipv6 route vrf clab-mgmt ::/0 Ethernet0/0 3FFF:172:20:20::1
route-map OSPF-TO-EIGRP permit 10 
 set metric 1000000 1 255 1 1500
!
route-map ACCESS-R2-LO permit 10 
 match ip address 100
 set ip next-hop 10.1.1.6
!
```

💾 **Router R9C**:
```
key chain MCP
 key 1
  key-string MCPLAB20
!
interface Loopback1
 ip address 9.9.1.1 255.255.255.0
!
interface Loopback2
 ip address 9.9.2.1 255.255.255.0
!
interface Loopback3
 ip address 9.9.3.1 255.255.255.0
!
interface Ethernet0/0
 description clab-mgmt
 vrf forwarding clab-mgmt
 ip address 172.20.20.209 255.255.255.0
 ipv6 address 3FFF:172:20:20::8/64
!
interface Ethernet0/1
 description TO-R8C
 ip address 192.168.20.2 255.255.255.252
 ip authentication mode eigrp 20 md5
 ip authentication key-chain eigrp 20 MCP
 ip summary-address eigrp 20 9.9.0.0 255.255.252.0
!
interface Ethernet0/2
 no ip address
 shutdown
!
interface Ethernet0/3
 no ip address
 shutdown
!
!
router eigrp 20
 network 9.9.1.0 0.0.0.255
 network 9.9.2.0 0.0.0.255
 network 9.9.3.0 0.0.0.255
 network 192.168.20.0 0.0.0.3
 passive-interface Loopback1
 passive-interface Loopback2
 passive-interface Loopback3
 eigrp stub connected summary
!
ip sla 1
 icmp-echo 11.11.11.11 source-ip 9.9.1.1
ip sla schedule 1 life forever start-time now
ip sla 2
 icmp-echo 5.5.2.1 source-ip 9.9.2.1
ip sla schedule 2 life forever start-time now
!
```

💾 **Router R10C**:
```
interface Loopback1
 ip address 10.10.10.10 255.255.255.0
!
interface Ethernet0/0
 description clab-mgmt
 vrf forwarding clab-mgmt
 ip address 172.20.20.210 255.255.255.0
 ipv6 address 3FFF:172:20:20::6/64
!
interface Ethernet0/1
 description TO-R1A
 ip address 172.16.0.6 255.255.255.252
 ip ospf authentication message-digest
 ip ospf message-digest-key 1 md5 AREA2
 ip ospf network point-to-point
!
interface Ethernet0/2
 description TO-R11C
 ip address 172.16.0.1 255.255.255.252
 ip ospf authentication message-digest
 ip ospf message-digest-key 1 md5 AREA2
 ip ospf network point-to-point
!
interface Ethernet0/3
 no ip address
 shutdown
!
router ospf 1
 router-id 10.10.10.10
 auto-cost reference-bandwidth 100000
 area 2 stub
 passive-interface Loopback1
 network 10.10.10.0 0.0.0.255 area 2
 network 172.16.0.0 0.0.0.3 area 2
 network 172.16.0.4 0.0.0.3 area 2
!
ip sla responder
!
```

💾 **Router R11C**:
```
interface Loopback1
 ip address 11.11.11.11 255.255.255.0
!
interface Ethernet0/0
 description clab-mgmt
 vrf forwarding clab-mgmt
 ip address 172.20.20.211 255.255.255.0
 ipv6 address 3FFF:172:20:20::C/64
!
interface Ethernet0/1
 description TO-R1A
 ip address 172.16.0.10 255.255.255.252
 ip ospf authentication message-digest
 ip ospf message-digest-key 1 md5 AREA2
 ip ospf network point-to-point
!
interface Ethernet0/2
 description TO-R10C
 ip address 172.16.0.2 255.255.255.252
 ip ospf authentication message-digest
 ip ospf message-digest-key 1 md5 AREA2
 ip ospf network point-to-point
!
interface Ethernet0/3
 no ip address
 shutdown
!
router ospf 1
 router-id 11.11.11.11
 auto-cost reference-bandwidth 100000
 area 2 stub
 passive-interface Loopback1
 network 11.11.11.0 0.255.255.255 area 2
 network 172.16.0.0 0.0.0.3 area 2
 network 172.16.0.8 0.0.0.3 area 2
!
ip sla responder
!
```

⚠️ **NOTE**: The router configurations above are considered the **default configuration** for this network and in **this version of the Lab Manual**, and they are **subject to change** with each new release, as the topology grows in complexity.

⚠️ **NOTE**: Since these configurations are considered the **default configuration** for the current network version, they are going to be your fallback config whenever you use `containerlab redeploy -t lab.yml`

## 💻 MCP Server Code
The latest version of the MCP server code:
```
import os
import json
import time
import pytz
import asyncio
from fastmcp import FastMCP
from dotenv import load_dotenv
from scrapli import AsyncScrapli
from pydantic import BaseModel, Field
from datetime import datetime, time as dt_time

# Load environment variables
load_dotenv()
USERNAME = os.getenv("ROUTER_USERNAME")
PASSWORD = os.getenv("ROUTER_PASSWORD")

if not USERNAME or not PASSWORD:
    raise RuntimeError("Credentials not set")

# Instantiate the FastMCP class
mcp = FastMCP("mcp_automation")

# Loading devices from inventory
INVENTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventory", "NETWORK.json")
if not os.path.exists(INVENTORY_FILE):
    raise RuntimeError(f"Inventory file not found: {INVENTORY_FILE}")

# Read the inventory file
with open(INVENTORY_FILE) as f:
    devices = json.load(f)

# Show command - input model
class ShowCommand(BaseModel):
    """Run a show command against a network device."""
    device: str = Field(..., description="Device name from inventory (e.g. R1, R2, R3)")
    command: str = Field(..., description="Show command to execute on the device")

# Config commands - input model
class ConfigCommand(BaseModel):
    """Send configuration commands to one or more devices."""
    devices: list[str] = Field(..., description="Device names from inventory (e.g. ['R1','R2','R3'])")
    commands: list[str] = Field(..., description="Configuration commands to apply")

# Empty placeholder - input model
class EmptyInput(BaseModel):
    pass

# Snapshot - input model
class SnapshotInput(BaseModel):
    devices: list[str] = Field(..., description="Devices to snapshot (e.g. R1, R2, R3)")
    profile: str = Field(..., description="Snapshot profile (e.g. ospf, stp)")

# Risk score - input model
class RiskInput(BaseModel):
    devices: list[str] = Field(..., description="Devices affected by the config change")
    commands: list[str] = Field(..., description="The configuration commands to apply")

# Read config tool
@mcp.tool(name="run_show")
async def run_show(params: ShowCommand) -> str:
    """
    Execute a show command asynchronously using Scrapli via SSH.
    """
    device = devices.get(params.device)
    if not device:
        return f"Unknown device. Available devices are: {list(devices.keys())}"
    
    connection = {
        "host": device["host"],
        "platform": device["platform"],
        "transport": device["transport"],
        "auth_username": USERNAME,
        "auth_password": PASSWORD,
        "auth_strict_key": False,
    }

    async with AsyncScrapli(**connection) as conn:
        response = await conn.send_command(params.command)
        return response.result

# Forbidden commands
FORBIDDEN = {"reload", "write erase", "format", "delete", "boot"}

def validate_commands(cmds: list[str]):
    for c in cmds:
        if any(bad in c.lower() for bad in FORBIDDEN):
            raise ValueError(f"Forbidden command detected: {c}")

# Function for pushing configs to a device
async def push_config_to_device(dev_name, device, commands):
    connection = {
                "host": device["host"],
                "platform": device["platform"],
                "transport": device["transport"],
                "auth_username": USERNAME,
                "auth_password": PASSWORD,
                "auth_strict_key": False,
            }

    async with AsyncScrapli(**connection) as conn:
        response = await conn.send_configs(commands)
        return dev_name, response.result

# Send config tool
@mcp.tool(name="push_config")
async def push_config(params: ConfigCommand) -> dict:
    """
    Push configuration commands to one or more devices.

    IMPORTANT:
    - This tool enforces maintenance window policy.
    - If changes are outside the approved window, the tool will refuse to run.
    - Maintenance policy files (e.g. MAINTENANCE.json) MUST NOT be modified
    by Claude or by any automation workflow.
    - If a change is blocked, Claude should inform the user and stop.
    - Risk assessment is advisory only and does not block changes.
    """
    # Check maintenance window
    await check_maintenance_window(EmptyInput())

    # Check risk score
    risk = await assess_risk(RiskInput(devices=params.devices, commands=params.commands))

    start = time.perf_counter()

    # Check for any forbidden commands
    validate_commands(params.commands)

    tasks = []

    for dev_name in params.devices:
        device = devices.get(dev_name)
        tasks.append(
            asyncio.create_task(
                push_config_to_device(dev_name, device, params.commands)
            )
        )

    results = {}

    completed = await asyncio.gather(*tasks, return_exceptions=True)

    for item in completed:
        if isinstance(item, Exception):
            continue
        dev_name, result = item
        results[dev_name] = result

    end = time.perf_counter()
    results["execution_time_seconds"] = round(end - start, 2)
    results["risk_assessment"] = risk

    return results

# Returns the expected network intent defined in INTENT.json (source of truth)
@mcp.tool(name="get_intent")
async def get_intent(params: EmptyInput) -> dict:
    """
    Return the desired network intent.
    """

    intent_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"intent","INTENT.json")

    if not os.path.exists(intent_file):
        raise RuntimeError("INTENT.json not found")

    with open(intent_file) as f:
        return json.load(f)

# Snapshot tool: collect current state, store it on disk, return snapshot metadata
@mcp.tool(name="snapshot_state")
async def snapshot_state(params: SnapshotInput) -> dict:
    """
    Takes a snapshot of device state for the given profile.
    Intended to be used before changes so differences can be reviewed manually.
    """

    snapshot_id = time.strftime("%Y%m%d-%H%M%S")
    base_path = os.path.join("snapshots", snapshot_id)
    os.makedirs(base_path, exist_ok=True)

    stored = {}

    for dev_name in params.devices:
        device = devices.get(dev_name)
        if not device:
            continue

        dev_path = os.path.join(base_path, dev_name)
        os.makedirs(dev_path, exist_ok=True)

        connection = {
            "host": device["host"],
            "platform": device["platform"],
            "transport": device["transport"],
            "auth_username": USERNAME,
            "auth_password": PASSWORD,
            "auth_strict_key": False,
        }

        async with AsyncScrapli(**connection) as conn:
            outputs = {}

            # Always save running config
            outputs["running_config"] = (
                await conn.send_command("show running-config")
            ).result

            # Profile-driven commands
            if params.profile == "ospf":
                outputs["ospf_config"] = (await conn.send_command("show ip ospf")).result
                outputs["neighbors"] = (await conn.send_command("show ip ospf neighbor")).result

            elif params.profile == "stp":
                outputs["stp_general"] = (await conn.send_command("show spanning-tree")).result
                outputs["stp_details"] = (await conn.send_command("show spanning-tree detail")).result

        for name, content in outputs.items():
            with open(os.path.join(dev_path, f"{name}.txt"), "w") as f:
                f.write(content)

        stored[dev_name] = list(outputs.keys())

    return {
        "snapshot_id": snapshot_id,
        "stored_at": base_path,
        "devices": stored,
    }

# Maintenance windows tool
@mcp.tool(name="check_maintenance_window")
async def check_maintenance_window(params: EmptyInput) -> dict:
    """
    Checks whether the current time falls within an approved maintenance window.

    This tool is intended to be called before making configuration changes.
    It does not block or apply changes by itself — it only reports whether
    changes are currently allowed based on time-based policy.

    The result of this tool is consumed by other tools (e.g. push_config)
    to enforce time-based change policies.

    Note: Maintenance policy is read-only and managed outside automation.
    """

    policy_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "policy",
        "MAINTENANCE.json"
    )

    if not os.path.exists(policy_file):
        return {
            "allowed": True,
            "reason": "No maintenance policy defined"
        }
    
    with open(policy_file) as f:
        policy = json.load(f)

    tz = pytz.timezone(policy.get("timezone", "UTC"))
    now = datetime.now(tz)

    current_day = now.strftime("%a").lower()[:3]
    current_time = now.time()

    for window in policy.get("windows", []):
        if current_day in window["days"]:
            start = dt_time.fromisoformat(window["start"])
            end = dt_time.fromisoformat(window["end"])

            if start <= current_time <= end:
                return {
                    "allowed": True,
                    "current_time": now.isoformat(),
                    "reason": "Within maintenance window"
                }
            
    return {
        "allowed": False,
        "current_time": now.isoformat(),
        "reason": "Outside maintenance window"
    }

# Risk assessment tool
@mcp.tool(name="assess_risk")
async def assess_risk(params: RiskInput) -> dict:
    """
    Assigns a simple risk level (low / medium / high) to a configuration change.
    This tool does NOT block changes. It only reports risk.
    """
    cmd_text = " ".join(params.commands).lower()
    device_count = len(params.devices)

    reasons = []

    # Blast radius
    if device_count >= 3:
        risk = "high"
        reasons.append(f"Change affects {device_count} devices")

    elif device_count > 1:
        risk = "medium"
        reasons.append(f"Change affects multiple devices ({device_count})")

    else:
        risk = "low"

    # Content-based assessment
    if any(k in cmd_text for k in ["router ", "ospf", "bgp", "isis", "eigrp"]):
        risk = "high"
        reasons.append("Touches routing control plane")

    if any(k in cmd_text for k in ["shutdown", "no shutdown"]):
        risk = "high"
        reasons.append("Interface disruption possible")

    return {
        "risk": risk,
        "devices": device_count,
        "reasons": reasons or ["Minor configuration change"]
    }

# Run the MCP Server
if __name__ == "__main__":
    mcp.run()
```

## 🔥 Automation and Troubleshooting
Troubleshooting scenarios are located in the [**troubleshoot.md**](https://github.com/pdudotdev/netaimcp/blob/main/scenarios/troubleshoot.md) file that is going to be constantly updated as the network grows in complexity.

✍️ **NOTE**: Each scenario is created by starting from the **default configuration** of the network (see [Network Topology](#-network-topology)) and intentionally breaking one or more things to trigger a certain type of failure. Then, with just a simple prompt, we enable Claude to use the MCP server for identifying the root cause(s) and fixing the network. 

### Example of scenario workflow
Each **troubleshooting scenario** has the following structure:
- [x] **Summary**:
```
R1A OSPF adjacency stuck in EXCHANGE, while R2A is stuck in EXCH START state.
```
- [x] **Causing Failure**: 
```
Changing the MTU on R2A to cause a mismatch with R1A, using the commands below:

interface Ethernet 3
 mtu 1400
```
- [x] **Confirming Failure**:
```
Checking the effects of the commands above:

R2A(config-if-Et3)#show interfaces Ethernet 3 | i MTU
  IP MTU 1400 bytes, BW 1000000 kbit
R2A(config-if-Et3)#show ip ospf neighbor 
Neighbor ID     Instance VRF      Pri State                  Dead Time   Address         Interface
3.3.3.3         1        default  1   FULL                   00:00:35    10.0.0.10       Ethernet4
1.1.1.1         1        default  0   EXCH START             00:00:34    10.0.0.1        Ethernet3
7.7.7.7         1        default  0   FULL                   00:00:34    10.1.1.9        Ethernet2
6.6.6.6         1        default  0   FULL                   00:00:33    10.1.1.13       Ethernet1

R1A#show ip ospf neighbor
Neighbor ID     Instance VRF      Pri State                  Dead Time   Address         Interface
2.2.2.2         1        default  0   EXCHANGE               00:00:32    10.0.0.2        Ethernet4
3.3.3.3         1        default  1   FULL                   00:00:38    10.0.0.6        Ethernet3
11.11.11.11     1        default  1   FULL                   00:00:32    172.16.0.10     Ethernet2
10.10.10.10     1        default  1   FULL                   00:00:30    172.16.0.6      Ethernet1
```
- [x] **User Prompt**:
```
Why is the R1A-R2A OSPF adjacency stuck? Can you check and fix please?
```
- [x] **Commands issued by Claude**:
```
show ip ospf neighbor
show ip ospf interface Ethernet 3
show running-config interface Ethernet 3
interface Ethernet 3
no mtu 1400
```
- [x] **Confirmation**:
```
R2A#show ip ospf neighbor
Neighbor ID     Instance VRF      Pri State                  Dead Time   Address         Interface
3.3.3.3         1        default  1   FULL                   00:00:34    10.0.0.10       Ethernet4
1.1.1.1         1        default  0   FULL                   00:00:38    10.0.0.1        Ethernet3
7.7.7.7         1        default  0   FULL                   00:00:29    10.1.1.9        Ethernet2
6.6.6.6         1        default  0   FULL                   00:00:33    10.1.1.13       Ethernet1 
```

## ⬆️ Planned Upgrades
Expected in version v2.0:
- [ ] Adding BGP
- [ ] Adding more routers
- [ ] Adding a new vendor
- [ ] New troubleshooting scenarios

## ⚠️ Disclaimer
This project is intended for educational purposes only. You are responsible for building your own lab environment and meeting the necessary conditions (e.g., RAM/vCPU, router OS images, Claude subscription/API key, etc.).

## 📜 License
Licensed under the [GNU GENERAL PUBLIC LICENSE Version 3](https://github.com/pdudotdev/netaimcp/blob/main/LICENSE).