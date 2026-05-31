#!/bin/bash

# Vision Weave Med - Quick Start Script
# This script sets up the ML infrastructure and trains models

set -e  # Exit on any error

echo "🚀 Vision Weave Med - ML Infrastructure Quick Start"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
# check_python() {
#     print_status "Checking Python installation..."
#     if command -v python3 &> /dev/null; then
#         PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
#         print_success "Python $PYTHON_VERSION found"
#     else
#         print_error "Python 3 is not installed. Please install Python 3.9+ and try again."
#         exit 1
#     fi
# }

# Check if Python is installed (cross-platform)
check_python() {
    print_status "Checking Python installation..."

    # Detect Python command
    if command -v python3 &> /dev/null; then
        PYTHON_CMD=python3
    elif command -v python &> /dev/null; then
        PYTHON_CMD=python
    else
        print_error "Python 3 is not installed. Please install Python 3.9+ and try again."
        exit 1
    fi

    # Get version number
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    print_success "Python $PYTHON_VERSION found"

    # Ensure it's >= 3.9
    MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    if [ "$MAJOR" -lt 3 ] || { [ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 9 ]; }; then
        print_error "Python version must be 3.9 or higher."
        exit 1
    fi

    # Export the correct Python command for later use
    export PYTHON_CMD
}


# Check if CUDA is available
check_cuda() {
    print_status "Checking CUDA availability..."
    if command -v nvidia-smi &> /dev/null; then
        CUDA_VERSION=$(nvidia-smi | grep "CUDA Version" | cut -d' ' -f9)
        print_success "CUDA $CUDA_VERSION found"
        return 0
    else
        print_warning "CUDA not found. Training will use CPU (slower)."
        return 1
    fi
}

# Setup virtual environment
setup_venv() {
    print_status "Setting up virtual environment..."
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_success "Virtual environment created"
    else
        print_status "Virtual environment already exists"
    fi
    
    source venv/bin/activate
    print_success "Virtual environment activated"
}

# Install dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    print_success "Dependencies installed"
}

# Setup dataset structure
setup_datasets() {
    print_status "Setting up dataset structure..."
    python scripts/setup_datasets.py --create-structure
    print_success "Dataset structure created"
    
    print_warning "Please organize your medical datasets in the following structure:"
    echo "data/"
    echo "├── brain/"
    echo "│   ├── train/"
    echo "│   ├── val/"
    echo "│   └── test/"
    echo "├── cardiac/"
    echo "├── chest/"
    echo "└── bone/"
}

# Train models
train_models() {
    print_status "Starting model training..."
    
    # Check if datasets exist
    if [ ! -d "data/brain" ] || [ ! -d "data/cardiac" ] || [ ! -d "data/chest" ] || [ ! -d "data/bone" ]; then
        print_warning "Datasets not found. Showing dataset sources..."
        python scripts/setup_datasets.py --show-sources
        print_error "Please organize your datasets before training models."
        return 1
    fi
    
    # Train models
    python train_models.py --config config/config.yaml --scan-type all
    print_success "Model training completed"
}

# Start model server
start_server() {
    print_status "Starting model server..."
    python -m src.serving.model_server --host 0.0.0.0 --port 8000 &
    SERVER_PID=$!
    print_success "Model server started (PID: $SERVER_PID)"
    
    # Wait for server to start
    sleep 5
    
    # Test server
    if curl -f http://localhost:8000/health &> /dev/null; then
        print_success "Model server is healthy"
    else
        print_error "Model server health check failed"
    fi
}

# Main execution
main() {
    echo
    print_status "Starting Vision Weave Med ML setup..."
    echo
    
    # Check prerequisites
    check_python
    CUDA_AVAILABLE=$(check_cuda && echo "true" || echo "false")
    
    # Setup environment
    setup_venv
    install_dependencies
    
    # Setup datasets
    setup_datasets
    
    # Ask user if they want to train models
    echo
    read -p "Do you have datasets ready and want to train models now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        train_models
        
        # Ask user if they want to start the server
        echo
        read -p "Do you want to start the model server now? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            start_server
            echo
            print_success "🎉 Vision Weave Med ML infrastructure is ready!"
            echo
            print_status "Access points:"
            echo "  • Model Server: http://localhost:8000"
            echo "  • Health Check: http://localhost:8000/health"
            echo "  • API Docs: http://localhost:8000/docs"
            echo
            print_status "Next steps:"
            echo "  1. Update your frontend .env with: REACT_APP_ML_SERVER_URL=http://localhost:8000"
            echo "  2. Update Supabase edge function with ML_MODEL_SERVER_URL"
            echo "  3. Deploy your frontend and test the integration"
            echo
        fi
    else
        print_status "Setup complete. You can train models later with:"
        echo "  python train_models.py --config config/config.yaml --scan-type all"
    fi
    
    echo
    print_success "Setup completed successfully!"
}

# Run main function
main "$@"
