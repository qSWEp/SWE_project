# E-Commerce Store

A full-stack e-commerce web application built with Django, covering the shopping
flow from product browsing to invoice generation.

## Features
- User registration, login, and logout
- Product catalog with images, pricing, and ratings
- Shopping cart with quantity increase/decrease and item removal
- Delivery information capture at checkout
- Printable invoice with order summary and delivery details
- Django admin interface for product management

## Tech Stack
- **Backend:** Django (Python)
- **Database:** MySQL / MariaDB
- **Frontend:** Django Templates, Bootstrap 5
- **Media:** Pillow

## Screenshots
_(add screenshots here)_

## Getting Started

```bash
git clone https://github.com/qSWEp/SWE_project.git
cd SWE_project

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install django pillow mysqlclient django-bootstrap-v5
```

Configure your database credentials in `Finel/settings.py`, then:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/`

## Notes
- Built during the Tuwaiq Academy Django bootcamp (Mar 2025) as a learning project,
  kept as-is to reflect the original coursework
- Payment gateway integration is out of scope — checkout completes with invoice generation
- `DEBUG = True` and the default `SECRET_KEY` are development settings only

## Author
Abdulelah Ali Alruwaili — [LinkedIn](https://linkedin.com/in/abdulelah-alruwaili)
