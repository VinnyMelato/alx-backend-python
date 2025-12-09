# Django Messaging App - Kubernetes Orchestration Project

## Project Overview

This project demonstrates container orchestration using Kubernetes (K8s) to manage, scale, and deploy a Django messaging application. It covers essential Kubernetes concepts including deployments, services, scaling, ingress, blue-green deployments, and rolling updates.

## Learning Objectives

By completing this project, you will understand:
- Core Kubernetes concepts (Pods, Nodes, Services, Deployments)
- Containerized application deployment on Kubernetes
- Scaling applications using replicas
- Traffic routing and load balancing
- Blue-green deployment strategy for zero-downtime updates
- Rolling updates with monitoring and testing
- Best practices for production-grade Kubernetes deployments

## Project Structure

```
messaging_app/
├── kurbeScript              # Cluster setup and verification script
├── deployment.yaml          # Initial Django app deployment configuration
├── kubctl-0x01             # Scaling and load testing script
├── ingress.yaml            # Nginx ingress configuration
├── commands.txt            # Ingress controller installation commands
├── blue_deployment.yaml    # Blue deployment (production v2.0)
├── green_deployment.yaml   # Green deployment (staging v1.0)
├── kubeservice.yaml        # Service definitions for blue-green switching
├── kubctl-0x02             # Blue-green deployment management script
├── kubctl-0x03             # Rolling update script with downtime testing
└── README.md              # This file
```

## Prerequisites

- **Minikube**: Local Kubernetes cluster (`minikube start`)
- **kubectl**: Kubernetes command-line tool (v1.24+)
- **Docker**: Container runtime (required by Minikube)
- **wrk**: HTTP load testing tool (optional, for performance testing)
- **curl**: HTTP client for testing endpoints
- **Helm** (optional): For easier Ingress controller installation
- **jq** (optional): For JSON parsing in scripts

### Installation Instructions

#### Windows

```powershell
# Install Minikube
choco install minikube

# Install kubectl
choco install kubernetes-cli

# Install Docker Desktop (includes Docker daemon)
# Download from: https://www.docker.com/products/docker-desktop

# Start Minikube with Docker driver
minikube start --driver=docker

# Verify installation
kubectl cluster-info
```

#### Linux/Mac

```bash
# Install Minikube
brew install minikube

# Install kubectl
brew install kubectl

# Install Docker
brew install --cask docker

# Start Minikube
minikube start --driver=docker

# Verify
kubectl cluster-info
```

## Task Breakdown

### Task 0: Kubernetes Cluster Setup

**File**: `kurbeScript`

Sets up and verifies a local Kubernetes cluster.

**How to run**:
```bash
bash kurbeScript
```

**What it does**:
- Checks Minikube and kubectl installation
- Starts Minikube cluster
- Verifies cluster status with `kubectl cluster-info`
- Displays available nodes and pods
- Shows cluster component status

---

### Task 1: Deploy Django App on Kubernetes

**Files**: `deployment.yaml`

Defines the Kubernetes deployment for the Django messaging application.

**Key components**:
- **Namespace**: `messaging-app` (logical isolation)
- **Deployment**: `django-app` with 1 initial replica
- **Image**: `django-messaging-app:1.0`
- **Service**: `django-service` (ClusterIP type for internal access)
- **ConfigMap**: Stores environment variables and configuration
- **Health Checks**: Liveness and readiness probes for automatic recovery
- **Resource Limits**: CPU and memory constraints to prevent resource starvation

**How to deploy**:
```bash
kubectl apply -f deployment.yaml
```

**Verify deployment**:
```bash
# Check pods
kubectl get pods -n messaging-app

# Check services
kubectl get svc -n messaging-app

# View logs
kubectl logs -n messaging-app -l app=django-messaging-app -f
```

---

### Task 2: Scale the Django App

**File**: `kubctl-0x01`

Demonstrates Kubernetes scaling capabilities and load testing.

