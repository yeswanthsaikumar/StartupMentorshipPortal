from app import app , db
from flask import render_template , redirect , flash , url_for ,request
from app.forms import LoginForm , RegistrationForm , EditProfileForm , PostForm , StoryForm , MessageForm , ResetPasswordRequestForm, ResetPasswordForm
from app.email import send_email , send_password_reset_email
from flask_login import current_user , login_user , logout_user , login_required
from app.models import User , Post , Stories , News , Message
from werkzeug.urls import url_parse
from datetime import datetime


@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()


@app.route('/' , methods=['GET' , 'POST'])
@app.route('/home/' , methods=['GET' , 'POST'])
@login_required
def home():

	form = PostForm()

	if form.validate_on_submit() :
		post = Post(body=form.post.data , author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('your post is on live')
		return redirect(url_for('home'))

	page = request.args.get('page', 1, type=int )

	posts = current_user.followed_posts().paginate( page, app.config['POSTS_PER_PAGE'],False)

	if posts.has_next :
		next_url = url_for('home' , page=posts.next_num)
	else :
		next_url = None

	if posts.has_prev :
		prev_url = url_for('home' , page=posts.prev_num)
	else :
		prev_url = None

	return render_template('home.html' , posts=posts.items, form=form, title='home' , next_url=next_url , prev_url=prev_url)




@app.route('/register/' , methods=['POST' , 'GET'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data , email=form.email.data , user_category=form.user_category.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('login'))
	return render_template("register.html" , title='Register' , form=form )




@app.route('/login/' ,methods=['POST' , 'GET'])
def login():
	
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()

		if user is None or not user.check_password(form.password.data):
			flash('Invalid login id or password')
			return redirect(url_for('login'))

		login_user( user , remember=form.remember_me.data)

		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '' :
			next_page = url_for('home')
		return redirect(next_page)

	return render_template( 'login.html', title='Sign In' , form=form)


@app.route('/logout/')
def logout():
	logout_user()

	return redirect(url_for('home'))


@app.route('/user/<username>/')
@login_required
def user(username):

	user = User.query.filter_by(username=username).first_or_404()

	return render_template("user.html", user=user )

	

@app.route('/editprofile/', methods=['GET', 'POST'])
@login_required
def editprofile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('editprofile.html', title='Edit Profile',
                           form=form)

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('home'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('home'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/stories/' , methods=['POST' , 'GET'])
@login_required
def stories():
	form = StoryForm()

	if form.validate_on_submit() :
		story = Stories(body=form.story.data , author=current_user)
		db.session.add(story)
		db.session.commit()
		flash('your post is on live')
		return redirect(url_for('stories'))

	page = request.args.get('page', 1, type=int )

	stories = Stories.query.order_by(Stories.timeStamp.desc()).paginate( page, app.config['POSTS_PER_PAGE'],False)	

	if stories.has_next :
		next_url = url_for('explore' , page=stories.next_num)
	else :
		next_url = None

	if stories.has_prev :
		prev_url = url_for('explore' , page=stories.prev_num)
	else :
		prev_url = None

	return render_template('stories.html' , posts=stories.items , title='stories' , next_url=next_url , prev_url=prev_url , form=form)


@app.route('/news/')
def news():

	page = request.args.get('page', 1, type=int )

	news = News.query.order_by(News.timeStamp.desc()).paginate( page, app.config['POSTS_PER_PAGE'],False)	

	if news.has_next :
		next_url = url_for('explore' , page=news.next_num)
	else :
		next_url = None

	if news.has_prev :
		prev_url = url_for('explore' , page=news.prev_num)
	else :
		prev_url = None

	return render_template('news.html' , posts=news.items , title='news' , next_url=next_url , prev_url=prev_url)



@app.route('/mentors/')
@login_required
def mentors():

	mentors = User.query.filter_by(user_category='mentor')	

	return render_template('mentors.html', mentors=mentors, title='mentors')


@app.route('/send_message/<recipient>/', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash('Your message has been sent.')
        return redirect(url_for('user', username=recipient))
    return render_template('send_message.html', title='Send Message', form=form, recipient=recipient)

@app.route('/messages/')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    db.session.commit()
    
    page = request.args.get('page', 1, type=int)
    
    messages = current_user.messages_recieved.order_by(
        Message.timestamp.desc()).paginate(
            page, app.config['POSTS_PER_PAGE'], False)
    
    next_url = url_for('messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('messages', page=messages.prev_num) \
        if messages.has_prev else None
    
    return render_template('messages.html', messages=messages.items, next_url=next_url, prev_url=prev_url)

@app.route('/reset_password_request/', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)