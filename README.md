### DevOps Assignment for a Microservices Architecture Deployment

From our discussions at the interview, I gather that there is a drive for On-Premise Deployments.
The following sections will discuss an On-Premise use-case.


---

### **On-Premise Environment with Physical Servers**


### 1. Choose the Infrastructure Platform

For the on-premise environment, I would deploy a **Private Cloud setup** using **Kubernetes** as the core orchestration layer. The following tools will be used as management nodes:

- MAAS (Metal as a Service)
- Ansible
- Harbor
- Git Repository (Bitbucket, GitLab, or Gitea)
- Jenkins

**MAAS (Metal as a Service):**  
I would use MAAS to automate the provisioning of physical servers and os deployment
- Automated server provisioning  
  - Wake-on-LAN  
  - DHCP and PXE booting  
  - OS imaging and deployment  
  - Hardware resource management  
  - Network configuration (VLANs, subnets, IPs)  
  - Remote power control  
  - Monitoring and inventory management  
  - RAID and disk management  
  - REST API access

**Ansible:**  
I would use Ansible to automate configuration management on these servers

**Harbor:**  
Harbor would act as the on-premises container image registry. 

**Git Repository (Bitbucket, GitLab, or Gitea):**  
The Git repository manages version control for application code, infrastructure scripts, and Helm charts.

**Jenkins:**  
Jenkins Pipeline would be used to stitch the various stages of the Infrastructure deployment together, and enable a Single-Click Installation.

**Ubuntu as Linux Distro:**  
I would use the Ubuntu Linux Distro because:
- Widely Supported: Broad community and commercial support.
- LTS Versions: 5 years of security updates with Long Term Support.
- Strong Ecosystem Integration: Excellent compatibility with tools like Docker, Kubernetes, and Ansible.
- Security: Includes built-in security features like AppArmor.
- Ease of Use: Simple package management with APT for easy installation and updates.
- Cloud and Server Optimized: Optimized for cloud platforms and physical servers.

---

### 2. Choose the Orchestration Technology

I would use **Kubernetes** as the Orchestration Technology.
There are a number of On-Premise Kubernetes Distributions to choose from Vanilla K8s, RKE2, OpenShift, Tanzu.

I would choose RKE2 distribution because:

- Simplified deployment and management
- Hardened images  
- Built-in security features  
  - CIS Kubernetes benchmark compliance  
  - SELinux and container runtime security out-of-the-box
- Free

### Additional Components to make Production-Ready Kubernetes Platform

- Longhorn
- Nginx Ingress Controller
- Vault
- CertManager
- Spire
- Istio
- CloudNativePG
- ArgoCD
- KEDA (Kubernetes Event-driven Autoscaler)
- Kube Prometheus Stack
- Elastic Operator
- OpenTelemetry Collector
- Kiali
- Velero
- External Object Storage


**Longhorn:**  
A cloud-native, distributed block storage solution for creating and managing persistent volumes in Kubernetes.
Longhorn creates a default storage class, which has 2 replicas for redundancy and high-availability.

  - **Storage Class for Distributed Applications:**
  For Distributed Applications which already have a built in replication mechanism - postgresql and other databases - I would create a custom storage class, having a single replica with data locality. This would offer a higher IOPS and lower latency performance. Illustration below

    ```
    apiVersion: storage.k8s.io/v1
    kind: StorageClass
    metadata:
      annotations:
        storageclass.kubernetes.io/is-default-class: "false"
      name: longhorn-local
    parameters:
      dataLocality: "strict-local"
      fromBackup: ""
      fsType: ext4
      numberOfReplicas: "1"
      staleReplicaTimeout: "30"
    provisioner: driver.longhorn.io
    reclaimPolicy: Delete
    volumeBindingMode: Immediate
    allowVolumeExpansion: true

    ```

**Nginx Ingress Controller:**  
Exposes microservices to external users securely by managing HTTP and HTTPS traffic.

**Vault:**  
Manages secrets, storing credentials and sensitive data securely. Configured as a Certificate Authority (CA) to issue TLS certificates

**CertManager:**  
Automates the management of TLS certificates for secure communication within the cluster. Integrates with Vault as the Issuer for TLS certificates.

**Spire:**  
Handles identity management and the issuance of SPIFFE IDs for microservices.

**Istio:**  
A service mesh that provides secure and efficient traffic management between microservices.

**CloudNativePG:**  
A PostgreSQL operator for Kubernetes that automates the deployment and management of PostgreSQL databases.

**ArgoCD:**  
A GitOps tool for continuous deployment, enabling declarative management of Kubernetes resources.

**KEDA (Kubernetes Event-driven Autoscaler):**  
Facilitates event-based scaling of microservices based on workload spikes.