**How to run**:
```bash
bash kubctl-0x01
```

**What it does**:
1. Scales deployment to 3 replicas
2. Verifies pods are running with `kubectl get pods`
3. Performs HTTP load testing using `wrk` (if installed)
4. Monitors resource usage with `kubectl top`
5. Sets up port forwarding for local testing

**Manual scaling**:
```bash
# Scale to 3 replicas
kubectl scale deployment django-app --replicas=3 -n messaging-app

# Scale down
kubectl scale deployment django-app --replicas=1 -n messaging-app

# Check replicas
kubectl get deployment django-app -n messaging-app
```

---

### Task 3: Kubernetes Ingress for External Access

**Files**: `ingress.yaml`, `commands.txt`

Exposes the Django app to external traffic using Nginx Ingress controller.

**Step-by-step setup**:

1. **Install Nginx Ingress Controller**:
   ```bash
   helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
   helm repo update
   helm install ingress-nginx ingress-nginx/ingress-nginx \
     --namespace ingress-nginx --create-namespace
   ```

2. **Apply Ingress Configuration**:
   ```bash
   kubectl apply -f ingress.yaml
   ```

3. **Verify Ingress**:
   ```bash
   kubectl get ingress -n messaging-app
   kubectl describe ingress django-ingress -n messaging-app
   ```

4. **Access the app**:
   ```bash
   # Get Minikube IP
   MINIKUBE_IP=$(minikube ip)
   
   # Port forward (alternative)
   kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 8080:80
   
   # Then access: http://localhost:8080
   ```

**Ingress paths configured**:
- `/` - Main application
- `/api/messages/` - API endpoint
- `/api/users/` - User API endpoint

---

### Task 4: Blue-Green Deployment Strategy

**Files**: `blue_deployment.yaml`, `green_deployment.yaml`, `kubeservice.yaml`, `kubctl-0x02`

Implements zero-downtime deployments using blue-green strategy.

**How to run**:
```bash
bash kubctl-0x02
```

**What it does**:
1. Deploys services for routing traffic
2. Deploys blue version (current production)
3. Deploys green version (new version)
4. Checks for errors in green deployment
5. Provides traffic switching instructions

**Architecture**:
- **Blue (django-app-blue)**: Current production (v1.0)
- **Green (django-app-green)**: New version ready for testing (v1.0)
- **Main Service**: Routes to currently active version
- **Individual Services**: Allow testing each version independently

**Traffic switching**:
```bash
# Switch to Green
kubectl patch svc django-service -n messaging-app -p '{"spec":{"selector":{"deployment-type":"green"}}}'

# Switch back to Blue
kubectl patch svc django-service -n messaging-app -p '{"spec":{"selector":{"deployment-type":"blue"}}}'

# Check current routing
kubectl get svc django-service -n messaging-app -o jsonpath='{.spec.selector}' | jq .
```

**Testing individual versions**:
```bash
# Test Blue
kubectl port-forward -n messaging-app svc/django-service-blue 8001:8000 &
curl http://localhost:8001

# Test Green
kubectl port-forward -n messaging-app svc/django-service-green 8002:8000 &
curl http://localhost:8002
```

---

### Task 5: Rolling Updates

**Files**: `blue_deployment.yaml` (updated to v2.0), `kubctl-0x03`

Demonstrates zero-downtime rolling updates with continuous availability testing.

**Key changes**:
- Docker image updated from `django-messaging-app:1.0` to `django-messaging-app:2.0`
- DEPLOYMENT_VERSION updated to `blue-2.0`
- Rolling update strategy: 1 surge, 0 unavailable

**How to run**:
```bash
bash kubctl-0x03
```

**What it does**:
1. Shows current deployment status
2. Applies updated deployment (v2.0)
3. Monitors rolling update with `kubectl rollout status`
4. Performs 120-second load test with continuous curl requests
5. Measures availability during update
6. Verifies all pods are updated
7. Displays rollback instructions

