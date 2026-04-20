# 🚗 GarageManager

A production-grade Django web application for managing an auto repair shop — clients, vehicles, repairs, parts, and invoices — with role-based access, a REST API, asynchronous notifications, and cloud media storage.

**Live demo:** https://rev.up.railway.app

> **Manager / Mechanic demo access.** Self-registration creates a regular client account. To evaluate the manager or mechanic role on the live demo, please contact me at **tstanoev991@gmail.com** and I will promote your account.

<img width="1765" height="935" alt="GarageManager dashboard" src="https://github.com/user-attachments/assets/3af8daa3-976b-4a08-ab7a-70e4ed5542ce" />

---

## 📑 Table of Contents

- [🎯 Overview](#-overview)
- [📸 Screenshots](#-screenshots)
- [✨ Key Features](#-key-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [🏗️ Architecture](#️-architecture)
- [🗄️ Data Model](#️-data-model)
- [🔐 Roles & Permissions](#-roles--permissions)
- [🔌 REST API](#-rest-api)
- [⚡ Asynchronous Tasks](#-asynchronous-tasks)
- [🗑️ Soft Deletion](#️-soft-deletion)
- [⚙️ Installation](#️-installation)
- [🔑 Environment Variables](#-environment-variables)
- [🚀 Deployment (Railway)](#-deployment-railway)
- [🧪 Testing](#-testing)
- [📂 Project Structure](#-project-structure)
- [🏷️ Custom Template Tags](#️-custom-template-tags)
- [🔗 URL Reference](#-url-reference)

---

## 🎯 Overview

GarageManager is a full-stack web application that digitises the daily workflow of a small-to-medium auto repair shop. Managers maintain the client registry, register vehicles, schedule repairs and generate invoices. Mechanics are assigned to repairs, update their status, and log the parts they consume. Clients have read-only access to their own vehicles, repairs and invoices through a REST API protected with JWT.

The project was built as the final assignment for **SoftUni — Django Advanced Retake Exam (April 2026)** and fulfils every requirement from the specification: custom user model, groups & permissions, class-based views, a soft-delete pattern, async Celery tasks, a REST API with JWT authentication, and a live production deployment.

---

## 📸 Screenshots


### Dashboard
Role-aware landing page with live counts of clients, vehicles, active repairs, parts and invoices.

<img width="1828" alt="Dashboard" src="https://github.com/user-attachments/assets/452ec0e5-5efd-45ca-9b91-ca4d8ef9d151" />

### Vehicle Detail
Vehicle card with Cloudinary-hosted photo, owner info and full repair history for the car.

<img width="1837" height="937" alt="image" src="https://github.com/user-attachments/assets/6bb60c4a-11f0-449e-8726-ed27a42ae9a3" />

### Repair Detail
Full cost breakdown (labor + parts), status controls, assigned mechanics and part management.

<img width="1860" height="942" alt="image" src="https://github.com/user-attachments/assets/8d13b885-58d6-4291-880e-5494f8f6a88b" />

### Invoice Detail
Print-ready invoice with auto-generated number, owner information and itemised total.

<img width="1866" height="943" alt="Image" src="https://github.com/user-attachments/assets/ca61852b-e61d-423e-a162-a7a37e1058a7" />

### Manager — User Management
Manager-only view with role toggle (promote/demote) and account activation controls.

<img width="1844" height="812" alt="image" src="https://github.com/user-attachments/assets/7b773a1c-68dd-44e0-b2d0-56d34e9113ca" />

---

## ✨ Key Features

### Authentication & Accounts
- Custom `User` model with **email** as the login identifier (no username)
- Self-registration with automatic login
- Password reset flow via e-mail (SMTP through Mailjet)
- Two user groups — `Manager` and `Mechanic` — with distinct permissions
- Managers can promote/demote users and toggle account activation

### Vehicles (`cars`)
- Register vehicles with brand, model, plate, year, engine type, mileage and photo
- Bulgarian licence-plate validation and production-year validation
- Vehicle photo upload to **Cloudinary**
- Cascading soft-delete to related repairs
- Ownership change triggers an asynchronous e-mail notification (Celery)

### Repairs & Parts (`repairs`)
- Repairs linked to vehicles with a full lifecycle: `Draft → In Progress → Completed → Cancelled`
- Many-to-many relationship to spare parts through an explicit `RepairPart` through-model (quantity + price at time of use)
- Many-to-many assignment of mechanics to repairs
- Computed cost breakdown: `labor_price`, `parts_price`, `total_price`
- Custom model permissions: `change_repair_status`, `change_repair_mechanic`
- Parts catalogue with category taxonomy and Cloudinary images

### Invoices (`invoices`)
- One-click invoice generation from a completed repair
- Auto-generated unique 10-digit invoice number
- Auto-populated owner and total amount from the source repair
- `PROTECT` constraints prevent accidental deletion of invoiced data
- Invoices cannot be issued for uncompleted or orphaned repairs (validated in `clean()`)
- Print-ready detail view

### Shared UX
- Dashboard with live counts (clients, vehicles, active repairs, parts, invoices)
- Search and pagination on every list view
- Responsive Bootstrap 5 UI with crispy-forms
- Custom 404 / 403 / 500 error pages
- Role-aware navigation (menu items shown only to the relevant group)

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12+ |
| Framework | Django 6.0.2 |
| Database | PostgreSQL (via `psycopg2-binary`) |
| Cache / Broker | Redis 7 |
| Task queue | Celery 5.6 |
| REST API | Django REST Framework 3.17 + SimpleJWT |
| Media storage | Cloudinary (`CloudinaryField`) |
| Static files | WhiteNoise (compressed manifest storage) |
| Frontend | Bootstrap 5.3, Bootstrap Icons, crispy-forms + crispy-bootstrap5 |
| Environment | `django-environ` |
| E-mail | SMTP via Mailjet |
| WSGI server | Gunicorn |
| Hosting | Railway (web + worker + Postgres + Redis) |

---

## 🏗️ Architecture

The project is organised into **five Django apps**, each owning a single bounded context:

| App | Responsibility |
|---|---|
| `common` | Abstract base models (`TimeStampedModel`, `SoftDeletionMixin`, `RepairPartMixin`), shared services, dashboard, JWT token endpoints, template tags, soft-delete/restore/hard-delete views |
| `accounts` | Custom user model, authentication, registration, password reset, group management, role toggling |
| `cars` | Vehicle CRUD, ownership transfer notifications, REST API |
| `repairs` | Repairs, parts catalogue, mechanic assignment, REST API |
| `invoices` | Invoice generation and retrieval, REST API |

**Cross-cutting concerns** (soft delete, timestamps, permissions, notifications) are implemented as mixins and reusable services in `common` and `accounts`, rather than being duplicated per app.

---

## 🗄️ Data Model

```
User (accounts) ─┬─< Car (cars) ─────────< Repair (repairs) ──── Invoice (invoices)
                 │                                │   │
                 │                                │   └──< RepairPart >── Part (repairs)
                 └──< Invoice                     └──>── assigned_mechanics (M2M → User)
```

### `accounts.User` (AbstractUser)
| Field | Type | Notes |
|---|---|---|
| `email` | EmailField | unique, login identifier |
| `phone_number` | CharField | unique, Bulgarian format |
| `first_name`, `last_name` | CharField | auto-capitalised on save |
| Group membership | M2M | `Manager` / `Mechanic` |

### `cars.Car`
| Field | Type | Notes |
|---|---|---|
| `brand` | CharField | choices: Audi, BMW, Volvo, Mercedes, Volkswagen |
| `model` | CharField(40) | |
| `plate` | CharField(10) | unique, Bulgarian format validator |
| `year` | PositiveIntegerField | 1900 – current year |
| `engine_type` | CharField | Gasoline, Diesel, Hybrid, Electric, LPG |
| `mileage` | PositiveIntegerField | |
| `image` | CloudinaryField | optional |
| `owner` | FK → User | `SET_NULL`, optional |

Soft-deleting a car soft-deletes all of its repairs. Cars with an owner or invoiced repairs cannot be deleted.

### `repairs.Part`
| Field | Type | Notes |
|---|---|---|
| `name` | CharField(50) | |
| `category` | CharField | from `RepairPartMixin.CategoryChoice` |
| `description` | TextField | |
| `image` | CloudinaryField | optional |

### `repairs.Repair`
| Field | Type | Notes |
|---|---|---|
| `status` | CharField | Draft, In Progress, Completed, Cancelled |
| `labor_hours`, `price_per_labor_hour` | DecimalField | non-negative |
| `car` | FK → Car | CASCADE |
| `parts` | M2M → Part | through `RepairPart` |
| `assigned_mechanics` | M2M → User | |
| `is_invoiced` | Boolean | |

Properties: `labor_price`, `parts_price`, `total_price`. Custom permissions: `change_repair_status`, `change_repair_mechanic`. Invoiced repairs cannot be deleted.

### `repairs.RepairPart`
Through-model carrying `quantity` and the `price` captured at the moment the part was added to the repair. Unique on `(repair, part)`.

### `invoices.Invoice`
| Field | Type | Notes |
|---|---|---|
| `invoice_number` | CharField(10) | auto-generated, unique, immutable |
| `repair` | OneToOne → Repair | `PROTECT` |
| `owner` | FK → User | `PROTECT`, auto-populated from `repair.car.owner` |
| `total_amount` | DecimalField | auto-populated from `repair.total_price` |

Issuing an invoice fails unless the underlying repair is `Completed` and has an owner.

---

## 🔐 Roles & Permissions

| Capability | Manager | Mechanic | Client (authenticated) |
|---|:---:|:---:|:---:|
| Browse & manage users | ✅ | ❌ | ❌ |
| Toggle role / activation | ✅ | ❌ | ❌ |
| Register / edit cars | ✅ | ❌ | ❌ |
| Browse parts catalogue | ✅ | ✅ | ❌ |
| Create / edit repairs | ✅ | ❌ | ❌ |
| Change repair status | ✅ | ✅ | ❌ |
| Be assigned to a repair | ❌ | ✅ | ❌ |
| Generate invoices | ✅ | ❌ | ❌ |
| REST: list own cars / repairs / invoices | ✅ | ✅ | ✅ |
| REST: manage all cars / repairs / invoices | ✅ | ❌ | ❌ |

Group checks are enforced at three layers: class-based-view mixins (`GroupRequiredMixin`, `GroupFilterMixin`), function-view decorator (`@group_required`), and DRF permissions (`IsManager`, `IsMechanic`).

---

## 🔌 REST API

All endpoints live under `/api/` and use JWT authentication (`rest_framework_simplejwt`).

### Authentication
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/token/` | Obtain access + refresh tokens |
| `POST` | `/api/token/refresh/` | Refresh an access token |

Send `Authorization: Bearer <access_token>` on every subsequent request.

### Cars
| Method | Endpoint | Permission |
|---|---|---|
| `GET` | `/api/cars/my-cars/` | Authenticated (owner scope) |
| `GET/POST` | `/api/cars/` | Manager |
| `GET/PUT/PATCH/DELETE` | `/api/cars/{id}/` | Manager |

### Repairs
| Method | Endpoint | Permission |
|---|---|---|
| `GET` | `/api/repairs/my-repairs/` | Authenticated (owner scope) |
| `*` | `/api/repairs/manager/` | Manager (full CRUD) |
| `*` | `/api/repairs/mechanic/` | Mechanic (assigned scope) |
| `GET/POST` | `/api/repairs/parts/` | Manager / Mechanic |
| `GET/PUT/PATCH/DELETE` | `/api/repairs/parts/{id}/` | Manager / Mechanic |

### Invoices
| Method | Endpoint | Permission |
|---|---|---|
| `GET` | `/api/invoices/my-invoices/` | Authenticated (owner scope) |
| `GET` | `/api/invoices/my-invoices/{id}/` | Authenticated (owner scope) |
| `GET/POST` | `/api/invoices/` | Manager |

Token lifetimes are configurable through `ACCESS_TOKEN_LIFETIME` (minutes) and `REFRESH_TOKEN_LIFETIME` (days).

---

## ⚡ Asynchronous Tasks

Celery is configured with Redis as both broker and result backend. The `common.tasks.send_mail_async` task dispatches all transactional e-mail off the request thread.

Triggers currently wired up:
- **Car ownership change** — `cars.mixins.CarNotificationMixin` e-mails the previous and/or new owner whenever a car is re-assigned.
- **Password reset** — Django's built-in flow, with rendering and SMTP delivery running through Celery.

Start the worker with:

```bash
celery -A GarageManager worker -l info --concurrency=2
```

> **Note:** The `--concurrency=2` flag is required on Railway's free tier; the default of 48 worker processes will exhaust the 512 MiB container.

---

## 🗑️ Soft Deletion

All primary models (`User`-linked `Car`, `Repair`, `Part`) inherit `SoftDeletionMixin`:

- `delete()` sets `is_deleted=True` and `deleted_at=now()` — rows stay in the database
- `hard_delete()` removes the row permanently (staff only, via `common.views.HardDeleteView`)
- `restore()` reverts a soft-deleted row
- `SoftDeleteManager` hides soft-deleted rows from default querysets; `all_objects` exposes them

Business rules enforced on delete:
- A car cannot be deleted while it has an owner or an invoiced repair
- A repair cannot be deleted if an invoice has been issued for it

---

## ⚙️ Installation

### Prerequisites
- Python **3.12+**
- PostgreSQL **14+**
- Redis **7+**
- A Cloudinary account (free tier is enough)
- An SMTP provider (Mailjet is used in production)

### Local setup

```bash
# 1. Clone
git clone https://github.com/TihomirStanoev/GarageManager.git
cd GarageManager

# 2. Virtualenv
python -m venv .venv
source .venv/bin/activate          # Linux / macOS
# .venv\Scripts\activate           # Windows

# 3. Dependencies
pip install -r requirements.txt

# 4. Environment — copy and edit
cp .env.example .env

# 5. Database (also creates the Manager and Mechanic groups via data migration)
python manage.py migrate

# 6. Superuser
python manage.py createsuperuser

# 7. Run the dev server
python manage.py runserver

# 8. In a separate terminal — start the Celery worker
celery -A GarageManager worker -l info
```

---

## 🔑 Environment Variables

| Variable | Required | Purpose |
|---|:---:|---|
| `SECRET_KEY` | ✅ | Django secret key |
| `DEBUG` | ✅ | `True` locally, `False` in production |
| `SITE_NAME` | ✅ | Displayed in navbar / e-mails |
| `ALLOWED_HOSTS` | ✅ | Comma-separated hostnames |
| `CSRF_TRUSTED_ORIGINS` | ✅ | Comma-separated origins incl. scheme |
| `DATABASE_URL` | ✅ | `postgres://USER:PASSWORD@HOST:PORT/DB` |
| `CELERY_BROKER_URL` | ✅ | `redis://...` |
| `CELERY_RESULT_BACKEND` | ✅ | `redis://...` |
| `CLOUDINARY_CLOUD_NAME` | ✅ | Cloudinary credentials |
| `CLOUDINARY_API_KEY` | ✅ | |
| `CLOUDINARY_API_SECRET` | ✅ | |
| `FROM_EMAIL` | ✅ | `DEFAULT_FROM_EMAIL` |
| `EMAIL_HOST` | ✅ | SMTP host |
| `EMAIL_PORT` | ✅ | SMTP port (default `587`) |
| `EMAIL_USE_TLS` | ✅ | Default `True` |
| `EMAIL_HOST_USER` | ✅ | SMTP username / API key |
| `EMAIL_HOST_PASSWORD` | ✅ | SMTP password / API secret |
| `ACCESS_TOKEN_LIFETIME` | ❌ | JWT access lifetime in minutes (default `5`) |
| `REFRESH_TOKEN_LIFETIME` | ❌ | JWT refresh lifetime in days (default `1`) |

When `DEBUG=False`, Django additionally enforces `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE` and the `X-Forwarded-Proto` header (set by Railway's edge proxy).

---

## 🚀 Deployment (Railway)

The production environment runs on **Railway** and consists of four managed services:

| Service | Purpose | Start command |
|---|---|---|
| `web` | Gunicorn + Django | From `Procfile` (migrate → collectstatic → gunicorn) |
| `worker` | Celery | `celery -A GarageManager worker -l info --concurrency=2` |
| `postgres` | Managed Postgres plugin | — |
| `redis` | Managed Redis plugin | — |

### Notable configuration

1. **`Procfile`** chains migrations, static collection and Gunicorn so deploys are idempotent:

   ```
   web: python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn GarageManager.wsgi --bind 0.0.0.0:$PORT
   ```

2. **Service-to-service references.** Railway does not auto-inject addon URLs into the web service; use variable references instead:

   ```
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   CELERY_BROKER_URL=${{Redis.REDIS_URL}}
   CELERY_RESULT_BACKEND=${{Redis.REDIS_URL}}
   ```

3. **Static files** are served by WhiteNoise using `CompressedManifestStaticFilesStorage` — no CDN needed.

4. **Media files** are uploaded directly to Cloudinary via `CloudinaryField`. The `django-cloudinary-storage` package is **not** used because it is incompatible with Django 6.0 (it still references the removed `settings.STATICFILES_STORAGE`).

5. **Django 6.0 storage format.** `DEFAULT_FILE_STORAGE` / `STATICFILES_STORAGE` are gone; the project uses the new `STORAGES` dict.

6. **Worker memory.** Celery is started with `--concurrency=2` — the default of 48 prefork children immediately OOM-kills the free-tier container.

---

## 🧪 Testing

```bash
python manage.py test
```

The suite covers **26 unit and integration tests** across `accounts`, `cars`, `repairs` and `invoices`, located under the top-level `tests/` package and grouped per app by type (`models`, `forms`, `views`). The tests exercise model validation, form cleaning, permission enforcement and the redirect/template flow of the class-based views.

---

## 📂 Project Structure

```
GarageManager/
├── GarageManager/              # Project package
│   ├── settings.py             # Environment-driven settings, STORAGES, Celery, JWT
│   ├── urls.py                 # Root URLconf
│   ├── api_urls.py             # Top-level /api/ router
│   ├── celery.py               # Celery app
│   └── wsgi.py / asgi.py
│
├── common/                     # Cross-cutting concerns
│   ├── models.py               # TimeStampedModel, RepairPartMixin, SoftDeletionMixin
│   ├── managers.py             # SoftDeleteManager
│   ├── views.py                # IndexView, RestoreView, HardDeleteView
│   ├── serivces.py             # hard_delete_object, restore_object
│   ├── tasks.py                # send_mail_async (Celery)
│   ├── api_urls.py             # JWT token endpoints
│   └── templatetags/garage_simple_tags.py
│
├── accounts/                   # Custom user + auth
│   ├── models.py               # User(AbstractUser), email login
│   ├── managers.py             # CustomUserManager
│   ├── backends.py             # EmailBackend
│   ├── forms.py                # Register / Login / Password reset
│   ├── mixins.py               # GroupRequiredMixin, GroupFilterMixin
│   ├── permissions.py          # IsManager, IsMechanic (DRF)
│   ├── decorators.py           # @group_required
│   ├── validators.py           # PhoneNumberValidator
│   ├── views.py                # Profile CBVs + toggle_role / toggle_active
│   └── urls.py
│
├── cars/                       # Vehicles
│   ├── models.py               # Car (with CloudinaryField + cascading soft delete)
│   ├── forms.py
│   ├── views.py                # CBVs
│   ├── api_views.py            # CarViewSet + UserCarListAPIView
│   ├── serializers.py
│   ├── mixins.py               # CarNotificationMixin (async email)
│   ├── choices.py / validators.py
│   ├── urls.py / api_urls.py
│
├── repairs/                    # Repairs + Parts
│   ├── models.py               # Repair, Part, RepairPart
│   ├── forms.py
│   ├── views.py                # Repair + Part CBVs, assignment
│   ├── api_views.py            # PartViewSet, RepairManager/Mechanic ViewSets
│   ├── serializers.py
│   ├── choices.py
│   ├── urls.py / api_urls.py
│
├── invoices/                   # Invoices
│   ├── models.py               # Invoice (auto number, PROTECT)
│   ├── views.py
│   ├── api_views.py
│   ├── serializers.py
│   ├── urls.py / api_urls.py
│
├── templates/                  # Global + per-app HTML templates
├── static/                     # Global CSS
├── tests/                      # Unit + integration test suite (26 tests)
├── Procfile                    # Railway web process
├── requirements.txt
├── .env.example
└── manage.py
```

---

## 🏷️ Custom Template Tags

Loaded with `{% load garage_simple_tags %}`.

| Tag / Filter | Example | Output |
|---|---|---|
| `{% site_name %}` | `{% site_name %}` | `GarageManager` |
| `{% year %}` | `{% year %}` | `2026` |
| `format_id` | `{{ 42\|format_id }}` | `#00042` |
| `currency` | `{{ 125.5\|currency }}` | `125.50€` |
| `is_in_group` | `{% if user\|is_in_group:'Manager' %}` | `True` / `False` |

---

## 🔗 URL Reference

### Public / Accounts
| URL | Name |
|---|---|
| `/` | `home:index` |
| `/accounts/register/` | `accounts:register` |
| `/accounts/login/` | `accounts:login` |
| `/accounts/logout/` | `accounts:logout` |
| `/accounts/password_reset/` | `accounts:password_reset` |
| `/accounts/list/` | `accounts:list` |
| `/accounts/profile/update/` | `accounts:update` |
| `/accounts/profile/<pk>/` | `accounts:profile` |
| `/accounts/profile/<pk>/toggle_active/` | `accounts:toggle_active` |
| `/accounts/profile/<pk>/toggle_role/` | `accounts:toggle_role` |

### Cars
| URL | Name |
|---|---|
| `/cars/` | `cars:list` |
| `/cars/create/` | `cars:create` |
| `/cars/<plate>/` | `cars:detail` |
| `/cars/<plate>/update/` | `cars:update` |
| `/cars/<plate>/delete/` | `cars:delete` |
| `/cars/<plate>/hard-delete/` | `cars:hard_delete` |
| `/cars/<plate>/restore/` | `cars:restore` |

### Repairs & Parts
| URL | Name |
|---|---|
| `/repairs/` | `repairs:repairs_list` |
| `/repairs/create/` | `repairs:repairs_create` |
| `/repairs/create/<car_plate>/` | `repairs:repairs_create_with_car` |
| `/repairs/<pk>/` | `repairs:repairs_detail` |
| `/repairs/<pk>/update/` | `repairs:repairs_update` |
| `/repairs/<pk>/delete/` | `repairs:repairs_delete` |
| `/repairs/<pk>/hard-delete/` | `repairs:repairs_hard_delete` |
| `/repairs/<pk>/restore/` | `repairs:repairs_restore` |
| `/repairs/<pk>/add_part/` | `repairs:repairs_add_part` |
| `/repairs/<pk>/delete_part/<part_pk>/` | `repairs:repairs_delete_part` |
| `/repairs/<pk>/assign/` | `repairs:assign_unassign_repair` |
| `/repairs/parts/` | `repairs:parts_list` |
| `/repairs/parts/create/` | `repairs:parts_create` |
| `/repairs/parts/<pk>/` | `repairs:parts_detail` |
| `/repairs/parts/<pk>/update/` | `repairs:parts_update` |
| `/repairs/parts/<pk>/delete/` | `repairs:parts_delete` |

### Invoices
| URL | Name |
|---|---|
| `/invoices/` | `invoices:invoices_list` |
| `/invoices/<repair_pk>/create/` | `invoices:invoices_create` |
| `/invoices/<slug>/` | `invoices:invoices_detail` |

### REST API
See the [🔌 REST API](#-rest-api) section above.

---

## 📄 License

This project was developed for educational purposes as part of the SoftUni Django Advanced curriculum.

## 👤 Author

**Tihomir Stanoev** — [GitHub](https://github.com/TihomirStanoev)
