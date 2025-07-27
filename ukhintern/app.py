from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, make_response
from form_pdf_generator import generate_form_pdf, download_pdf
from form_pdf_generator import generate_all_entries_pdf
import os
import json

from models import db, ExpectationEssay, ConflictOfInterestForm, LearningContract, StudentLoginInfo, MonthlyAttendance, SupervisorEvaluation, BiweeklyObservationLog, FinalEvaluationForm
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db  # ✅ Import the db from models.py

app = Flask(__name__)
app.secret_key = 'ukh-internship-secret-key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///internship.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # ✅ Register the app with SQLAlchemy
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login/user', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        student_name = request.form['student_name']
        school = request.form['school']
        program = request.form['program']

        # Save to session
        session['student_name'] = student_name
        session['school'] = school
        session['program'] = program

        # Save to DB
        student = StudentLoginInfo(email=student_name, school=school, program=program)
        db.session.add(student)
        db.session.commit()

        flash(f'Welcome, {student_name}!', 'success')
        return redirect(url_for('forms_dashboard'))

    return render_template('login_user.html')


ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'
# ------------------ Work Supervisor Login ------------------

WORK_SUPERVISOR_USERNAME = 'supervisor'
WORK_SUPERVISOR_PASSWORD = '12345'

@app.route('/login/work_supervisor', methods=['GET', 'POST'])
def login_work_supervisor():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == WORK_SUPERVISOR_USERNAME and password == WORK_SUPERVISOR_PASSWORD:
            session['work_supervisor'] = True
            flash('Logged in as Work Supervisor!', 'success')
            return redirect(url_for('dashboard_work_supervisor'))
        else:
            flash('Invalid credentials!', 'danger')
            return redirect(url_for('login_work_supervisor'))
    return render_template('login_work_supervisor.html')


@app.route('/dashboard/work_supervisor')
def dashboard_work_supervisor():
    if not session.get('work_supervisor'):
        return redirect(url_for('login_work_supervisor'))
    return render_template('supervisor_dashboard.html')  # 👈 Use a dedicated template


@app.route('/login/admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            flash('Logged in as admin!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials!', 'danger')
            return redirect(url_for('login_admin'))
    return render_template('login_admin.html')

@app.route('/forms')
def forms_dashboard():
    if 'student_name' not in session:
        return redirect(url_for('login_user'))
    return render_template('forms_dashboard.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('login_admin'))

    students = StudentLoginInfo.query.all()

    grouped = {}
    for student in students:
        school = student.school
        program = student.program

        if school not in grouped:
            grouped[school] = {}
        if program not in grouped[school]:
            grouped[school][program] = []
        grouped[school][program].append(student.email)

    return render_template('admin_dashboard.html', grouped=grouped)


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))


# ---------------------- Form 1 ----------------------
@app.route('/form1', methods=['GET', 'POST'])
def form1():
    if request.method == 'POST':
        entry = ExpectationEssay(
            student_name=request.form['student_name'],
            school_programme=request.form['school_programme'],
            student_id=request.form['student_id'],
            essay=request.form['essay']
        )
        db.session.add(entry)
        db.session.commit()
        return redirect('/form2')
    return render_template('form1_expectation_essay.html')


@app.route('/admin/form1')
def admin_view_form1():
    entries = ExpectationEssay.query.all()
    return render_template('admin_view_form1.html', entries=entries)





# ---------------------- Form 2 ----------------------
@app.route('/form2', methods=['GET', 'POST'])
def form2():
    if request.method == 'POST':
        entry = ConflictOfInterestForm(
            full_name=request.form.get('full_name'),
            student_id=request.form.get('student_id'),
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            organization_name=request.form.get('organization_name'),
            internship_position=request.form.get('internship_position'),
            internship_supervisor=request.form.get('internship_supervisor'),
            start_date=request.form.get('start_date'),
            end_date=request.form.get('end_date'),

            q1=request.form.get('q1'),
            q2=request.form.get('q2'),
            q3=request.form.get('q3'),
            q4=request.form.get('q4'),
            q5=request.form.get('q5'),
            q6=request.form.get('q6'),

            management_description=request.form.get('management_description'),
            action1=request.form.get('action1'),
            action2=request.form.get('action2'),
            action3=request.form.get('action3'),

            agree_disclose='agree_disclose' in request.form,
            agree_confidential='agree_confidential' in request.form,
            agree_advantage='agree_advantage' in request.form,
            agree_recuse='agree_recuse' in request.form,
            agree_policies='agree_policies' in request.form,
            agree_consequences='agree_consequences' in request.form,

            student_signature=request.form.get('student_signature'),
            signature_date=request.form.get('signature_date')
        )

        db.session.add(entry)
        db.session.commit()
        return redirect('/form3')
    return render_template('form2_conflict_of_interest.html')

