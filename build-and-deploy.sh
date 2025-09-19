#!/bin/bash

# Build and Deploy Script for Green Next Shopping Agent (ADK Web)
# Usage: ./build-and-deploy.sh [PROJECT_ID] [REGION] [CLUSTER_NAME] [GEMINI_API_KEY]

set -e

# Configuration
PROJECT_ID=${1:-"your-gcp-project-id"}
REGION=${2:-"us-central1"}
CLUSTER_NAME=${3:-"microservices-demo"}
GEMINI_API_KEY=${4:-""}
IMAGE_NAME="green-next-shopping-agent"
IMAGE_TAG="latest"
SERVICE_NAME="green-next-shopping-agent"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting build and deployment for Green Next Shopping Agent (ADK Web)${NC}"

# Function to print colored output
print_step() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if required tools are installed
check_tools() {
    print_step "Checking required tools..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        exit 1
    fi
    
    if ! command -v gcloud &> /dev/null; then
        print_error "Google Cloud SDK is not installed"
        exit 1
    fi
    
    if ! command -v kubectl &> /dev/null; then
        print_error "kubectl is not installed"
        exit 1
    fi
    
    print_step "All required tools are available"
}

# Set up Google Cloud authentication
setup_gcloud() {
    print_step "Setting up Google Cloud configuration..."
    
    gcloud config set project $PROJECT_ID
    gcloud auth configure-docker
    
    print_step "Google Cloud configuration completed"
}

# Build Docker image
build_image() {
    print_step "Building Docker image for ADK Web..."
    
    # Get git commit hash for tagging
    GIT_COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo "latest")
    
    # Build with multi-platform support and build args for optimization
    docker build \
        --platform linux/amd64 \
        --build-arg BUILDKIT_INLINE_CACHE=1 \
        --tag gcr.io/$PROJECT_ID/$IMAGE_NAME:$IMAGE_TAG \
        --tag gcr.io/$PROJECT_ID/$IMAGE_NAME:$GIT_COMMIT \
        .
    
    print_step "Docker image built successfully"
}

# Push image to Google Container Registry
push_image() {
    print_step "Pushing image to Google Container Registry..."
    
    docker push gcr.io/$PROJECT_ID/$IMAGE_NAME:$IMAGE_TAG
    docker push gcr.io/$PROJECT_ID/$IMAGE_NAME:$(git rev-parse --short HEAD 2>/dev/null || echo "latest")
    
    print_step "Image pushed to GCR successfully"
}

# Connect to GKE cluster
connect_cluster() {
    print_step "Connecting to GKE cluster..."
    
    gcloud container clusters get-credentials $CLUSTER_NAME --region $REGION --project $PROJECT_ID
    
    print_step "Connected to GKE cluster: $CLUSTER_NAME"
}

# Create or update secrets
setup_secrets() {
    print_step "Setting up Kubernetes secrets..."
    
    if [ -z "$GEMINI_API_KEY" ]; then
        print_warning "GEMINI_API_KEY not provided. Please create the secret manually:"
        echo "kubectl create secret generic gemini-api-secret --from-literal=api-key=\"YOUR_ACTUAL_API_KEY\""
    else
        # Delete existing secret if it exists
        kubectl delete secret gemini-api-secret --ignore-not-found=true
        
        # Create new secret
        kubectl create secret generic gemini-api-secret --from-literal=api-key="$GEMINI_API_KEY"
        print_step "Gemini API secret created successfully"
    fi
}

# Update Kubernetes deployment
update_deployment() {
    print_step "Updating Kubernetes deployment..."
    
    # Create a temporary deployment file with replaced values
    cp deployment.yml deployment-temp.yml
    sed -i.bak "s/YOUR_PROJECT_ID/$PROJECT_ID/g" deployment-temp.yml
    
    # Apply the deployment
    kubectl apply -f deployment-temp.yml
    
    # Wait for rollout to complete
    kubectl rollout status deployment/$SERVICE_NAME --timeout=600s
    
    # Clean up temporary file
    rm deployment-temp.yml deployment-temp.yml.bak 2>/dev/null || true
    
    print_step "Deployment updated successfully"
}