**Manual rolling update**:
```bash
# Apply update
kubectl apply -f blue_deployment.yaml

# Monitor progress
kubectl rollout status deployment/django-app-blue -n messaging-app

# Check history
kubectl rollout history deployment/django-app-blue -n messaging-app

# Rollback if needed
kubectl rollout undo deployment/django-app-blue -n messaging-app
```

---

## Best Practices Implemented

### 1. **Declarative Configuration**
- All resources defined in YAML for version control
- Enables reproducible deployments

### 2. **Namespace Isolation**
- Uses `messaging-app` namespace to isolate resources
- Supports multi-environment setups (dev, staging, prod)

### 3. **Health Checks**
- **Liveness Probe**: Detects and restarts failing containers
- **Readiness Probe**: Ensures traffic only goes to ready pods
- Automatic recovery without manual intervention

### 4. **Resource Management**
- CPU requests: 100m, limits: 500m
- Memory requests: 128Mi, limits: 512Mi
- Prevents resource starvation and ensures fair scheduling

### 5. **ConfigMaps**
- Separates configuration from container image
- Easy environment-specific customization

### 6. **Service Abstraction**
- Multiple service types for different use cases
- ClusterIP for internal communication
- NodePort for external access (Ingress)

### 7. **Rolling Update Strategy**
- `maxSurge: 1`: One extra pod during update
- `maxUnavailable: 0`: Zero downtime guarantee
- Automatic rollback on failure

### 8. **Blue-Green Deployments**
- Run both versions simultaneously
- Instant traffic switching
- Easy rollback to previous version

### 9. **Monitoring and Logging**
- Pod disruption budgets prevent accidental outages
- Resource monitoring via `kubectl top`
- Log aggregation with `kubectl logs`

### 10. **Security Considerations**
- ImagePullPolicy set appropriately
- No hardcoded secrets (use Secrets instead of ConfigMaps for sensitive data)
- RBAC can be added for fine-grained access control

---

## Common Commands Reference

### Cluster Management
```bash
# Start cluster
minikube start --driver=docker

# Stop cluster
minikube stop

# Delete cluster
minikube delete

# Get cluster info
kubectl cluster-info

# View nodes
kubectl get nodes -o wide
```

### Deployments
```bash
# List deployments
kubectl get deployments -n messaging-app

# Describe deployment
kubectl describe deployment django-app-blue -n messaging-app

# Edit deployment
kubectl edit deployment django-app-blue -n messaging-app

# Delete deployment
kubectl delete deployment django-app-blue -n messaging-app
```

### Pods
```bash
# List pods
kubectl get pods -n messaging-app -o wide

# View pod details
kubectl describe pod <pod-name> -n messaging-app

# View pod logs
kubectl logs <pod-name> -n messaging-app

# Stream logs
kubectl logs -f <pod-name> -n messaging-app

# Execute command in pod
kubectl exec -it <pod-name> -n messaging-app -- /bin/bash
```

### Services & Network
```bash
# List services
kubectl get svc -n messaging-app

# Port forward
kubectl port-forward svc/django-service 8000:8000 -n messaging-app

# Get service endpoints
kubectl get endpoints django-service -n messaging-app

# Check ingress
kubectl get ingress -n messaging-app
```

### Scaling & Updates
```bash
# Scale deployment
kubectl scale deployment django-app-blue --replicas=5 -n messaging-app

# Check rollout status
kubectl rollout status deployment/django-app-blue -n messaging-app

# View rollout history
kubectl rollout history deployment/django-app-blue -n messaging-app

# Undo rollout
kubectl rollout undo deployment/django-app-blue -n messaging-app

# Pause/Resume rollout
kubectl rollout pause deployment/django-app-blue -n messaging-app
kubectl rollout resume deployment/django-app-blue -n messaging-app
```

