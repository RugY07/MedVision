# 🚀 Vision Weave Med - Complete Deployment Guide

This guide provides step-by-step instructions for deploying the Vision Weave Med medical AI system with trained models for Brain, Cardiac, Chest, and Bone scan analysis.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Dataset Preparation](#dataset-preparation)
4. [Model Training](#model-training)
5. [Model Serving](#model-serving)
6. [Frontend Integration](#frontend-integration)
7. [Production Deployment](#production-deployment)
8. [Monitoring & Maintenance](#monitoring--maintenance)
9. [Troubleshooting](#troubleshooting)

## 🔧 Prerequisites

### Hardware Requirements
- **GPU**: NVIDIA GPU with CUDA support (recommended RTX 3080 or better)
- **RAM**: Minimum 16GB, recommended 32GB+
- **Storage**: 100GB+ free space for datasets and models
- **CPU**: Multi-core processor (8+ cores recommended)

### Software Requirements
- **Python**: 3.9 or higher
- **CUDA**: 11.8 or higher (for GPU training)
- **Docker**: 20.10+ (for containerized deployment)
- **Node.js**: 18+ (for frontend)
- **Git**: Latest version

### Cloud Services (Optional)
- **Supabase**: For database and edge functions
- **AWS/GCP/Azure**: For cloud deployment
- **Wandb**: For experiment tracking
- **MLflow**: For model registry

## 🌍 Environment Setup

### 1. Clone and Setup Repository

```bash
# Clone the repository
git clone <your-repo-url>
cd vision-weave-med-main

# Setup ML infrastructure
cd ml-infrastructure
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
# Copy environment template
cp env.example .env

# Edit environment variables
nano .env
```

**Required Environment Variables:**
```bash
# ML Model Server
ML_MODEL_SERVER_URL=http://localhost:8000

# Supabase (for edge functions)
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key

# AI API Keys (fallback)
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key

# Training (optional)
WANDB_PROJECT=vision-weave-med
WANDB_ENTITY=your_username
```

### 3. Dataset Preparation

```bash
# Create dataset structure
python scripts/setup_datasets.py --create-structure

# Show sample dataset sources
python scripts/setup_datasets.py --show-sources
```

**Dataset Sources (Replace with actual medical datasets):**

| Scan Type | Recommended Datasets | Classes |
|-----------|---------------------|---------|
| **Brain** | BRATS, ADNI, IXI | normal, tumor, stroke, hemorrhage, atrophy |
| **Cardiac** | EchoNet-Dynamic, Cardiac MRI | normal, cardiomyopathy, valvular_disease, coronary_disease, arrhythmia |
| **Chest** | ChestX-ray14, COVID-19 CT, NIH Chest X-rays | normal, pneumonia, covid, tuberculosis, lung_cancer, pneumothorax |
| **Bone** | MURA, Bone X-ray datasets | normal, fracture, osteoporosis, arthritis, tumor |

**Organize your datasets:**
```bash
# Example: Organize brain scan dataset
python scripts/setup_datasets.py \
  --source-dir /path/to/raw/brain/data \
  --target-dir ./data \
  --scan-type brain
```

## 🎯 Model Training

### 1. Quick Start Training

```bash
# Train all models
python train_models.py --config config/config.yaml --scan-type all

# Train specific model
python train_models.py --config config/config.yaml --scan-type brain

# Dry run (validate setup)
python train_models.py --config config/config.yaml --dry-run
```

### 2. Custom Training Configuration

Edit `config/config.yaml`:

```yaml
# Example: Brain scan training config
datasets:
  brain:
    path: "data/brain_scans"
    classes: ["normal", "tumor", "stroke", "hemorrhage", "atrophy"]
    image_size: [224, 224]
    augmentations: true

models:
  architecture: "efficientnet-b4"
  pretrained: true
  num_classes: 5
  dropout: 0.3

training:
  batch_size: 32
  learning_rate: 0.001
  epochs: 100
  patience: 15
```

### 3. Training with Monitoring

```bash
# Enable experiment tracking
export WANDB_PROJECT=vision-weave-med
export WANDB_ENTITY=your-username

# Start MLflow server
mlflow server --host 0.0.0.0 --port 5000 &

# Train with monitoring
python train_models.py --config config/config.yaml --scan-type all
```

### 4. Model Evaluation

After training, check results:
```bash
# View training summary
cat models/training_summary.yaml

# Check model performance
ls models/brain/
# Output: brain_best_model.pth, brain_confusion_matrix.png, brain_test_results.json
```

## 🚀 Model Serving

### 1. Local Model Server

```bash
# Start model server
python -m src.serving.model_server --host 0.0.0.0 --port 8000

# Test server
curl http://localhost:8000/health
curl http://localhost:8000/models/status
```

### 2. Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Check services
docker-compose ps
```

**Services included:**
- ML Model Server (port 8000)
- Redis Cache (port 6379)
- MLflow Tracking (port 5000)
- Prometheus Monitoring (port 9090)
- Grafana Dashboard (port 3000)

### 3. Production Deployment

**Option A: Cloud Deployment (AWS/GCP/Azure)**

```bash
# Build production image
docker build -t vision-weave-med:latest .

# Push to container registry
docker tag vision-weave-med:latest your-registry/vision-weave-med:latest
docker push your-registry/vision-weave-med:latest

# Deploy to cloud (example: AWS ECS)
aws ecs create-service \
  --cluster your-cluster \
  --service-name vision-weave-med \
  --task-definition vision-weave-med:1 \
  --desired-count 2
```

**Option B: Kubernetes Deployment**

```bash
# Create Kubernetes manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

## 🌐 Frontend Integration

### 1. Update Frontend Configuration

```bash
# Update .env in main project
cd ../
echo "REACT_APP_ML_SERVER_URL=http://your-ml-server:8000" >> .env
```

### 2. Deploy Updated Frontend

```bash
# Build frontend
npm run build

# Deploy to your hosting platform
# Example: Vercel
vercel --prod

# Example: Netlify
netlify deploy --prod --dir=dist
```

### 3. Update Supabase Edge Functions

```bash
# Update edge function with ML server URL
cd supabase
supabase functions deploy analyze-medical-scan

# Set environment variable
supabase secrets set ML_MODEL_SERVER_URL=http://your-ml-server:8000
```

## 📊 Monitoring & Maintenance

### 1. Access Monitoring Dashboards

- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **MLflow**: http://localhost:5000

### 2. Key Metrics to Monitor

**Model Performance:**
- Prediction accuracy
- Response time
- Error rates
- Model drift

**System Health:**
- CPU/GPU utilization
- Memory usage
- Disk space
- Network latency

**Business Metrics:**
- Request volume
- User satisfaction
- Cost per prediction

### 3. Automated Monitoring

```bash
# Setup alerts in Prometheus
# Edit monitoring/alerts.yml

# Setup log aggregation
# Example: ELK Stack
docker-compose -f docker-compose.monitoring.yml up -d
```

### 4. Model Updates

```bash
# Retrain models with new data
python train_models.py --config config/config.yaml --scan-type brain

# A/B testing
# Deploy new model alongside existing one
# Gradually shift traffic to new model

# Model rollback
# Revert to previous model version if issues detected
```

## 🔧 Troubleshooting

### Common Issues

**1. Model Loading Errors**
```bash
# Check model files exist
ls -la models/brain/

# Verify model compatibility
python -c "import torch; print(torch.__version__)"
```

**2. CUDA/GPU Issues**
```bash
# Check CUDA availability
python -c "import torch; print(torch.cuda.is_available())"

# Check GPU memory
nvidia-smi
```

**3. Memory Issues**
```bash
# Reduce batch size in config
# Increase swap space
# Use model quantization
```

**4. API Connection Issues**
```bash
# Check ML server status
curl http://localhost:8000/health

# Check firewall settings
# Verify environment variables
```

### Performance Optimization

**1. Model Optimization**
```python
# Use model quantization
model = torch.quantization.quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)

# Use TensorRT for NVIDIA GPUs
# Use ONNX for cross-platform deployment
```

**2. Caching**
```bash
# Enable Redis caching
# Cache preprocessed images
# Cache model predictions
```

**3. Load Balancing**
```bash
# Deploy multiple model server instances
# Use nginx for load balancing
# Implement auto-scaling
```

## 📚 Additional Resources

### Documentation
- [PyTorch Documentation](https://pytorch.org/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Supabase Documentation](https://supabase.com/docs)

### Medical AI Resources
- [MONAI Framework](https://monai.io/)
- [Medical Image Analysis Papers](https://paperswithcode.com/task/medical-image-classification)
- [Medical Datasets](https://www.kaggle.com/search?q=medical+imaging)

### Support
- Create issues in the repository
- Check logs: `tail -f logs/training.log`
- Monitor system resources: `htop`, `nvidia-smi`

## ✅ Deployment Checklist

- [ ] Environment setup complete
- [ ] Datasets organized and validated
- [ ] Models trained and evaluated
- [ ] Model server deployed and tested
- [ ] Frontend updated and deployed
- [ ] Supabase edge functions updated
- [ ] Monitoring setup complete
- [ ] Load testing performed
- [ ] Security review completed
- [ ] Documentation updated
- [ ] Team training completed

---

**🎉 Congratulations!** Your Vision Weave Med medical AI system is now deployed and ready to analyze medical scans with specialized AI models for Brain, Cardiac, Chest, and Bone scans.

For support or questions, please refer to the troubleshooting section or create an issue in the repository.
