# senior_DE_challanege


# Technologies

- Python >= 3.10
- Pandas
- Docker/Kubernetes for deployment & scale


# Overview

Main packages:

- `data_pipeline.data_loader`: implementation of Data Loader from various data sources and data types
- `tests.test_data_loader`: unit and integration tests for data loader.

# Development
- pip list --format=freeze > requirements.txt
```
cd path/to/project

virtualenv -p python3.10 venv    # Or conda create -n tcb-pool python=3.8
source venv/bin/activate        # Or conda activate tcb-pool
pip install -r requirements.txt

# Set PYTHONPATH for module imports
export PYTHONPATH=path/to/project/folder/
```

# Testings
Run unit tests in `tests/` folder:

```bash
# To run all tests
python -m unittest discover -p *test*.py -v
```

Test coverage: just replace the initial `python` with `coverage run`

```bash
coverage run -m unittest discover -p *test*.py -v

# To show report on console
coverage report -m  # must above 90%

# To show report on Web UI
coverage html
```

# Docker Commands
```bash
# get original image
docker pull postgres:alpine

# docker run container based on image
docker run --name postgres-0 -e POSTGRES_PASSWORD=password -d -p 5432:5432 postgres:alpine 

# remove container and rerun
docker rm postgres-0
docker run --name postgres-0 -e POSTGRES_PASSWORD=password -d -p 5432:5432 postgres:alpine 

# remove all stopped containers
docker container prune

# connect to container
docker exec -it postgres-0 bash

# connect to database
psql -U postgres

# list all database roles (users) 
\du

# create database 
create database ecommerce;

# list databases
\l

# connect to database
\c ecommerce

# list tables
\d

```


```bash
# Build an image from a Dockerfile
# docker build [OPTIONS] PATH_TO_DOCKER_FILE 
# -t tag:latest -f file_path --build-arg APP_VERSION=1.0 
docker build -t ecommerce-db ./database

# Check list of local images
docker images 

# remove image
docker rmi image-name
docker exec -it ecommerce-db bash

# Run the container 
# docker run [OPTIONS] IMAGE [COMMAND] [ARG]
# -d : runs in background
# -p : maps host port 5432 to container port 5432  
# -v : bind mount a volume
docker run -p 5432:5432 --name ecommerce-db -d ecommerce-db


# Check running do
# -a : including stopped ones
docker ps

# Stop container
# docker stop [OPTIONS] CONTAINER(name or id)
docker stop ecommerce-db

# Force stop
docker kill ecommerce-db

# Restart
docker start ecommerce-db

# Inspecting container configuration
docker inspect ecommerce-db

# View logs of container
docker logs ecommerce-db

# Rebuild image
# --no-cache doesn't use any cached layers from the previous build.
docker build --no-cache -t ecommerce-db ./database/

# Connect to container
docker exec -it ecommerce-db bash

# Verify database
# docker exec -it CONTAINER psql -U USERNAME
docker exec -it ecommerce-db psql -U user -d ecommerce

```

# Database Optimization
1. Use indexes: index on columns that are frequently used in WHERE, JOIN or ORDER BY clauses
2. Analyze the query plan: Use EXPLAIN to identify slow or inefficient queries 
3. Use partition: partition table on columns that oare frequently used in WHERE
4. Use VACUUM and ANALYZE: 
   1. VACUUM removes dead rows and frees up spaces in dataabse
   2. ANALYZE updates the statistics that the query planner uses to optimize queries
   3. Run VACUUM and ANALYZE regularly
5. Use appropriate data types: integer, date or timestamp 
6. Optimize queries: use appropriate JOINs, WHERE and SELECT statement
   1. avoid using subqueries or overly complex expressions
7. Use connection pooling: Reduce the overhead of establishing and closing database connections