@app.route('/admin/form2')
def admin_view_form2():
    entries = ConflictOfInterestForm.query.all()
    return render_template('admin_view_form2.html', entries=entries)



# ---------------------- Form 3 ----------------------
@app.route('/form3', methods=['GET', 'POST'])
def form3():
    if request.method == 'POST':
        entry = LearningContract(
            student_name=request.form['student_name'],
            student_id=request.form['student_id'],
            class_year=request.form['class_year'],
            home_address=request.form['home_address'],
            student_phone=request.form['student_phone'],
            emergency_contact=request.form['emergency_contact'],
            student_email=request.form['student_email'],
            personality_note=request.form['personality_note'],
            supervisor_name=request.form['supervisor_name'],
            supervisor_title=request.form['supervisor_title'],
            supervisor_phone=request.form['supervisor_phone'],
            work_relevance=request.form['work_relevance'],
            organization=request.form['organization'],
            internship_address=request.form['internship_address'],
            supervisor_email=request.form['supervisor_email'],
            internship_title=request.form['internship_title'],
            department=request.form['department'],
            begin_date=request.form['begin_date'],
            end_date=request.form['end_date'],
            internship_paid=request.form['internship_paid'],
            primary_objective=request.form['primary_objective'],
            secondary_objective=request.form['secondary_objective'],
            skills_objective=request.form['skills_objective'],
            agree_attendance='agree_attendance' in request.form,
            agree_conduct='agree_conduct' in request.form,
            agree_confidentiality='agree_confidentiality' in request.form,
            agree_policies='agree_policies' in request.form,
            agree_communication='agree_communication' in request.form,
            student_signature=request.form['student_signature'],
            student_date=request.form['student_date'],
            supervisor_signature=request.form['supervisor_signature'],
            supervisor_date=request.form['supervisor_date'],
            coordinator_signature=request.form['coordinator_signature'],
            coordinator_date=request.form['coordinator_date'],
            leader_signature=request.form['leader_signature'],
            leader_date=request.form['leader_date']
        )
        db.session.add(entry)
        db.session.commit()
        return redirect('/form4')
    return render_template('form3_learning_contract.html')

@app.route('/admin/form3')
def admin_view_form3():
    entries = LearningContract.query.all()
    return render_template('admin_view_form3.html', entries=entries)



# ---------------------- Form 4 ----------------------
@app.route('/form4', methods=['GET', 'POST'])
def form4():
    if request.method == 'POST':
        attendance = []
        for i in range(20):
            row = {
                'day': request.form.get(f'day_{i}'),
                'date': request.form.get(f'date_{i}'),
                'time_in': request.form.get(f'time_in_{i}'),
                'time_out': request.form.get(f'time_out_{i}'),
                'total_hours': request.form.get(f'total_hours_{i}'),
                'remarks': request.form.get(f'remarks_{i}')
            }
            attendance.append(row)

        entry = MonthlyAttendance(
            full_name=request.form['full_name'],
            student_id=request.form['student_id'],
            program=request.form['program'],
            site=request.form['site'],
            supervisor=request.form['supervisor'],
            month=request.form['month'],
            year=request.form['year'],
            attendance_data=json.dumps(attendance),
            total_hours_month=request.form['total_hours_month'],
            remaining_hours=request.form['remaining_hours'],
            performance_notes=request.form['performance_notes'],
            student_signature=request.form['student_signature'],
            student_date=request.form['student_date'],
            supervisor_signature=request.form['supervisor_signature'],
            supervisor_date=request.form['supervisor_date']
        )
        db.session.add(entry)
        db.session.commit()
        return redirect('/form6')
    return render_template('form4_monthly_attendance.html')


