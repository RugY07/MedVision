# Monitoring Guide

## Overview

Monitoring ensures the MedVision platform remains reliable, observable, and scalable.

The monitoring stack consists of:

* Prometheus
* Grafana
* Application Logs
* Supabase Logs

---

# Monitoring Architecture

```text id="3s1zxt"
FastAPI
    │
    ▼
Prometheus
    │
    ▼
Grafana
```

---

# Metrics Collection

## API Metrics

Track:

* Request count
* Request latency
* Error rate
* Active requests

---

## Model Metrics

Track:

* Inference latency
* Model load time
* Prediction volume
* Failed predictions

---

## Infrastructure Metrics

Track:

* CPU usage
* Memory usage
* Disk usage
* Network activity

---

# Health Endpoints

## Server Health

```http id="u7dyuv"
GET /health
```

---

## Model Status

```http id="6z0xhz"
GET /models/status
```

---

# Alerting Rules

## High Error Rate

Trigger when:

```text id="tv9dks"
Error Rate > 5%
```

for more than:

```text id="t9p9is"
5 minutes
```

---

## High Latency

Trigger when:

```text id="4m5izn"
Average latency > 3 seconds
```

---

## Model Failure

Trigger when:

```text id="ghv0v5"
Model unavailable
```

---

## Service Down

Trigger when:

```text id="11r9ml"
Health endpoint unreachable
```

---

# Grafana Dashboards

## API Dashboard

Visualize:

* Requests/minute
* Latency
* Errors

---

## ML Dashboard

Visualize:

* Predictions by scan type
* Confidence distributions
* Inference times

---

## Infrastructure Dashboard

Visualize:

* CPU
* Memory
* Storage
* Uptime

---

# Logging

## FastAPI Logs

Capture:

* Requests
* Errors
* Startup events
* Model loading

---

## Edge Function Logs

Capture:

* Inference requests
* Database writes
* Storage operations

---

## Supabase Logs

Capture:

* Authentication
* Database activity
* Storage activity

---

# Monitoring Checklist

Daily:

* Health checks passing
* Error rate normal

Weekly:

* Review latency trends
* Review infrastructure usage

Monthly:

* Capacity planning
* Model performance review

---

# Success Criteria

Monitoring is successful when:

* Failures detected quickly
* Root causes identifiable
* Historical trends available
* Alerts actionable
