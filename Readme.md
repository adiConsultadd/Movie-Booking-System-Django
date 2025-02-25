# Movie Ticket Booking System - Django REST Framework

A movie ticket booking system built using Django REST Framework (DRF), implementing role-based access control (RBAC) and JWT authentication.

---

## 🚀 Features

### **Authentication Endpoints**
- `POST /api/auth/register/` → Create a new user  
- `POST /api/auth/login/` → Login and obtain an access token and refresh token

### **Admin Endpoints** (Requires `is_admin=True`)
- `POST /api/movies/` → Add a new movie  
- `PUT /api/movies/{id}/` → Update movie details  
- `DELETE /api/movies/{id}/` → Remove a movie  
- `GET /api/bookings/` → View all ticket bookings  

### **User Endpoints** (Requires `Login`)
- `GET /api/movies/` → View all available movies  
- `GET /api//movies/{id}/` → View Information About A Specific Movie
- `GET /api/bookings/history` → View booking history of a user  
- `POST /api/movies/{id}/book` → Book a ticket  
- `DELETE /movies/{id}/cancel` → Cancel a booking  

---

## 🛠 Tech Stack

- **Django REST Framework** - API Development  
- **SQLite** - Database  
- **JWT Authentication** - Secure user authentication  
- **Pytest-Django** - Automated testing  

---

## 🔧 Installation & Setup

### Clone the Repository
```bash
git clone https://github.com/adiConsultadd/Movie-Booking-System-Django.git
```

### Create a Virtual Environment
```bash
python3 -m venv venv  
source venv/bin/activate  # For Mac/Linux  
venv\Scripts\activate  # For Windows  
```

### Install Dependencies
```bash
pip install -r requirements.txt
```
### Set Up Environment Variables
- Create a .env file and add the following details:
```bash
SECRET_KEY="*************"
```

### Movie Inside The Main App
```bash
cd movie_booking/
```

### Apply Migrations
```bash
python manage.py migrate  
```

### Create Superuser
```bash
python manage.py createsuperuser 
```

### Run The Django Server
```bash
python manage.py runserver  
```

## Authentication
### Users & Admins must authenticate using JWT tokens.
- Use the /auth/login endpoint to get a token, then pass it in the Authorization header:
```bash
Authorization: Bearer <your_token_here>
```
- Tokens expire as per JWT settings in settings.py.


## Project Structure
```bash
    movie_booking/
    │── core/
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py
    │
    │── auth/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── permissions.py
    │   ├── serializers.py
    │   ├── tests.py
    │   ├── urls.py
    │   ├── views.py
    │
    │── booking/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── serializers.py
    │   ├── tests.py
    │   ├── urls.py
    │   ├── views.py
    │
    │── movie/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── serializers.py
    │   ├── tests.py
    │   ├── urls.py
    │   ├── views.py
    |
    │── .env
    │── .gitignore
    │── manage.py
    │── requirements.txt
    │── README.md
```

## Running Tests (Pytest)
### Tests are divided into three files:

- auth/test.py → Tests authentication mechanisms
- booking/test.py → Tests booking-related endpoints
- movie/test.py → Tests movie-related endpoints

### To run all tests:
```bash
pytest
```

### Run A Specific Test File
```bash
pytest -v -m movies
pytest -v -m auth
pytest -v -m bookings
```

### To See Coverage Of Test Files
```bash
pytest --cov
```

## Postman Collection
### Import the Collection
- Open Postman and go to File > Import.
- Select the exported .json file and import it.

![Image](https://github.com/user-attachments/assets/21851803-477f-4d55-996a-6754ef268d55)