from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from app.users.forms import RegistrationForm, EditForm
from app.images.forms import UserUploads
from app.users.models import User
from app import db
import pdb
import os
import braintree
from app.helpers import upload_file_to_s3, allowed_images, generate_client_token, transact, find_transaction
from app.config import S3_LOCATION, S3_BUCKET, S3_KEY, S3_SECRET
from app.images.models import Image, Donation


TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]



users_blueprint = Blueprint('users', __name__)



@users_blueprint.route('/signup', methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('sessions.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'{form.username.data}, your account has been created, you can now log in!')
        return redirect(url_for('sessions.login'))
    return render_template('signup.html', title='Register', form=form)

@users_blueprint.route('/edit/<id>', methods=["GET", "POST"])
@login_required
def edit(id):
    user = User.query.get(id)
    form = EditForm()
    if form.validate_on_submit():
        user.password = generate_password_hash(form.password.data)
        user.email = form.email.data
        db.session.add(user)
        db.session.commit()
        flash(f'{user.username}, your account has been updated, you can now log in!')
        return redirect(url_for('sessions.login'))        
        
    return render_template('edit.html', form=form)


@users_blueprint.route('/profilepic/<id>', methods=["POST"])
@login_required
def profilepic(id):
    user = User.query.get(id)
    form = EditForm()
    
    if not form.image_file.data:
        flash("no image")
        return redirect(url_for("users.edit", id=current_user.id))
    
    file = form.image_file.data

    
    if file and allowed_images(file.filename):
        file.filename = secure_filename(user.username + "-" + file.filename)
        user.image_file = file.filename

        output = upload_file_to_s3(file, S3_BUCKET)

        db.session.add(user)
        db.session.commit()

        flash(f'{user.username}, your profile image has been updated')
        return redirect(url_for('sessions.home'))  

    else:  
        flash('doesnt work bitch')
        return render_template('edit.html', form=form)

@users_blueprint.route('/profile/<id>', methods=["GET"])
@login_required
def user_profile(id):
    user = User.query.get(id)
    image = user.images
    form = UserUploads()
    if user.image_file is None:
        image_file = url_for('static', filename='default.jpg')
        return image_file
    else:
        image_file = (S3_LOCATION + user.image_file)


    return render_template('profile.html', form=form, image_file=image_file, user=user, image=image)



@users_blueprint.route('/images/<id>', methods=["POST"])
@login_required
def user_image(id):
    user = User.query.get(id)

    form = UserUploads()
    
    if not form.image.data:
        flash("no image")
        return redirect(url_for("users.edit", id=current_user.id))
    
    file = form.image.data


    if file and allowed_images(file.filename):
        file.filename = secure_filename(user.username + "-" + file.filename)
        image = Image(user_id=current_user.id, image_name=file.filename)

        output = upload_file_to_s3(file, S3_BUCKET)

        db.session.add(image)
        db.session.commit()

        flash(f'{user.username}, your image has been posted')
        return redirect(url_for('sessions.home'))  

    else:  
        flash('doesnt work bitch')
        return render_template('edit.html', form=form)

@users_blueprint.route('/checkout', methods=["GET"])
def checkout():

    client_token = generate_client_token()


    return render_template('donate.html', client_token=client_token)


@users_blueprint.route('/checkouts/<transaction_id>', methods=['GET'])
def show_checkout(transaction_id):
    transaction = find_transaction(transaction_id)
    result = {}
    if transaction.status in TRANSACTION_SUCCESS_STATUSES:
        result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': 'Your test transaction has been successfully processed. See the Braintree API response and try again.'
        }
    else:
        result = {
            'header': 'Transaction Failed',
            'icon': 'fail',
            'message': 'Your test transaction has a status of ' + transaction.status + '. See the Braintree API response and try again.'
        }

    return render_template('show.html', transaction=transaction, result=result)


@users_blueprint.route('/checkouts', methods=['POST'])
def create_checkout():

    result = transact({
        'amount': request.form['amount'],
        'payment_method_nonce': request.form['payment_method_nonce'],
        'options': {
            "submit_for_settlement": True
        }
    })
    amount = request.form['amount']


    if result.is_success or result.transaction:
        transaction = Donation(amount=amount)
        db.session.add(transaction)
        db.session.commit()

        return redirect(url_for('users.show_checkout',transaction_id=result.transaction.id))
    else:
        for x in result.errors.deep_errors: flash('Error: %s: %s' % (x.code, x.message))
        return redirect(url_for('users.checkout'))


@users_blueprint.route('/<id>', methods=['GET'])
def show(id):

    return redirect(url_for('users.checkout', image_id=id))

