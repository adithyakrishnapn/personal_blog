# Personal Blog Application

A full-featured blog platform built with Django and MongoDB, allowing users to create, read, update, and delete blog posts with user authentication.

## Features

- 📝 Create, edit, and delete blog posts
- 👤 User authentication (signup, login, logout)
- 📱 Responsive design
- 🔒 Session-based authentication
- 📊 Chronological blog post listing
- 🎨 Clean and intuitive UI

## Tech Stack

- **Backend Framework:** Django 3.1.12
- **Database:** MongoDB (via djongo and pymongo)
- **WSGI Server:** Gunicorn
- **Static Files:** WhiteNoise
- **Python Version:** 3.12

## Prerequisites

- Python 3.12
- MongoDB Atlas account or local MongoDB instance
- Git

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/adithyakrishnapn/personal_blog.git
cd personal_blog
```

### 2. Create Virtual Environment

```bash
python -m venv .venv

# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/dbname
DB_NAME=your_database_name
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Configure MongoDB

Update your `settings.py` or ensure your MongoDB connection is properly configured:

```python
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': os.environ.get('DB_NAME', 'blog_db'),
        'CLIENT': {
            'host': os.environ.get('MONGODB_URI'),
            'serverSelectionTimeoutMS': 5000,
        }
    }
}
```

### 6. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

## Project Structure

```
personal_blog/
├── blog/                   # Main blog application
│   ├── views.py           # View functions for blog operations
│   ├── db.py              # MongoDB connection utilities
│   ├── middleware.py      # Custom middleware
│   ├── templates/         # HTML templates
│   └── urls.py            # URL routing
├── static/                # Static files (CSS, JS, images)
├── requirements.txt       # Python dependencies
├── manage.py             # Django management script
├── deploy.sh             # Deployment script
└── .python-version       # Python version specification
```

## API Endpoints

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/` | GET | Homepage with all blogs | No |
| `/add/` | GET/POST | Add new blog post | Required |
| `/view/<id>/` | GET | View single blog post | No |
| `/edit/<id>/` | GET/POST | Edit blog post | Required |
| `/delete/<id>/` | POST | Delete blog post | Required |
| `/blogs/` | GET | List all blogs | Required |
| `/signup/` | GET/POST | User registration | No |
| `/login/` | GET/POST | User login | No |
| `/logout/` | GET | User logout | Required |

## Database Schema

### Blogs Collection

```javascript
{
  _id: ObjectId,
  title: String,
  content: String,
  created_at: DateTime,
  updated_at: DateTime
}
```

### Users Collection

```javascript
{
  _id: ObjectId,
  username: String,
  email: String,
  password: String,  // Note: Should be hashed in production
  created_at: DateTime
}
```

## Deployment

### Deploy to Render

1. **Create `.python-version` file:**
   ```
   3.12
   ```

2. **Set Environment Variables in Render:**
   - `SECRET_KEY`: Your Django secret key
   - `DEBUG`: False
   - `MONGODB_URI`: Your MongoDB connection string
   - `DB_NAME`: Your database name
   - `ALLOWED_HOSTS`: your-app.onrender.com

3. **Configure Build Command:**
   ```bash
   bash deploy.sh
   ```

4. **Configure Start Command:**
   ```bash
   gunicorn your_project.wsgi:application
   ```

### MongoDB Atlas Setup

1. Create a free cluster at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a database user
3. Whitelist IP addresses (use `0.0.0.0/0` for Render)
4. Get your connection string
5. Add it to your environment variables

## Security Notes

⚠️ **Important Security Improvements Needed:**

1. **Password Hashing:** Currently passwords are stored in plain text. Implement proper password hashing:
   ```python
   from django.contrib.auth.hashers import make_password, check_password
   ```

2. **CSRF Protection:** Ensure all forms have `{% csrf_token %}`

3. **Input Validation:** Add proper form validation

4. **Environment Variables:** Never commit `.env` file to version control

5. **Django Version:** Consider upgrading to Django 4.2 LTS for better security

## Common Issues

### Issue: `ModuleNotFoundError: No module named 'cgi'`
**Solution:** Use Python 3.12 instead of 3.13. Create `.python-version` file with `3.12`

### Issue: MongoDB Connection Timeout
**Solution:** 
- Check your `MONGODB_URI` environment variable
- Verify MongoDB Atlas IP whitelist includes `0.0.0.0/0`
- Ensure your connection string is correct

### Issue: Worker Timeout in Production
**Solution:** Increase Gunicorn timeout in `gunicorn.conf.py`:
```python
timeout = 120
workers = 2
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Author

**Adithya Krishna PN**
- GitHub: [@adithyakrishnapn](https://github.com/adithyakrishnapn)

## Acknowledgments

- Django Documentation
- MongoDB Documentation
- Render Deployment Guides

## Support

For issues and questions, please open an issue on GitHub or contact the maintainer.

---

**Note:** This is a learning project. For production use, implement proper security measures including password hashing, HTTPS, rate limiting, and regular security audits.