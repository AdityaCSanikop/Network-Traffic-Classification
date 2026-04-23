# SDN Traffic Classification System

## Project Title
**Software-Defined Network (SDN) Traffic Classification using Ryu Controller and Mininet**

---

## Problem Statement

In traditional networks, traffic classification and monitoring are challenging tasks. Network administrators struggle with:
- Identifying and categorizing different protocol types (TCP, UDP, ICMP) in real-time
- Monitoring packet flows without deep packet inspection overhead
- Understanding network behavior patterns

This project implements an **intelligent traffic classification system** using **Software-Defined Networking (SDN)** principles to automatically detect, classify, and analyze network protocols in an emulated network environment.

---

## Objectives

- ✅ Implement an SDN controller using Ryu framework to intercept and classify network packets
- ✅ Create a virtualized network topology using Mininet with 4 hosts
- ✅ Classify incoming traffic by protocol type (TCP, UDP, ICMP)
- ✅ Count and display statistics for each protocol
- ✅ Generate reports in real-time as packets flow through the network
- ✅ Provide performance metrics and visualization for network analysis

---

## Technologies Used

| Technology | Purpose |
|-----------|---------|
| **Ryu Controller** | OpenFlow SDN controller for intelligent packet classification |
| **Mininet** | Network emulation platform for creating virtual topologies |
| **OpenFlow 1.3** | Protocol for SDN switch-controller communication |
| **Python 3** | Core programming language |
| **OVS (Open vSwitch)** | Virtual switch implementation |

---

## Project Structure

```
sdn_project/
│
├── traffic_classifier.py      # Ryu SDN controller application
│                               # - Intercepts packets from OpenFlow switch
│                               # - Classifies by protocol (TCP/UDP/ICMP)
│                               # - Maintains packet statistics
│
├── topology.py                 # Mininet network topology creator
│                               # - Creates 4 hosts in single network
│                               # - Configures OpenFlow switch (OVSSwitch)
│                               # - Connects hosts to controller
│
├── README.md                   # Project documentation (this file)
│
└── screenshots/                # Proof of execution images
    ├── ping.png               # ICMP test screenshot
    ├── tcp.png                # TCP test screenshot
    ├── udp.png                # UDP test screenshot
    └── output.png             # Controller console output
```

---

## Installation Steps

### Prerequisites
- Ubuntu 20.04 or later
- Python 3.6+
- Sudo access

### Step 1: Update System Packages
```bash
sudo apt update
sudo apt upgrade -y
```

### Step 2: Install Mininet
```bash
sudo apt install mininet -y
```

### Step 3: Install Ryu SDN Controller
```bash
pip3 install ryu
```

### Step 4: Install Additional Dependencies
```bash
pip3 install --upgrade pip
pip3 install netaddr eventlet msgpack
```

### Step 5: Clone/Download Project
```bash
cd ~
git clone <your-repo-url>  # Replace with your repository
cd sdn_project
```

---

## How to Run

### Step 1: Start the Ryu Controller

Open **Terminal 1** and execute:

```bash
cd ~/sdn_project
ryu-manager traffic_classifier.py
```

**Expected Output:**
```
loading app traffic_classifier.py
loading app ryu.controller.ofp_event
instantiating app traffic_classifier.py
...
Switch connected: dpid=1
```

---

### Step 2: Create Network Topology

Open **Terminal 2** and execute:

```bash
cd ~/sdn_project
sudo python3 topology.py
```

**Expected Output:**
```
*** Network ready. h1=10.0.0.1  h2=10.0.0.2  h3=10.0.0.3  h4=10.0.0.4
mininet>
```

---

### Step 3: Run Test Scenarios

Once you see the `mininet>` prompt, execute the test commands below.

---

## Test Scenarios

### Scenario 1: ICMP Protocol Test (Ping)

**Command:**
```bash
mininet> h1 ping -c 10 h2
```

**What it does:** Host 1 sends 10 ICMP echo requests to Host 2. The controller will classify these as ICMP packets and update statistics.

**Expected Output in Terminal 1:**
```
ICMP packets: 20 (10 echo + 10 reply)
```

---

### Scenario 2: TCP Protocol Test (iPerf)

**Command:**
```bash
mininet> h3 iperf -s &
mininet> h1 iperf -c 10.0.0.3 -t 5
```

