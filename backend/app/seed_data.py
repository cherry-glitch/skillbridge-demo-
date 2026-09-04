"""
Seed the database with a starter skill taxonomy, three target roles,
an assessment question bank, learning resources, and a handful of
internships — enough to demo the full student flow end-to-end.

Run automatically on startup (see main.py) if the `skills` table is empty,
so `uvicorn app.main:app` alone is enough to get a working demo.
"""
from sqlalchemy.orm import Session

from . import models


SKILLS = [
    # name, category
    ("Embedded C", "Embedded"),
    ("ESP32", "Embedded"),
    ("MQTT", "Embedded"),
    ("RTOS", "Embedded"),
    ("Linux", "Systems"),
    ("AWS IoT", "Cloud"),
    ("Python", "Core CS"),
    ("JavaScript", "Core CS"),
    ("Data Structures & Algorithms", "Core CS"),
    ("Git", "Tools"),
    ("REST APIs", "Backend"),
    ("React", "Frontend"),
    ("Node.js", "Backend"),
    ("System Design", "Core CS"),
    ("SQL", "Data"),
    ("Pandas", "Data"),
    ("Statistics", "Data"),
    ("Data Visualization", "Data"),
    ("Machine Learning Basics", "Data"),
    ("Docker", "DevOps"),
]

ROLES = {
    "IoT Engineer": {
        "description": "Builds embedded firmware and connects devices to the cloud.",
        "skills": {
            "Embedded C": 5, "ESP32": 5, "MQTT": 4, "RTOS": 4,
            "Linux": 3, "AWS IoT": 3,
        },
    },
    "Software Developer": {
        "description": "Builds and ships full-stack web applications.",
        "skills": {
            "Python": 4, "JavaScript": 4, "Data Structures & Algorithms": 5,
            "Git": 3, "REST APIs": 4, "React": 3, "Node.js": 3, "System Design": 3,
        },
    },
    "Data Analyst": {
        "description": "Turns raw data into decisions using SQL, stats and visualization.",
        "skills": {
            "SQL": 5, "Pandas": 4, "Statistics": 4,
            "Data Visualization": 4, "Python": 3, "Machine Learning Basics": 2,
        },
    },
}

