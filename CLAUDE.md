# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Blueking Lite (BKLite) is an AI-first lightweight operations and maintenance platform with a multi-component monorepo architecture. The project consists of frontend applications (web, mobile), backend services (server, metis), AI/ML components (pilot, neco), and data collection agents.

## Repository Structure

- **server/** - Django-based backend API server (Python 3.12+)
- **web/** - Next.js frontend application for desktop
- **mobile/** - Next.js + Tauri mobile/desktop application
- **pilot/** - Rasa-based AI operations assistant
- **metis/** - AI/ML service using Sanic framework
- **neco/** - Shared ML/LLM/DevOps utility library
- **agents/** - Data collection and execution agents
  - **stargazer/** - Multi-cloud resource collector (Python)
  - **nats-executor/** - SSH command executor (Go)
  - **fusion-collector/** - Metrics collection agent
- **docs-website/** - Docusaurus documentation site
- **deploy/** - Docker Compose deployment configurations

## Core Dependencies and Tech Stack

### Server (Django Backend)
- Python 3.12+ with Django 4.2
- Uses `uv` package manager
- PostgreSQL, Redis, MinIO, Celery
- NATS for messaging
- Django REST Framework for APIs

### Web (Next.js Frontend)
- Next.js 14.2 with React 18.2
- TypeScript
- Ant Design UI components
- Uses `pnpm` package manager (enforced via preinstall)
- Storybook for component development

### Mobile
- Next.js 15.5 with React 18.3
- Tauri 2.8 for native wrapper
- Ant Design Mobile components
- Android build support with AAB/APK targets

### Pilot (AI Assistant)
- Rasa framework for conversational AI
- Python 3.10 with virtualenv
- Custom actions, channels, and NLU components

### Metis (AI/ML Service)
- Sanic async web framework
- Neco library for LLM/ML operations
- LangChain, LangGraph for AI workflows
- MLflow for model tracking

### Neco (Shared Library)
- Core ML/LLM utilities
- Optional extras: mlflow, llm, devops, doc_parser, ocr
- Graph database support (FalkorDB)

## Local Development with dev.sh Script

For local development, use the unified `dev.sh` management script. This script handles environment setup, service management, and common development tasks.

### Quick Start
```bash
# Check environment
./dev.sh check

# Install all dependencies
./dev.sh install

# Start infrastructure services (Docker)
./dev.sh start infra

# Initialize database
./dev.sh db init

# Start all services (infra + server + web)
./dev.sh start all

# View status
./dev.sh status
```

### Service Management
```bash
./dev.sh start [all|infra|server|web]    # Start services
./dev.sh stop [all|infra|server|web]     # Stop services
./dev.sh restart [all|infra|server|web]  # Restart services
./dev.sh status                          # View service status
./dev.sh logs [infra|server|web]         # View logs
```

### Database Operations
```bash
./dev.sh db init      # Initialize database and create admin user
./dev.sh db migrate   # Run migrations
./dev.sh db shell     # Open database shell
./dev.sh db reset     # Reset database (WARNING: deletes all data)
```

### Configuration Files
- `docker-compose.dev.yml` - Infrastructure services configuration
- `server/.env.dev` - Server environment template
- `web/.env.local.dev` - Web environment template

**See [DEVELOPMENT.md](DEVELOPMENT.md) for complete local development guide.**

---

## Common Development Commands

### Server Development
```bash
cd server

# Install dependencies
make install              # Install with uv (all groups and extras)

# Database operations
make migrate              # Run migrations and create cache table

# Initialize server (first-time setup)
make server-init          # Initialize resources, create admin user, etc.

# Development server
make dev                  # Run uvicorn on port 8001

# Testing
make test                 # Run pytest

# Background tasks
make celery               # Run Celery worker with beat scheduler
make start-nats           # Start NATS listener

# Django shell
make shell                # Open Django shell_plus

# Collect static files
make collect-static
```

### Web Development
```bash
cd web

# Development server
pnpm dev                  # Next.js dev server (default port 3000)

# Build and production
pnpm build                # Build production bundle
pnpm start                # Start production server
pnpm clean                # Clean .next directory

# Code quality
pnpm lint                 # ESLint
pnpm type-check           # TypeScript type checking

# Component development
pnpm storybook            # Run Storybook on port 6006
pnpm build-storybook      # Build static Storybook

# Docker builds (module-specific)
make build-system-manager  # Build system manager module
make build-console         # Build ops console module
make build-node-manager    # Build node manager module
make build-cmdb            # Build CMDB module
make build-monitor         # Build monitor module
make build-opspilot        # Build OpsPilot module
```

### Mobile Development
```bash
cd mobile

# Development
pnpm dev                  # Next.js dev on port 3001
pnpm dev:tauri            # Tauri development mode

# Build
pnpm build                # Build Next.js app

# Android builds
pnpm build:android        # Build for aarch64
pnpm build:android-debug  # Debug build for aarch64
pnpm build:android-all    # Build for all architectures
pnpm build:aab            # Build Android App Bundle
```

### Pilot Development
```bash
cd pilot

# Training
make train                # Train Rasa model with basic data
make online-train         # Train with online data

# Running
make run                  # Run Rasa server with API enabled
make actions              # Run actions server with auto-reload
make shell                # Interactive shell for testing

# Fine-tuning and visualization
make finetune             # Fine-tune existing model
make visualize            # Visualize conversation flows
```

### Metis Development
```bash
cd metis

# Install dependencies
make install              # Install with uv

# Database and models
make sync-db              # Sync database schema
make download-models      # Download required ML models

# Development server
make dev                  # Run Sanic server on port 18082
```

### Documentation Site
```bash
cd docs-website

# Development
pnpm start                # Docusaurus dev server on port 3001

# Build
pnpm build                # Build static site
pnpm serve                # Serve built site
```

## Architecture Notes

### Multi-Module Frontend Structure
The web frontend is organized by functional modules matching backend apps:
- `src/app/system-manager/` - System management UI
- `src/app/ops-console/` - Operations console
- `src/app/node-manager/` - Node management
- `src/app/cmdb/` - Configuration management database
- `src/app/monitor/` - Monitoring dashboards
- `src/app/opspilot/` - AI operations assistant interface
- `src/app/log/` - Log management
- `src/app/alarm/` - Alert management

Each module can be built independently as a Docker image for deployment.

### Backend Apps Architecture
The Django server uses a modular app structure:
- `apps/core/` - Core functionality, authentication, base models
- `apps/system_mgmt/` - System settings and user management
- `apps/console_mgmt/` - Console operations
- `apps/node_mgmt/` - Node lifecycle management
- `apps/cmdb/` - CMDB models and APIs
- `apps/monitor/` - Metrics collection and monitoring
- `apps/alerts/` - Alert rules and notifications
- `apps/log/` - Log aggregation and search
- `apps/opspilot/` - AI assistant integration
- `apps/mlops/` - ML operations and model management

### NATS Messaging System
- Server publishes events to NATS
- nats-executor (Go) subscribes to SSH execution requests
- stargazer subscribes to cloud resource collection tasks
- Used for asynchronous job execution and inter-service communication

### AI/ML Pipeline
1. **Pilot** handles NLU and intent recognition using Rasa
2. **Metis** processes complex AI tasks using LangChain/LangGraph
3. **Neco** provides shared ML utilities and LLM abstractions
4. Server coordinates AI workflows via REST APIs

### Authentication Flow
- Next.js uses NextAuth.js for authentication
- Server provides token-based API authentication
- Mobile app integrates with same auth backend
- Support for WeChat login integration

## Testing

### Server Tests
```bash
cd server
make test                 # Run all pytest tests
```

### Web Component Tests
```bash
cd web
pnpm storybook            # Visual testing in Storybook
```

## Key Configuration Files

- `server/settings.py` - Django settings entry point
- `server/config/` - Split Django settings
- `server/envs/` - Environment-specific configurations
- `web/.env.example` - Frontend environment variables template
- `metis/.env.example` - Metis service configuration template

## Package Management

- **Server/Pilot/Metis/Neco**: Use `uv` for Python dependency management
- **Web/Mobile/Docs**: Use `pnpm` (enforced via preinstall script)
- **Web enforces pnpm**: The web package.json has a preinstall hook that blocks npm/yarn

## Database Migrations

When modifying Django models:
```bash
cd server
make migrate              # Creates and applies migrations
```

The migrate target runs:
1. `makemigrations` - Generate migration files
2. `migrate` - Apply migrations
3. `createcachetable` - Create Django cache table

## Docker Deployment

The project supports Docker Compose deployment. See `deploy/docker-compose/` for:
- Service definitions in `compose/` directory
- Configuration files in `conf/` directory
- Bootstrap script for initialization

## Husky Git Hooks

Both web and mobile use Husky for pre-commit hooks. The hooks run:
- Type checking
- Linting
- Workspace generation (web only)

## 其他要求
- 中文答复用户
- 交流、修改过程把相关内容分文档记录在“二次开发及部署文档”目录下
- 修改提交到git
- 开发环境使用名为bklite的conda