### Resources & Monitoring
```bash
# View resource usage
kubectl top nodes
kubectl top pods -n messaging-app

# Get resource requests/limits
kubectl describe node <node-name>

# Check events
kubectl get events -n messaging-app

# View resource definitions
kubectl api-resources
```

---

## Troubleshooting

### Issue: Pods stuck in Pending

```bash
# Check pod events
kubectl describe pod <pod-name> -n messaging-app

# Check node resources
kubectl top nodes
kubectl describe node

# Increase node resources (Minikube)
minikube start --cpus=4 --memory=8192
```

### Issue: Image pull errors

```bash
# Ensure image exists locally or in registry
docker images | grep django-messaging-app

# Set imagePullPolicy to IfNotPresent for local images
# Already configured in deployment files
```

### Issue: Service not accessible

```bash
# Check service exists
kubectl get svc -n messaging-app

# Check service endpoints
kubectl get endpoints django-service -n messaging-app

# Port forward for testing
kubectl port-forward svc/django-service 8000:8000 -n messaging-app
```

### Issue: Rolling update stuck

```bash
# Check rollout status
kubectl rollout status deployment/django-app-blue -n messaging-app

# Check pod events
kubectl describe pod <pod-name> -n messaging-app

# Force rollback
kubectl rollout undo deployment/django-app-blue -n messaging-app
```

---

## Project Assessment Checklist

### Files Submitted
- [x] `kurbeScript` - Cluster setup script
- [x] `deployment.yaml` - Initial deployment
- [x] `kubctl-0x01` - Scaling script
- [x] `ingress.yaml` - Ingress configuration
- [x] `commands.txt` - Ingress installation commands
- [x] `blue_deployment.yaml` - Blue deployment (v2.0)
- [x] `green_deployment.yaml` - Green deployment
- [x] `kubeservice.yaml` - Service definitions
- [x] `kubctl-0x02` - Blue-green script
- [x] `kubctl-0x03` - Rolling update script

### Features Implemented
- [x] Kubernetes cluster setup and verification
- [x] Django app deployment with ConfigMaps and health checks
- [x] Horizontal pod autoscaling to 3 replicas
- [x] Load testing with resource monitoring
- [x] Nginx Ingress controller setup
- [x] Routing configuration for multiple paths
- [x] Blue-green deployment strategy
- [x] Traffic switching mechanism
- [x] Rolling updates with zero-downtime deployment
- [x] Continuous availability testing during updates
- [x] Complete documentation and usage examples

---

## Next Steps

1. **Build Docker Image**: Create a Dockerfile for your Django app
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
   ```

2. **Build and Push Image**:
   ```bash
   docker build -t django-messaging-app:1.0 .
   docker build -t django-messaging-app:2.0 .
   # Push to registry if using one
   ```

3. **Implement Health Endpoints**: Create `/health/` and `/ready/` endpoints in Django
   ```python
   # urls.py
   path('health/', health_check_view),
   path('ready/', readiness_check_view),
   ```

4. **Add Persistent Storage**: Implement PersistentVolumes for database
   ```yaml
   apiVersion: v1
   kind: PersistentVolumeClaim
   metadata:
     name: django-pvc
   spec:
     accessModes: [ReadWriteOnce]
     resources:
       requests:
         storage: 1Gi
   ```

5. **Implement Auto-scaling**: Configure Horizontal Pod Autoscaler
   ```bash
   kubectl autoscale deployment django-app-blue --min=1 --max=10 -n messaging-app
   ```

6. **Add Monitoring**: Integrate Prometheus and Grafana for observability

---

## Resources

- [Kubernetes Official Documentation](https://kubernetes.io/docs/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/best-practices/)
- [Minikube Documentation](https://minikube.sigs.k8s.io/)
- [Nginx Ingress Controller](https://kubernetes.github.io/ingress-nginx/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)

---

**Project Repository**: `alx-backend-python`  
**Project Directory**: `messaging_app`  
**Created**: December 9, 2025
