from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.node import CPULimitedHost
import time
import os

class MyTopo ( Topo ):
    def __init__( self, **opts):
        Topo.__init__( self, **opts )

        # Host
        h1 = self.addHost( 'h1' )
        h2 = self.addHost( 'h2' )

        # Router
        r1 = self.addHost( 'r1' )
        r2 = self.addHost( 'r2' )
        r3 = self.addHost( 'r3' )
        r4 = self.addHost( 'r4' )

        # Linkopt
        linkopt = {'bw' : 1}
        linkopt2 = {'bw' : 0.5}

        # Link
        self.addLink(h1, r1, intfName1='h1-eth0', intfName2='r1-eth0', cls=TCLink, **linkopt)
        self.addLink(h1, r2, intfName1='h1-eth1', intfName2='r2-eth1', cls=TCLink, **linkopt)
        self.addLink(r1, r3, intfName1='r1-eth1', intfName2='r3-eth1', cls=TCLink, **linkopt2)
        self.addLink(r1, r4, intfName1='r1-eth2', intfName2='r4-eth2', cls=TCLink, **linkopt)
        self.addLink(r3, h2, intfName1='r3-eth0', intfName2='h2-eth0', cls=TCLink, **linkopt)
        self.addLink(r3, r2, intfName1='r3-eth2', intfName2='r2-eth2', cls=TCLink, **linkopt)
        self.addLink(h2, r4, intfName1='h2-eth1', intfName2='r4-eth1', cls=TCLink, **linkopt)
        self.addLink(r4, r2, intfName1='r4-eth0', intfName2='r2-eth0', cls=TCLink, **linkopt2)

