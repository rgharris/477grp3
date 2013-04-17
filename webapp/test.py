import bottle
from bottle import get, post, request

@get('/')
def show_form():
    return '''\
<img src="images/wood.png" />
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
