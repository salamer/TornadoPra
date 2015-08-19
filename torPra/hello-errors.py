import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define,options

def ("port",default=8000,help="run on the given port ",type=int)

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		greeting=self.get_argument("greeting",'hello')
		self.write(greeting+',friendly user!')
	def write_error(self,status_code,**kwargs):
		self.write("gosh fuck damn!!you caused a %d error." % status_code)

if __name__=="__main__":
	tornado.options.parse_command_line()
	app=tornado.web.Application(handlers=[(r"/",IndexHandler)])
	http_server=tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOloop.instance().start()