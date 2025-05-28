A **load balancer** is a device or software that distributes network or application traffic across multiple servers. Its main goal is to ensure no single server becomes overwhelmed, which improves responsiveness and availability of applications, websites, or services.

### Key Functions of a Load Balancer

1. **Traffic Distribution**: Splits incoming requests across multiple servers (also called backend servers or nodes).
2. **Health Monitoring**: Continuously checks the status of servers and reroutes traffic away from unhealthy ones.
3. **Scalability**: Allows more servers to be added or removed to handle varying load.
4. **Redundancy**: Improves fault tolerance by maintaining service availability even if some servers fail.
5. **SSL Termination**: Decrypts incoming HTTPS traffic to offload work from backend servers.

### Types of Load Balancers

- **Layer 4 Load Balancer (Transport Layer)**:
    - Makes routing decisions based on IP address, TCP/UDP ports.
    - Faster and simpler.
- **Layer 7 Load Balancer (Application Layer)**:
    - Makes routing decisions based on content of the request (e.g., URL, cookies, headers).
    - Allows more complex rules (e.g., send all API requests to server A, all static files to server B).

### Common Load Balancer Algorithms

- **Round Robin**: Sends requests to servers in a fixed order.
- **Least Connections**: Sends traffic to the server with the fewest active connections.
- **IP Hash**: Routes traffic based on a hash of the client’s IP address.
- **Weighted Distribution**: Assigns different weights to servers based on capacity or performance.

### Examples

- **Hardware-based**: F5, Cisco
- **Software-based/Open Source**: HAProxy, NGINX, Traefik
- **Cloud-native**:
    - AWS Elastic Load Balancer (ELB)
    - Azure Load Balancer
    - Google Cloud Load Balancing