**Kube Prometheus Stack:**  
Monitors the Kubernetes cluster with Prometheus and Grafana, ensuring observability and metrics collection.

**Elastic Operator:**  
Deploys and manages an Elasticsearch cluster for log aggregation and analysis.

**OpenTelemetry Collector:**  
Collects distributed traces and metrics for monitoring and observability of microservices.

**Kiali:**  
Visualizes the service mesh topology, traffic, and performance metrics within Istio.

**Velero:**  
Provides backup and recovery capabilities for Kubernetes workloads.

**External Object Storage:**  
This would be external to Kubernetes for storing backup items - databases, etcd, pvc, etc.
MinIO Cluster is a good option for this, in the absence of an existing solution.

---

### 3. Automate Infrastructure Deployment

#### **Infrastructure Automation:**

- **Operating System:**
  - **MAAS:**  
    I would use MAAS to provision the physical servers. With MAAS, I can have
        - Remote Power Control
        - PXE booting and DHCP
        - OS Imaging and Deployment
        - REST API access (which I can call from a build tool like Jenkins)
  - **Cloud-init:**  
    I would leverage Cloud-init for initial server configuration. This would handle network settings and SSH keys on the first boot.
  - **Ansible:**  
    I would use Ansible to automate configuration management tasks across all servers.

- **Kubernetes Deployment (RKE2):**
  - **Ansible Role:**  
    I would deploy Kubernetes (RKE2) using an Ansible Role and Playbook.
    I have provided a sample Ansible Role in the code_snippet section of this repo, here [ansible_snippet](./code_snippets/infrastructure/ansible/)
  - **Dynamic Inventory:**  
    I would creat a Python script for dynamic inventory generation from the MAAS API.

      - Control Plane nodes:
    I would reserve a certain range of IP's from the DHCP pool for the Kubernetes Control Plane nodes
      - Worker nodes
    The rest can be used for the Kubernetes Worker nodes.

    I have provided a sample Python Script for Dynamic Invenotry in the code_snippet section of this repo, here [dynamic_inventory_snippet](./code_snippets/infrastructure/ansible/inventory.py)

- **Additional Kubernetes Deployment Components:**
  - **Helm Charts and Manifests:**  
    I would use Helm charts and manifests to deploy Additional Kubernetes applications, like Longhorn, Nginx Ingress Controller, etc.
    These would be included as Tasks in the Ansible Role.
  - **Harbor:**  
    I would set up Harbor as an On-Premise Container registry, so as to support Air-Gapped and Offline Installations

- **Single Click Installation (Jenkins Pipeline):**
  - **Jenkins Pipeline:**  
    I would create a Jenkins Pipeline to Automate and stitch the various stages of the Infrastructure deployment together, and enable a Single-Click Installation.

    Jenkins would leverage the MAAS cli to connect to the MAAS REST API to remotely trigger MAAS activities.
    - **Jenkins Pipeline Stages:**
      - **MAAS:** Provision servers.
      - **Hardware Test with MAAS cli:** Validate server hardware.
      - **Kubernetes Pre-Deployment Test with Ansible:** Verify pre-requisites for Kubernetes.
      - **Kubernetes Deployment with Ansible:** Execute the Kubernetes setup.
      - **Kubernetes Post-Deployment Test with Ansible:** Confirm the successful deployment of Kubernetes.
      - **Additional Components Deployment with Ansible:** Deploy additional Kubernetes components with Helm charts and Manifests

    I have provided a sample Jenkins Pipeline in the code_snippet section of this repo, here [jenkinsfile](./code_snippets/infrastructure/jenkins/Jenkinsfile)

---

### 4. Automate Microservices Deployment

- **Helm**
- **ArgoCD**


**Helm:**  
I would use **Helm** to package, manage, and deploy Kubernetes applications. 
Helm simplifies deploying complex microservices by templating Kubernetes manifests and enabling consistent version management. 
A sample Helm chart has been provided in the code_snippet section, here [helm_chart](./code_snippets/deployment/helm/app/)

**ArgoCD:**  
For continuous deployment, I would leverage **ArgoCD**. 
It enables GitOps by syncing the Kubernetes cluster with the desired state in a Git repository, automating deployments and ensuring any changes in Git are applied directly to the cluster.
A sample Argo Application has been provided in the code_snippet section, here [argo_application](./code_snippets/deployment/argocd/)

To achieve the requirements of:

- **Fault Tolerant / Highly Available**  
- **Secure**  
- **Autoscaling**  

The following strategies would be implemented:

1. **Fault Tolerant / Highly Available:**  
   - **Replicas** and **podAntiAffinity** ensure redundancy and fault tolerance across node failures.
   - **CloudnativPG PostgreSQL Operator** manages high availability for the PostgreSQL database.

