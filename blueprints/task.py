from asyncio import tasks

from alembic.script.write_hooks import console_scripts
from flask import Blueprint, session, request, redirect, url_for, flash
from flask import render_template
from form import form

from blueprints import user
from exts import db
from forms import TaskForm, TitleForm

from models import UserModel, TaskModel, TitleModel

bp = Blueprint('task', __name__, url_prefix="/task")

#dashboard page
@bp.route('/dashboard',methods=['GET', 'POST'])
def dashboard():
    if request.method == 'GET':
        user_id = session.get('user_id')
        titles_data = TitleModel.query.filter_by(user_id=user_id).all()
        return render_template('dashboard.html',titles_data=titles_data)
    else:
        form = TitleForm(request.form)
        if form.validate():
            titleName = form.titleName.data
            reviewNote = ""
            user_id = session.get('user_id')
            newTitle = TitleModel(titleName=titleName, reviewNote=reviewNote, user_id=user_id)

            db.session.add(newTitle)
            db.session.commit()
            flash("Task added successfully")
            return redirect(url_for("task.home"))
        else:
            flash("Cannot find user")
            print(form.errors)
            return redirect(url_for("task.dashboard"))

@bp.route('/review/<int:title_id>',methods=['GET', 'POST'])
def review(title_id):
    # print(title_id)
    review_title = db.session.execute(db.select(TitleModel).filter_by(id=title_id)).scalar_one()

    if review_title:
        if request.method == 'POST':
            form = TitleForm(request.form)
            if form.validate():

                new_titleName = review_title.titleName
                new_reviewNote = request.form['reviewNote']
                new_user_id = session.get('user_id')
                db.session.delete(review_title)

                review_title.id = title_id
                review_title.titleName = new_titleName
                review_title.ReviewNote = new_reviewNote
                review_title.user_id = new_user_id

                print(review_title.titleName)
                print(review_title.ReviewNote)
                print(review_title.user_id)

                new_review_title = TitleModel(id=review_title.id,titleName=review_title.titleName, reviewNote=review_title.ReviewNote, user_id=review_title.user_id)
                db.session.add(new_review_title)
                db.session.commit()
                flash("Note added successfully")
                return redirect(url_for("task.dashboard"))
            else:
                flash("Note added unsuccessfully")
                return redirect(url_for("task.review"))

        elif request.method == 'GET':
                print(review_title)
                return render_template('review.html', title=review_title)

@bp.route('/delete/<int:title_id>',methods=['GET', 'POST'])
def delete(title_id):
    review_title = db.session.execute(db.select(TitleModel).filter_by(id=title_id)).scalar_one()
    if review_title:
        if request.method == 'POST':
            db.session.delete(review_title)
            db.session.commit()
            flash("Note deleted successfully")
            return redirect(url_for("task.dashboard"))
        else:
            flash("Note deleted unsuccessfully")
            return redirect(url_for("task.dashboard"))

#add task page
@bp.route('/home',methods=['GET', 'POST'])
def home():

    if request.method == 'GET':

        tasks = db.session.query(TaskModel).all()

        return render_template('home.html', tasks=tasks)
    else:
        return render_template('home.html')



