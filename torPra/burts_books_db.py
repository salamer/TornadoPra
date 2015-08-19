import os.path
import tornado.locale
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define,options
import pymongo

define("port",default=8002,help="run the given port",type=int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers=[
			(r'/',MainHandler),
			(r'/recommended',RecommandedHandler),
			(r'/edit/([0-9Xx\-]+)',BookEditHandler),
			(r'/add',BookEditHandler)
		]
		settings=dict(
			template_path=os.path.join(os.path.dirname(__file__),"templates"),
			static_path=os.path.join(os.path.dirname(__file__),"statics"),
			ui_modules={"Book":BookModule},
			debug=True
		)
		client=pymongo.MongoClient("localhost",27017)
		self.db=client.bookstore
		tornado.web.Application.__init__(self,handlers,**settings)

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render(
			"index.html",
			page_title="burt's book |home",
			header_text="welcome to burt's books",
		)

class RecommandedHandler(tornado.web.RequestHandler):
	def get(self):
		coll=self.application.db.books
		books=coll.find()
		self.render(
			"recommanded.html",
			page_title="burt's books | recommanded Reading",
			header_text="recommanded Reading",
			books=books,
		)

class BookEditHandler(tornado.web.RequestHandler):
	def get(self,isbn=None):
		book=dict()
		if isbn:
			coll=self.application.db.books
			book=coll.find_one({"isbn":isbn})
		self.render("book_edit.html",
			page_title="burt's books",
			header_text="Edit books",
			book=book)

	def post(self,isbn=None):
		import time
		book_fields=['isbn','title','subtitle','image','author','date_released','description']
		coll=self.application.db.books
		book=dict()
		if isbn:
			book=coll.find_one({"isbn":isbn})
		for key in book_fields:
			book[key]=self.get_argument(key,None)

		if isbn:
			coll.save(book)
		else:
			book['date_added']=int(time.time())
			coll.insert(book)
		self.redirect("/recommanded/")


class BookModule(tornado.web.UIModule):
	def render(self,book):
		return self.render_string(
			"modules/book.html",
			book=book,
		)

	def css_files(self):
		return "/static/css/recommanded.css"

	def javascript_files(self):
		return "/static/js/recommanded.js"

if __name__=="__main__":
	tornado.options.parse_command_line()
	http_server=tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