2. **Scaling:**  
   - **HPA** scales microservices based on CPU and Memory utilization.  
   - **KEDA** enables event-driven scaling, and can be configured with a wide range of scalers.

3. **Security:**  
   - **Istio** enforces **mTLS** for secure communication between microservices.  
   - **Spire** provides identity management to secure microservice authentication.

---

### 5. Release Lifecycle for the Different Components

#### **5.1. Development**
- **Purpose:** Write code, build microservices, and run unit tests.
- **Process:** Use Git for version control. CI pipelines (e.g., Jenkins) run automated tests and build microservices. 
- **Outcome:** Container image is ready for Testing phase.

#### **5.2. Testing**
- **Purpose:** Validate functionality, performance, and security.
- **Process:** Deploy to a test Kubernetes environment with ArgoCD. Run automated integration, performance, and security tests.
- **Outcome:** Code passes all tests and is ready for Staging phase.

#### **5.3. Staging**
- **Purpose:** Final validation in a production-like environment.
- **Process:** ArgoCD deploys to staging. Conduct UAT, load testing, and disaster recovery tests. Validate scaling with KEDA and HPA. Test blue-green/canary deployments.
- **Outcome:** Approved release candidate ready for Production phase.

#### **5.4. Production**
- **Purpose:** Deploy services to live environments.
- **Process:** ArgoCD deploys to production. 
- **Outcome:** Services run in production, with rollback options in case of failure.

I have created a gitops folder, with sample values.yml files, showing how gitops might be applied to the dev, test, stg and prod environments, here [gitops](./code_snippets/deployment/gitops/)

---

### 6. Testing Approach for the Infrastructure

#### Infrastructure Test
I focus on three main areas to ensure the infrastructure is reliable and functional:

#### 6.1. Hardware Test with MAAS
I use MAAS to test the physical servers:
- cpu
- memory
- disks

#### 6.2. Kubernetes Pre-Deployment Test with Ansible
Before deploying Kubernetes, I run Ansible playbooks to:
- Validate OS configurations
- Check Network Connectivity
- Check that required Ports are Open

#### 6.3. Kubernetes Post-Deployment Test with Ansible
After deployment, I use Ansible to:
- Check that required Services are Healthy
    - containerd
    - kubelet
    - rke2-server
    - rke2-agent
- Check control plane pods are healthy
- Check overall cluster health 

---

## 7. Monitoring Approach 

I would adopt a wholistic Observability and Monitoring approach for the solution, covering:

- Metrics
- Logs
- Traces

#### 7.1. **Metrics with Prometheus Stack**  
   - **Node metrics**: Monitor CPU, memory, and disk usage to ensure nodes are functioning efficiently.  
   - **Pod metrics**: Track resource usage and health of individual pods to prevent issues like resource starvation.  
   - **Application metrics**: Measure application-specific performance indicators to gauge overall health and performance.

#### 7.2. **Logs with Elastic Stack**  
   - **Node logs**: Collect system logs from nodes to identify hardware or OS-level issues.  
   - **Pod logs**: Capture logs from pods to debug application-level problems and monitor container behavior.  
   - **Application logs**: Analyze application logs for error tracking and performance insights.

#### 7.3. **Traces with OpenTelemetry Collector, Jaegar and Elastic APM**  
   - **Response time**: Measure how long it takes for the application to respond to requests, indicating performance.  
   - **Latency**: Track delays in processing requests to identify performance bottlenecks.  
   - **Error rates**: Monitor the frequency of errors to detect and address issues impacting the application's reliability.

#### 7.4. **Monitoring From Outside Kubernetes using Nagios**  
   - **Node metrics**:  
     - **CPU**: Track CPU usage to detect over-utilization.  
     - **Memory**: Monitor memory usage to avoid memory leaks or overuse.  
     - **Storage**: Ensure there is sufficient disk space to prevent failures.  
   - **Endpoints**: Check the availability and performance of critical endpoints.

#### 7.5. **Alerting**  
   - **Critical alerts**: Set up notifications for critical conditions or thresholds to enable prompt response to issues.

#### 7.6. **List of Monitoring Tools**  
   - **Prometheus stack**: Provides powerful metrics collection and querying capabilities.  
   - **Elastic Stack (Elastic Operator)**: Offers log management and analysis with Elasticsearch, Logstash, and Kibana.  
   - **OpenTelemetry Collector**: Collects and exports telemetry data for observability across various components. 
   - **Elastic APM**: For Application Performance Monitoring 
   - **Jaegar**: For Traces and Application Performance Monitoring.  
   - **Kiali**: Provides visualization and monitoring for service meshes to understand service interactions.  
   - **Nagios**: Monitors infrastructure components from outside Kubernetes, offering comprehensive system checks and alerts.