# DSQuest

**DSQuest** is a dynamic and interactive web-based platform designed to help users master data science through hands-on challenges, structured courses, and real-world problem-solving. The platform combines gamification, self-paced learning, and a comprehensive curriculum to make learning data science accessible and engaging for users of all skill levels.

## Core Features
1. Interactive Learning Pathways:
   - Structured courses covering Python, SQL, Pandas, and more.
   - Lesson content includes examples, exercises, and real-world applications.
2. Hands-On Practice:
   - Problem sets categorized by language, difficulty, and topic.
   - Built-in code editor with syntax highlighting and instant feedback.
3. Progress Tracking:
   - Visual progress bars for courses and challenges.
   - Track completed lessons and solved problems.
4. Gamification and Rewards:
   - Earn badges for milestones like solving problems without hints or completing courses.
   - Leaderboards for community engagement.
5. Secure Registration and Login:
   - Two-Factor Authentication (2FA) and Google CAPTCHA for user account protection.
   - User-friendly forms with validation.
6. Subscription Management:
   - Flexible pricing plans: Pro ($29/month) and Premium ($49/year).
   - Secure payment gateway with real-time card validation.
7. Scalable Backend and Responsive Design:
   - Developed using Python (Flask) for scalable backend services.
   - Fully responsive interface using Tailwind CSS for seamless user experience across devices.


## Technologies Used
- Backend: Python and Flask for API and server-side logic.
- Frontend: HTML, CSS, JavaScript, and Tailwind CSS for creating an engaging user interface.
- Database: SQLite for storing user data, progress, challenges, and subscription details.
- Additional Libraries:
    - Pandas and NumPy for data manipulation examples.
    - SQLAlchemy for database interactions.
 

## Key Files and Directories

- **app.yaml**: Used for configuring application settings.
- **requirements.txt**: Contains a list of Python dependencies needed to run the project.
- **Dockerfile**: Enables containerization for easy deployment.
- **app.py**: The main script that handles the core logic of the application.
- **logs/**: Directory where logs are stored, helping with debugging and monitoring.
- **instance/**: Stores Sql Lit database files.
- **portal/**: Houses the core features and functionality of the application.
- **qrdata/**: Manages data related to QR codes.
- **course_images/**: Stores images that are linked to courses within the platform.
- **temp/**: Temporary files used during runtime or development.
- **config/**: Holds additional configuration files required for specific setups.
- **.git/**: Directory for Git version control, containing history and other Git-related data.


## Prerequisites

- **Python** (version 3.7+ recommended)
- **Docker** (if using the containerized setup)
- **Cloud Service** (if deploying to a platform like Google App Engine)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/DSQuest.git
   cd DSQuest

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
3. Install dependencies:
   ```bash
   pip install -r requirements.txt

## Running the Application
- Local :
   ```bash
   python app.py
## Configuration
- Configuration files are located in the config/ directory.
- Ensure environment variables are set for sensitive information like database credentials.
  




