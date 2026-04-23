from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ipv4, tcp, udp, icmp
from collections import defaultdict

class TrafficClassifier(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(TrafficClassifier, self).__init__(*args, **kwargs)
        self.stats = defaultdict(int)
        self.packet_count = 0

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto  = datapath.ofproto
        parser   = datapath.ofproto_parser
        match    = parser.OFPMatch()
        actions  = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                           ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)
        self.logger.info("Switch connected: dpid=%s", datapath.id)

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser  = datapath.ofproto_parser
        inst = [parser.OFPInstructionActions(
                    ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg      = ev.msg
        datapath = msg.datapath
        ofproto  = datapath.ofproto
        parser   = datapath.ofproto_parser
        in_port  = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        if eth is None:
            return

        proto = self._classify(pkt)
        self.stats[proto] += 1
        self.packet_count += 1

        self.logger.info("Packet #%d | Protocol: %s | Total stats: %s",
                         self.packet_count, proto, dict(self.stats))

        if self.packet_count % 5 == 0:
            self._print_stats()

        actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
        data = msg.data if msg.buffer_id == ofproto.OFP_NO_BUFFER else None
        out = parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=data
        )
        datapath.send_msg(out)

    def _classify(self, pkt):
        if pkt.get_protocol(tcp.tcp):
            return 'TCP'
        elif pkt.get_protocol(udp.udp):
            return 'UDP'
        elif pkt.get_protocol(icmp.icmp):
            return 'ICMP'
        else:
            return 'OTHER'

    def _print_stats(self):
        total = sum(self.stats.values())
        if total == 0:
            return
        print("\n" + "="*48)
        print("      TRAFFIC CLASSIFICATION RESULTS")
        print("="*48)
        print(f"  {'Protocol':<10} {'Packets':>8} {'Percent':>8}  Bar")
        print("-"*48)
        for proto in ['TCP', 'UDP', 'ICMP', 'OTHER']:
            count = self.stats.get(proto, 0)
            pct   = (count / total * 100) if total else 0
            bar   = '#' * int(pct / 5)
            print(f"  {proto:<10} {count:>8} {pct:>7.1f}%  {bar}")
        print("-"*48)
        print(f"  {'TOTAL':<10} {total:>8}")
        print("="*48 + "\n")