@app.route('/admin/form4')
def admin_view_form4():
    entries = MonthlyAttendance.query.all()
    return render_template('admin_view_form4.html', entries=entries)



@app.route('/form5', methods=['GET', 'POST'])
def form5_comprehensive():
    # Restrict access to only Work Supervisor
    if not session.get('work_supervisor'):
        return redirect(url_for('login_work_supervisor'))

    if request.method == 'POST':
        ratings_data = {
            'technical': [
                {'criteria': 'Quality of work', 'rating': request.form.get('tech_1'), 'comment': request.form.get('com_tech_1')},
                {'criteria': 'Competency and learning', 'rating': request.form.get('tech_2'), 'comment': request.form.get('com_tech_2')},
                {'criteria': 'Academic application', 'rating': request.form.get('tech_3'), 'comment': request.form.get('com_tech_3')}
            ],
            'professional': [
                {'criteria': 'Punctuality', 'rating': request.form.get('prof_1'), 'comment': request.form.get('com_prof_1')},
                {'criteria': 'Initiative', 'rating': request.form.get('prof_2'), 'comment': request.form.get('com_prof_2')},
                {'criteria': 'Appearance', 'rating': request.form.get('prof_3'), 'comment': request.form.get('com_prof_3')}
            ],
            'communication': [
                {'criteria': 'Verbal/Written', 'rating': request.form.get('comm_1'), 'comment': request.form.get('com_comm_1')},
                {'criteria': 'Listening', 'rating': request.form.get('comm_2'), 'comment': request.form.get('com_comm_2')},
                {'criteria': 'Teamwork', 'rating': request.form.get('comm_3'), 'comment': request.form.get('com_comm_3')}
            ],
            'adaptability': [
                {'criteria': 'Feedback receptiveness', 'rating': request.form.get('adap_1'), 'comment': request.form.get('com_adap_1')},
                {'criteria': 'Problem solving', 'rating': request.form.get('adap_2'), 'comment': request.form.get('com_adap_2')},
                {'criteria': 'Continuous improvement', 'rating': request.form.get('adap_3'), 'comment': request.form.get('com_adap_3')}
            ]
        }

        form = SupervisorEvaluation(
            student_name=request.form['student_name'],
            student_id=request.form['student_id'],
            department_program=request.form['department_program'],
            duration_from=request.form['duration_from'],
            duration_to=request.form['duration_to'],
            company=request.form['company'],
            division=request.form['division'],
            supervisor_name=request.form['supervisor_name'],
            supervisor_title=request.form['supervisor_title'],
            contact=request.form['contact'],
            email=request.form['email'],
            eval_date=request.form['eval_date'],
            ratings=json.dumps(ratings_data),
            major_projects=request.form['major_projects'],
            value_added=request.form['value_added'],
            development_areas=request.form['development_areas'],
            dev_recommendations=request.form['dev_recommendations'],
            overall_rating=request.form['overall_rating'],
            employment_rec=request.form['employment_rec'],
            explanation=request.form['explanation'],
            programme_suggestions=request.form['programme_suggestions'],
            communication_support=request.form['communication_support'],
            supervisor_comments=request.form['supervisor_comments'],
            supervisor_signature=request.form['supervisor_signature'],
            supervisor_date=request.form['supervisor_date'],
            supervisor_title_final=request.form['supervisor_title_final']
        )
        db.session.add(form)
        db.session.commit()


    return render_template('form5_supervisor_evaluation.html')


import json

import json

@app.route('/admin/form5')
def admin_view_form5():
    entries = SupervisorEvaluation.query.all()

    for entry in entries:
        try:
            entry.ratings_json = json.loads(entry.ratings)
        except Exception:
            entry.ratings_json = {}  # fallback if malformed JSON

    return render_template('admin_view_form5.html', entries=entries)




@app.route('/form6', methods=['GET', 'POST'])
def form6():
    if request.method == 'POST':
        entry = BiweeklyObservationLog(
            student_name=request.form['student_name'],
            student_id=request.form['student_id'],
            program=request.form.get('program', ''),
            organization_name=request.form['organization_name'],
            department=request.form['department'],
            week_number=request.form['week_number'],
            start_date=request.form['start_date'],
            end_date=request.form['end_date'],
            tasks_description=request.form['tasks_description'],
            skills_gained=request.form['skills_gained'],
            challenges=request.form['challenges'],
            reflections=request.form['reflections'],
            plans_next_period=request.form['plans_next_period']
        )
        db.session.add(entry)
        db.session.commit()


        return redirect('/form7')

    return render_template('form6_observation_log.html')


