import pandas as pd

def clean_student_data():
    try:
        # 1. Load the CSV file
        df = pd.read_csv('student_data.csv')
        
        # 2. Check for and remove duplicate rows
        initial_count = len(df)
        df = df.drop_duplicates()
        final_count = len(df)
        
        if initial_count > final_count:
            print(f"Removed {initial_count - final_count} duplicate rows.")
        else:
            print("No duplicate rows found.")

        # 3. Categorize 'score' into 'grade'
        def assign_grade(score):
            if score > 85:
                return 'High'
            elif score >= 60:
                return 'Medium'
            else:
                return 'Low'

        df['grade'] = df['score'].apply(assign_grade)

        # 4. Save the result
        output_file = 'cleaned_students.csv'
        df.to_csv(output_file, index=False)
        print(f"\nData successfully saved to {output_file}")

        # 5. Print the first 5 rows
        print("\nFirst 5 rows of cleaned data:")
        print(df.head())

    except FileNotFoundError:
        print("Error: 'student_data.csv' not found. Make sure to run the generation script first.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    clean_student_data()