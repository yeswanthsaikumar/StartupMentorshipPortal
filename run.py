from app import app , db
from app.models import User , Post , Stories , News



@app.shell_context_processor
def make_shell_context():
	return {'db':db , 'User':User , 'Post':Post  , 'Stories':Stories , 'News':News }


if __name__ == '__main__':

	app.run(debug=True)