@app.route('/admin/form6')
def admin_view_form6():
    entries = BiweeklyObservationLog.query.all()
    return render_template('admin_view_form6.html', entries=entries)




from flask import request, render_template
from models import db, FinalEvaluationForm
import traceback

@app.route("/form7", methods=["GET", "POST"])
def form7():
    if request.method == "POST":
        try:
            # Checkbox selections (grab first selected if any)
            recommendation = [k for k in request.form.keys() if k.startswith("recommend_")]
            employment_future = [k for k in request.form.keys() if k.startswith("employment_")]
            overall_rating = [k for k in request.form.keys() if k.startswith("rating_")]

            # Ratings (section_a_1_rating, section_b_4_rating, etc.)
            overall_ratings = {f"overall_{i}": request.form.get(f"section_a_{i}_rating", "") for i in range(1, 4)}
            skills_ratings = {f"skills_{i}": request.form.get(f"section_b_{i}_rating", "") for i in range(4, 7)}
            env_ratings = {f"env_{i}": request.form.get(f"section_c_{i}_rating", "") for i in range(7, 10)}
            supervision_ratings = {f"supervision_{i}": request.form.get(f"section_d_{i}_rating", "") for i in range(10, 13)}
            work_ratings = {f"work_{i}": request.form.get(f"section_e_{i}_rating", "") for i in range(13, 16)}
            career_ratings = {f"career_{i}": request.form.get(f"section_f_{i}_rating", "") for i in range(16, 19)}
            growth_ratings = {f"growth_{i}": request.form.get(f"section_g_{i}_rating", "") for i in range(19, 22)}
            challenge_ratings = {f"challenges_{i}": request.form.get(f"section_h_{i}_rating", "") for i in range(22, 25)}

            # Comments section
            comments = {
                "comments_overall": request.form.get("overall_experience_comments", ""),
                "skills_comments": request.form.get("skills_developed", ""),
                "env_comments": request.form.get("professional_environment_comments", ""),
                "supervision_comments": request.form.get("supervision_comments", ""),
                "work_project": request.form.get("valuable_project", ""),
                "work_comments": request.form.get("assignments_comments", ""),
                "career_comments": request.form.get("career_impact_comments", ""),
                "growth_comments": request.form.get("personal_development_comments", ""),
                "challenge_faced": request.form.get("challenge_faced", ""),
                "challenge_addressed": request.form.get("challenge_response", ""),
                "challenge_learned": request.form.get("challenge_learned", "")
            }

            # Create and commit model
            data = FinalEvaluationForm(
                student_name=request.form.get("student_name", ""),
                student_id=request.form.get("student_id", ""),
                department=request.form.get("department", ""),
                semester=request.form.get("semester", ""),
                internship_site=request.form.get("site", ""),
                site_supervisor=request.form.get("site_supervisor", ""),
                university_supervisor=request.form.get("university_supervisor", ""),
                duration_from=request.form.get("start_date", ""),
                duration_to=request.form.get("end_date", ""),
                overall_ratings=overall_ratings,
                skills_ratings=skills_ratings,
                env_ratings=env_ratings,
                supervision_ratings=supervision_ratings,
                work_ratings=work_ratings,
                career_ratings=career_ratings,
                growth_ratings=growth_ratings,
                challenge_ratings=challenge_ratings,
                comments=comments,
                recommendation=recommendation[0] if recommendation else "",
                rec_explanation=request.form.get("recommend_explanation", ""),
                employment_future=employment_future[0] if employment_future else "",
                employment_explanation=request.form.get("employment_explanation", ""),
                overall_rating=overall_rating[0] if overall_rating else "",
                additional_comments=request.form.get("additional_comments", ""),
                advice=request.form.get("future_advice", ""),
                student_signature=request.form.get("student_signature", ""),
                student_date=request.form.get("student_date", ""),
                review=request.form.get("review", ""),
                final_grade=request.form.get("final_grade", ""),
                grade_date=request.form.get("grade_date", ""),
                supervisor_signature=request.form.get("supervisor_signature", ""),
                supervisor_date=request.form.get("supervisor_date", "")
            )

            db.session.add(data)
            db.session.commit()
            return "Submitted successfully"

        except Exception as e:
            traceback.print_exc()
            return f"An error occurred: {str(e)}", 500

    return render_template("form7_final_evaluation.html")



