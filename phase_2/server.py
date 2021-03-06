import socket


def log(*args, **kwargs):
    print('log', *args, **kwargs)


# handler of index page, path `/`
def route_index():
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = '<h1>"Hello Joe, I mean, Haobo, my dude!"</h1>' \
           '<h1>"Ah OK."</h1>' \
           '<img src="/doge.gif">'
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


# helper method for loading a static HTML file
def page(name):
    with open(name, encoding='utf-8') as f:
        return f.read()


# handler of message page, path `/message`
def route_message():
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = page('html_basic.html')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


# handler for the doge gif, hard coded for testing
def route_image():
    with open('doge.gif', 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
        img = header + b'\r\n' + f.read()
        return img


# error handler, supporting 404 only currently
def error(code=404):
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


# core routing
def response_for_path(path):
    r = {
        '/': route_index,
        '/doge.gif': route_image,
        '/message': route_message,
    }
    response = r.get(path, error)
    return response()


def run(host='', port=3000):
    with socket.socket() as s:
        s.bind((host, port))
        while True:
            s.listen(5)
            connection, address = s.accept()
            request = connection.recv(1024)
            log('raw, ', request)
            request = request.decode('utf-8')
            log('ip and request, {}\n{}'.format(address, request))
            try:
                path = request.split()[1]
                response = response_for_path(path)
                connection.sendall(response)
            except Exception as e:
                log('error', e)
            connection.close()


def main():
    config = dict(
        host='',
        port=3000,
    )
    run(**config)


if __name__ == '__main__':
    main()
