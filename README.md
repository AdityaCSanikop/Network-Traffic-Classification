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
    ├── icmp_test.png          # ICMP ping test terminal output
    ├── tcp_test.png           # TCP iPerf test terminal output
    ├── udp_test.png           # UDP iPerf test terminal output
    ├── wireshark_icmp.png     # ICMP packet analysis (Wireshark)
    ├── wireshark_tcp.png      # TCP packet analysis (Wireshark)
    ├── wireshark_udp.png      # UDP packet analysis (Wireshark)
    ├── controller_output.png  # Ryu controller statistics
    └── mininet_setup.png      # Network initialization (optional)
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

### Step 5: Install Wireshark (for Packet Analysis)
```bash
sudo apt install wireshark -y
sudo usermod -aG wireshark $USER
newgrp wireshark
```

### Step 6: Clone/Download Project
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

### Step 3: Start Packet Capture (Terminal 3)

Open **Terminal 3** to capture network traffic with Wireshark:

```bash
sudo wireshark &
```

**In Wireshark GUI:**
1. Select interface `s1-eth0` (the switch interface)
2. Click the **Start capturing packets** button (blue shark icon)
3. Keep Wireshark running during all tests

---

### Step 4: Run Test Scenarios

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

#### Wireshark Analysis for ICMP Test

**In Wireshark GUI:**
1. Apply filter: `icmp`
2. Look for:
   - **ICMP Echo Request** (Type 8) - Ping request from h1
   - **ICMP Echo Reply** (Type 0) - Response from h2
   - Source IP: `10.0.0.1`, Destination IP: `10.0.0.2`
3. Verify packet count matches controller output (~20 packets)
4. Note the TTL (Time To Live) value in each packet
5. Check timestamp differences between requests and replies

**Wireshark Screenshot (ICMP Test):**
![ICMP Wireshark Capture](screenshots/wireshark_icmp.png)

*Figure: Wireshark filter showing ICMP Echo Request and Reply packets between hosts*

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

#### Wireshark Analysis for TCP Test

**In Wireshark GUI:**
1. Apply filter: `tcp.port == 5001`
2. Look for:
   - **TCP SYN** packet - Initial connection (h1 → h3)
   - **TCP ACK** packets - Acknowledgments
   - **TCP FIN** packet - Connection close
   - Protocol sequence shows TCP three-way handshake
3. Verify source `10.0.0.1` and destination `10.0.0.3` on port 5001 (iPerf default)
4. Observe data transfer packets with varying payload sizes
5. Confirm total TCP packet count

**Wireshark Screenshot (TCP Test):**
![TCP Wireshark Capture](screenshots/wireshark_tcp.png)

*Figure: Wireshark filter showing TCP three-way handshake (SYN, SYN-ACK, ACK) and data transfer*

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

#### Wireshark Analysis for UDP Test

**In Wireshark GUI:**
1. Apply filter: `udp.port == 5001`
2. Look for:
   - **UDP packets** - No handshake (connectionless protocol)
   - Source `10.0.0.2` to destination `10.0.0.4` on port 5001
   - Consistent packet sizes (typical iPerf UDP payloads ~1470 bytes)
   - No SYN/ACK sequence (unlike TCP)
3. Observe unidirectional traffic from server port to client
4. Note that UDP has minimal overhead compared to TCP
5. Verify UDP packet count matches controller statistics

**Wireshark Screenshot (UDP Test):**
![UDP Wireshark Capture](screenshots/wireshark_udp.png)

*Figure: Wireshark filter showing UDP data packets flowing directly from source to destination (no handshake)*

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

### ⚠️ Important: Displaying Screenshots

For images to display correctly on GitHub:

1. **File Placement:** All screenshots must be in the `screenshots/` folder
2. **File Naming:** Filenames are **case-sensitive** - use exact names below
3. **Git Tracking:** Commit screenshots using:
   ```bash
   git add screenshots/*.png
   git commit -m "Add execution screenshots"
   git push
   ```
4. **Verification:** After pushing, verify images appear on GitHub repository page

> **If images are not visible:** Ensure you have cloned the full repository with `git clone` and the `screenshots/` folder is present locally.

---

### 1. ICMP Test (Ping) - Terminal Output

