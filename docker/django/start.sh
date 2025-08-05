#!/bin/bash

# Function to print messages in green (success)
print_success() {
    echo -e "\e[32m$1\e[0m"  # 32 is the code for green text
}

# Function to print messages in yellow (warning)
print_warning() {
    echo -e "\e[33m$1\e[0m"  # 33 is the code for yellow text
}

# Function to print messages in red (error)
print_error() {
    echo -e "\e[31m$1\e[0m"  # 31 is the code for red text
}

Function to create a manager
create_superuser() {
    if [ ! -z "$DJANGO_SUPERUSER_USERNAME" ] && [ ! -z "$DJANGO_SUPERUSER_PASSWORD" ]; then
        echo "Creating manager..."
        
        # Create the superuser
        python manage.py createsuperuser --noinput  --username "${DJANGO_SUPERUSER_USERNAME}" --email "${DJANGO_SUPERUSER_EMAIL}" &>/dev/null

        # Check if superuser creation was successful
        if [ $? -eq 0 ]; then
            print_success "Manager created successfully."
        else
            print_error "Manager creation failed. It may already exist."
        fi
    else
        print_warning "Manager creation skipped. Please set DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD environment variables."
    fi
}

echo "Making migrations..."
python manage.py makemigrations --noinput 


echo "Applying migrations..."
python manage.py migrate --noinput


create_superuser

echo "Collecting static files..."
python manage.py collectstatic --noinput 

echo "Starting the Django server..."
python manage.py runserver 0.0.0.0:8000