@app.route("/admin/form7")
def admin_form7():
    entries = FinalEvaluationForm.query.all()
    return render_template("admin_form7.html", entries=entries)




@app.route('/admin/form1/download/<int:id>')
def download_form1_pdf(id):
    entry = ExpectationEssay.query.get_or_404(id)
    generate_form_pdf(entry, form_number=1, filename='form1_entry.pdf')
    return download_pdf('form1_entry.pdf')

@app.route('/admin/form1/download-all')
def download_all_form1():
    entries = ExpectationEssay.query.all()
    return generate_all_entries_pdf(entries, form_number=1, filename='form1_all_entries.pdf')



@app.route('/admin/form2/download/<int:id>')
def download_form2_pdf(id):
    entry = ConflictOfInterestForm.query.get_or_404(id)
    generate_form_pdf(entry, form_number=2, filename='form2_entry.pdf')
    return download_pdf('form2_entry.pdf')


@app.route('/admin/form2/download-all')
def download_all_form2():
    entries = ConflictOfInterestForm.query.all()
    return generate_all_entries_pdf(entries, form_number=2, filename='form2_all_entries.pdf')


@app.route('/admin/form3/download/<int:id>')
def download_form3_pdf(id):
    entry = LearningContract.query.get_or_404(id)
    generate_form_pdf(entry, form_number=3, filename='form3_entry.pdf')
    return download_pdf('form3_entry.pdf')
@app.route('/admin/form3/download-all')
def download_all_form3():
    entries = LearningContract.query.all()
    return generate_all_entries_pdf(entries, form_number=3, filename='form3_all_entries.pdf')

@app.route('/admin/form4/download/<int:id>')
def download_form4_pdf(id):
    entry = MonthlyAttendance.query.get_or_404(id)
    attendance = json.loads(entry.attendance_data)
    entry.attendance_data = "\n".join(
        [f"{row['day']} {row['date']}: {row['time_in']} - {row['time_out']} ({row['total_hours']}h)" for row in attendance]
    )
    generate_form_pdf(entry, form_number=4, filename='form4_entry.pdf')
    return download_pdf('form4_entry.pdf')


@app.route('/admin/form4/download-all')
def download_all_form4():
    entries = MonthlyAttendance.query.all()
    return generate_all_entries_pdf(entries, form_number=4, filename='form4_all_entries.pdf')


@app.route('/admin/form5/download/<int:id>')
def download_form5_pdf(id):
    entry = SupervisorEvaluation.query.get_or_404(id)
    generate_form_pdf(entry, form_number=5, filename='form5_entry.pdf')
    return download_pdf('form5_entry.pdf')
@app.route('/admin/form5/download-all')
def download_all_form5():
    entries = SupervisorEvaluation.query.all()
    return generate_all_entries_pdf(entries, form_number=5, filename='form5_all_entries.pdf')

@app.route('/admin/form6/download/<int:id>')
def download_form6_pdf(id):
    entry = BiweeklyObservationLog.query.get_or_404(id)
    generate_form_pdf(entry, form_number=6, filename='form6_entry.pdf')
    return download_pdf('form6_entry.pdf')

@app.route('/admin/form6/download-all')
def download_all_form6():
    entries = BiweeklyObservationLog.query.all()
    return generate_all_entries_pdf(entries, form_number=6, filename='form5_all_entries.pdf')


@app.route('/admin/form7/download/<int:id>')
def download_form7_pdf(id):
    entry = FinalEvaluationForm.query.get_or_404(id)
    generate_form_pdf(entry, form_number=7, filename='form7_entry.pdf')
    return download_pdf('form7_entry.pdf')





@app.route('/admin/form1\7/download-all')
def download_all_form7():
    entries = ExpectationEssay.query.all()
    return generate_all_entries_pdf(entries, form_number=7, filename='form1_all_entries.pdf')

