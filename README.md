## django_moneyterm/README.md

## Project Structure

```
django_moneyterm/
│
├── cart_app/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── templates/
│
├── management/commands/
│
├── media/
│
├── orders_app/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── templates/
│
├── payments/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── templates/
│
├── product_app/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── templates/
│
├── project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── static/
│   └── images/
│
├── support_app/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── templates/
│
├── user_app/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── templates/
│
├── db.sqlite3
│
├── manage.py
│
├── README.md
│
├── requirements.txt
│
└── stripe.exe
```
## Description

django_moneyterm is an online prepaid card selling website that uses Stripe for payments. It allows users to view popular prepaid cards, browse through different products, view detailed information about each product, and search for specific products. The application integrates Stripe for seamless and secure payment processing.

## Features

- Browse and search for prepaid cards.
- View detailed information about each product.
- Secure payment processing with Stripe.
- User authentication and profile management.
- Order tracking and history.

## System Requirements

- Python 3.x
- Django 5.x
- SQLite database (included by default with Django)
- Web browser (Chrome, Firefox, Safari, etc.)

## Usage

To install and use django_moneyterm, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/arrkpong/django_moneyterm.git
    ```
2. Navigate to the project directory:
    ```bash
    cd django_moneyterm
    ```
3. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. Run migrations:
    ```bash
    python manage.py migrate
    ```
6. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```
7. Collect static files:
    ```bash
    python manage.py collectstatic
    ```
8. Start the development server:
    ```bash
    python manage.py runserver
    ```
### Setting Up Email Configuration

To enable email functionality in django_moneyterm, follow these steps:

1. Update the `settings.py` file in your Django project with your email backend settings:

    ```python
    # settings.py
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = EMAIL_HOST = 'smtp.your-email-provider.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'your-email@example.com'
    EMAIL_HOST_PASSWORD = 'your-email-password'
    ```

    Replace `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, and `EMAIL_HOST_PASSWORD` with your email provider's SMTP server details and your email credentials.

2. Send a test email to verify your configuration:

    ```bash
    python manage.py sendtestemail recipient@example.com
    ```

    This command will send a test email and confirm whether your email settings are correct.

3. If emails are not being sent, ensure that your email provider allows SMTP connections from your application and that you've correctly configured any necessary security settings.

For further assistance with email configuration, refer to the Django documentation on [sending email](https://docs.djangoproject.com/en/stable/topics/email/).

### Setting Up Stripe Integration

1. **Create a Stripe Account**: If you don't have a Stripe account yet, you can register and create one at the [Stripe website](https://stripe.com/).

2. **Add Stripe API Keys to Django Settings**: Update the `settings.py` file in your Django project with your Stripe API keys: `STRIPE_PUBLIC_KEY`, `STRIPE_SECRET_KEY`, `STRIPE_ENDPOINT_SECRET`.

    ```python
    # settings.py
    STRIPE_PUBLIC_KEY = 'your_stripe_public_key'
    STRIPE_SECRET_KEY = 'your_stripe_secret_key'
    STRIPE_ENDPOINT_SECRET = 'your_stripe_endpoint_secret'
    ```

    Replace `'your_stripe_public_key'`, `'your_stripe_secret_key'`, and `'your_stripe_endpoint_secret'` with the respective keys obtained from your Stripe account dashboard.

3. **Set Up Stripe CLI**:
    - Download and install the Stripe CLI from the [official website](https://stripe.com/docs/stripe-cli).
    - Add the Stripe CLI to your system's PATH to use it from any terminal.

    **For Windows**:
    - Download `stripe.exe` and move it to a directory of your choice.
    - Add the directory to your system PATH.
        ```shell
        setx PATH "%PATH%;C:\path\to\directory"
        ```

    **For macOS and Linux**:
    - Download the appropriate binary for your OS.
    - Move the binary to `/usr/local/bin` or another directory included in your PATH.
        ```shell
        sudo mv stripe /usr/local/bin/
        ```

4. **Authenticate the Stripe CLI with Your Account**:
    ```shell
    stripe login
    ```

5. **Forward Webhook Events to Your Local Server for Testing**:
    ```shell
    stripe listen --forward-to localhost:8000/payments/webhook/
    ```

6. **Trigger an Event to Simulate a Successful Payment**:
    ```shell
    stripe trigger payment_intent.succeeded
    ```

## Testing

To run the tests, use the following command: `python manage.py test`
    
    
## Credits

This project was developed by computer science students from Bangkok University School of Information Technology and Innovation. Special thanks to the Django Thailand Facebook group for their support and contributions.

## Support

For support or inquiries, please contact us via email at arrkpong1@gmail.com.

## Contributing and Collaboration

Contributions to django_moneyterm are welcomed and appreciated! To contribute:

1. Fork the repository.
2. Create your feature branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -am 'Add some feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Submit a pull request.

We encourage contributors of all experience levels to participate. Your help makes a difference!

## Deployment Instructions

To deploy moneyterm_django in a production environment, follow these steps:

1. **Configure Apache/Nginx**: Set up your web server to serve the Django application. Example configurations can be found in the Django documentation.

2. **Set Up Database**: Ensure your database settings (`settings.py`) are configured correctly to connect to your production database.

3. **Configure Form and Authentication Settings**: Adjust form and authentication settings in `settings.py` for production environment security requirements.

4. **Run Django in Production Mode**: Change `DEBUG` setting to `False` in `settings.py` and set appropriate `ALLOWED_HOSTS`.

5. **Collect Static Files**: Use `collectstatic` management command to gather all static files into one directory for production.

6. **Start Application**: Start your Django application using WSGI server of your choice (e.g., Gunicorn) and configure the server to serve the application.

## FAQ

### How do I resolve "Emails Not Sending" issue?

To ensure emails are sent, enable "Less secure app access" in your Google account's Security settings.

### What should I do if I encounter other issues?

For further troubleshooting or to report new issues, please open an issue on our [GitHub repository](https://github.com/arrkpong/django_moneyterm/issues).

## Roadmap

- **Version 1.1 (Upcoming Release)**: Introduce user reviews for products.
- **Version 1.2**: Implement Two-Factor Authentication and Receive Notification.
- **Future Releases**: Enhance mobile responsiveness of the application.

## License

This project is licensed under the MIT License. See the [LICENSE.md](./LICENSE.md) file for more details.

