# Transcriptive MySQL Integration

## Overview

MySQL has been implemented as the database management system as a reliable solution for security, data integrity, and interactibility. It currently runs as a part of the Compose, and starts up alongside the server. In order for the server to run, though, MySQL needs to be properly set up. 

## Setup and Deployment

The first thing that needs to be created is the environment variables for the service. Place a file named `.env` in the `backend-container` folder, and edit it to create these two environment variables:
```
MYSQL_PASSWORD=your_password
MYSQL_ROOT_PASSWORD=your_password
```

Then, all that needs to be done is to run `docker compose up` along with the top level container. Be sure to check your local volumes for correct permissions if data is not being written, labeled here:
- `mysql_data:/var/lib/mysql`
- `./db/init:/docker-entrypoint-initdb.d:Z`
- `./db/exports:/var/lib/mysql-files:Z`
