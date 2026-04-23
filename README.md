# SDN Traffic Classification System

## Problem Statement
Classify network traffic by protocol (TCP, UDP, ICMP) using
Ryu SDN controller and Mininet network emulator.

## Setup
1. sudo apt install mininet -y
2. pip3 install ryu
3. git clone <your-repo-url>

## Running
Terminal 1: ryu-manager traffic_classifier.py
Terminal 2: sudo python3 topology.py

## Test Scenarios
Scenario 1 — ICMP: h1 ping -c 10 h2
Scenario 2 — TCP:  h1 iperf -c 10.0.0.3 -t 5
Scenario 3 — UDP:  h2 iperf -c 10.0.0.4 -u -t 5

## Expected Output
Protocol   Packets  Percent  Bar
TCP             24    48.0%  #########
UDP             16    32.0%  ######
ICMP            10    20.0%  ####

## Proof of Execution
[Add your 10 screenshots here]
