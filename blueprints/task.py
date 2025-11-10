import os
from asyncio import tasks
from alembic.script.write_hooks import console_scripts
from flask import Blueprint, session, request, redirect, url_for, flash
from flask import render_template
from form import form
from werkzeug.utils import secure_filename
from common.image import Image
from blueprints import user
from exts import db
from forms import TaskForm, TitleForm

from models import UserModel, TaskModel, TitleModel

bp = Blueprint('task', __name__, url_prefix="/task")

#set upload image file and file extension name
UPLOAD_FOLDER = 'static/media/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

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

            # print(newTitle.titleName)
            # print(newTitle.reviewNote)
            # print(newTitle.user_id)

            db.session.add(newTitle)
            db.session.commit()
            title_id = newTitle.id                                               # can be removed????
            flash("New task list created successfully")
            return redirect(url_for("task.dashboard",title_id=title_id)) #title_id = title_id canbe removed?
        else:
            flash("Cannot find user")
            print(form.errors)
            return redirect(url_for("task.dashboard"))

# write review note
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

# delete function for all tasks under same title
@bp.route('/delete/<int:title_id>',methods=['POST'])
def delete(title_id):
    delete_title = TitleModel.query.get_or_404(title_id)

    TaskModel.query.filter_by(title_id=title_id).delete()
    db.session.delete(delete_title)
    db.session.commit()
    flash("Task deleted successfully")

    return redirect(url_for("task.dashboard"))

#adding tasks page
@bp.route('/home/<int:title_id>',methods=['GET', 'POST'])
def home(title_id):
    if request.method == 'POST':

            description = request.form['description']
            status = request.form.get('task-status')
            priority = request.form.get('task-priorities')
            image = ""

            #Adding new task
            new_task = TaskModel(description=description, status=status, priority=priority, title_id=title_id,image=image)

            db.session.add(new_task)
            db.session.commit()

            flash("Task add successfully")
            return redirect(url_for("task.home",title_id=title_id))
    else:
        #display all tasks from same title
        tasks_data = TaskModel.query.filter_by(title_id=title_id).all()
        return render_template('home.html',tasks_data=tasks_data,title_id=title_id)


# delete tasks
@bp.route('/deleteTask/<int:task_id>',methods=['POST'])
def deleteTask(task_id):

    delete_task = TaskModel.query.get_or_404(task_id)

    title_id = delete_task.title_id

    #delete image
    if delete_task.image:
        file_path = os.path.join('static/media', delete_task.image)
        if os.path.exists(file_path):
            os.remove(file_path)

    # print(f"Delete Task {task_id}")

    db.session.delete(delete_task)
    db.session.commit()
    flash("Task deleted successfully")

    return redirect(url_for("task.home",title_id = title_id))

@bp.route('/editTask/<int:task_id>',methods=['GET', 'POST'])
def editTask(task_id):
    # edit_task = TaskModel.query.get_or_404(task_id)
    edit_task = db.session.execute(db.select(TaskModel).filter_by(id = task_id)).scalar_one()

    if request.method == 'POST':

        edit_task.description = request.form.get('description')
        edit_task.status = request.form.get('task-status')
        edit_task.priority = request.form.get('task-priorities')

        # print(request.form)

        db.session.commit()
        flash("Task edited successfully")
        return redirect(url_for("task.home",title_id = edit_task.title_id))
    else:
        return render_template('editTask.html',task=edit_task)


@bp.route('/upload/<int:task_id>',methods=['GET','POST'])
def upload(task_id):
    uploadImage_task = db.session.execute(db.select(TaskModel).filter_by(id=task_id)).scalar_one()

    if request.method == 'POST':

        file = request.files['image']

        if 'image' not in request.files:
            flash("No file provided")
            return redirect(url_for("task.home",title_id = uploadImage_task.title_id))

        if file.filename == '':
            flash("No file selected for uploading")
            return redirect(url_for("task.home",title_id = uploadImage_task.title_id))

        if file and allowed_file(file.filename):

            file_path = Image.get_images_path()
            filename = secure_filename(file.filename)
            fullpath = file_path.joinpath(filename)
            file.save(fullpath)

            print(filename)

            uploadImage_task.image=filename

            db.session.commit()

            flash("Uploaded successfully")
            return redirect(url_for("task.home",title_id = uploadImage_task.title_id))

        else:
            flash("File type not supported.")
            return redirect(url_for("task.home",title_id = uploadImage_task.title_id))

    else:
        return redirect(url_for("task.home",title_id = uploadImage_task.title_id))
