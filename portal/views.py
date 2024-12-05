import json
import gc
import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_file, make_response, \
    Response, jsonify
import flask
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
import threading
from . import APP, LOG
from portal.models import db
from portal.models.problems import Problem
import subprocess
import json
from os import environ as env
from urllib.parse import quote_plus, urlencode
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for, request, jsonify
import requests
import pyotp
import qrcode
import io
from base64 import b64encode
import random
import re
import string
from datetime import datetime, timedelta
from .security import Encryption
import tempfile
import sqlite3
from portal import LOG, login_required, APP, check_for_sub
from portal.models.users import User
from portal.models.cources import Courses
from portal.models.subscriptions import Subscription
from portal.models.payment import Payment
from portal.models.cources_status import CoursesStatus
from portal.models.user_solutions import UserSolution
import flask_login

# def get_random_characters(string_length=3):
#     return ''.join(random.choice(string.ascii_letters) for x in range(string_length))


bp = Blueprint('view', __name__, url_prefix='/', template_folder="./templates", static_folder="./static")


@bp.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    r.headers["server"] = ""
    return r


@bp.before_request
def before_request():
    flask.session.permanent = True
    APP.permanent_session_lifetime = timedelta(minutes=15)
    flask.session.modified = True
    flask.g.user = flask_login.current_user
    # if request.url.startswith('http://'):
    #     url = request.url.replace('http://', 'https://', 1)
    #     code = 301
    #     return redirect(url, code=code)


def get_random_numbers(string_length=3):
    return ''.join(random.choice(string.digits) for x in range(string_length))


@bp.route('/', methods=["GET", "POST"])
def home2():
    if request.method == "GET":
        cousrces_ava = Courses.query.all()
        if 'user' in session:
            return redirect(url_for('view.home'))
        else:
            user_cred = "hidden"
            user_id = ''
            main_count_row = 0
            count_row = 0
            return render_template('landingPage.html', user_cred=user_cred, user_id=user_id, cousrces_ava=cousrces_ava,
                                   main_count_row=main_count_row, count_row=count_row)


def verify_recaptcha(recaptcha_response):
    """Verify reCAPTCHA response with Google"""
    RECAPTCHA_SECRET_KEY = APP.config['RECAPTCHA_SECRET_KEY']
    GOOGLECAPTCHA_URL = APP.config['GOOGLECAPTCHA_URL']
    print(RECAPTCHA_SECRET_KEY)
    print(GOOGLECAPTCHA_URL)
    verify_response = requests.post(
        url=f'{GOOGLECAPTCHA_URL}?secret={RECAPTCHA_SECRET_KEY}&response={recaptcha_response}').json()
    print(verify_response, "verify_response")
    return verify_response.get("success", False)


def generate_totp_secret():
    return


def get_totp_uri(username, secret):
    return pyotp.totp.TOTP(secret).provisioning_uri(username, issuer_name="DsQuest")


@bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        recaptcha_response = data["g_recaptcha_response"]
        reg_username = data["reg_username"]
        reg_email = data["reg_email"]
        mfa_enabled = data["mfa_enabled"]
        # session["reg_email"] = reg_email
        encrypted_pwd = Encryption().encrypt(data['reg_password'])

        if not verify_recaptcha(recaptcha_response):
            return jsonify({"error": "reCAPTCHA verification failed."}), 400

        header_id = datetime.now().strftime("%d%m%Y%H%M%S") + get_random_numbers(5)

        if mfa_enabled == 'yes':
            save_path = os.path.join(APP.config['QRDATA'], header_id + '.txt')
            mfa_secret = pyotp.random_base32()
            mfa_enabled = True
            totp_uri = get_totp_uri(reg_email, mfa_secret)
            qr_img = qrcode.make(totp_uri)
            buffered = io.BytesIO()
            qr_img.save(buffered, format="PNG")
            qr_code_data = b64encode(buffered.getvalue()).decode('utf-8')
            session["mfa_secret"] = mfa_secret
            with open(save_path, "w") as file:
                file.write(qr_code_data)
            qr_code_data = 'yes'
        else:
            mfa_secret = None
            mfa_enabled = False
            qr_code_data = 'no'

        head = User(user_id=header_id,
                    password=encrypted_pwd,
                    username=reg_username,
                    email_id=reg_email,
                    active='y',
                    status='created',
                    role='user',
                    mfa_enabled=mfa_enabled,
                    mfa_secret=mfa_secret)
        try:
            db.session.merge(head)
            db.session.commit()
            db.session.close()
        except Exception as e:
            LOG.error(e, exc_info=True)
            db.session.rollback()
            LOG.error("Error while pushing data")
            msg = "Failed"
            Status = {"status": msg, "header_id": '', 'qr_code_data': 'none'}
            return jsonify(Status)

        return jsonify({"status": "Registration successful!", "header_id": header_id, "qr_code_data": qr_code_data})

    except Exception as e:
        return jsonify(
            {"status": "Registration unsuccessful!" + 'error message:' + str(e), "header_id": '', "qr_code_data": 'no'})


