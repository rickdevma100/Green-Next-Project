# Green Next Shopping Agent - Deployment Guide

A comprehensive guide to deploy the Green Next Shopping Agent as an external LoadBalancer service on Google Kubernetes Engine (GKE).

## 🚀 Quick Start

```bash
# 1. Clone and navigate to the project
cd Green-Next-Project

# 2. Set your configuration
export PROJECT_ID="youtube-project-462619"
export GEMINI_API_KEY="AIzaSyCIIoEbK6dHFVAyvEnUtq_LUWXlUJBwF_A"

# 3. Deploy to GKE
./build-and-deploy.sh $PROJECT_ID us-east1 online-boutique $GEMINI_API_KEY

# 4. Access your agent
# The script will display the external IP when ready
```

## 📋 Prerequisites

### Required Tools
- [Docker](https://docs.docker.com/get-docker/) installed and running
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) configured
- [kubectl](https://kubernetes.io/docs/tasks/tools/) installed
- Active GCP account with billing enabled

### GKE Cluster Requirements
- **Existing GKE cluster** with the following microservices already deployed:
  - `productcatalogservice` (port 3550)
  - `cartservice` (port 7070)  
  - `checkoutservice` (port 5050)
  - `paymentservice` (port 50051)
  - `frontend` (port 80)

### API Keys
- **Gemini API Key** for the agent's AI capabilities

## 🏗️ Architecture Overview

```mermaid
graph TB
    Internet[Internet] --> LB[LoadBalancer]
    LB --> AGT[Green Next Agent]
    AGT --> PCS[Product Catalog Service]
    AGT --> CS[Cart Service]
    AGT --> COS[Checkout Service]
    AGT --> PS[Payment Service]
    AGT --> FS[Frontend Service]
```

The Green Next Shopping Agent:
- Runs as an **external LoadBalancer service**
- Provides **ADK web interface** accessible from the internet
- Integrates with your existing microservices architecture
- Auto-scales based on demand (2-10 replicas)

## 📁 Project Structure

```
Green-Next-Project/
├── Dockerfile              # Optimized Python 3.11 slim image
├── deployment.yml           # Kubernetes manifests
├── build-and-deploy.sh     # Automated deployment script
├── .dockerignore           # Docker build optimization
├── requirements.txt        # Python dependencies
├── demo.proto             # Protocol buffer definitions
└── green_next_shopping_agent/
    ├── agent.py           # Main agent definition
    ├── constants.py       # Configuration constants
    └── sub_agents/        # Sub-agent modules
```

## ⚙️ Configuration

### 1. Environment Variables

The deployment automatically configures these environment variables:

```yaml
# Microservice endpoints
PRODUCT_CATALOG_SERVICE: "productcatalogservice:3550"
CART_SERVICE: "cartservice:7070"
CHECKOUT_SERVICE: "checkoutservice:5050"
PAYMENT_SERVICE: "paymentservice:50051"
FRONTEND_SERVICE: "frontend:80"

# ADK Web configuration
ADK_WEB_HOST: "0.0.0.0"
ADK_WEB_PORT: "8080"

# API credentials
GEMINI_API_KEY: "<from-secret>"
```

### 2. Resource Allocation

**Per Pod Resources:**
- **Requests**: 500m CPU, 1Gi memory
- **Limits**: 1000m CPU, 2Gi memory

**Auto-scaling:**
- **Min replicas**: 2
- **Max replicas**: 10
- **CPU threshold**: 70%
- **Memory threshold**: 80%

## 🚢 Deployment Options

### Option 1: Automated Script (Recommended)

```bash
# Full deployment with all parameters
./build-and-deploy.sh PROJECT_ID REGION CLUSTER_NAME GEMINI_API_KEY

# Example
./build-and-deploy.sh my-project-123 us-central1 microservices-demo "your-api-key-here"
```

### Option 2: Manual Deployment

```bash
# 1. Configure gcloud
gcloud config set project $PROJECT_ID
gcloud auth configure-docker

# 2. Build and push image
docker build -t gcr.io/$PROJECT_ID/green-next-shopping-agent:latest .
docker push gcr.io/$PROJECT_ID/green-next-shopping-agent:latest

# 3. Connect to cluster
gcloud container clusters get-credentials $CLUSTER_NAME --region $REGION

# 4. Create secrets
kubectl create secret generic gemini-api-secret --from-literal=api-key="$GEMINI_API_KEY"

# 5. Update deployment manifest
# For Linux/WSL:
sed -i "s/YOUR_PROJECT_ID/$PROJECT_ID/g" deployment.yml
# For macOS:
sed -i '' "s/YOUR_PROJECT_ID/$PROJECT_ID/g" deployment.yml

# 6. Deploy to Kubernetes
kubectl apply -f deployment.yml

# 7. Wait for deployment
kubectl rollout status deployment/green-next-shopping-agent

# 8. Get external IP
kubectl get service green-next-shopping-agent
```

## 🌐 Accessing the Application

### Getting the External IP

```bash
# Check service status
kubectl get service green-next-shopping-agent

# Wait for EXTERNAL-IP assignment
kubectl get service green-next-shopping-agent -w
```

### Service Endpoints

Once deployed, your agent will be available at:

- **HTTP**: `http://<EXTERNAL-IP>`
- **HTTPS**: `https://<EXTERNAL-IP>`
- **ADK Web Interface**: Direct access to agent's web UI

### Load Balancer Features

- **Session Affinity**: ClientIP with 3-hour timeout
- **Health Checks**: TCP socket checks on port 8080
- **SSL Termination**: Automatic HTTPS support
- **Global Access**: Accessible from anywhere

## 📊 Monitoring and Scaling

### Viewing Logs

```bash
# Real-time logs
kubectl logs -f deployment/green-next-shopping-agent

# Recent logs from all pods
kubectl logs -l app=green-next-shopping-agent --tail=50

# Logs from specific pod
kubectl logs <pod-name>
```

### Monitoring Pod Status

```bash
# Check pod status
kubectl get pods -l app=green-next-shopping-agent

# Detailed pod information
kubectl describe pods -l app=green-next-shopping-agent

# Resource usage
kubectl top pods -l app=green-next-shopping-agent
```

### Scaling

```bash
# Manual scaling
kubectl scale deployment green-next-shopping-agent --replicas=5

# Check HPA status
kubectl get hpa green-next-shopping-agent

# HPA details
kubectl describe hpa green-next-shopping-agent
```

## 🔒 Security Features

### Network Security
- **NetworkPolicy**: Restricts pod-to-pod communication
- **Non-root execution**: Containers run as non-root user
- **Resource limits**: Prevents resource exhaustion
- **Secret management**: API keys stored as Kubernetes secrets

### Image Security
- **Optimized base image**: Python 3.11 slim (150MB vs 1GB)
- **Minimal attack surface**: Only required packages installed
- **Security updates**: Latest package versions
- **Health checks**: Kubernetes TCP socket liveness and readiness probes

## 🔧 Troubleshooting

### Common Issues

#### 1. Image Pull Errors

```bash
# Check if image exists
gcloud container images list --repository=gcr.io/$PROJECT_ID

# Verify Docker authentication
gcloud auth configure-docker

# Re-push image if needed
docker push gcr.io/$PROJECT_ID/green-next-shopping-agent:latest
```

#### 2. Pod CrashLoopBackOff

```bash
# Check pod logs for errors
kubectl logs -l app=green-next-shopping-agent

# Check pod events
kubectl get events --sort-by=.metadata.creationTimestamp

# Describe problematic pods
kubectl describe pod <pod-name>
```

#### 3. Service Connection Issues

```bash
# Test internal connectivity
kubectl exec -it <pod-name> -- nslookup productcatalogservice

# Check all service endpoints
kubectl get endpoints

# Verify microservices are running
kubectl get services
```

#### 4. LoadBalancer IP Not Assigned

```bash
# Check service events
kubectl describe service green-next-shopping-agent

# Verify GKE load balancer quotas
gcloud compute project-info describe --format="table(quotas.metric,quotas.limit,quotas.usage)"

# Check firewall rules
gcloud compute firewall-rules list --filter="name~'gke'"
```

#### 5. Health Check Failures

```bash
# Test application endpoint manually
kubectl port-forward service/green-next-shopping-agent 8080:80
curl http://localhost:8080/

# Test TCP connectivity (matches health check)
telnet localhost 8080

# Alternative: Check if process is running inside pod
kubectl exec -it <pod-name> -- ps aux | grep adk

# Check application startup logs
kubectl logs -l app=green-next-shopping-agent --since=10m
```

**Note**: The deployment uses TCP socket health checks instead of HTTP `/health` endpoint since ADK web doesn't provide a built-in health endpoint.

### Performance Issues

#### High Memory Usage

```bash
# Check memory metrics
kubectl top pods -l app=green-next-shopping-agent

# Adjust memory limits in deployment.yml
# Then apply changes
kubectl apply -f deployment.yml
```

#### Slow Response Times

```bash
# Check if HPA is scaling up
kubectl get hpa green-next-shopping-agent

# Manual scale for immediate relief
kubectl scale deployment green-next-shopping-agent --replicas=5

# Check microservice connectivity
kubectl exec -it <pod-name> -- ping productcatalogservice
```

## 🔄 Updates and Maintenance

### Updating the Application

```bash
# 1. Build new image with updated tag
docker build -t gcr.io/$PROJECT_ID/green-next-shopping-agent:v2.0 .
docker push gcr.io/$PROJECT_ID/green-next-shopping-agent:v2.0

# 2. Update deployment
kubectl set image deployment/green-next-shopping-agent \
  green-next-agent=gcr.io/$PROJECT_ID/green-next-shopping-agent:v2.0

# 3. Monitor rollout
kubectl rollout status deployment/green-next-shopping-agent

# 4. Rollback if needed
kubectl rollout undo deployment/green-next-shopping-agent
```

### Backup and Disaster Recovery

```bash
# Backup deployment configuration
kubectl get deployment green-next-shopping-agent -o yaml > backup-deployment.yml

# Backup service configuration
kubectl get service green-next-shopping-agent -o yaml > backup-service.yml

# Backup secrets
kubectl get secret gemini-api-secret -o yaml > backup-secret.yml
```

## 📈 Production Considerations

### High Availability
- Deploy across multiple zones
- Use regional persistent disks for any stateful data
- Implement proper monitoring and alerting

### Performance Optimization
- Use node pools with appropriate machine types
- Enable horizontal pod autoscaling
- Consider vertical pod autoscaling for optimal resource usage

### Security Hardening
- Enable Pod Security Standards
- Use Workload Identity for service-to-service authentication
- Implement network policies for micro-segmentation
- Regular security scanning of container images

### Cost Optimization
- Use preemptible instances for non-critical workloads
- Implement cluster autoscaling
- Monitor resource usage and adjust requests/limits

## 📞 Support

### Getting Help

1. **Check logs first**: `kubectl logs -l app=green-next-shopping-agent`
2. **Verify prerequisites**: Ensure all microservices are running
3. **Test connectivity**: Check network policies and service endpoints
4. **Review resource usage**: Monitor CPU/memory consumption
5. **Check Google Cloud status**: Verify GKE service status

### Useful Commands

```bash
# Complete status check
kubectl get pods,services,deployments,hpa -l app=green-next-shopping-agent

# Detailed troubleshooting
kubectl describe deployment green-next-shopping-agent
kubectl get events --sort-by=.metadata.creationTimestamp

# Resource monitoring
kubectl top nodes
kubectl top pods -A
```

## 📝 Version History

- **v1.0**: Initial deployment with miniconda base image
- **v1.1**: Optimized with Python slim base image (85% size reduction)
- **v1.2**: Added comprehensive monitoring and scaling features

## 🏷️ Tags

`kubernetes` `gke` `google-cloud` `microservices` `adk-web` `python` `grpc` `loadbalancer` `auto-scaling`
