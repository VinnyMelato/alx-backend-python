# Quick Reference Guide - Kubernetes Messaging App Project

## Essential Commands

### Initialize Cluster
```bash
bash kurbeScript
```

### Deploy & Scale
```bash
# Deploy initial app
kubectl apply -f deployment.yaml

# Scale to 3 replicas
bash kubctl-0x01

# Check status
kubectl get pods -n messaging-app -o wide
kubectl get svc -n messaging-app
```

### Setup Ingress
```bash
# Install Nginx Ingress Controller
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx --create-namespace

# Apply Ingress configuration
kubectl apply -f ingress.yaml
```

### Blue-Green Deployment
```bash
# Deploy both versions
bash kubctl-0x02

# Switch traffic to Green
kubectl patch svc django-service -n messaging-app \
  -p '{"spec":{"selector":{"deployment-type":"green"}}}'

# Switch back to Blue
kubectl patch svc django-service -n messaging-app \
  -p '{"spec":{"selector":{"deployment-type":"blue"}}}'
```

### Rolling Updates
```bash
# Update blue_deployment.yaml image to v2.0
# Then run:
bash kubctl-0x03
```

## File Reference

| File | Purpose |
|------|---------|
| `kurbeScript` | Start and verify Minikube cluster |
| `deployment.yaml` | Initial Django deployment (v1.0) |
| `kubctl-0x01` | Scale to 3 replicas + load test |
| `ingress.yaml` | Nginx Ingress configuration |
| `commands.txt` | Ingress controller installation steps |
| `blue_deployment.yaml` | Blue deployment (v2.0) |
| `green_deployment.yaml` | Green deployment (v1.0) |
| `kubeservice.yaml` | Service definitions |
| `kubctl-0x02` | Blue-green deployment manager |
| `kubctl-0x03` | Rolling update with availability test |

## Monitor & Debug

```bash
# View pods
kubectl get pods -n messaging-app -o wide

# View pod logs
kubectl logs -n messaging-app -l app=django-messaging-app -f

# Port forward to service
kubectl port-forward svc/django-service 8000:8000 -n messaging-app

# Check resource usage
kubectl top pods -n messaging-app

# View deployment rollout history
kubectl rollout history deployment/django-app-blue -n messaging-app

# Rollback to previous version
kubectl rollout undo deployment/django-app-blue -n messaging-app
```

## Traffic Management

```bash
# Test Blue service
kubectl port-forward -n messaging-app svc/django-service-blue 8001:8000
curl http://localhost:8001

# Test Green service
kubectl port-forward -n messaging-app svc/django-service-green 8002:8000
curl http://localhost:8002

# Check current routing
kubectl get svc django-service -n messaging-app -o jsonpath='{.spec.selector}'
```

## Cleanup

```bash
# Delete all messaging app resources
kubectl delete namespace messaging-app

# Stop Minikube
minikube stop

# Delete Minikube cluster
minikube delete
```

---

For detailed documentation, see `README.md`
For submission details, see `SUBMISSION.md`
