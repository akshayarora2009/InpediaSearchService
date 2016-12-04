from gevent.wsgi import WSGIServer
from InpediaSearchService import app

http_server = WSGIServer(('', 80), app)
http_server.serve_forever()
