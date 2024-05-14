#!/bin/bash

# Define the Docker image and tag
IMAGE="mcr.microsoft.com/playwright/python:v1.43.0-jammy"
CONTAINER_NAME="playwright-container"

# Pull the Docker image
echo "Pulling Docker image..."
docker pull $IMAGE

# Run the Docker container and set up the environment
echo "Running Docker container and setting up the environment..."
docker run --name $CONTAINER_NAME --rm -it -v $(pwd):/home/pwuser/project $IMAGE bash -c "
    echo 'Installing dependencies...'
    pip install playwright pytest pytest-playwright;

    echo 'Navigating to project directory...'
    cd /home/pwuser/project;

    echo 'Entering interactive mode...'
    echo 'Run pytest playwright to run all playwright tests or use pytest (pwd to name of file) to run a single test'
    exec bash
"

echo "Container $CONTAINER_NAME has finished running."
