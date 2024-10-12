# Distributed Intrusion Detection System (DIDS)

## Overview

The Distributed Intrusion Detection System (DIDS) is a scalable, real-time security monitoring solution designed for enterprise-level networks. It employs a distributed architecture to monitor multiple endpoints simultaneously, providing centralized alert management and analysis.

## Key Features

- Distributed architecture for scalable monitoring
- Real-time log analysis using asynchronous I/O
- Centralized alert collection and management
- Pattern matching for threat detection
- Message queue integration for high-volume alert handling
- Extensible analysis framework

## Real-World Use Cases

1. **Enterprise Network Monitoring**: 
   Deploy agents across various departments to monitor critical systems, providing a comprehensive view of the organization's security posture.

2. **Cloud Infrastructure Security**:
   Monitor logs from multiple cloud instances and services, detecting potential security breaches or misconfigurations.

3. **Compliance Monitoring**:
   Track access to sensitive data across different systems to ensure compliance with regulations like GDPR or HIPAA.

4. **Insider Threat Detection**:
   Analyze user behaviors across multiple systems to identify potential insider threats or compromised accounts.

5. **IoT Device Monitoring**:
   Deploy lightweight agents on IoT gateways to monitor and protect large-scale IoT deployments.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/kashimkyari/distributed-ids.git
   cd distributed-ids
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up RabbitMQ:
   ```
   sudo apt-get install rabbitmq-server
   sudo systemctl enable rabbitmq-server
   sudo systemctl start rabbitmq-server
   ```

4. Configure `server_config.yaml` and `agent_config.yaml` files.

## Usage

1. Start the central server:
   ```
   python central_server.py
   ```

2. Deploy and start agents on target machines:
   ```
   python agent.py
   ```

## Configuration

- `server_config.yaml`: Define central server settings (host, port, message queue URL).
- `agent_config.yaml`: Specify agent settings (ID, log file path, central server address).

## Extending the System

- Implement custom analysis algorithms in `central_server.py`.
- Add new pattern matching rules in `agent.py`.
- Integrate with SIEM tools for advanced correlation and visualization.

## Testing

Run the test suite:
```
python -m unittest discover tests
```

## Contributing

Contributions are welcome. Please submit pull requests for any enhancements, bug fixes, or documentation improvements.

