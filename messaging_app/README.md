

## Overview
The **Messaging App** is a backend API built with **Django 5.2** and **Django REST Framework**.  
It allows users to create conversations and send messages. This project demonstrates:

- Custom user model with roles
- One-to-many and many-to-many relationships
- RESTful API design
- Modular Django project structure

---

## Features

- Custom `User` model extending Django’s AbstractUser
- `Conversation` model with multiple participants
- `Message` model linked to conversations and users
- JSON-only API endpoints:
  - List and create conversations
  - Send and list messages

---

## Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/your-username/alx-backend-python.git
cd alx-backend-python/messaging_app