@bp.route('/check_for_gmail', methods=['POST'])
def check_for_gmail():
    data = request.json
    reg_email = data['reg_email']
    try:
        users2 = User.query.filter_by(email_id=reg_email).one()
        if users2 is not None:
            msg = "email_id"
            return jsonify({
                "msg": msg})
        else:
            msg = "clear"
            return jsonify({
                "msg": msg})
    except NoResultFound:
        pass
    except Exception as e:
        LOG.error("Error occurred while login ")
        LOG.error(e, exc_info=True)
    finally:
        db.session.close()
    Status = {"msg": "msg"}
    return jsonify(Status)


@bp.route('/enable_2fa/<string:header_id>', methods=['GET', 'POST'])
def enable_2fa(header_id):
    file_path = os.path.join(APP.config['QRDATA'], header_id + '.txt')
    with open(file_path, "r") as file:
        loaded_data = file.read()
    return render_template('auth.html', qr_code_data=loaded_data, header_id=header_id)


def verify_totp(secret, token):
    totp = pyotp.TOTP(secret)
    return totp.verify(token)


@bp.route('/enable_2fa_final', methods=['GET', 'POST'])
def enable_2fa_final():
    data = request.json
    token = data['token']
    header_id = data['header_id']
    mfa_secret = session['mfa_secret']
    if verify_totp(mfa_secret, token):
        session['user'] = header_id
        return jsonify({'status': 'successful!'})
    else:
        return jsonify({'status': 'In valid token please try again!'})


def get_cources():
    courses_id = []
    cource_name = []
    description = []
    course_image_ = []
    course_status = []
    amount = []
    page_to_load = []

    user_id_get = session.get('user')
    try:
        event_to_attend = db.session.query(Courses, CoursesStatus).filter(CoursesStatus.user_id == user_id_get,
                                                                          CoursesStatus.status_of_course == 'In Progress',
                                                                          Courses.course_status == 'active').outerjoin(
            CoursesStatus,
            Courses.courses_id == CoursesStatus.courses_id).all()

        for cource, courcestatsu in event_to_attend:
            courses_id.append(cource.courses_id)
            cource_name.append(cource.cource_name)
            description.append(cource.description)
            course_image_.append(cource.course_image_)
            course_status.append(cource.course_status)
            amount.append(cource.amount)
            page_to_load.append(cource.page_to_load)
    except Exception as e:
        LOG.info(e)
        pass

    cousrces_ava = Courses.query.all()
    main_courses_id = []
    main_cource_name = []
    main_description = []
    main_course_image_ = []
    main_course_status = []
    main_amount = []
    main_page_to_load = []
    for cource_ in cousrces_ava:
        if cource_.courses_id not in courses_id:
            main_courses_id.append(cource_.courses_id)
            main_cource_name.append(cource_.cource_name)
            main_description.append(cource_.description)
            main_course_image_.append(cource_.course_image_)
            main_course_status.append(cource_.course_status)
            main_amount.append(cource_.amount)
            main_page_to_load.append(cource_.page_to_load)

    return courses_id, cource_name, description, course_image_, course_status, amount, page_to_load, main_courses_id, main_cource_name, main_description, main_course_image_, main_course_status, main_amount, main_page_to_load


@bp.route('/home', methods=["GET", "POST"])
@login_required
def home():
    if request.method == "GET":
        if 'user' in session:
            cousrces_ava = []
            # if user open any cource that mean user is started the course
            courses_id, cource_name, description, course_image_, course_status, amount, page_to_load, main_courses_id, main_cource_name, main_description, main_course_image_, main_course_status, main_amount, main_page_to_load = get_cources()
            user_cred = ""
            user_id = session.get('user')
            count_row = len(courses_id)
            main_count_row = len(main_courses_id)
            return render_template('landingPage.html', user_cred=user_cred, user_id=user_id, courses_id=courses_id,
                                   cource_name=cource_name,
                                   description=description, course_image_=course_image_, course_status=course_status,
                                   amount=amount, count_row=count_row, main_count_row=main_count_row,
                                   main_cource_name=main_cource_name, main_description=main_description,
                                   main_course_image_=main_course_image_,
                                   main_course_status=main_course_status, main_amount=main_amount,
                                   cousrces_ava=cousrces_ava, main_courses_id=main_courses_id,
                                   main_page_to_load=main_page_to_load, page_to_load=page_to_load)
        else:
            invalid_msg = "hidden"
            access_name = "hidden"
            access_pass = "hidden"
            return render_template("login.html", invalid_msg=invalid_msg, access_name=access_name,
                                   access_pass=access_pass)


@bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        invalid_msg = "hidden"
        access_name = "hidden"
        access_pass = "hidden"
        return render_template("login.html", invalid_msg=invalid_msg, access_name=access_name, access_pass=access_pass)
    if request.method == "POST":
        username = request.form.get('loginEmail')
        password = request.form.get('loginPassword')
        print('asmnasm')
        if username == '':
            invalid_msg = "hidden"
            access_name = ""
            access_pass = "hidden"
            return render_template("login.html", invalid_msg=invalid_msg, access_name=access_name,
                                   access_pass=access_pass)
        if password == '':
            invalid_msg = "hidden"
            access_name = "hidden"
            access_pass = ""
            return render_template("login.html", invalid_msg=invalid_msg, access_name=access_name,
                                   access_pass=access_pass)
        try:
            encrypted_pwd = Encryption().encrypt(password)
            print(encrypted_pwd)
            users = User.query.filter_by(email_id=username, password=encrypted_pwd).one()
            user_id_get = users.user_id
            print(users, 'asxs')
            if users is not None:
                if users.role == 'admin':
                    session['role'] = "admin"
                if users.mfa_enabled:
                    session['mfa_secret'] = users.mfa_secret
                    return render_template("otp.html", mfa_secret=users.mfa_secret, header_id=user_id_get,
                                           gmail=users.email_id)
                else:
                    session['user'] = users.user_id
                    if 'user' in session:
                        cousrces_ava = []
                        # if user open any cource that mean user is started the course
                        courses_id, cource_name, description, course_image_, course_status, amount, page_to_load, main_courses_id, main_cource_name, main_description, main_course_image_, main_course_status, main_amount, main_page_to_load = get_cources()
                        user_cred = ""
                        user_id = session.get('user')
                        count_row = len(courses_id)
                        main_count_row = len(main_courses_id)
                        return render_template('landingPage.html', user_cred=user_cred, user_id=user_id,
                                               courses_id=courses_id,
                                               cource_name=cource_name,
                                               description=description, course_image_=course_image_,
                                               course_status=course_status,
                                               amount=amount, count_row=count_row, main_count_row=main_count_row,
                                               main_cource_name=main_cource_name, main_description=main_description,
                                               main_course_image_=main_course_image_,
                                               main_course_status=main_course_status, main_amount=main_amount,
                                               cousrces_ava=cousrces_ava, main_courses_id=main_courses_id,
                                               main_page_to_load=main_page_to_load, page_to_load=page_to_load)
        except NoResultFound:
            pass
        except Exception as e:
            LOG.error("Error occurred while login ")
            LOG.error(e, exc_info=True)
        finally:
            db.session.close()
        invalid_msg = ""
        access_name = "hidden"
        access_pass = "hidden"
        return render_template("login.html", invalid_msg=invalid_msg, access_name=access_name, access_pass=access_pass)


@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == "GET":
        invalid_msg = "hidden"
        access_name = "hidden"
        access_pass = "hidden"
        session['user'] = False
        session.clear()
        gc.collect()
        return render_template("login.html", invalid_msg=invalid_msg, access_name=access_name, access_pass=access_pass)


@bp.route('/add_problems', methods=["GET", "POST"])
@login_required
def add_problems():
    if session['role'] == 'admin':
        return render_template('add_questions.html')
    else:
        invalid_msg = "hidden"
        access_name = "hidden"
        access_pass = "hidden"
        return render_template("login.html", invalid_msg=invalid_msg, access_name=access_name, access_pass=access_pass)


@bp.route('/add_solutions', methods=["GET", "POST"])
@login_required
def add_solutions():
    if session['role'] == 'admin':
        return render_template('add_questions.html')
    else:
        invalid_msg = "hidden"
        access_name = "hidden"
        access_pass = "hidden"
        return render_template("login.html", invalid_msg=invalid_msg, access_name=access_name, access_pass=access_pass)



@bp.route('/load_course/<string:courses>/<string:courses_id>', methods=["GET", "POST"])
@login_required
@check_for_sub
def load_course_sql(courses, courses_id):
    user_id = session.get('user')
    if request.method == "GET":
        try:
            users = CoursesStatus.query.filter_by(user_id=user_id, courses_id=courses_id).one()
        except:
            users = False
        if users:
            variable_completed_modules = json.loads(users.completed_modules)
            return render_template(courses + '.html', courses_id=courses_id,
                                   completedModules=variable_completed_modules,
                                   courses_status_id=users.courses_status_id)
        else:
            print(',wnbdmbasdbasdbkbfvkjdkasskd')
            courses_status_id = datetime.now().strftime("%d%m%Y%H%M%S") + get_random_numbers(5)
            head = CoursesStatus(courses_status_id=courses_status_id,
                                 courses_id=courses_id,
                                 completed_modules=json.dumps([]),
                                 user_id=user_id,
                                 percentage_completed='0')
            try:
                db.session.merge(head)
                db.session.commit()
                db.session.close()
                LOG.info("inserted sucess")
            except Exception as e:
                LOG.error(e, exc_info=True)
                db.session.rollback()
                LOG.error("Error while pushing data")
                msg = "Failed"
                Status = {"status": msg, "message": "Error while pushing data"}
                print(Status)
            return render_template(courses + '.html', completedModules=json.loads("[]"), courses_id=courses_id,
                                   courses_status_id=courses_status_id)
    if request.method == "POST":
        user_id = session.get('user')
        data = request.json
        completed_modules = data["moduleId"]
        print(completed_modules)
        courses_status_id = data["courses_status_id"]
        # try:
        try:
            users_1 = CoursesStatus.query.filter_by(user_id=user_id, courses_status_id=courses_status_id,
                                                    courses_id=courses_id).one()
        except:
            users_1 = False
        if users_1:
            variable_completed_modules = json.loads(users_1.completed_modules)
            print(type(variable_completed_modules))
            if isinstance(variable_completed_modules, list):
                final_modules_list = variable_completed_modules
                # for i in variable_completed_modules:
                if completed_modules not in variable_completed_modules:
                    final_modules_list.append(completed_modules)
                    head = CoursesStatus(Id=users_1.Id,
                                         courses_status_id=courses_status_id,
                                         courses_id=courses_id,
                                         completed_modules=json.dumps(final_modules_list),
                                         user_id=user_id,
                                         percentage_completed='0')
                    try:
                        db.session.merge(head)
                        db.session.commit()
                        db.session.close()
                    except Exception as e:
                        LOG.error(e, exc_info=True)
                        db.session.rollback()
                        LOG.error("Error while pushing data")
                        return jsonify({
                            "status": "UnSuccess",
                            "message": f"Data Not Inserted"
                        }), 400
                    return jsonify({
                        "status": "Success",
                        "message": f"Successfully Inserted The Data"
                    }), 200
                else:
                    return jsonify({
                        "status": "existed",
                        "message": f"Model is already Completed"
                    }), 400

        else:
            return jsonify({
                "status": "UnSuccess",
                "message": f"Please Login and try again!"
            }), 400