# 2 MCQs per skill: (skill_name, prompt, a, b, c, d, correct_letter, difficulty)
QUESTIONS = [
    ("Embedded C", "In embedded C, what does 'volatile' tell the compiler about a variable?",
     "It can be optimized away", "Its value may change outside normal program flow",
     "It is a constant", "It must be stored in ROM", "b", 2),
    ("Embedded C", "Which header is typically used for fixed-width integer types (uint8_t, uint32_t)?",
     "stdint.h", "stdlib.h", "string.h", "limits.h", "a", 1),

    ("ESP32", "What are the two processor cores on a standard ESP32 typically used for?",
     "Graphics and audio only", "One for Wi-Fi/BT stack, one free for app tasks",
     "Both are disabled by default", "Only used for Bluetooth", "b", 2),
    ("ESP32", "Which built-in wireless capability does ESP32 have, in addition to Wi-Fi?",
     "Zigbee only", "Bluetooth (Classic + BLE)", "LTE", "LoRa", "b", 1),

    ("MQTT", "What is the role of the 'broker' in an MQTT system?",
     "It stores firmware updates", "It routes messages between publishers and subscribers",
     "It compiles the device code", "It only sends SMS alerts", "b", 1),
    ("MQTT", "What does QoS level 1 guarantee in MQTT?",
     "Exactly once delivery", "At least once delivery",
     "No delivery guarantee", "Delivery only to the broker", "b", 2),

    ("RTOS", "What is the main purpose of an RTOS in an embedded system?",
     "To provide a desktop GUI", "To schedule multiple tasks with predictable timing",
     "To replace the compiler", "To manage cloud billing", "b", 2),
    ("RTOS", "In FreeRTOS, what is a 'task' most similar to?",
     "A lightweight thread with its own stack", "A database record",
     "A network packet", "A compiler flag", "a", 2),

    ("Linux", "Which command shows currently running processes on Linux?",
     "ls -l", "ps aux", "cd /proc", "chmod +x", "b", 1),
    ("Linux", "What does 'chmod +x script.sh' do?",
     "Deletes the script", "Makes the script executable",
     "Compiles the script", "Moves the script", "b", 1),

    ("AWS IoT", "What does AWS IoT Core primarily provide?",
     "A managed MQTT message broker for connecting devices",
     "A video streaming service", "A spreadsheet tool", "A DNS registrar", "a", 2),
    ("AWS IoT", "What is a 'Thing' in AWS IoT terminology?",
     "A billing plan", "A representation of a physical device in the cloud",
     "A Lambda function", "A CSS class", "b", 1),

    ("Python", "What does the following return: len([1, 2, 3])?",
     "2", "3", "Error", "None", "b", 1),
    ("Python", "Which keyword defines a function in Python?",
     "func", "def", "function", "lambda only", "b", 1),

    ("JavaScript", "What does '===' check in JavaScript, unlike '=='?",
     "Only value, ignoring type", "Value AND type (strict equality)",
     "Only type", "Nothing, they're identical", "b", 2),
    ("JavaScript", "What will typeof [] return in JavaScript?",
     "'array'", "'object'", "'list'", "'undefined'", "b", 2),

    ("Data Structures & Algorithms", "What is the average time complexity of binary search on a sorted array?",
     "O(n)", "O(log n)", "O(n^2)", "O(1)", "b", 2),
    ("Data Structures & Algorithms", "Which data structure uses LIFO (last in, first out) ordering?",
     "Queue", "Stack", "Linked List", "Graph", "b", 1),

    ("Git", "What does 'git commit' do?",
     "Uploads code to a website", "Records a snapshot of staged changes locally",
     "Deletes the repository", "Creates a new branch automatically", "b", 1),
    ("Git", "What is the purpose of 'git branch'?",
     "To list/create isolated lines of development", "To delete the whole repo",
     "To compile the project", "To send an email", "a", 1),

    ("REST APIs", "Which HTTP method is typically used to update an existing resource?",
     "GET", "PUT/PATCH", "DELETE only", "OPTIONS", "b", 1),
    ("REST APIs", "What does a 404 HTTP status code mean?",
     "Server error", "Resource not found", "Success", "Unauthorized", "b", 1),

    ("React", "What is the purpose of the useState hook in React?",
     "To fetch data from a server only", "To add local state to a function component",
     "To style components", "To route between pages", "b", 2),
    ("React", "What does JSX allow you to write directly inside JavaScript?",
     "SQL queries", "HTML-like markup", "CSS-only files", "Python code", "b", 1),

    ("Node.js", "What is Node.js primarily used for?",
     "Running JavaScript on the server", "Styling web pages",
     "Only running in the browser", "Managing databases exclusively", "a", 1),
    ("Node.js", "Which built-in Node.js module is commonly used to create an HTTP server?",
     "fs", "http", "path", "os", "b", 1),

    ("System Design", "What does 'horizontal scaling' mean?",
     "Adding more machines to share load", "Upgrading a single machine's CPU",
     "Reducing the number of servers", "Only applies to databases", "a", 2),
    ("System Design", "What is the main purpose of a load balancer?",
     "To store files permanently", "To distribute incoming traffic across multiple servers",
     "To compile code", "To encrypt passwords only", "b", 2),

    ("SQL", "Which SQL clause is used to filter rows before grouping?",
     "HAVING", "WHERE", "ORDER BY", "GROUP", "b", 1),
    ("SQL", "What does a JOIN do in SQL?",
     "Deletes a table", "Combines rows from two or more tables based on a related column",
     "Creates an index", "Encrypts data", "b", 2),

    ("Pandas", "What does df.head() do in pandas?",
     "Returns the last 5 rows", "Returns the first 5 rows by default",
     "Deletes the dataframe", "Sorts the dataframe", "b", 1),
    ("Pandas", "Which pandas method is used to handle missing values by removing them?",
     "fillna()", "dropna()", "isnull()", "describe()", "b", 1),

    ("Statistics", "What does the 'mean' of a dataset represent?",
     "The middle value", "The average value", "The most frequent value", "The range", "b", 1),
    ("Statistics", "What does a low p-value (< 0.05) typically suggest in hypothesis testing?",
     "Strong evidence against the null hypothesis", "The data is invalid",
     "The sample size was too small", "Nothing statistically", "a", 2),

    ("Data Visualization", "Which chart type is best suited for showing trends over time?",
     "Pie chart", "Line chart", "Scatter plot only", "Heatmap only", "b", 1),
    ("Data Visualization", "What is the main risk of a poorly scaled bar chart axis?",
     "It can visually exaggerate or hide differences", "It always crashes the tool",
     "It removes the data", "None, axis scale doesn't matter", "a", 2),

    ("Machine Learning Basics", "What is 'overfitting' in machine learning?",
     "A model performs well on training data but poorly on new data",
     "A model that trains too fast", "A dataset with too few features",
     "A model with no parameters", "a", 2),
    ("Machine Learning Basics", "Which of these is a supervised learning task?",
     "Clustering with no labels", "Predicting house prices from labeled data",
     "Random data generation", "Data cleaning", "b", 1),

    ("Docker", "What is a Docker container?",
     "A virtual machine with its own OS kernel", "A lightweight, isolated unit that packages an app and its dependencies",
     "A database engine", "A programming language", "b", 2),
    ("Docker", "What does a Dockerfile define?",
     "Network firewall rules", "The steps to build a Docker image",
     "User passwords", "A CSS stylesheet", "b", 1),
]

