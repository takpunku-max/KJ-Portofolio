# AWS EC2 Web Server with NGINX and Firewall Hardening

## Overview
This project demonstrates deploying a secure, production-style web application on AWS EC2 using NGINX, FastAPI, and Docker. The application is exposed through a custom domain, protected by firewall rules and SSH key-based authentication, and designed to automatically recover after system reboots.

---

## Goal
Deploy a secure EC2-hosted web application that mirrors real-world production architecture, with an emphasis on security, reliability, and maintainability.

---

## Architecture

The following diagram shows the request flow from the client to the application:
```text
Client
  → Custom Domain (DNS)
      → EC2 Instance (Public)
          → NGINX (Reverse Proxy, Port 80)
              → FastAPI Application (Docker, localhost:8000)
```



- Only NGINX is publicly accessible
- The FastAPI application runs privately on localhost
- Docker and NGINX are managed by systemd

---

## What I Did

- Launched a Linux EC2 instance and configured security groups for SSH and HTTP/HTTPS
- Installed and configured NGINX as a reverse proxy
- Configured UFW to allow only required inbound traffic
- Secured server access using SSH key-based authentication and disabled password logins
- Containerized the FastAPI application using Docker
- Configured Docker and NGINX to start automatically using systemd
- Verified application availability and security after system reboots

---

## Backup Strategy

- EC2 root volume snapshot taken after stable deployment
- Snapshot includes OS, NGINX, Docker containers, and application state

---

## Technology Stack

- **Cloud Provider:** AWS
- **Compute:** EC2 (Linux)
- **Containerization:** Docker
- **Web Server / Reverse Proxy:** NGINX
- **Backend Framework:** FastAPI (Python)
- **Process Management:** systemd
- **Firewall:** UFW
- **DNS:** Custom domain

---

## Key Features

- Containerized FastAPI application
- NGINX reverse proxy with domain-based routing
- Application isolated from direct internet exposure
- Firewall-restricted network access
- Automatic service recovery after reboot

---

## Challenges & Lessons Learned

- Resolved NGINX configuration conflicts caused by duplicate default server blocks
- Learned how Host headers affect virtual host routing
- Debugged Docker permission issues related to Unix groups
- Gained a deeper understanding of VM networking versus container networking
- Developed experience troubleshooting real-world infrastructure issues
- HTTPS enabled using Let’s Encrypt with automatic certificate renewal via Certbot

---

## Running the Project

- Docker daemon and NGINX are enabled via systemd
- FastAPI container runs with an automatic restart policy
- NGINX proxies incoming HTTP requests to the FastAPI container

---

## Future Improvements

- Integrate PostgreSQL using Amazon RDS
- Add authentication and authorization
- Implement CI/CD for automated deployments
- Add monitoring and alerting

---

## Security & Hardening

This project implements multiple layers of security to mirror real-world production practices while maintaining developer accessibility.

---

### Network Security
- AWS Security Groups restrict inbound traffic to only required ports:
  - **22 (SSH)** – Key-based access only
  - **80 (HTTP)** – Redirects to HTTPS
  - **443 (HTTPS)** – Public web access
- No other inbound ports are exposed

---

### SSH Hardening
- SSH access is restricted to **key-based authentication**
- Password-based login is disabled
- Root login is disabled
- SSH is kept enabled to support VS Code Remote SSH during development

---

### Fail2ban (Intrusion Prevention)
- Fail2ban actively monitors SSH authentication logs
- Automatically bans IPs after repeated failed login attempts
- Provides protection against brute-force and automated scanning attacks
- Works alongside AWS Security Groups for layered defense

---

### Web Application Security
- NGINX acts as a reverse proxy, isolating the FastAPI application from direct internet access
- The FastAPI application runs privately on localhost within a Docker container
- Only NGINX is publicly exposed
- TLS encryption is enforced using Let’s Encrypt certificates

---

### Defense-in-Depth Approach
Security is implemented at multiple layers:
1. AWS Security Groups (network perimeter)
2. Linux firewall and intrusion prevention (Fail2ban)
3. SSH hardening (key-only access)
4. Reverse proxy isolation (NGINX)
5. Containerized application runtime (Docker)

This layered approach ensures that a failure at one level does not compromise the entire system.

---

## Conclusion
This project provided hands-on experience deploying and securing a web application in a cloud environment.
By configuring firewalls, reverse proxies, containerization, and service automation,
I learned how to take an application from local development to a stable, secure, and publicly accessible production deployment.


