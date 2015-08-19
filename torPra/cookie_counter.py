import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options

from tornado.options import define,options

define("port",default=8002,help="run the given port ",type=int)

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		cookie=self.get_secure_cookie("count")
		count=int(cookie)+1 if cookie else 1

		countString="1 time" if count ==1 else "%d times" % count

		self.set_secure_cookie("count",str(count))

		

		self.write(

             countString+"times"
            )

if __name__=='__main__':
	tornado.options.parse_command_line()

	settings={
	"cookie_secret":"bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
	"xsrf_cookies":True
	}

	application=tornado.web.Application([
		(r'/',MainHandler)
		],**settings)

	http_server=tornado.httpserver.HTTPServer(application)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

