import tornado.ioloop
import tornado.web

class MainHnalder(tornado.web.RequestHandler):
	def get(self):
		self.write("hello world")

application=tornado.web.Application([
	(r'/',MainHnalder),
])

if __name__=="__main__":
	application.listen(8000)
	tornado.ioloop.IOLoop.instance().start()