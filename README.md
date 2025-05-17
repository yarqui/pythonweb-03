# Python Web App with Poetry & Docker

This project is a Python web application configured to use **Poetry** for dependency management and **Docker** for containerization.

---

## Docker Build & Run Instructions

### 1. Build the Docker Image

```bash
docker build -t <your_app_name> .
```

### 2. Run the Docker Container

```bash
docker run -d -p 3000:3000 -v "<absolute_path_to_storage_folder>":/app/storage <your_app_name>
```