@bp.route('/cardDetails', methods=["GET", "POST"])
@login_required
def cardDetails():
    if request.method == "GET":
        return render_template('cardDetails_new.html')


@bp.route('/problemQuestions', methods=["GET", "POST"])
@login_required
def problemQuestions():
    if request.method == "GET":
        user_id = session.get('user')
        print("user", user_id)
        try:
            users = Subscription.query.filter_by(user_id=user_id).one()
            if users.subscription_type == 'Premium':
                problems = db.session.query(Problem).all()
                print("problems", problems)
                title = []
                difficulty = []
                type = []
                id_ = []
                for Quote in problems:
                    print(Quote.title)
                    title.append(Quote.title)
                    difficulty.append(Quote.difficulty)
                    type.append(Quote.type)
                    id_.append(Quote.Id)
                count_row = len(id_)
                return render_template('problemQuestions.html', titles=title, difficultys=difficulty, types=type,
                                       id_s=id_,
                                       count_row=count_row)
            else:
                return redirect(url_for('view.payment_plan'))
        except Exception as e:
            print(e)
            return redirect(url_for('view.payment_plan'))


@bp.route('/problem/<int:problem_id>')
@login_required
def view_problem(problem_id):
    user_id = session.get('user')
    try:
        users = Subscription.query.filter_by(user_id=user_id).one()
        if users.subscription_type == 'Premium':
            problem = Problem.query.filter_by(Id=problem_id).one()
            solution_found = True
            try:
                user_solutions = UserSolution.query.filter_by(user_id=user_id, problem_id=problem_id).one()
            except:
                solution_found = False
                user_solutions = False
                LOG.info("User Not Exists")
            return render_template('view_problem.html', problem=problem, user_solutions=user_solutions,solution_found=solution_found,default_func=problem.function_signature)
        else:
            return redirect(url_for('view.payment_plan'))
    except:
        return redirect(url_for('view.home'))


@bp.route('/problem_sql/<int:problem_id>')
@login_required
def view_sql_problem(problem_id):
    user_id = session.get('user')
    try:
        users = Subscription.query.filter_by(user_id=user_id).one()
        if users.subscription_type == 'Premium':
            problem = Problem.query.filter_by(Id=problem_id).one()
            solution_found = True
            try:
                user_solutions = UserSolution.query.filter_by(user_id=user_id, problem_id=problem_id).one()
            except:
                solution_found = False
                user_solutions = False
                LOG.info("User Not Exists")
            return render_template('view_sql_problem.html', problem=problem, user_solutions=user_solutions,
                                   solution_found=solution_found)
        else:
            return redirect(url_for('view.payment_plan'))
    except:
        return redirect(url_for('view.home'))


@bp.route('/payment_plan', methods=["GET", "POST"])
@login_required
def payment_plan():
    if request.method == "GET":
        username = session.get('user')
        try:
            users = Subscription.query.filter_by(user_id=username).one()
            subscription_type = users.subscription_type
            current_selected_plan = 'Your Current Plan'
            if subscription_type == 'Pro':
                type_pro_ = 'hidden'
                type_premium_ = ''
            else:
                type_pro_ = ''
                type_premium_ = 'hidden'
        except:
            type_pro_ = ''
            type_premium_ = ''
            current_selected_plan = ''
        return render_template('payment_plan.html', type_pro_=type_pro_, type_premium_=type_premium_,
                               current_selected_plan=current_selected_plan)
    if request.method == "POST":
        price = request.form.get('price')
        type = request.form.get('type')
        # head = User(user_id=header_id,
        #             password=encrypted_pwd,
        #             username=reg_username,
        #             email_id=reg_email,
        #             active='y',
        #             status='created',
        #             role='user',
        #             mfa_enabled=mfa_enabled,
        #             mfa_secret=mfa_secret)
        # try:
        #     db.session.merge(head)
        #     db.session.commit()
        #     db.session.close()
        # except Exception as e:
        #     LOG.error(e, exc_info=True)
        #     db.session.rollback()
        #     LOG.error("Error while pushing data")
        #     msg = "Failed"
        #     Status = {"status": msg, "header_id": '', 'qr_code_data': 'none'}
        #     return jsonify(Status)
        return render_template('cardDetails_new.html', price=price, type=type)


