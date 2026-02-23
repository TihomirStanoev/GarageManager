# 🚗 GarageManager 

A Django-based web application for managing car repairs, clients, parts, and invoices for an auto repair shop.

---
<img width="1828" height="906" alt="image" src="https://github.com/user-attachments/assets/452ec0e5-5efd-45ca-9b91-ca4d8ef9d151" />

## 📑 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Data Models](#data-models)
- [Installation](#installation)
- [Configuration](#configuration)
- [URL Reference](#url-reference)
- [Custom Template Tags](#custom-template-tags)

---

## 📖 Overview

GarageManager is a complete garage management system that allows a repair shop to:

- Manage client profiles
- Track vehicles and assign them to clients
- Create and manage repairs with status tracking
- Add parts to repairs with quantity and pricing
- Generate invoices automatically from completed repairs

---

## ✨ Features

### Client Management
- Create, update, and delete client profiles
- Search clients by name or phone number
- View all vehicles and invoices associated with a client
- Pagination (10 per page)

### Vehicle Management
- Register vehicles with brand, model, plate, year, engine type, and mileage
- Assign/unassign vehicles to clients
- Browse unassigned vehicles separately
- Validate Bulgarian license plate format (e.g. `CB1234AB`)
- Search by plate or model
- Pagination (8 per page)

### Repair Management
- Create repairs linked to a vehicle
- Status workflow: `Draft → In Progress → Completed`
- Add parts to repairs (filtered by repair category)
- Update labor hours and hourly rate
- View repair cost breakdown (labor + parts)
- Filter active (non-invoiced) repairs separately from all repairs
- Search by car plate or client name
- Pagination (8 per page)

### Parts Catalogue
- Maintain a catalogue of parts organized by category
- Part categories: Engine & Transmission, Brakes & Wheels, Suspension & Steering, Electrical System, Fuel System, Other
- Search parts by name or description
- Pagination (8 per page)

### Invoice Management
- One-click invoice generation from a completed repair
- Auto-generated unique 10-digit invoice number
- Auto-populated owner and total amount from repair data
- Search invoices by client, car, or invoice number
- Print-ready invoice layout with `window.print()`
- Pagination (8 per page)

### General
- Dashboard with live statistics (clients, cars, active repairs, parts, invoices)
- Responsive UI with Bootstrap 5.3
- Custom 404 page
- Django Admin panel for all models

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Framework | Django 6.0.2 |
| Database | PostgreSQL |
| Frontend | Bootstrap 5.3.3, Bootstrap Icons |
| Forms | django-crispy-forms + crispy-bootstrap5 |
| Images | Pillow |
| Environment | django-environ |

---

## 📂 Project Structure

```
GarageManager/
├── GarageManager/          # Project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── common/                 # Shared utilities, home page, base models
│   ├── models.py           # TimeStampedModel, RepairPartMixin (abstract)
│   ├── views.py            # IndexView (dashboard)
│   └── templatetags/
│       └── garage_simple_tags.py
│
├── profiles/               # Client management
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── validators.py
│
├── cars/                   # Vehicle management
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── choices.py
│   └── validators.py
│
├── repairs/                # Repairs, parts, and invoices
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── choices.py
│
├── templates/              # HTML templates
│   ├── base.html
│   ├── 404.html
│   ├── common/
│   ├── profiles/
│   ├── cars/
│   ├── repairs/
│   │   ├── repairs/
│   │   ├── parts/
│   │   └── invoices/
│   └── shared/             # Reusable partials (nav, footer, paginator)
│
├── static/
│   └── css/style.css
├── media/                  # User-uploaded images
└── requirements.txt
```

---

## 🗄️ Data Models

### Profile
Represents a client of the garage.

| Field | Type | Notes |
|---|---|---|
| first_name | CharField(20) | |
| last_name | CharField(20) | |
| email | EmailField | unique |
| phone_number | CharField(15) | unique, Bulgarian format (+359...) |
| created_at | DateTimeField | auto |
| updated_at | DateTimeField | auto |

**Relations:** has many `Car`, has many `Invoice`

---

### Car
Represents a vehicle registered in the system.

| Field | Type | Notes |
|---|---|---|
| brand | CharField | choices: Audi, BMW, Volvo, Mercedes, Volkswagen |
| model | CharField(40) | |
| plate | CharField(10) | unique, Bulgarian format |
| year | PositiveIntegerField | validated 1900–current year |
| engine_type | CharField | choices: Gasoline, Diesel, Hybrid, Electric, LPG |
| mileage | PositiveIntegerField | |
| image | ImageField | optional |
| owner | FK → Profile | optional, SET_NULL |

**Relations:** belongs to `Profile` (optional), has many `Repair`

---

### Part
A catalogue entry for a spare part.

| Field | Type | Notes |
|---|---|---|
| name | CharField(50) | |
| category | CharField | shared with Repair (via RepairPartMixin) |
| description | TextField | |
| image | ImageField | optional |

**Relations:** many-to-many with `Repair` (through `RepairPart`)

---

### Repair
Represents a repair job for a vehicle.

| Field | Type | Notes |
|---|---|---|
| category | CharField | Engine & Transmission, Brakes, Suspension, Electrical, Fuel, Other |
| description | TextField | |
| status | CharField | Draft / In Progress / Completed / Cancelled |
| labor_hours | DecimalField | |
| price_per_labor_hour | DecimalField | |
| car | FK → Car | CASCADE |
| parts | M2M → Part | through RepairPart |
| is_invoiced | BooleanField | default False |

**Computed properties:** `labor_price`, `parts_price`, `total_price`

**Relations:** belongs to `Car`, has many `Part` (through `RepairPart`), has one `Invoice`

---

### RepairPart
Through model connecting a Repair and a Part.

| Field | Type | Notes |
|---|---|---|
| repair | FK → Repair | CASCADE |
| part | FK → Part | CASCADE |
| quantity | PositiveIntegerField | default 1 |
| price | DecimalField | |

**Constraint:** unique_together (repair, part)

**Computed property:** `parts_price` = price × quantity

---

### Invoice
A billing document generated from a repair.

| Field | Type | Notes |
|---|---|---|
| invoice_number | CharField(10) | auto-generated, unique |
| repair | OneToOneField → Repair | CASCADE |
| owner | FK → Profile | auto-populated, SET_NULL |
| total_amount | DecimalField | auto-populated from repair.total_price |

**Auto-populated on save:** `invoice_number`, `owner` (from repair.car.owner), `total_amount` (from repair.total_price)

---

## 🛠️ Installation

### Prerequisites
- Python 3.12+
- PostgreSQL

### Steps

```bash
# 1. Clone the repository
git clone <repo-url>
cd GarageManager

# 2. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file (see Configuration section)

# 5. Apply migrations
python manage.py migrate

# 6. Create superuser (optional, for admin access)
python manage.py createsuperuser

# 7. Run the development server
python manage.py runserver
```

---

## 🪛 Configuration

Create a `.env` file in the project root with the following variables:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/DB_NAME
SITE_NAME=GarageManager
```

---

## 🔗 URL Reference

### Home
| URL | View | Name |
|---|---|---|
| `/` | Dashboard | `home:index` |

### Profiles
| URL | View | Name |
|---|---|---|
| `/profiles/` | Client list | `profiles:list` |
| `/profiles/create/` | Create client | `profiles:create` |
| `/profiles/<pk>/` | Client detail | `profiles:detail` |
| `/profiles/<pk>/update/` | Edit client | `profiles:update` |
| `/profiles/<pk>/delete/` | Delete client | `profiles:delete` |

### Cars
| URL | View | Name |
|---|---|---|
| `/cars/` | Car list | `cars:list` |
| `/cars/filtered/` | Unassigned cars | `cars:filtered` |
| `/cars/create/` | Register car | `cars:create` |
| `/cars/<plate>/` | Car detail | `cars:detail` |
| `/cars/<plate>/update/` | Edit car | `cars:update` |
| `/cars/<plate>/delete/` | Delete car | `cars:delete` |

### Repairs
| URL | View | Name |
|---|---|---|
| `/repairs/` | Active repairs | `repairs:repairs_list` |
| `/repairs/all/` | All repairs | `repairs:repairs_list_all` |
| `/repairs/create/` | New repair | `repairs:repairs_create` |
| `/repairs/create/<plate>/` | New repair for car | `repairs:repairs_create_with_car` |
| `/repairs/<pk>/` | Repair detail | `repairs:repairs_detail` |
| `/repairs/<pk>/update/` | Edit repair | `repairs:repairs_update` |
| `/repairs/<pk>/delete/` | Delete repair | `repairs:repairs_delete` |
| `/repairs/<pk>/add_part/` | Add part to repair | `repairs:repairs_add_part` |
| `/repairs/<pk>/delete_part/<part_pk>/` | Remove part | `repairs:repairs_delete_part` |

### Parts
| URL | View | Name |
|---|---|---|
| `/repairs/parts/` | Parts catalogue | `repairs:parts_list` |
| `/repairs/parts/create/` | Add part | `repairs:parts_create` |
| `/repairs/parts/<pk>/` | Part detail | `repairs:parts_detail` |
| `/repairs/parts/<pk>/update/` | Edit part | `repairs:parts_update` |
| `/repairs/parts/<pk>/delete/` | Delete part | `repairs:parts_delete` |

### Invoices
| URL | View | Name |
|---|---|---|
| `/repairs/invoices/` | Invoice list | `repairs:invoices_list` |
| `/repairs/invoices/<repair_pk>/create/` | Generate invoice | `repairs:invoices_create` |
| `/repairs/invoices/<pk>/` | Invoice detail / print | `repairs:invoices_detail` |

---

## 🏷️ Custom Template Tags

Load with `{% load garage_simple_tags %}` in templates.

| Tag / Filter | Usage | Output |
|---|---|---|
| `{% site_name %}` | Renders site name | `GarageManager` |
| `{% year %}` | Renders current year | `2026` |
| `{{ id\|format_id }}` | Formats numeric ID | `#00042` |
| `{{ amount\|currency }}` | Formats decimal as currency | `125.50€` |
