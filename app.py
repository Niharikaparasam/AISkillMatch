from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

students_file = "C:/Users/Niharika PM/OneDrive/Desktop/project/aiskillmatch/students.csv"
courses_file = "C:/Users/Niharika PM/OneDrive/Desktop/project/aiskillmatch/courses.csv"

if os.path.exists(students_file):
    students_df = pd.read_csv(students_file)
else:
 
    students_df = pd.DataFrame(columns=["Name", "Branch", "Goal", "CompletedCourses"])
    students_df.to_csv(students_file, index=False)
if os.path.exists(courses_file):
    courses_df = pd.read_csv(courses_file)
else:
   
    courses_df = pd.DataFrame({
        "Course": ["Advanced Python", "Deep Learning", "Intro to Robotics", "3D Modeling"],
        "Provider": ["Udemy", "Coursera", "edX", "Skillshare"],
        "Difficulty": ["Intermediate", "Advanced", "Beginner", "Intermediate"],
        "Category": ["Programming", "AI", "Robotics", "Design"]
    }
    )
    courses_df.to_csv(courses_file, index=False)

def get_knn_recommendations(student_name, student_branch, student_goal, completed_courses):
    """
    Recommends courses based on the student's branch, goal, and courses completed.
    For new users, this logic generates recommendations by filtering the dataset.
    """
    global students_df  # Access the global students DataFrame

    if student_name in students_df["Name"].values:
        # Old user
        student = students_df[students_df["Name"] == student_name].iloc[0]
        completed_courses_list = student["CompletedCourses"].split(", ")
    else:
        # New user: Add the new user to the dataset
        completed_courses_list = completed_courses.split(", ")
        new_user_data = {
            "Name": student_name,
            "Branch": student_branch,
            "Goal": student_goal,
            "CompletedCourses": ", ".join(completed_courses_list)
        }
        students_df = pd.concat([students_df, pd.DataFrame([new_user_data])], ignore_index=True)
        students_df.to_csv(students_file, index=False)  # Save the updated students dataset

    # Generate recommendations
    recommendations = []
    for _, course in courses_df.iterrows():
        if course["Course"] not in completed_courses_list:
            recommendations.append({
                "name": course["Course"],
                "provider": course["Provider"],
                "difficulty": course["Difficulty"]
            })

    if not recommendations:
        return None, "No new courses to recommend based on your input."
    return recommendations, None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    student_name = request.form.get("student_name", "").strip()
    student_branch = request.form.get("student_branch", "").strip()
    student_goal = request.form.get("student_goal", "").strip()
    completed_courses = request.form.get("completed_courses", "").strip()

    recommendations, error = get_knn_recommendations(
        student_name, student_branch, student_goal, completed_courses
    )

    return render_template("recommendations.html", student_name=student_name, recommendations=recommendations, error=error)

if __name__ == "__main__":
    app.run(debug=True)