@bp.route('/sub', methods=["GET", "POST"])
@login_required
def subscribe():
    if request.method == "POST":
        data = request.json
        user_id = session.get('user')
        subscription_start_date = datetime.now().date()
        subscription_end_date = subscription_start_date + timedelta(days=365)
        try:
            users = Subscription.query.filter_by(user_id=user_id).one()
        except:
            users = False
        if users:
            transaction_id = users.transaction_id
            head = Subscription(Id=users.Id,
                                subscription_type=data['type_of_subscription'],
                                subscription_status="active",
                                subscription_start_date=subscription_start_date,
                                subscription_end_date=subscription_end_date)
            try:
                db.session.merge(head)
                db.session.commit()
                db.session.close()
            except Exception as e:
                LOG.error(e, exc_info=True)
                db.session.rollback()
                LOG.error("Error while pushing data")
                msg = "Failed"
                Status = {"status": msg, "message": "Error while pushing data"}
                return jsonify(Status)

            users2 = Payment.query.filter_by(transaction_id=transaction_id).one()
            head2 = Payment(Id=users2.Id,
                            amount=data['price_selected'],
                            card_number=data['cardNumber'],
                            name_on_card=data['cardName'],
                            expire_year=data['cardYear'],
                            expire_month=data['cardMonth'],
                            cvv_on_card=data['cardCvv'],
                            payment_status='Completed')
            try:
                db.session.merge(head2)
                db.session.commit()
                db.session.close()
            except Exception as e:
                LOG.error(e, exc_info=True)
                db.session.rollback()
                LOG.error("Error while pushing data")
                msg = "Failed"
                Status = {"status": msg, "message": "Error while pushing data"}
                return jsonify(Status)
        else:
            transaction_id = datetime.now().strftime("%d%m%Y%H%M%S") + get_random_numbers(5)
            head = Payment(transaction_id=transaction_id,
                           amount=data['price_selected'],
                           card_number=data['cardNumber'],
                           name_on_card=data['cardName'],
                           expire_year=data['cardYear'],
                           expire_month=data['cardMonth'],
                           cvv_on_card=data['cardCvv'],
                           payment_status='Completed')
            try:
                db.session.merge(head)
                db.session.commit()
                db.session.close()
            except Exception as e:
                LOG.error(e, exc_info=True)
                db.session.rollback()
                LOG.error("Error while pushing data")
                msg = "Failed"
                Status = {"status": msg, "message": "Error while pushing data"}
                return jsonify(Status)

            head = Subscription(transaction_id=transaction_id,
                                user_id=user_id,
                                subscription_type=data['type_of_subscription'],
                                subscription_status="active",
                                subscription_start_date=subscription_start_date,
                                subscription_end_date=subscription_end_date)
            try:
                db.session.merge(head)
                db.session.commit()
                db.session.close()
            except Exception as e:
                LOG.error(e, exc_info=True)
                db.session.rollback()
                LOG.error("Error while pushing data")
                msg = "Failed"
                Status = {"status": msg, "message": "Error while pushing data"}
                return jsonify(Status)
        Status = {"status": "success", "message": "Successfully inserted the data"}
        return jsonify(Status)


def extract_function_name(signature):
    match = re.search(r'def (\w+)\(', signature)
    if match:
        return match.group(1)
    return None


def convert_to_container(data_str):
    import ast
    try:
        # Safely evaluate the string
        data = ast.literal_eval(data_str)

        # Check if it is indeed a list or a dictionary
        if isinstance(data, (list, dict)):
            return data
        else:
            raise ValueError("Provided string is neither a list nor a dictionary")
    except (SyntaxError, ValueError) as e:
        # Handle errors if the string is not a valid Python literal or the right type
        return f"Error: {str(e)}"