# Verify deployment and get external IP
verify_deployment() {
    print_step "Verifying deployment..."
    
    # Check pod status
    kubectl get pods -l app=$SERVICE_NAME
    
    # Check service status
    kubectl get service $SERVICE_NAME
    
    # Wait for LoadBalancer IP assignment
    print_step "Waiting for LoadBalancer IP assignment..."
    SERVICE_IP=""
    for i in {1..30}; do
        SERVICE_IP=$(kubectl get service $SERVICE_NAME -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "")
        if [ -n "$SERVICE_IP" ] && [ "$SERVICE_IP" != "null" ]; then
            break
        fi
        echo "Waiting for LoadBalancer IP... (attempt $i/30)"
        sleep 10
    done
    
    if [ -n "$SERVICE_IP" ] && [ "$SERVICE_IP" != "null" ]; then
        echo -e "${GREEN}🌐 Green Next Shopping Agent is available at:${NC}"
        echo -e "${BLUE}   HTTP:  http://$SERVICE_IP${NC}"
        echo -e "${BLUE}   HTTPS: https://$SERVICE_IP${NC}"
        echo -e "${GREEN}🎯 ADK Web Interface: http://$SERVICE_IP${NC}"
    else
        print_warning "LoadBalancer IP not yet assigned. Check status with:"
        echo "kubectl get service $SERVICE_NAME -w"
    fi
    
    # Show additional information
    echo -e "\n${BLUE}Additional Information:${NC}"
    echo "  Project ID: $PROJECT_ID"
    echo "  Cluster: $CLUSTER_NAME ($REGION)"
    echo "  Image: gcr.io/$PROJECT_ID/$IMAGE_NAME:$IMAGE_TAG"
    echo "  Replicas: $(kubectl get deployment $SERVICE_NAME -o jsonpath='{.status.readyReplicas}')/$(kubectl get deployment $SERVICE_NAME -o jsonpath='{.spec.replicas}')"
    
    print_step "Deployment verification completed"
}

# Check microservices connectivity
check_microservices() {
    print_step "Checking microservices connectivity..."
    
    SERVICES=("productcatalogservice:3550" "cartservice:7070" "checkoutservice:5050" "paymentservice:50051" "frontend:80")
    
    for service in "${SERVICES[@]}"; do
        if kubectl get service ${service%:*} &> /dev/null; then
            echo -e "${GREEN}✓${NC} ${service%:*} service found"
        else
            print_warning "${service%:*} service not found - please ensure it's deployed"
        fi
    done
}

# Show logs
show_logs() {
    print_step "Recent application logs:"
    kubectl logs -l app=$SERVICE_NAME --tail=20 --since=60s || true
}

# Cleanup function
cleanup() {
    print_step "Cleaning up temporary files..."
    rm -f deployment-temp.yml deployment-temp.yml.bak
}

# Main execution
main() {
    echo -e "${BLUE}Configuration:${NC}"
    echo "  Project ID: $PROJECT_ID"
    echo "  Region: $REGION"
    echo "  Cluster: $CLUSTER_NAME"
    echo "  Image: gcr.io/$PROJECT_ID/$IMAGE_NAME:$IMAGE_TAG"
    echo "  Gemini API Key: $([ -n "$GEMINI_API_KEY" ] && echo "Provided" || echo "Not provided")"
    echo ""
    
    # Ask for confirmation
    read -p "Do you want to proceed with deployment? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Deployment cancelled."
        exit 0
    fi
    
    # Set trap for cleanup on exit
    trap cleanup EXIT
    
    # Execute deployment steps
    check_tools
    setup_gcloud
    build_image
    push_image
    connect_cluster
    setup_secrets
    check_microservices
    update_deployment
    verify_deployment
    show_logs
    
    echo -e "\n${GREEN}🎉 Green Next Shopping Agent deployment completed successfully!${NC}"
    echo -e "${YELLOW}💡 The ADK Web interface should be accessible via the LoadBalancer IP above${NC}"
}

# Help function
show_help() {
    echo "Usage: $0 [PROJECT_ID] [REGION] [CLUSTER_NAME] [GEMINI_API_KEY]"
    echo ""
    echo "Arguments:"
    echo "  PROJECT_ID      : Google Cloud Project ID"
    echo "  REGION          : GKE cluster region (default: us-central1)"
    echo "  CLUSTER_NAME    : GKE cluster name (default: microservices-demo)"
    echo "  GEMINI_API_KEY  : Gemini API key for the agent (optional)"
    echo ""
    echo "Examples:"
    echo "  $0 my-project us-west1 my-cluster \"your-api-key\""
    echo "  $0 my-project                    # Use defaults for region and cluster"
    echo ""
    echo "Prerequisites:"
    echo "  - Docker installed and running"
    echo "  - Google Cloud SDK installed and authenticated"
    echo "  - kubectl installed"
    echo "  - Access to the GKE cluster"
    echo "  - Microservices (productcatalogservice, cartservice, etc.) already deployed"
    echo ""
    echo "The application will be accessible via LoadBalancer as an external service."
}

# Handle script arguments
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    show_help
    exit 0
fi

# Validate required arguments
if [[ -z "$1" ]]; then
    print_error "PROJECT_ID is required"
    show_help
    exit 1
fi

# Run main function
main