# resources: (skill_name, title, provider, url, type, est_hours)
RESOURCES = [
    ("Embedded C", "Embedded C Programming Essentials", "NPTEL", "https://nptel.ac.in", "course", 20),
    ("Embedded C", "Build a Sensor Logger in C", "Self-project", "", "project", 8),
    ("ESP32", "ESP32 for IoT Developers", "Udemy", "https://udemy.com", "course", 15),
    ("MQTT", "MQTT Essentials", "HiveMQ", "https://hivemq.com/mqtt-essentials", "article", 3),
    ("RTOS", "Mastering FreeRTOS", "Coursera", "https://coursera.org", "course", 18),
    ("Linux", "Linux Command Line Basics", "freeCodeCamp", "https://freecodecamp.org", "course", 10),
    ("AWS IoT", "AWS IoT Core Getting Started", "AWS Skill Builder", "https://aws.amazon.com/training", "course", 12),
    ("Python", "Python for Everybody", "Coursera", "https://coursera.org", "course", 25),
    ("JavaScript", "JavaScript: The Hard Parts", "Frontend Masters", "https://frontendmasters.com", "course", 15),
    ("Data Structures & Algorithms", "DSA Practice Track", "LeetCode", "https://leetcode.com", "practice", 40),
    ("Git", "Git & GitHub Crash Course", "freeCodeCamp", "https://freecodecamp.org", "course", 5),
    ("REST APIs", "Designing RESTful APIs", "Postman Academy", "https://academy.postman.com", "course", 8),
    ("React", "React Official Tutorial", "react.dev", "https://react.dev/learn", "course", 15),
    ("Node.js", "Node.js: The Complete Guide", "Udemy", "https://udemy.com", "course", 20),
    ("System Design", "System Design Primer", "GitHub", "https://github.com/donnemartin/system-design-primer", "article", 15),
    ("SQL", "SQL for Data Analysis", "Mode Analytics", "https://mode.com/sql-tutorial", "course", 12),
    ("Pandas", "Pandas Official 10-min Guide", "pandas.pydata.org", "https://pandas.pydata.org/docs", "article", 4),
    ("Statistics", "Statistics with Python", "Khan Academy", "https://khanacademy.org", "course", 15),
    ("Data Visualization", "Storytelling with Data", "Book/Practice", "", "article", 10),
    ("Machine Learning Basics", "Machine Learning Crash Course", "Google", "https://developers.google.com/machine-learning/crash-course", "course", 20),
    ("Docker", "Docker for Beginners", "Docker Docs", "https://docs.docker.com/get-started", "course", 8),
]