def runTopo():
    # Mininet bersih dari cache
    os.system('mn -c')
    # Topologi
    topo = MyTopo()
    net = Mininet( topo=topo, host=CPULimitedHost, link=TCLink )
    net.start()
    # Memasukkan objek ke host pada variabel
    h1,h2,r1,r2,r3,r4 = net.get('h1', 'h2', 'r1', 'r2', 'r3', 'r4')
    # Iperf background process

    # h1
    h1.cmd('ifconfig h1-eth0 0')
    h1.cmd('ifconfig h1-eth1 0')
    h1.cmd('ifconfig h1-eth0 192.168.0.1 netmask 255.255.255.0')
    h1.cmd('ifconfig h1-eth1 192.168.5.1 netmask 255.255.255.0')

    # h2
    h2.cmd('ifconfig h2-eth0 0')
    h2.cmd('ifconfig h2-eth1 0')
    h2.cmd('ifconfig h2-eth0 192.168.2.1 netmask 255.255.255.0')
    h2.cmd('ifconfig h2-eth1 192.168.3.1 netmask 255.255.255.0')

    # r1
    r1.cmd('ifconfig r1-eth0 0')
    r1.cmd('ifconfig r1-eth1 0')
    r1.cmd('ifconfig r1-eth2 0')
    r1.cmd('ifconfig r1-eth0 192.168.0.2 netmask 255.255.255.0')
    r1.cmd('ifconfig r1-eth1 192.168.1.1 netmask 255.255.255.0')
    r1.cmd('ifconfig r1-eth2 192.168.6.1 netmask 255.255.255.0')

    # r2
    r2.cmd('ifconfig r2-eth0 0')
    r2.cmd('ifconfig r2-eth1 0')
    r2.cmd('ifconfig r2-eth2 0')
    r2.cmd('ifconfig r2-eth0 192.168.4.1 netmask 255.255.255.0')
    r2.cmd('ifconfig r2-eth1 192.168.5.2 netmask 255.255.255.0')
    r2.cmd('ifconfig r2-eth2 192.168.7.1 netmask 255.255.255.0')

    # r3
    r3.cmd('ifconfig r3-eth0 0')
    r3.cmd('ifconfig r3-eth1 0')
    r3.cmd('ifconfig r3-eth2 0')
    r3.cmd('ifconfig r3-eth0 192.168.2.2 netmask 255.255.255.0')
    r3.cmd('ifconfig r3-eth1 192.168.1.2 netmask 255.255.255.0')
    r3.cmd('ifconfig r3-eth2 192.168.7.2 netmask 255.255.255.0')

    # r4
    r4.cmd('ifconfig r4-eth0 0')
    r4.cmd('ifconfig r4-eth1 0')
    r4.cmd('ifconfig r4-eth2 0')
    r4.cmd('ifconfig r4-eth0 192.168.4.2 netmask 255.255.255.0')
    r4.cmd('ifconfig r4-eth1 192.168.3.2 netmask 255.255.255.0')
    r4.cmd('ifconfig r4-eth2 192.168.6.2 netmask 255.255.255.0')

    # router conf
    r1.cmd('echo > /proc/sys/net/ip_forward')
    r2.cmd('echo > /proc/sys/net/ip_forward')
    r3.cmd('echo > /proc/sys/net/ip_forward')
    r4.cmd('echo > /proc/sys/net/ip_forward')

    # static routing host
    h1.cmd('ip rule add from 192.168.0.1 table 1')
    h1.cmd('ip rule add from 192.168.5.1 table 2')
    h1.cmd('ip route add 192.168.0.0/24 dev h1-eth0 scope link table 1')
    h1.cmd('ip route add default via 192.168.0.2 dev h1-eth0 table 1')
    h1.cmd('ip route add 192.168.5.0/24 dev h1-eth1 scope link table 2')
    h1.cmd('ip route add default via 192.168.5.2 dev h1-eth1 table 2')
    h1.cmd('ip route add default scope global nexthop via 192.168.0.2 dev h1-eth0')

    h2.cmd('ip rule add from 192.168.2.1 table 1')
    h2.cmd('ip rule add from 192.168.3.1 table 2')
    h2.cmd('ip route add 192.168.2.0/24 dev h2-eth0 scope link table 1')
    h2.cmd('ip route add default via 192.168.2.2 dev h2-eth0 table 1')
    h2.cmd('ip route add 192.168.3.0/24 dev h2-eth1 scope link table 2')
    h2.cmd('ip route add default via 192.168.3.2 dev h2-eth1 table 2')
    h2.cmd('ip route add default scope global nexthop via 192.168.3.2 dev h2-eth1')
    
    # static routing router
    r1.cmd('route add -net 192.168.2.0/24 gw 192.168.1.2')
    r1.cmd('route add -net 192.168.3.0/24 gw 192.168.6.2')
    r1.cmd('route add -net 192.168.4.0/24 gw 192.168.6.2')
    r1.cmd('route add -net 192.168.5.0/24 gw 192.168.6.2')
    r1.cmd('route add -net 192.168.7.0/24 gw 192.168.1.2')

    r2.cmd('route add -net 192.168.0.0/24 gw 192.168.7.2')
    r2.cmd('route add -net 192.168.1.0/24 gw 192.168.7.2')
    r2.cmd('route add -net 192.168.2.0/24 gw 192.168.7.2')
    r2.cmd('route add -net 192.168.3.0/24 gw 192.168.4.2')
    r2.cmd('route add -net 192.168.6.0/24 gw 192.168.4.2')

    r3.cmd('route add -net 192.168.0.0/24 gw 192.168.1.1')
    r3.cmd('route add -net 192.168.3.0/24 gw 192.168.7.1')
    r3.cmd('route add -net 192.168.4.0/24 gw 192.168.7.1')
    r3.cmd('route add -net 192.168.5.0/24 gw 192.168.7.1')
    r3.cmd('route add -net 192.168.6.0/24 gw 192.168.1.1')

    r4.cmd('route add -net 192.168.0.0/24 gw 192.168.6.1')
    r4.cmd('route add -net 192.168.1.0/24 gw 192.168.6.1')
    r4.cmd('route add -net 192.168.2.0/24 gw 192.168.6.1')
    r4.cmd('route add -net 192.168.5.0/24 gw 192.168.4.1')
    r4.cmd('route add -net 192.168.7.0/24 gw 192.168.4.1')

    time.sleep(15)

    #h1.cmdPrint(fg)
    CLI(net)
    net.stop()

if __name__=='__main__':
    setLogLevel('info')
    runTopo()
