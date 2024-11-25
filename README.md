
# Matrimonial Software

This project is a matrimonial platform that enables users to create profiles, manage preferences, send messages, and express interest in potential matches. It includes various features for user management, notifications, and data tracking.

## Features

1. **User Management**:
   - Registration, login, and authentication of users.
   - Profile management through the `user_profile` app.

2. **Match Interest**:
   - Allows users to express interest in other users via the `match_interest` module.

3. **User Preferences**:
   - Users can define their preferences using the `user_preference` app.

4. **Messaging**:
   - A messaging system implemented in the `message` module for communication between users.

5. **Notifications**:
   - Real-time and batch notifications handled by the `notification` module.

6. **Admin Management**:
   - Standardized tables and utilities for managing application-wide data (`tables` and `utils` apps).

7. **Media Management**:
   - A `media` folder for handling uploaded content.

## Project Structure

- **`match_interest/`**: Handles user interest features.
- **`Matrimonial_sw/`**: Core Django project settings and configurations.
- **`media/`**: Stores uploaded media files.
- **`message/`**: Contains functionality for user communication.
- **`notification/`**: Manages notifications for users.
- **`scripts/`**: Holds custom scripts for specific tasks.
- **`tables/`**: Standardized tables for managing choices and other reusable data.
- **`user/`**: Manages user authentication and roles.
- **`user_preference/`**: Handles user-specific preferences.
- **`user_profile/`**: Manages user profile details and data.
- **`utils/`**: Contains utility functions.
- **`db.sqlite3`**: The SQLite database file for development purposes.
- **`manage.py`**: Django's command-line utility for administrative tasks.
- **`user_icon.jpg`**: Default icon for users.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/manuhari05/Matrimony-trail.git
   cd matrimonial-trail
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # For Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser for admin access:
   ```bash
   python manage.py createsuperuser
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the application at `http://127.0.0.1:8000`.

## Usage

1. Register as a new user or log in with the admin credentials.
2. Update your profile and define preferences.
3. Express interest in other users, send messages, and receive notifications.
4. Admins can manage standardized tables, monitor user activity, and customize options.