@bp.route('/compile_code', methods=['POST'])
def compile_code():
    user_code = request.json.get('code', '')
    problem_id = request.json.get('problem_id', None)

    problem = Problem.query.get(problem_id)
    if not problem:
        return jsonify({"error": "Problem not found"}), 404

    function_signature = problem.function_signature
    test_cases = json.loads(problem.test_cases)
    expected_function_name = extract_function_name(function_signature)

    if expected_function_name not in user_code:
        print(expected_function_name, 'expected_function_name')
        return jsonify({
            "status": "Unscess",
            "message": f"The function name '{expected_function_name}' is required but not found in your code."
        }), 400

    test_case = test_cases[0]
    input_data = test_case['input']
    expected_output = test_case['expected_output']
    print(input_data)

    # Check if input_data is a list for multi-argument support
    if isinstance(input_data, dict):

        # Use **input_data to unpack dictionary into named arguments
        function_call = f"{expected_function_name}(**{input_data})"
        input_data = json.dumps(input_data)
    elif isinstance(input_data, list):

        print('asss')
        # If it's a list, we assume each element corresponds to an argument
        formatted_input = ",".join(arg for arg in input_data)
        function_call = f"{expected_function_name}(*[{formatted_input}])"
    else:
        # If it's a single argument, convert it directly
        # formatted_input = input_data
        function_call = f"{expected_function_name}({(input_data)})"

    output_conversion = """
    if isinstance(result, pd.DataFrame):
        output = {
            "headers": result.columns.tolist(),
            "values": result.values.tolist()
        }
    elif isinstance(result, list) or isinstance(result, dict):
        output = json.dumps(result)  # Convert list or dict to JSON
    else:
        output = result  # For simple types like int, str, etc.
    try:
        print(json.dumps(output))
    except:
        print(output)
    """
    standard_imports = """
import json
import pandas as pd
from typing import List, Optional
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    """

    code_with_input_handling = f"""{standard_imports}
{user_code}  # Inject user code

if __name__ == '__main__':
    
    result = {function_call}  # Pass input(s) dynamically
    {output_conversion}"""
    temp_dir = APP.config['TEMP_DIR']
    # Write code to a temporary file
    with tempfile.NamedTemporaryFile(suffix="_compile_code.py", mode='w', dir=temp_dir, delete=False) as temp_file:
        temp_file.write(code_with_input_handling)
        temp_file_path = temp_file.name

    # Run the temporary file with subprocess to check for syntax and runtime errors
    try:
        run_result = subprocess.run(
            ['python3', temp_file_path],
            capture_output=True,
            text=True,
            check=True
        )
        try:
            # Attempt to parse stdout as JSON
            output = json.loads(run_result.stdout.strip())
        except json.JSONDecodeError:
            # If stdout is not JSON, treat it as a simple string
            output = run_result.stdout.strip()
        try:
            output_check_ = convert_to_container(output)
            if output_check_.__contains__('Error'):
                output_check_ = output
        except:
            print('asmnsc')
            output_check_ = output

        success = json.dumps(output_check_) == json.dumps(expected_output)
        print(output_check_, 'asmnsc')
        # print(json.dumps(expected_output))
        # print(json.dumps(output))
        # print(success,"success")
        # If code runs without errors, return a success message
        return jsonify({
            "input_data": input_data,
            "expected_output": json.dumps(expected_output),
            "actual_Output": json.dumps(output_check_),
            "status": "success",
            "message": "Code compiled successfully!"
        })

    except subprocess.CalledProcessError as e:
        # If there is an error, capture the stderr and return as error message
        return jsonify({
            "status": "error",
            "message": e.stderr.strip()
        })

    finally:
        print('am')
        #Clean up the temporary file
        try:
            os.remove(temp_file_path)
        except OSError:
            pass


def insert_solutions(user_code, problem_id, exist_, id_=None):
    if exist_:
        user_id = session.get('user')
        head_insert = UserSolution(Id=id_, user_id=user_id, problem_id=problem_id,
                                   submission_code=user_code, status='Completed')
        try:
            db.session.merge(head_insert)
            db.session.commit()
            db.session.close()
            LOG.info("Successfully Updated data")
            msg = "Success"
        except Exception as e:
            LOG.error(e, exc_info=True)
            db.session.rollback()
            LOG.error("Error while pushing data")
            msg = "Failed"
        Status = {"status": msg}
        return jsonify(Status)
    else:
        user_id = session.get('user')
        head_insert = UserSolution(user_id=user_id, problem_id=problem_id,
                                   submission_code=user_code, status='Completed')
        try:
            db.session.merge(head_insert)
            db.session.commit()
            db.session.close()
            LOG.info("Successfully Inserted data")
            msg = "Success"
        except Exception as e:
            LOG.error(e, exc_info=True)
            db.session.rollback()
            LOG.error("Error while pushing data")
            msg = "Failed"
        Status = {"status": msg}
        return jsonify(Status)


