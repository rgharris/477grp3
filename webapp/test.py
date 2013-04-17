import bottle
from bottle import get, post, request, static_file, template, TEMPLATE_PATH

if '/home/pi/477grp3/webapp/layouts/' not in TEMPLATE_PATH:
	TEMPLATE_PATH.insert(0,'/home/pi/477grp3/webapp/layouts/')

@get('/images/<filename>')
def serve_image(filename):
	return static_file(filename, root='/home/pi/477grp3/webapp/images/')

@get('/styles/style.css')
def serve_stylesheet():
	return static_file("style.css", root='/home/pi/477grp3/webapp/styles/')

@get('/')
def show_webapp():
	return template('layout')

@get('/blah')
def show_form():
	return '''\
<img src="/images/wood.png" />
<form action="" method="POST">
    <label for="name">What is your name?</label>
    <input type="text" name="name"/>
    <input type="submit"/>
</form>'''

@post('/')
def show_name():
	return "Hello, {}!".format(request.POST.name)

application=bottle.default_app()       # run in a WSGI server
#bottle.run(host='localhost', port=8080) # run in a local test server
