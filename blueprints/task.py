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
            reviewNote = "None"
            user_id = session.get('user_id')
            newTitle = TitleModel(titleName=titleName, reviewNote=reviewNote, user_id=user_id)

            print(newTitle.titleName)
            print(newTitle.reviewNote)
            print(newTitle.user_id)


            db.session.add(newTitle)
            db.session.commit()
            title_id = newTitle.id                                               # can be removed????
            flash("New task list created successfully")
            return redirect(url_for("task.dashboard",title_id=title_id)) #title_id = title_id canbe removed?
        else:
            flash("Cannot find user")
            print(form.errors)
            return redirect(url_for("task.dashboard"))

@bp.route('/review/<int:title_id>',methods=['GET', 'POST'])
def review(title_id):
    # print(title_id)
    review_title = TitleModel.query.get_or_404(title_id)
    form = TitleForm(request.form)
    if request.method == 'POST':

        if form.validate():

            review_title.reviewNote = request.form.get('reviewNote',"").strip()
            review_title.user_id = session.get('user_id')

            db.session.commit()
            flash("Note added successfully")
            return redirect(url_for("task.dashboard",title_id=title_id))
        else:
            flash("Note added unsuccessfully")
            return redirect(url_for("task.review",title_id=title_id))

    else:
            # print(review_title)
            return render_template('review.html', title=review_title,form=form)

@bp.route('/delete/<int:title_id>',methods=['POST'])
def delete(title_id):
    delete_title = TitleModel.query.get_or_404(title_id)

    TaskModel.query.filter_by(title_id=title_id).delete()
    db.session.delete(delete_title)
    db.session.commit()
    flash("Task deleted successfully")

    return redirect(url_for("task.dashboard"))

#add task page
@bp.route('/home/<int:title_id>',methods=['GET', 'POST'])
def home(title_id):
    if request.method == 'POST':

            description = request.form['description']
            status = request.form.get('task-status')
            priority = request.form.get('task-priorities')

            print(description)
            print(status)
            print(priority)
            print(title_id)

            new_task = TaskModel(description=description, status=status, priority=priority, title_id=title_id)

            db.session.add(new_task)
            db.session.commit()

            flash("Task add successfully")
            return redirect(url_for("task.home",title_id=title_id))
    else:
        tasks_data = TaskModel.query.filter_by(title_id=title_id).all()
        return render_template('home.html',tasks_data=tasks_data,title_id=title_id)



