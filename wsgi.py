#!/usr/bin/env python


import os
import tempfile
import names


def application(environ, start_response):

    ctype = 'text/plain'
    name = None
    if environ['REQUEST_METHOD'] == 'POST' and environ.get('CONTENT_LENGTH', 0):
        ctype = "image/jpeg"

        # Get rid of headers.
        stream = environ['wsgi.input']
        while len(stream.readline().strip()):
            pass

        # Save as temporary file
        fp = tempfile.NamedTemporaryFile()
        fp.write(stream.read())

        with tempfile.TemporaryDirectory() as d:
            name = names.generate_name() + ".jpg"
            tmp_name = d + name

            # Now call ImageMagick
            os.system("convert {0} -gravity center -crop 582x328+0+0 - | "
                      "convert - {1}/watermark.png -gravity southeast "
                      "-composite {2}".format(fp.name,
                                              environ["OPENSHIFT_REPO_DIR"],
                                              tmp_name))

            with open(tmp_name, 'rb') as out_fp:
                response_body = out_fp.read()

    elif environ['PATH_INFO'] == '/juice':
        response_body = ['%s: %s' % (key, value)
                         for key, value in sorted(environ.items())]
        response_body = '\n'.join(response_body)
    else:
        ctype = 'text/html'
        response_body = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2//EN">

<html>
<head>
  <meta name="generator" content="Deges">
  <title>Hitler was pretty OK I guess.</title>
  <!-- https://i.imgur.com/jIxVqZA.jpg -->
</head>

<body style="background-color: black; color: black">
  <form action="/juice" method="post" enctype="multipart/form-data">
    <input type="file" name="pic" accept="image/*">
    <input type="submit">
  </form>
  <img src="http://pospolitost.sk/potoo.jpeg" style="position: absolute; right: 20%; bottom: 0px">
</body>
</html>
'''

    if ctype.startswith('text'):
        response_body = response_body.encode('utf-8')

    status = '200 OK'
    response_headers = [('Content-Type', ctype),
                        ('Content-Length', str(len(response_body)))]
    if name:
        response_headers.append(('Content-Disposition',
                                 "attachment; filename=\"{0}\"".format(name)))
    start_response(status, response_headers)
    return [response_body]

#
# Below for testing only
#
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8051, application)
