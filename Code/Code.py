import csv
import random
from datetime import datetime, timedelta
from faker import Faker

# Initialize Faker
fake = Faker()

# Configuration
filename = 'student_data.csv'
num_rows = 100
subjects = ['Math', 'Science', 'History', 'English']

def generate_random_date(year=2024):
    """Generates a random date within the given year."""
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    return random_date.strftime("%Y-%m-%d")

def generate_data():
    data = []
    for i in range(1, num_rows + 1):
        # Create a formatted Student ID (e.g., STU001)
        student_id = f"STU{i:03d}"
        
        name = fake.name()
        subject = random.choice(subjects)
        
        # Generate score (skewed slightly towards higher scores for realism)
        score = random.randint(35, 100) 
        
        date = generate_random_date(2024)
        
        # Generate attendance (realistic range between 60% and 100%)
        attendance = random.randint(60, 100)
        
        data.append([student_id, name, subject, score, date, attendance])
    return data

def write_csv(filename, data):
    headers = ['student_id', 'name', 'subject', 'score', 'date', 'attendance']
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)
    
    print(f"Successfully generated {filename} with {len(data)} rows.")

if __name__ == "__main__":
    student_data = generate_data()
    write_csv(filename, student_data)