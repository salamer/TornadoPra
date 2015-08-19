import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import os.path

from tornado.options import define,options
define("port",default=8002,help="run on given port",type=int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers=[
			(r'/',MainHandler),
		]
		settings=dict(template_path=os.path.join(os.path.dirname(__file__),"templates"),
			static_path=os.path.join(os.path.dirname(__file__),"statics"),
			debug=True
			)
		tornado.web.Application.__init__(self,handlers,**settings)

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("index.html",
			page_title="burt's book | home",
			header_text="welcome to burt's books!",
		)

class BookModule(tornado.web.UIModule):
	def render(self,book):
		return self.render_string("module/book.html",book=book)

class RecommendedHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "recommended.html",
            page_title="Burt's Books | Recommended Reading",
            header_text="Recommended Reading",
            books=[
                {
                    "title":"Programming Collective Intelligence",
                    "subtitle": "Building Smart Web 2.0 Applications",
                    "image":"/static/images/collective_intelligence.gif",
                    "author": "Toby Segaran",
                    "date_added":1310248056,
                    "date_released": "August 2007",
                    "isbn":"978-0-596-52932-1",
                    "description":"<p>This fascinating book demonstrates how you "
                        "can build web applications to mine the enormous amount of data created by people "
                        "on the Internet. With the sophisticated algorithms in this book, you can write "
                        "smart programs to access interesting datasets from other web sites, collect data "
                        "from users of your own applications, and analyze and understand the data once "
                        "you've found it.</p>"
                },
                ...
            ]
        )

if __name__=="__main__":
	tornado.options.parse_command_line()
	http_server=tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