@bp.route('/run_code', methods=['POST'])
def run_code():
    user_code = request.json.get('code', '')
    problem_id = request.json.get('problem_id', None)
    user_id = session.get('user')
    try:
        problem = UserSolution.query.filter_by(user_id=user_id, problem_id=problem_id).one()
    except:
        LOG.info("User Not Exists")
        problem = False
    if problem:
        exist_ = True
        insert_solutions(user_code, problem_id, exist_, id_=problem.Id)
    else:
        exist_ = False
        insert_solutions(user_code, problem_id, exist_)

    problem = Problem.query.get(problem_id)
    if not problem:
        return jsonify({"error": "Problem not found"}), 404

    function_signature = problem.function_signature
    expected_function_name = extract_function_name(function_signature)

    if expected_function_name not in user_code:
        return jsonify({
            "status": "Unscess",
            "message": f"The function name '{expected_function_name}' is required but not found in your code."
        }), 400

        # Load test cases from JSON
    test_cases = json.loads(problem.test_cases)
    results = []
    successful_run = True

    output_conversion = """
    if isinstance(result, pd.DataFrame):
        output = { "headers": result.columns.tolist(),"values": result.values.tolist()}
    elif isinstance(result, list) or isinstance(result, dict):
        output = json.dumps(result)  # Convert list or dict to JSON
    else:
        output = result  # For simple types like int, str, etc.
    try:
        print(json.dumps(output))
    except:
        print(output)
    """
    for case in test_cases:
        input_data = case['input']
        expected_output = case['expected_output']

        # Check if input_data is a list for multi-argument support
        if isinstance(input_data, dict):

            # Use **input_data to unpack dictionary into named arguments
            function_call = f"{expected_function_name}(**{input_data})"
            input_data = json.dumps(input_data)
        elif isinstance(input_data, list):
            # If it's a list, we assume each element corresponds to an argument
            formatted_input = ", ".join(arg for arg in input_data)
            function_call = f"{expected_function_name}(*[{formatted_input}])"
        else:
            # If it's a single argument, convert it directly
            # formatted_input = input_data
            function_call = f"{expected_function_name}({input_data})"

        # if isinstance(input_data, list):
        #     formatted_input = ", ".join(arg for arg in input_data)
        # else:
        #     formatted_input = input_data
        standard_imports = """
import json
import pandas as pd
from typing import List, Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
        """

        code_with_input_handling = f"""{standard_imports}
{user_code}  # Inject user code

if __name__ == '__main__':
    
    result = {function_call}  # Pass input(s) dynamically
    {output_conversion}"""
        temp_dir = APP.config['TEMP_DIR']
        with tempfile.NamedTemporaryFile(suffix="_compile_code.py", mode='w', dir=temp_dir, delete=False) as temp_file:
            temp_file.write(code_with_input_handling)
            temp_file_path = temp_file.name

        # Run the temporary file with subprocess to check for syntax and runtime errors
        try:
            run_result = subprocess.run(
                ['python3', temp_file_path],
                capture_output=True,
                text=True,
                check=True
            )
            try:
                # Attempt to parse stdout as JSON
                output = json.loads(run_result.stdout.strip())
            except json.JSONDecodeError:
                # If stdout is not JSON, treat it as a simple string
                output = run_result.stdout.strip()

            try:
                output_check_ = convert_to_container(output)
                if output_check_.__contains__('Error'):
                    output_check_ = output
            except:
                print('asmnsc')
                output_check_ = output

            print(type(output))
            success = json.dumps(output_check_) == json.dumps(expected_output)
            if success:
                results.append(
                    {'input': input_data, 'expected': json.dumps(expected_output), 'actual': json.dumps(output_check_),
                     'status': 'Passed'})
            else:
                results.append(
                    {'input': input_data, 'expected': json.dumps(expected_output), 'actual': json.dumps(output_check_),
                     'status': 'Failed'})

        except subprocess.CalledProcessError as e:
            successful_run = False
            print('dacmvvdc')
            # If there is an error, capture the stderr and return as error message
            return jsonify({'results': {}, 'successful_run': successful_run})
        finally:
            try:
                os.remove(temp_file_path)
            except OSError:
                pass

    return jsonify({'results': results, 'successful_run': successful_run})


@bp.route('/compile_sql_code', methods=['POST'])
def compile_sql_code():
    user_query = request.json.get('code', '')
    problem_id = request.json.get('problem_id', None)

    user_id = session.get('user')
    try:
        problem = UserSolution.query.filter_by(user_id=user_id, problem_id=problem_id).one()
    except:
        LOG.info("User Not Exists")
        problem = False
    if problem:
        exist_ = True
        insert_solutions(user_query, problem_id, exist_, id_=problem.Id)
    else:
        exist_ = False
        insert_solutions(user_query, problem_id, exist_)

    problem = Problem.query.get(problem_id)
    if not problem:
        return jsonify({"error": "Problem not found"}), 404

    test_cases = json.loads(problem.test_cases)
    results = []

    for case in test_cases:
        # Connect to a temporary in-memory SQLite database
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()

        # Run setup commands from 'input' in the test case to create tables and insert data
        try:
            for setup_sql in case['input']:
                cursor.execute(setup_sql)
        except sqlite3.Error as e:
            conn.close()
            return jsonify({"error": f"Setup error: {str(e)}"}), 400

        # Execute the user's query on the temporary database
        try:
            cursor.execute(user_query)
            user_output = cursor.fetchall()

            # Format the user output to match expected output format
            column_names = [description[0] for description in cursor.description]
            formatted_output = [dict(zip(column_names, row)) for row in user_output]

            # Compare the formatted output with the expected output
            success = formatted_output == case['expected_output']
            results.append({
                "user_output": json.dumps(formatted_output),
                "expected_output": json.dumps(case['expected_output']),
                "status": "success" if success else "failure",
                "message": "Query executed successfully" if success else "Output does not match expected result."
            })

        except sqlite3.Error as e:
            results.append({
                "error": str(e),
                "status": "error",
                "message": "Query execution failed."
            })
        finally:
            # Close the connection to reset the in-memory database for the next test case
            conn.close()

    # Check if all test cases passed for an overall status
    overall_status = all(result.get("status") == "success" for result in results)
    print(results)
    return jsonify({
        "results": results,
        "overall_status": "success" if overall_status else "failure"
    })

