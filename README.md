# Recipe Cookbook Management System

A Django REST API for managing recipes, cookbooks, authors, and ingredients. This application provides a comprehensive system for organizing culinary content with JWT authentication.

## Features

- **User Management**: Custom user model with email-based authentication
- **Recipe Management**: Create and manage recipes with difficulty levels (Easy, Intermediate, Hard)
- **Cookbook Organization**: Group recipes into cookbooks with recipe count tracking
- **Ingredient Tracking**: Manage ingredients and their associations with recipes
- **Author Profiles**: User profiles linked to recipes and cookbooks
- **REST API**: Full RESTful API with Django REST Framework
- **Query Filtering**: Filter recipes and cookbooks by title and description
- **JWT Authentication**: Secure token-based authentication using SimpleJWT
- **API Documentation**: Interactive Swagger/OpenAPI documentation
- **Admin Interface**: Django admin panel for easy data management
- **Type Safety**: django-stubs for improved IDE support and type checking

## Technology Stack

- **Framework**: Django 6.0
- **API**: Django REST Framework 3.16.1
- **Authentication**: djangorestframework-simplejwt
- **API Documentation**: drf-yasg (Swagger/OpenAPI)
- **Type Checking**: django-stubs (for IDE support)
- **Database**: SQLite3 (Development)
- **Python**: 3.x

## Project Structure
```
RecipeCookbokManagement/
├── author/                      # Author profiles
├── cookbook/                    # Cookbook management
├── ingredient/                  # Ingredient management
├── recipe/                      # Recipe management
├── registration_profile/        # User registration
├── user/                        # Custom user model
├── recipe_cookbok_management/   # Project settings
├── templates/                   # HTML templates
├── db.sqlite3                   # Database file
└── manage.py                    # Django management script
```

## Models

### User
- Custom user model with email as username field
- Extends Django's AbstractUser

### Author
- One-to-one relationship with User
- Manages author profiles for recipes and cookbooks

### Recipe
- Title, difficulty level, timestamps
- Foreign key to Author
- Favorite flag for marking preferred recipes

### Cookbook
- Title, description, timestamps
- Many-to-many relationship with Recipes
- Foreign key to Author
- Computed field: `recipe_count` (number of recipes in cookbook)

### Ingredient
- Title and description
- Many-to-many relationship with Recipes

## API Endpoints

### Authentication
- `POST /api/token/` - Obtain JWT token pair
- `POST /api/token/refresh/` - Refresh access token
- `POST /api/token/verify/` - Verify token validity

### Resources
- `/api/registration-profiles/` - User registration
- `/api/authors/` - Author management
- `/api/cookbooks/` - Cookbook CRUD operations
- `/api/recipes/` - Recipe CRUD operations
- `/api/users/` - User management
- `/admin/` - Django admin interface

### Query Parameters & Filtering

The API supports filtering on list endpoints using query parameters:

**Recipes** (`/api/recipes/`):
- `?title=str` - Filter recipes by title (case-insensitive partial match)

**Cookbooks** (`/api/cookbooks/`):
- `?title=str` - Filter cookbooks by title (case-insensitive partial match)
- `?description=str` - Filter cookbooks by description (case-insensitive partial match)

**Example:**
```bash
GET /api/recipes/?title=pasta
GET /api/cookbooks/?title=italian&description=traditional
```

### API Documentation
- `/swagger/` - Swagger UI (interactive API documentation)
- `/redoc/` - ReDoc UI (alternative API documentation)
- `/swagger.json` - OpenAPI schema in JSON format
- `/swagger.yaml` - OpenAPI schema in YAML format

## Installation

1. **Clone the repository**
```bash
   git clone <repository-url>
   cd RecipeCookbokManagement
```

2. **Create a virtual environment**
```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

   Or install manually:
```bash
   pip install django djangorestframework djangorestframework-simplejwt drf-yasg django-stubs
```

4. **Apply migrations**
```bash
   python manage.py migrate
```

5. **Create user groups** (if custom management command exists)
```bash
   python manage.py create_groups
```

6. **Create a superuser**
```bash
   python manage.py createsuperuser
```

7. **Run the development server**
```bash
   python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## Configuration

### JWT Settings
- Access token lifetime: 5 days
- Refresh token lifetime: 30 days

### Database
- Default: SQLite3 (`db.sqlite3`)
- For production, configure PostgreSQL or MySQL in `settings.py`

### Authentication
- JWT authentication required for all endpoints (except registration and token endpoints)
- Configure in `REST_FRAMEWORK` settings

## Development

### Virtual Environment
This project uses Python virtual environments (`venv`). Always activate the virtual environment before working:

```bash
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows
```

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Access Admin Panel
Navigate to `http://127.0.0.1:8000/admin/` and login with superuser credentials.

## Security Notes

⚠️ **Important**: Before deploying to production:
- Change `SECRET_KEY` in `settings.py`
- Set `DEBUG = False`
- Configure `ALLOWED_HOSTS`
- Use environment variables for sensitive data
- Set up a production-ready database (PostgreSQL/MySQL)
- Configure HTTPS
- Set up proper CORS settings if needed

## License

This project is for educational purposes.