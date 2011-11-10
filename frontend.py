import sys
import getopt

import web

import BasicSender

from web import form

urls = (
    '/', 'index')
app = web.application(urls,globals())
render = web.template.render('templates/')

message_form = form.Form(
    form.Textbox('from'),
    form.Textbox('to'),
    form.Textbox('message')
)

class index():
    def GET(self):
        f = message_form()
        return render.message(f)

    def POST(self):
        f = message_form()
        if not f.validates():
            return render.message(f)
        from_addr = f['from'].value
        to_addr = f['to'].value
        message = f['message'].value
        packet = "%s -> %s: %s" % (from_addr, to_addr, message)
        print "sending message: %s" % (packet)
        web.sender.send(packet)
        return render.message(f)

if __name__ == "__main__":
    def usage():
        print "Usage: python frontend.py [-h HOST] [-p PORT]"
        print ""
        print "EE122 collision example web interface"
        print "Requires web.py, BasicSender, and the templates folder to run."
        print "-h HOST | --host=HOST Host that collider.py is running on, default localhost"
        print "-p PORT | --port=PORT The listen port, defaults to 33122"
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 
                               "h:p:t:", ["host=", "port="])
    except:
        usage()
        exit()

    host = "127.0.0.1"
    port = 33122
    debug = False

    for o,a in opts:
        if o in ("-h", "--host="):
            host = str(h)
        if o in ("-p", "--port="):
            port = int(a)
        else:
            print usage()
            exit()
    web.sender = BasicSender.BasicSender(host,port,None)    
    app.run()
