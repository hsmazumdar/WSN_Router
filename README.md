# WSN_Router
A Novel Energy Efficient Routing Algorithm for Wireless Sensor Network

Wireless sensor networks (WSNs) have become integral to various applications, necessitating energy-efficient strategies to extend their lifespan. This algorithm addresses the challenge of limited energy availability in wireless sensor nodes, which is particularly critical in applications where direct human intervention is impractical. A novel routing strategy involving both mobile and static sinks is proposed that optimizes retransmissions and puts low battery powered nodes in sleep.

The proposed routing algorithm for the wireless sensor network (WSN), our aim is to optimize the number of retransmissions in order to save the battery power of the nodes. Each node runs this algorithm in distributed edge computing mode and follows the following rules when receives a packet:

Algorithm:

1. If the received packet's destination address is the same as the receiver node's address, the node sends an acknowledge packet back to the source node with the same packet number and a hop count of 0. In the acknowledge packet, the source and destination addresses are interchanged, and the packet type is set to 1.

2. If the received packet's destination address is different, the node generates a time delay that is inversely proportional to the distance of the destination node from the stored localization table. During this delay, the node enters a "ready to transmit" mode while waiting for the delay to expire.

3. While waiting for the delay time to expire, the receiver node checks for any further received packets. If it receives a packet with the same packet number but an increased hop count, it abandons the "ready to transmit" mode.

4. If no packet is received with the same packet number during the waiting period, the receiver node retransmits the packet with an increased hop count and updates the relay node number.

By implementing these rules, the algorithm aims to minimize the number of retransmissions required to deliver packets in the network, thus conserving the battery power of the nodes.



Quick Start Steps-

1. Download the zip file and unzip in a folder ‘WSN_Router’.
2. Select ‘WsnRoutPwr.py’ file and load in VS Code
3. Install necessary library components in VC Code
4. Run WsnRoutPwr.py to popup 'WSN Auto Routing' application of figure-1
5. Open 'File' menu tab and press 'Draw Nodes (Cnt+d)' tab or press 'Control + d' to populate randomly distributed nodes as shown in figure-1. The default number of nodes are 100 and can be changed using ‘Max Nodes’ tab
6. Select a source and destination node pair from 'File' menu as shown in figure-2 or by simply pressing (Cnt+l)
7. Select and press 'File->Send Pkt (Cnt+s) from 'File' menu as shown in figure-3 or by simply pressing (Cnt+s). This will demonstrate data packet sending from source node to destination node and returning acknowledge packet back to source node using proposed power saving algorithm
8. Select and press 'File->Auto Pkt On (Cnt+a) from 'File' menu as shown in figure-4 to continuously send data packets from random source to random destination. During this process all transmitting nodes will discharge their batteries and show blue at 40% life. Blue nodes will inhibit themselves in relaying packets, however they will send or receive packets for self-use till 10% life.   


<img src="Readme_files/Main.png">

Figure-1 Simulation of a Wireless Sensor Network (WSN) with interactive GUI to demonstrate a new Novel Energy Efficient Routing Algorithm. Initially populate selected number of nodes, with random placement on canvas using 'File' menu of by simply pressing (Cnt+d)

<img src="Readme_files/SrcDstLine.png">

Figure-2 Select a source and destination node pair from 'File' menu or by simply pressing (Cnt+l) 

***************************************  

<img src="Readme_files/SrcDstSend.png">

Figure-3 Select and press 'File->Send Pkt (Cnt+s) from 'File' menu or by simply pressing (Cnt+s).

***************************************  

<img src="Readme_files/SrcDstAuto.png">

Figure-4 Select and press 'File->Auto Pkt On (Cnt+a) from 'File' menu to continuously send data packets from random source to random destination. The blue nodes represents low battery and unable to relay paskets.
***************************************  


