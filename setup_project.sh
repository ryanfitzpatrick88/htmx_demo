#!/bin/bash

# Create directories
mkdir -p app/api/dependencies
mkdir -p app/api/routes
mkdir -p app/core
mkdir -p app/crud
mkdir -p app/models
mkdir -p app/schemas
mkdir -p app/services
mkdir -p app/templates
mkdir -p static/css
mkdir -p data

# Create initial Python files
touch app/__init__.py
touch app/api/__init__.py
touch app/api/dependencies/__init__.py
touch app/api/routes/__init__.py
touch app/api/routes/auth.py
touch app/api/routes/dashboard.py
touch app/core/config.py
touch app/core/security.py
touch app/crud/__init__.py
touch app/models/__init__.py
touch app/models/user.py
touch app/schemas/__init__.py
touch app/services/__init__.py
touch app/services/auth_service.py
touch main.py

# Create initial template files
echo "<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>{% block title %}{% endblock %}</title>
    <link href='/static/css/tailwind.css' rel='stylesheet'>
</head>
<body>
    <header>{% block header %}{% endblock %}</header>
    <nav>{% block nav %}{% endblock %}</nav>
    <main>{% block content %}{% endblock %}</main>
    <footer>{% block footer %}{% endblock %}</footer>
</body>
</html>" > app/templates/base.html

echo "{% extends 'base.html' %}
{% block title %}Login{% endblock %}
{% block content %}
<div>Login Form Here</div>
{% endblock %}" > app/templates/login.html

echo "{% extends 'base.html' %}
{% block title %}Dashboard{% endblock %}
{% block content %}
<div>Dashboard Content Here</div>
{% endblock %}" > app/templates/dashboard.html

# Create a placeholder for the CSS file
echo "/* Add your Tailwind CSS here */" > static/css/style.css

echo "Project structure created successfully."
