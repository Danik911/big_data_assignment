

# SmartX/Azure diagram

## Overview
This project is designed as a part of Big Data management assignmet.

## Architecture Diagram
![Architecture Diagram](https://github.com/Danik911/big_data_assignment/blob/main/IoT_diagram.drawio.svg)

# Azure IoT Data Architecture Components

This document outlines the components of our Azure-based IoT data architecture, detailing the secure flow of data from IoT devices through processing layers to end-user applications.

## Architecture Components

### Edge Layer

**Device Communication & Security**
- **Secure IoT Communication**: IoT devices (EyeCon2, TempSensors, HumidiProbes) transmit raw data to the Edge Layer using TLS 1.3, ensuring data integrity and confidentiality.
- **Azure Sphere Security**: Validates device connections with secure authentication and encryption to prevent unauthorized access and tampering.
- **Local Anomaly Detection**: Edge modules analyze preprocessed data in real-time, filtering irrelevant information to reduce bandwidth usage.
- **Edge-to-Ingestion Pipeline**: Processed data is sent to IoT Hub for centralized ingestion of critical insights and telemetry.
- **Device Provisioning**: Device Provisioning Service securely onboards and configures IoT devices for seamless IoT Hub communication.

### Ingestion Layer

**Data Routing & Processing**
- **Batch Ingestion**: Non-urgent data is transferred to Azure Data Factory for Cold Path storage and transformation.
- **Data Gateway Routing**: Determines whether data follows the Hot Path (real-time processing) or Cold Path (batch storage).
- **Real-Time Event Hubs**: High-priority, time-sensitive data is streamed to Event Hubs for immediate Hot Path processing.

### Processing Layer

**Hot Path (Real-Time)**
- **Real-Time Analytics**: Event Hubs forward data streams to Apache Flink and HDInsight Spark for low-latency analysis and anomaly detection.

**Cold Path (Batch)**
- **Tiered Storage**: Batch data is organized in Azure Data Lake Storage Gen2 with Bronze (raw), Silver (standardized), and Gold (curated) tiers.
- **Databricks Processing**: Handles data transformations, batch processing, and machine learning workflows for advanced analytics.
- **Model Deployment**: Trained AI models are deployed back to Edge devices for local processing.
- **Synapse Analytics**: Provides advanced querying capabilities for refined data from Delta Lake, supporting compliance and reporting.

### Serve Layer

**Data Delivery & Protection**
- **Real-Time Insights**: Hot Path analytics are delivered to dashboards, mobile apps, and APIs for immediate use.
- **Strategic Insights**: Refined Cold Path data provides strategic insights, compliance reports, and long-term visualization.
- **Firewall Protection**: Azure Firewall filters traffic to/from the Serve Layer, protecting systems from unauthorized access.
- **DDoS Protection**: Application Gateway applies DDoS protection and security layers against malicious traffic.

### Governance Layer

**Monitoring & Compliance**
- **Governance Framework**: Monitor and Govern Layer (Purview, Monitor, Key Vault) tracks data lineage, performance, and ensures regulatory compliance.
- **Compliance Tracking**: Metadata, logs, and lineage information from Delta Lake tiers support auditing and compliance requirements.

## Security Features

The architecture implements multiple security layers including TLS 1.3 encryption, Azure Sphere device security, Azure Firewall, and DDoS protection via Application Gateway, ensuring end-to-end data protection.

