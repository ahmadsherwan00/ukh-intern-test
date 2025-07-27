
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()





class StudentLoginInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    school = db.Column(db.String(50), nullable=False)
    program = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Student {self.email} - {self.school}/{self.program}>"


class ExpectationEssay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100))
    school_programme = db.Column(db.String(150))
    student_id = db.Column(db.String(50))
    essay = db.Column(db.Text)


class ConflictOfInterestForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Section A: Personal and Internship Info
    full_name = db.Column(db.String(100))
    student_id = db.Column(db.String(50))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    organization_name = db.Column(db.String(100))
    internship_position = db.Column(db.String(100))
    internship_supervisor = db.Column(db.String(100))
    start_date = db.Column(db.String(50))
    end_date = db.Column(db.String(50))

    # Section B
    q1 = db.Column(db.Text)
    q2 = db.Column(db.Text)
    q3 = db.Column(db.Text)
    q4 = db.Column(db.Text)
    q5 = db.Column(db.Text)

    # Section C
    q6 = db.Column(db.Text)

    # Section D
    management_description = db.Column(db.Text)
    action1 = db.Column(db.String(255))
    action2 = db.Column(db.String(255))
    action3 = db.Column(db.String(255))

    # Section E
    agree_disclose = db.Column(db.Boolean)
    agree_confidential = db.Column(db.Boolean)
    agree_advantage = db.Column(db.Boolean)
    agree_recuse = db.Column(db.Boolean)
    agree_policies = db.Column(db.Boolean)
    agree_consequences = db.Column(db.Boolean)

    # Section F
    student_signature = db.Column(db.String(100))
    signature_date = db.Column(db.String(50))

class LearningContract(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Part I - Contact Info
    student_name = db.Column(db.String(100))
    student_id = db.Column(db.String(50))
    class_year = db.Column(db.String(20))
    home_address = db.Column(db.String(150))
    student_phone = db.Column(db.String(30))
    emergency_contact = db.Column(db.String(100))
    student_email = db.Column(db.String(100))
    personality_note = db.Column(db.Text)

    supervisor_name = db.Column(db.String(100))
    supervisor_title = db.Column(db.String(100))
    supervisor_phone = db.Column(db.String(30))
    work_relevance = db.Column(db.Text)
    organization = db.Column(db.String(100))
    internship_address = db.Column(db.String(150))
    supervisor_email = db.Column(db.String(100))

    # Part II - Academic Info
    internship_title = db.Column(db.String(100))
    department = db.Column(db.String(100))
    begin_date = db.Column(db.String(30))
    end_date = db.Column(db.String(30))
    internship_paid = db.Column(db.String(10))

    # Part III - Objectives
    primary_objective = db.Column(db.Text)
    secondary_objective = db.Column(db.Text)
    skills_objective = db.Column(db.Text)

    # Part VI - Terms
    agree_attendance = db.Column(db.Boolean)
    agree_conduct = db.Column(db.Boolean)
    agree_confidentiality = db.Column(db.Boolean)
    agree_policies = db.Column(db.Boolean)
    agree_communication = db.Column(db.Boolean)

    # Part VII - Signatures
    student_signature = db.Column(db.String(100))
    student_date = db.Column(db.String(30))
    supervisor_signature = db.Column(db.String(100))
    supervisor_date = db.Column(db.String(30))
    coordinator_signature = db.Column(db.String(100))
    coordinator_date = db.Column(db.String(30))
    leader_signature = db.Column(db.String(100))
    leader_date = db.Column(db.String(30))
class MonthlyAttendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(100))
    student_id = db.Column(db.String(50))
    program = db.Column(db.String(100))
    site = db.Column(db.String(100))
    supervisor = db.Column(db.String(100))
    month = db.Column(db.String(30))
    year = db.Column(db.String(10))

    attendance_data = db.Column(db.Text)  # Store JSON string for 20 rows

    total_hours_month = db.Column(db.String(20))
    remaining_hours = db.Column(db.String(20))
    performance_notes = db.Column(db.Text)

    student_signature = db.Column(db.String(100))
    student_date = db.Column(db.String(20))
    supervisor_signature = db.Column(db.String(100))
    supervisor_date = db.Column(db.String(20))

class SupervisorEvaluation(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        student_name = db.Column(db.String(100))
        student_id = db.Column(db.String(50))
        department_program = db.Column(db.String(100))
        duration_from = db.Column(db.String(20))
        duration_to = db.Column(db.String(20))

        company = db.Column(db.String(100))
        division = db.Column(db.String(100))
        supervisor_name = db.Column(db.String(100))
        supervisor_title = db.Column(db.String(100))
        contact = db.Column(db.String(100))
        email = db.Column(db.String(100))
        eval_date = db.Column(db.String(20))

        ratings = db.Column(db.Text)  # JSON string for all criteria ratings + comments

        major_projects = db.Column(db.Text)
        value_added = db.Column(db.Text)
        development_areas = db.Column(db.Text)
        dev_recommendations = db.Column(db.Text)

        overall_rating = db.Column(db.String(20))
        employment_rec = db.Column(db.String(100))
        explanation = db.Column(db.Text)
        programme_suggestions = db.Column(db.Text)
        communication_support = db.Column(db.String(50))
        supervisor_comments = db.Column(db.Text)
        supervisor_signature = db.Column(db.String(100))
        supervisor_date = db.Column(db.String(20))
        supervisor_title_final = db.Column(db.String(100))


class BiweeklyObservationLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100))
    student_id = db.Column(db.String(20))
    program = db.Column(db.String(100))
    organization_name = db.Column(db.String(100))
    department = db.Column(db.String(100))
    week_number = db.Column(db.Integer)
    start_date = db.Column(db.String(20))
    end_date = db.Column(db.String(20))
    tasks_description = db.Column(db.Text)
    skills_gained = db.Column(db.Text)
    challenges = db.Column(db.Text)
    reflections = db.Column(db.Text)
    plans_next_period = db.Column(db.Text)


class FinalEvaluationForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100))
    student_id = db.Column(db.String(50))
    department = db.Column(db.String(100))
    semester = db.Column(db.String(50))
    internship_site = db.Column(db.String(100))
    site_supervisor = db.Column(db.String(100))
    university_supervisor = db.Column(db.String(100))
    duration_from = db.Column(db.String(20))
    duration_to = db.Column(db.String(20))

    # Ratings stored as JSON
    overall_ratings = db.Column(db.JSON)
    skills_ratings = db.Column(db.JSON)
    env_ratings = db.Column(db.JSON)
    supervision_ratings = db.Column(db.JSON)
    work_ratings = db.Column(db.JSON)
    career_ratings = db.Column(db.JSON)
    growth_ratings = db.Column(db.JSON)
    challenge_ratings = db.Column(db.JSON)

    comments = db.Column(db.JSON)
    recommendation = db.Column(db.String(50))
    rec_explanation = db.Column(db.Text)
    employment_future = db.Column(db.String(50))
    employment_explanation = db.Column(db.Text)
    overall_rating = db.Column(db.String(50))
    additional_comments = db.Column(db.Text)
    advice = db.Column(db.Text)