![ICMP Test Output](screenshots/icmp_test.png)

**Expected filename:** `screenshots/icmp_test.png`

Shows Mininet terminal output of ICMP ping test between h1 (10.0.0.1) and h2 (10.0.0.2) with:
- Echo request/reply packets
- TTL values
- Response times
- Statistics (0% packet loss)

---

### 2. TCP Test (iPerf) - Terminal Output

![TCP Test Output](screenshots/tcp_test.png)

**Expected filename:** `screenshots/tcp_test.png`

Shows Mininet terminal output of TCP iPerf test with:
- Server initialization on h3 (port 5001)
- Client connection from h1
- Bandwidth statistics (e.g., 9.50 MBits/sec)
- Connection duration (0-5 sec interval)

---

### 3. UDP Test (iPerf) - Terminal Output

![UDP Test Output](screenshots/udp_test.png)

**Expected filename:** `screenshots/udp_test.png`

Shows Mininet terminal output of UDP iPerf test with:
- Server initialization on h4 (port 5001, UDP mode)
- Client connection from h2
- Datagram statistics (1470 byte payloads)
- Bandwidth and jitter measurements

---

### 4. ICMP Packets - Wireshark Analysis

![ICMP Wireshark](screenshots/wireshark_icmp.png)

**Expected filename:** `screenshots/wireshark_icmp.png`

Wireshark packet capture filtered by `icmp`:
- ICMP Echo Request packets (Type 8)
- ICMP Echo Reply packets (Type 0)
- Source: 10.0.0.1, Destination: 10.0.0.2
- Complete handshake visible with timestamps

---

### 5. TCP Packets - Wireshark Analysis

![TCP Wireshark](screenshots/wireshark_tcp.png)

**Expected filename:** `screenshots/wireshark_tcp.png`

Wireshark packet capture filtered by `tcp.port == 5001`:
- **TCP Three-Way Handshake:**
  - SYN (from 10.0.0.1:47148 to 10.0.0.3:5001)
  - SYN-ACK (return)
  - ACK (connection established)
- Data transfer packets with payloads
- Protocol details visible in packet inspector

---

### 6. UDP Packets - Wireshark Analysis

![UDP Wireshark](screenshots/wireshark_udp.png)

**Expected filename:** `screenshots/wireshark_udp.png`

Wireshark packet capture filtered by `udp.port == 5001`:
- UDP data packets (connectionless, no handshake)
- Source: 10.0.0.2:port, Destination: 10.0.0.4:5001
- Consistent 1470-byte UDP datagram payloads
- Direct transmission without acknowledgment

---

### 7. Ryu Controller Output - Traffic Statistics

![Controller Output](screenshots/controller_output.png)

**Expected filename:** `screenshots/controller_output.png`

Ryu controller console showing:
- **Real-time packet statistics** displayed as packets arrive
- **Summary table** with protocol breakdown:
  - TCP: count and percentage
  - UDP: count and percentage
  - ICMP: count and percentage
  - OTHER: unclassified packets
- **Visual bar chart** using `#` characters for comparison
- **Total packet count** across all protocols

---

### 8. Mininet Network Initialization

![Mininet Setup](screenshots/mininet_setup.png)

**Expected filename:** `screenshots/mininet_setup.png` (optional)

Shows Mininet CLI startup with:
- Host configurations (h1-h4 with IP addresses)
- Controller connection
- Switch creation
- Network readiness message
- "mininet>" prompt ready for commands

---

## Screenshot Storage Instructions

Create the `screenshots/` folder if it doesn't exist:

```bash
mkdir -p screenshots
```

Copy your captured images into this folder:

```bash
# Example: after taking screenshots
cp ~/Pictures/icmp_test.png screenshots/
cp ~/Pictures/tcp_test.png screenshots/
cp ~/Pictures/udp_test.png screenshots/
cp ~/Pictures/udp_test.png screenshots/
cp ~/Pictures/wireshark_icmp.png screenshots/
cp ~/Pictures/wireshark_tcp.png screenshots/
cp ~/Pictures/wireshark_udp.png screenshots/
cp ~/Pictures/controller_output.png screenshots/
```

Verify files are present:

```bash
ls -la screenshots/
```

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
