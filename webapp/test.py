import bottle
from bottle import get, post, request, response, static_file, template, TEMPLATE_PATH

##########################USEFUL FUNCTIONS################################
#def displayResources():
	

if '/home/pi/477grp3/webapp/layouts/' not in TEMPLATE_PATH:
	TEMPLATE_PATH.insert(0,'/home/pi/477grp3/webapp/layouts/')

@get('/images/<filename>')
def serve_image(filename):
	return static_file(filename, root='/home/pi/477grp3/webapp/images/')

@get('/styles/style.css')
def serve_stylesheet():
	return static_file("style.css", root='/home/pi/477grp3/webapp/styles/')

@get('/js/functions.js')
def serve_javascript():
	return static_file("functions.js", root='/home/pi/477grp3/webapp/js/')

@get('/styles/<filename>')
def serve_image(filename):
	return static_file(filename, root='/home/pi/477grp3/webapp/styles')

#@get('/modal')
#def display_modal():
#  return template('layout', modal=True) 

# This request happens every X seconds in case anything needs to be updated in the webapp
@get('/refreshContent')
def handle_ajax():
	rid = request.query.id
	if rid == "resources":
		#return displayResources()
		return "{\"clay\":\"" + request.get_cookie("playerID") + "\"}"
	return "<p>This is a test of how long it takes to open a modal box with dynamic content!!!</p>"

# This request handles a 

@get('/')
def show_webapp():
	response.set_cookie("playerID", "-1")
	return template('layout')

#@get('/blah')
#def show_form():
#	return '''\
#<img src="/images/wood.png" />
#<form action="" method="POST">
#    <label for="name">What is your name?</label>
#    <input type="text" name="name"/>
#    <input type="submit"/>
#</form>'''

#@post('/')
#def show_name():
#	return "Hello, {}!".format(request.POST.name)

application=bottle.default_app()       # run in a WSGI server
#bottle.run(host='localhost', port=8080) # run in a local test server
