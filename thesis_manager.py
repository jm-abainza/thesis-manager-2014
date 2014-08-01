import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'
DEFAULT_GUESTBOOK_NAME1 = 'default_guestbook1'
DEFAULT_GUESTBOOK_NAME2 = 'default_guestbook2'


# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('Guestbook', guestbook_name)

class Greeting(ndb.Model):
    """Models an individual Guestbook entry."""
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

class MainPage(webapp2.RequestHandler):

    def get(self):
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class Guestbook(webapp2.RequestHandler):
    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each Greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
    
        greeting = Greeting(parent=guestbook_key(guestbook_name))


        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()
        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))


class Guestbook1(webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each Greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
        guestbook_name = self.request.get('guestbook_name1',
                                          DEFAULT_GUESTBOOK_NAME1)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/module-1/1?' + urllib.urlencode(query_params))

class Guestbook2(webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each Greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
        guestbook_name = self.request.get('guestbook_name2',
                                          DEFAULT_GUESTBOOK_NAME2)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/module-1/2?' + urllib.urlencode(query_params))


class SigninHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                        (user.nickname(), users.create_logout_url('/')))
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                        users.create_login_url('/'))

        self.response.out.write("<html><body>%s</body></html>" % greeting)


class MemberOnePage(webapp2.RequestHandler):
    
    def get(self):
        guestbook_name = self.request.get('guestbook_name1',
                                          DEFAULT_GUESTBOOK_NAME1)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(5)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('memberone.html')
        self.response.write(template.render(template_values))

class MemberTwoPage(webapp2.RequestHandler):
    
    def get(self):
        guestbook_name = self.request.get('guestbook_name2',
                                          DEFAULT_GUESTBOOK_NAME2)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(5)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('membertwo.html')
        self.response.write(template.render(template_values))


class Thesis(ndb.Model):
    """Models an individual Guestbook entry."""
    title = ndb.StringProperty(indexed=False)
    description = ndb.StringProperty(indexed=False)
    schoolyear = ndb.StringProperty(indexed=False)
    status = ndb.StringProperty(indexed=False)


class ThesisViewHandler(webapp2.RequestHandler):
	def get(self, id):

		thesis = Thesis.get_by_id(long(id))
		template_values = {
		"thesis" : thesis
		}

	 	template = JINJA_ENVIRONMENT.get_template('thesisviewid.html')
 		self.response.write(template.render(template_values))

class ThesisListHandler(webapp2.RequestHandler):
	def get(self):
		thesis= Thesis.query().fetch()
		template_values={
			"all_thesis": thesis
		}
	 	template = JINJA_ENVIRONMENT.get_template('thesislist.html')
 		self.response.write(template.render(template_values))


class ThesisNewHandler(webapp2.RequestHandler):
	def get(self):
	 	template = JINJA_ENVIRONMENT.get_template('thesisnew.html')
 		self.response.write(template.render())

 	def post(self):
 		thesis= Thesis()
 		thesis.title=self.request.get('title');
 		thesis.description=self.request.get('description');
 		thesis.schoolyear=self.request.get('schoolyear');
 		thesis.status=self.request.get('status');
 		thesis.put()
		self.redirect('/thesis/success')

class ThesisSuccessHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('thesissuccess.html')
        self.response.write(template.render())

class ThesisEditHandler(webapp2.RequestHandler):

    def get(self, id):

        thesis = Thesis.get_by_id(long(id))
        template_values = {
        "thesis" : thesis
        }

        template = JINJA_ENVIRONMENT.get_template('thesisedit.html')
        self.response.write(template.render(template_values))

    def post(self, id):
        thesis= Thesis.get_by_id(long(id))
        thesis.title=self.request.get('title');
        thesis.description=self.request.get('description');
        thesis.schoolyear=self.request.get('schoolyear');
        thesis.status=self.request.get('status');
        thesis.put()
        self.redirect('/thesis/success')
        
        



class Adviser(ndb.Model):
    """Models an individual Guestbook entry."""
    title = ndb.StringProperty(indexed=False)
    firstname = ndb.StringProperty(indexed=False)
    lastname = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)
    phonenumber = ndb.StringProperty(indexed=False)
    department = ndb.StringProperty(indexed=False)

class AdviserViewHandler(webapp2.RequestHandler):
    def get(self, id):

        adviser = Adviser.get_by_id(long(id))
        template_values = {
        "adviser" : adviser
        }

        template = JINJA_ENVIRONMENT.get_template('adviserviewid.html')
        self.response.write(template.render(template_values))

class AdviserNewHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('advisernew.html')
        self.response.write(template.render())

    def post(self):
        adviser = Adviser()
        adviser.title=self.request.get('title');
        adviser.firstname=self.request.get('firstname');
        adviser.lastname=self.request.get('lastname');
        adviser.email=self.request.get('email');
        adviser.phonenumber=self.request.get('phonenumber');
        adviser.department=self.request.get('department');
        adviser.put()
        self.redirect('/adviser/success')

class AdviserListHandler(webapp2.RequestHandler):
    def get(self):
        adviser = Adviser.query().fetch()
        template_values={
            "all_adviser": adviser
        }
        template = JINJA_ENVIRONMENT.get_template('adviserlist.html')
        self.response.write(template.render(template_values))

class AdviserSuccessHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('advisersuccess.html')
        self.response.write(template.render())

class AdviserEditHandler(webapp2.RequestHandler):
        
    def get(self, id):

        adviser = Adviser.get_by_id(long(id))
        template_values = {
        "adviser" : adviser
        }

        template = JINJA_ENVIRONMENT.get_template('adviseredit.html')
        self.response.write(template.render(template_values))

    def post(self, id):
        adviser = Adviser.get_by_id(long(id))
        adviser.title=self.request.get('title');
        adviser.firstname=self.request.get('firstname');
        adviser.lastname=self.request.get('lastname');
        adviser.email=self.request.get('email');
        adviser.phonenumber=self.request.get('phonenumber');
        adviser.department=self.request.get('department');
        adviser.put()
        self.redirect('/adviser/success')





class Student(ndb.Model):
    """Models an individual Guestbook entry."""
    first_name = ndb.StringProperty(indexed=False)
    last_name = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)
    student_number = ndb.StringProperty(indexed=False)

class StudentSuccessHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('studentsuccess.html')
        self.response.write(template.render())


class StudentViewHandler(webapp2.RequestHandler):
    def get(self, id):

        student = Student.get_by_id(long(id))
        template_values = {
        "student" : student
        }

        template = JINJA_ENVIRONMENT.get_template('studentviewid.html')
        self.response.write(template.render(template_values))

class StudentListHandler(webapp2.RequestHandler):
    def get(self):
        student= Student.query().fetch()
        template_values={
            "all_students": student
        }
        template = JINJA_ENVIRONMENT.get_template('student_list.html')
        self.response.write(template.render(template_values))

class StudentNewHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('student_new.html')
        self.response.write(template.render())

    def post(self):
        student= Student()
        student.first_name=self.request.get('first_name');
        student.last_name=self.request.get('last_name');
        student.email=self.request.get('email');
        student.student_number=self.request.get('student_number');
        student.put()
        self.redirect('/student/success')

class StudentSuccessHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('studentsuccess.html')
        self.response.write(template.render())



class StudentEditHandler(webapp2.RequestHandler):
    def get(self, id):
        student = Student.get_by_id(long(id))
        template_values = {
        "student" : student
        }

        template = JINJA_ENVIRONMENT.get_template('studentedit.html')
        self.response.write(template.render(template_values))

    def post(self, id):
        student = Student.get_by_id(long(id))
        student.first_name=self.request.get('first_name');
        student.last_name=self.request.get('last_name');
        student.email=self.request.get('email');
        student.student_number=self.request.get('student_number');
        student.put()
        self.redirect('/student/success')







application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
    ('/sign1', Guestbook1),
    ('/sign2', Guestbook2),
    ('/module-1/1', MemberOnePage),
    ('/module-1/2', MemberTwoPage),
    ('/thesis/new', ThesisNewHandler),
    ('/adviser/view/(.*)', AdviserViewHandler),
    ('/thesis/list', ThesisListHandler),
    ('/thesis/view/(.*)', ThesisViewHandler), 
    ('/adviser/new', AdviserNewHandler),
    ('/adviser/list', AdviserListHandler),
    ('/adviser/success',AdviserSuccessHandler),
    ('/thesis/success',ThesisSuccessHandler),
    ('/student/success', StudentSuccessHandler),
    ('/student/new', StudentNewHandler),
    ('/student/list', StudentListHandler),
    ('/student/view/(.*)', StudentViewHandler), 
    ('/thesis/edit/(.*)', ThesisEditHandler),
    ('/student/edit/(.*)', StudentEditHandler),
    ('/adviser/edit/(.*)', AdviserEditHandler),
    ('/signin',SigninHandler),     
], debug=True)
