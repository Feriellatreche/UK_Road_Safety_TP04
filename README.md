# TP04 – Containerization and Big Data Environment Deployment Using Docker

## 1. Project Overview

This project demonstrates how to containerize and deploy a Python-based data analysis application using Docker and Docker Compose.

The application analyzes a UK road safety dataset containing vehicle records and produces summary statistics, CSV tables, and visualizations.

### Dataset Summary

- **Vehicle records:** 599,882
- **Unique accidents:** 452,611
- **Number of columns:** 10
- **Charts generated:** 8
- **Missing values:** The `Age_of_Vehicle` column contains 77,147 missing values (12.86%).

The dataset is used to analyze accident severity, yearly trends, weather conditions, road surface conditions, lighting conditions, and missing values.

## 2. Project Structure

```text
UK_Road_Safety_TP04/
├── data/
├── results/
├── screenshots/
├── app.py
├── merge_data.py
├── Dockerfile
├── compose.yaml
├── requirements.txt
├── .dockerignore
└── README.md
```

The `data/` directory contains the input dataset. The `results/` directory contains generated charts and CSV files. The `screenshots/` directory documents the practical tasks.

## 3. Task 1 – Docker Installation

Docker Desktop was installed and verified successfully on Windows.

The Docker installation was tested using:

```powershell
docker --version
docker run hello-world
```

A Docker Hub account was created to publish and download the project image.

## 4. Task 2 – Build, Push, and Pull the Image

### Build the image

```powershell
docker build -t uk-road-safety-analysis:v1 .
```

### Docker Hub image

The image was tagged and pushed to Docker Hub.

**Repository:** https://hub.docker.com/r/aidatalabdz2026/uk-road-safety-analysis

### Pull the image

```powershell
docker pull aidatalabdz2026/uk-road-safety-analysis:v1
```

### Run the analysis

From the project directory:

```powershell
docker run --rm -v "${PWD}/data:/app/data:ro" aidatalabdz2026/uk-road-safety-analysis:v1
```

The `-v` option mounts the local data directory into the container in read-only mode.

## 5. Task 3 – Multiple Containers and Networking

A Docker network was created to connect three containers:

```powershell
docker network create tp04-network
```

Three containers were launched from the downloaded image, with host ports 8001, 8002, and 8003 mapped to container port 8000.

The containers were connected to `tp04-network` and configured to read the dataset using a read-only volume.

The containers were verified using:

```powershell
docker ps
docker network inspect tp04-network
```

The results server can be accessed through the corresponding host ports while the containers are running:

- http://localhost:8001
- http://localhost:8002
- http://localhost:8003

## 6. Task 4 – Docker Compose

The following `compose.yaml` configuration was used:

```yaml
services:
  data-analysis:
    build: .
    container_name: tp04-analysis
    volumes:
      - ./data:/app/data:ro
    restart: "no"
```

### Run the application

```powershell
docker compose up --build
```

### Check container status

```powershell
docker compose ps -a
```

### Stop and remove Compose resources

```powershell
docker compose down
```

The analysis completed successfully with exit code 0. Since the application performs a batch analysis and then terminates, the container is expected to stop after completing its task.

### What problem does Docker Compose solve?

Docker Compose defines application services and their configurations in a single YAML file. It simplifies the process of creating, starting, and stopping services and makes deployments more consistent and repeatable.

### Docker run vs. Docker Compose

`docker run` creates and starts an individual container using options specified in the terminal. `docker compose up` reads the Compose configuration and creates or starts the services defined in the YAML file.

### Extending Compose with a database

A database service, such as PostgreSQL, can be added to the Compose file by specifying its image, environment variables, persistent storage, and network configuration. The application can communicate with the database using its service name.

## 7. Task 5 – Docker Report

### Usefulness of Docker in Data Science

Docker helps data scientists create reproducible and portable environments. It packages application code and dependencies into an image, reduces compatibility problems, isolates dependencies, and supports collaboration across different systems.

In this project, Docker was used to package and execute a Python-based road safety analysis application.

### Docker Image vs. Docker Container

A **Docker image** is a template containing the application code, dependencies, and instructions needed to run the application.

A **Docker container** is an instance of an image in which the application runs. A container may be running or stopped.

### Dockerfile Directives

| Directive | Purpose |
|---|---|
| `FROM` | Specifies the base image. |
| `WORKDIR` | Sets the working directory inside the image. |
| `COPY` | Copies files from the build context into the image. |
| `RUN` | Executes commands during image construction. |
| `CMD` | Specifies the default command executed when the container starts. |

The project's Dockerfile uses `python:3.11-slim` as its base image, sets `/app` as the working directory, copies the dependency file and application code, installs Python libraries, and runs `python app.py`.

## 8. Results

The containerized application successfully analyzed 599,882 vehicle records, identified 452,611 unique accidents, and generated eight charts and corresponding CSV outputs.

The analysis examined accident severity, annual accident trends, weather, road conditions, lighting, severity relationships, and missing data.

## 9. Screenshots and Submission

The `screenshots/` directory contains screenshots documenting Docker installation, image building and publishing, container execution, networking, and Docker Compose commands.

The source code, configuration files, screenshots, report, and this README should be uploaded to the student's GitHub repository.

**Note:** The dataset is not included in this repository by default. Users must provide the dataset in `data/UK_Road_Safety_Merged.csv` before running the analysis.