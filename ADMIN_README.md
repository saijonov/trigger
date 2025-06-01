# Bucket List App - Administrator Guide 🛠️

## Technical Stack

- **Backend**: Django 5.0.4
- **Frontend**: Tailwind CSS
- **Database**: SQLite (default)
- **Authentication**: Django built-in auth
- **File Storage**: Local storage (media files)

## Installation & Setup

### Prerequisites

```bash
# Required system packages
python3.10 or higher
nodejs (for Tailwind CSS)
virtualenv (recommended)
```

### Initial Setup

1. Clone the repository:
```bash
git clone [repository-url]
cd project
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Install Tailwind CSS dependencies:
```bash
python manage.py tailwind install
```

5. Set up the database:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

### Running the Development Server

1. Start the Tailwind CSS build process:
```bash
python manage.py tailwind start
```

2. Run the Django development server:
```bash
python manage.py runserver
```

## Project Structure

```
project/
├── bucket_list/        # Project configuration
├── core/              # Main app
│   ├── models.py      # Data models
│   ├── views.py       # View logic
│   ├── forms.py       # Form definitions
│   ├── urls.py        # URL routing
│   └── tests/         # Test files
├── users/             # User management app
├── templates/         # HTML templates
├── static/           # Static files
└── media/            # User-uploaded files
```

## Administrative Tasks

### Managing Bucket List Items

- Access the staff interface at `/staff/pending/`
- Review and approve/reject suggested items
- Monitor reported content
- Manage user submissions

### User Management

- Create staff accounts through Django admin (`/admin/`)
- Monitor user activity
- Handle user reports and issues

### Content Moderation

1. Reviewing Suggested Items:
   - Visit `/staff/pending/`
   - Review title and description
   - Approve or reject with consideration

2. Managing Completed Items:
   - Monitor photo uploads
   - Check for inappropriate content
   - Review user descriptions

### Backup & Maintenance

1. Database Backup:
```bash
python manage.py dumpdata > backup.json
```

2. Media Files Backup:
```bash
tar -czf media_backup.tar.gz media/
```

## Security Considerations

- Keep `SECRET_KEY` secure
- Regular security updates
- Monitor user uploads
- Implement rate limiting
- Regular backup schedule

## Testing

Run the test suite:
```bash
python manage.py test
```

Test coverage includes:
- Models
- Views
- Forms
- User authentication
- Admin functionality

## Deployment

### Production Settings

1. Update `settings.py`:
```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']
```

2. Configure production database
3. Set up static file serving
4. Configure media file storage
5. Set up SSL certificate

### Server Requirements

- 1GB RAM minimum
- Modern CPU (2+ cores recommended)
- Adequate storage for media files
- Regular backup system

## Monitoring & Maintenance

### Regular Tasks

- Monitor server logs
- Check error reports
- Update dependencies
- Backup database
- Clean old media files

### Performance Monitoring

- Watch database performance
- Monitor file storage
- Check page load times
- Monitor user activity

## Troubleshooting

### Common Issues

1. Tailwind CSS not updating:
   - Restart the Tailwind build process
   - Clear browser cache

2. Media files not showing:
   - Check permissions
   - Verify media root settings

3. Database issues:
   - Check migrations
   - Verify database connections

### Debug Tools

- Django Debug Toolbar
- Server logs
- Browser developer tools

## Support & Resources

- Django Documentation: [docs.djangoproject.com](https://docs.djangoproject.com)
- Tailwind CSS: [tailwindcss.com](https://tailwindcss.com)
- Project Repository: [repository-url]
- Issue Tracker: [issues-url]

## Emergency Contacts

- Technical Lead: [contact]
- Server Admin: [contact]
- Security Team: [contact]

---
Last updated: [date] 