#include <rte_eal.h>
#include <rte_ethdev.h>
#include <rte_mbuf.h>
#include <rte_ether.h>
#include <rte_dev.h>

#include <stdio.h>

#define RX_RING_SIZE 1024

int main(int argc, char* argv[]) {

    /* Initializion the Environment Abstraction Layer (EAL). 8< */
	// int ret = rte_eal_init(argc, argv);
	// if (ret < 0)
	// 	rte_exit(EXIT_FAILURE, "Error with EAL initialization\n");

    /* Initialize the Environment Abstraction Layer (EAL). */
    int nb_ports = rte_eth_dev_count_avail();
    printf("Number of available ports: %d\n", nb_ports);

    /* Create a vhost_user port for each physical port */
    unsigned port_count = 0;
    int portid;
    RTE_ETH_FOREACH_DEV(portid) {
        char portname[32];
        char portargs[256];
        struct rte_ether_addr addr = {0};

        /* once we have created a virtio port for each physical port, stop creating more */
        if (++port_count > nb_ports)
            break;

        /* get MAC address of physical port to use as MAC of virtio_user port */
        rte_eth_macaddr_get(portid, &addr);

        /* set the name and arguments */
        snprintf(portname, sizeof(portname), "virtio_user%u", portid);
        snprintf(portargs, sizeof(portargs),
                "path=/dev/vhost-net,queues=1,queue_size=%u,iface=%s,mac=" RTE_ETHER_ADDR_PRT_FMT,
                RX_RING_SIZE, portname, RTE_ETHER_ADDR_BYTES(&addr));

        /* add the vdev for virtio_user */
        if (rte_eal_hotplug_add("vdev", portname, portargs) < 0)
            rte_exit(EXIT_FAILURE, "Cannot create paired port for port %u\n", portid);

    }
}