**What it does:** Host 3 starts an iPerf server, Host 1 sends TCP traffic for 5 seconds. Controller classifies these as TCP packets.

**Expected Output in Terminal 1:**
```
TCP packets: 50+
```

---

### Scenario 3: UDP Protocol Test (iPerf)

**Command:**
```bash
mininet> h4 iperf -s -u &
mininet> h2 iperf -c 10.0.0.4 -u -t 5
```

**What it does:** Host 4 starts UDP iPerf server, Host 2 sends UDP traffic. Controller classifies these as UDP packets.

**Expected Output in Terminal 1:**
```
UDP packets: 50+
```

---

## Expected Output (Statistics Table)

After running all test scenarios, the controller output should resemble:

| Protocol | Packets | Percentage | Visual Bar |
|----------|---------|------------|-----------|
| TCP      | 48      | 48.0%      | ############ |
| UDP      | 32      | 32.0%      | ######### |
| ICMP     | 20      | 20.0%      | ###### |
| **Total** | **100** | **100%** | ############ |

---

## File Explanations

### traffic_classifier.py

**Purpose:** Ryu SDN Controller Application

**Key Functions:**
- `switch_features_handler()` → Handles switch connection and registers default flow
- `packet_in_handler()` → Intercepts incoming packets and extracts protocol headers
- `_classify()` → Analyzes packet headers to determine protocol type
- Statistics tracking → Maintains count and percentage of each protocol

**How it works:**
1. Listens to OpenFlow switch events
2. Captures packets sent to controller
3. Parses Ethernet, IPv4, TCP, UDP, ICMP headers
4. Updates counters for each protocol
5. Logs statistics in real-time

---

### topology.py

**Purpose:** Mininet Network Topology Creator

**Key Components:**
- `create_topology()` → Builds entire virtual network
- 1 OpenFlow Switch (OVSSwitch)
- 4 Hosts (h1, h2, h3, h4) with IP addresses 10.0.0.1-4
- RemoteController connection to Ryu (localhost:6633)

**Network Layout:**
```
         ┌─────────────┐
         │   Ryu       │
         │ Controller  │
         │ :6633       │
         └──────┬──────┘
                │
         ┌──────▼──────┐
         │   OVSSwitch │
         │     (s1)    │
         └──┬───┬───┬──┘
            │   │   │
        h1  h2  h3  h4
```

---

## Screenshots Section

### ICMP Test (Ping)
![Ping Test](screenshots/ping.png)

*Figure 1: ICMP echo requests and replies between hosts. Controller logs show ICMP packet classification and count.*

---

### TCP Test (iPerf)
![TCP Test](screenshots/tcp.png)

*Figure 2: TCP traffic generation and transmission between hosts. Controller classifies and counts TCP packets in real-time.*

---

### UDP Test (iPerf)
![UDP Test](screenshots/udp.png)

*Figure 3: UDP protocol traffic flowing through the network. Controller distinguishes UDP packets from TCP and ICMP.*

---

### Controller Output
![Controller Output](screenshots/output.png)

*Figure 4: Ryu controller console showing real-time packet classification, protocol statistics, and summary report after all tests.*

---

## Conclusion

This **SDN Traffic Classification System** demonstrates the power of Software-Defined Networking for intelligent network monitoring and management. By leveraging the Ryu controller and Mininet emulation, we achieved:

✅ **Real-time Protocol Classification** → Packets identified by type (TCP/UDP/ICMP)  
✅ **Network Visibility** → Complete statistics and flow analysis  
✅ **Scalability** → Can be extended to more protocols and complex topologies  
✅ **Educational Value** → Practical understanding of SDN concepts  

### Potential Enhancements
- Add support for more protocols (DNS, HTTP, etc.)
- Implement traffic shaping policies
- Create web dashboard for visualization
- Add anomaly detection capabilities
- Deploy on physical OpenFlow switches

---

## Author

**Project Submission for:** Software-Defined Networking Course  
**Date:** April 2026

---

## References

- [Ryu Controller Documentation](https://ryu.readthedocs.io/)
- [Mininet Documentation](http://mininet.org/)
- [OpenFlow 1.3 Specification](https://opennetworking.org/)
- [SDN Fundamentals](https://www.cisco.com/c/en/us/products/ios-nx-os-software/software-defined-networking/index.html)

---

**Status:** ✅ Complete and Tested