# internships: (title, company, description, location, stipend, skills{name: weight})
INTERNSHIPS = [
    ("Embedded Systems Intern", "BoschTech Labs",
     "Work on firmware for sensor nodes and help bring up new hardware revisions.",
     "Bengaluru", "₹15,000/month",
     {"Embedded C": 5, "ESP32": 4, "RTOS": 3, "Linux": 2}),
    ("IoT Cloud Developer Intern", "Jio Platforms",
     "Connect field devices to the cloud and build device telemetry pipelines.",
     "Mumbai", "₹20,000/month",
     {"MQTT": 4, "AWS IoT": 5, "Linux": 3, "Python": 2}),
    ("Frontend Developer Intern", "Zoho Corp",
     "Build and ship UI features for a production SaaS product used by millions.",
     "Chennai", "₹18,000/month",
     {"JavaScript": 5, "React": 5, "Git": 3, "REST APIs": 2}),
    ("Backend Developer Intern", "Freshworks",
     "Design and build backend services and APIs powering customer support tools.",
     "Chennai", "₹20,000/month",
     {"Node.js": 4, "REST APIs": 4, "SQL": 3, "Git": 2, "System Design": 3}),
    ("Data Analyst Intern", "Flipkart",
     "Analyze marketplace data and build dashboards to guide business decisions.",
     "Bengaluru", "₹22,000/month",
     {"SQL": 5, "Pandas": 4, "Statistics": 4, "Data Visualization": 3}),
    ("Full-Stack Developer Intern", "Razorpay",
     "Ship end-to-end features across a React frontend and Node.js backend.",
     "Bengaluru", "₹25,000/month",
     {"JavaScript": 4, "React": 3, "Node.js": 4, "SQL": 2, "Git": 2}),
]


def seed_if_empty(db: Session) -> None:
    if db.query(models.Skill).count() > 0:
        return  # already seeded

    skill_by_name = {}
    for name, category in SKILLS:
        s = models.Skill(name=name, category=category)
        db.add(s)
        skill_by_name[name] = s
    db.flush()

    for role_name, data in ROLES.items():
        role = models.Role(name=role_name, description=data["description"])
        db.add(role)
        db.flush()
        for skill_name, weight in data["skills"].items():
            db.add(models.RoleSkill(role_id=role.id, skill_id=skill_by_name[skill_name].id, weight=weight))

    for skill_name, prompt, a, b, c, d, correct, difficulty in QUESTIONS:
        db.add(models.Question(
            skill_id=skill_by_name[skill_name].id, prompt=prompt,
            option_a=a, option_b=b, option_c=c, option_d=d,
            correct_option=correct, difficulty=difficulty,
        ))

    for skill_name, title, provider, url, rtype, hours in RESOURCES:
        db.add(models.Resource(
            skill_id=skill_by_name[skill_name].id, title=title, provider=provider,
            url=url, resource_type=rtype, est_hours=hours,
        ))

    for title, company, desc, location, stipend, skills in INTERNSHIPS:
        internship = models.Internship(
            title=title, company=company, description=desc,
            location=location, stipend=stipend,
        )
        db.add(internship)
        db.flush()
        for skill_name, weight in skills.items():
            db.add(models.InternshipSkill(
                internship_id=internship.id, skill_id=skill_by_name[skill_name].id, weight=weight,
            ))

    db.commit()