# @bp.route('/getallusers', methods=["GET", "POST"])
# def getallusers():
#     # Query all users from the ICICIMedUserTbl
#     users = User.query.all()
#
#     # Loop through each user and print the email_id
#     for user in users:
#         print(user.email_id)
#
#     return 'hellio'

# @bp.route('/run_code_sql', methods=['POST'])
# def run_code_sql():
#     user_code = request.json.get('code', '')
#     problem_id = request.json.get('problem_id', None)
#
#     problem = Problem.query.get(problem_id)
#     if not problem:
#         return jsonify({"error": "Problem not found"}), 404
#
#     function_signature = problem.function_signature
#     expected_function_name = extract_function_name(function_signature)
#
#     if expected_function_name not in user_code:
#         return jsonify({
#             "status": "Unscess",
#             "message": f"The function name '{expected_function_name}' is required but not found in your code."
#         }), 400
#
#         # Load test cases from JSON
#     test_cases = json.loads(problem.test_cases)
#     results = []
#     successful_run = True
#
#     output_conversion = """
#     if isinstance(result, pd.DataFrame):
#         output = { "headers": result.columns.tolist(),"values": result.values.tolist()}
#     elif isinstance(result, list) or isinstance(result, dict):
#         output = json.dumps(result)  # Convert list or dict to JSON
#     else:
#         output = result  # For simple types like int, str, etc.
#     try:
#         print(json.dumps(output))
#     except:
#         print(output)
#     """
#     for case in test_cases:
#         input_data = case['input']
#         expected_output = case['expected_output']
#
#         # Check if input_data is a list for multi-argument support
#         if isinstance(input_data, dict):
#
#             # Use **input_data to unpack dictionary into named arguments
#             function_call = f"{expected_function_name}(**{input_data})"
#             input_data = json.dumps(input_data)
#         elif isinstance(input_data, list):
#             # If it's a list, we assume each element corresponds to an argument
#             formatted_input = ", ".join(arg for arg in input_data)
#             function_call = f"{expected_function_name}(*[{formatted_input}])"
#         else:
#             # If it's a single argument, convert it directly
#             # formatted_input = input_data
#             function_call = f"{expected_function_name}({input_data})"
#
#         # if isinstance(input_data, list):
#         #     formatted_input = ", ".join(arg for arg in input_data)
#         # else:
#         #     formatted_input = input_data
#
#         code_with_input_handling = f"""from portal.solutions import *
# {user_code}  # Inject user code
#
# if __name__ == '__main__':
#     from portal.solutions import *
#     result = {function_call}  # Pass input(s) dynamically
#     {output_conversion}"""
#         temp_dir = APP.config['TEMP_DIR']
#         with tempfile.NamedTemporaryFile(suffix="_compile_code.py", mode='w', dir=temp_dir, delete=False) as temp_file:
#             temp_file.write(code_with_input_handling)
#             temp_file_path = temp_file.name
#
#         # Run the temporary file with subprocess to check for syntax and runtime errors
#         try:
#             run_result = subprocess.run(
#                 ['python3', temp_file_path],
#                 capture_output=True,
#                 text=True,
#                 check=True
#             )
#             try:
#                 # Attempt to parse stdout as JSON
#                 output = json.loads(run_result.stdout.strip())
#             except json.JSONDecodeError:
#                 # If stdout is not JSON, treat it as a simple string
#                 output = run_result.stdout.strip()
#
#             try:
#                 output = convert_to_container(output)
#                 print('assad', output, type(output))
#             except:
#                 output = output
#
#             print(type(output))
#             success = json.dumps(output) == json.dumps(expected_output)
#             if success:
#                 results.append(
#                     {'input': input_data, 'expected': json.dumps(expected_output), 'actual': json.dumps(output),
#                      'status': 'Passed'})
#             else:
#                 results.append(
#                     {'input': input_data, 'expected': json.dumps(expected_output), 'actual': json.dumps(output),
#                      'status': 'Failed'})
#
#         except subprocess.CalledProcessError as e:
#             successful_run = False
#             print('dacmvvdc')
#             # If there is an error, capture the stderr and return as error message
#             return jsonify({'results': {}, 'successful_run': successful_run})
#         finally:
#             print('am')
#             try:
#                 os.remove(temp_file_path)
#             except OSError:
#                 pass
#
#     return jsonify({'results': results, 'successful_run': successful_run})
