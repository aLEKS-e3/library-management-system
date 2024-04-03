# Library Management System
This project is a comprehensive Library Management System that provides various functionalities for efficiently managing a library's operations. It is a web-based system that offers features such as managing the books inventory, handling book borrowings, managing customer information, displaying notifications, and handling payments seamlessly. Below are the key components and features implemented in this system:

## Features Implemented:
* JWT Authorization
* Telegram Bot Integration
* Stripe Payments
* Different Levels of Permissions
* Filtering
* Documentation
* Browsable API

## Functionalities:
* Manage Books Inventory: Add, update, or remove books from the library inventory, including details such as title, author, and inventory status.
* Manage Books Borrowing: Track book borrowings, issue and return books, manage due dates, and send notifications to administrators regarding overdue books.
* Manage Customers: Maintain customer records, including personal details, contact information, and borrowing history.
* Display Notifications: Send notifications to users via Telegram Bot regarding book availability, due dates, overdue reminders, and other relevant updates.
* Handle Payments: Process payments securely using Stripe for new book borrowings and overdue fees, providing a convenient payment solution for users.

## Technologies Used:
* Backend: Django Rest Framework
* Database: PostgreSQL
* Authentication: JSON Web Tokens (JWT)
* Notifications: Telegram API
* Payments: Stripe API

## Installation:
Clone the repository:

```bash
git clone https://github.com/aLEKS-e3/library-management-system.git
cd library-management-system
```

Create a .env file in the root directory.
Add necessary environment variables such as Stripe API keys, Telegram Bot token, etc.

### Run the application using Docker:

```bash
docker-compose build
docker-compose up
```
## License:
This project is licensed under the MIT License.