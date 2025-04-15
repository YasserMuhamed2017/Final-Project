# Final Project

## Overview
This is a crowdfunding platform built using Django. The platform allows users to create and manage campaigns, make donations, and interact with other users through comments and ratings. It also includes features for reporting inappropriate content and managing user profiles.

## Features
- User authentication and profile management
- Campaign creation and management
- Donation tracking
- Commenting and rating on campaigns
- Reporting inappropriate content
- Custom filters for templates

## Project Structure
- `finalproject/`: Contains the main project settings and configurations.
- `funding/`: Contains the core app for the crowdfunding platform, including models, views, forms, and templates.
- `media/`: Stores uploaded media files such as campaign images and profile pictures.
- `static/`: Contains static files for the project.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd Final-Project-master/finalproject
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
5. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Usage
1. Access the application in your web browser at `http://127.0.0.1:8000/`.
2. Register a new account or log in with an existing account.
3. Create, view, and manage campaigns.
4. Make donations and interact with other users through comments and ratings.

## Models

The project uses Django's ORM to define the following models:

### UserProfile
- Extends the default Django user model to include additional fields such as `birth_date`, `country`, and `profile_picture`.

### Category
- Represents categories for campaigns, allowing users to filter and organize campaigns by type.

### Project
- Represents a crowdfunding campaign with fields such as `title`, `description`, `goal_amount`, `current_amount`, `start_date`, `end_date`, and `category`.
- Includes a `reported` field to track campaigns flagged for inappropriate content.

### CampaignImage
- Stores images associated with a campaign.

### Donation
- Tracks donations made by users to specific campaigns, including the `amount` and `date` of the donation.

### Comment
- Allows users to leave comments on campaigns, with fields for `content`, `author`, and `timestamp`.
- Includes a `reported` field to track inappropriate comments.

### Rating
- Enables users to rate campaigns, with fields for `score` and `user`.

## Relationships
- `UserProfile` is linked to the default Django user model via a one-to-one relationship.
- `Project` is linked to `Category` via a foreign key.
- `Donation`, `Comment`, and `Rating` are linked to `Project` via foreign keys.
- `Comment` and `Rating` are also linked to `UserProfile` via foreign keys.

## Team
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## Team Members
- Abdullah Mahany Kamal Mahany
- Andrew Essam Amin
- Mohammed Ali Ahmed ElGhannam
- Omar Sadek Fathy Alazhary
- Yasser Mohamed Metwally Salem

## License
This project is licensed under ITI License.
