# coding=utf-8
import socket
import select
import sys
import urllib3


class Proxy:
    def __init__(self, addr,proxy_pool_url):
        self.proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.proxy.bind(addr)
        self.proxy.listen(10)
        self.inputs = [self.proxy]
        self.route = {}
        self.proxy_pool_url = proxy_pool_url
        self.addr = addr

    def getProxyIP(self):
        getIP_Port = urllib3.PoolManager()
        content = getIP_Port.request('GET', self.proxy_pool_url).data
        content = str(content, encoding="utf-8")
        ip_port = content.split(':')
        to_addr = (ip_port[0].strip(), int(ip_port[1].strip()))
        return to_addr

    def serve_forever(self):
        print('Proxy server listening : ' + str(self.addr))
        while 1:
            try:
                readable, _, _ = select.select(self.inputs, [], [])
                for self.sock in readable:
                    if self.sock == self.proxy:
                        self.on_join()
                    else:
                        data = self.sock.recv(8096)
                        #data = self.sock.recv(1024)
                        if not data:
                            pass
                            self.on_quit()
                        else:
                            self.route[self.sock].send(data)
            except ConnectionAbortedError as e:
                print('error',e)
                pass
            except OSError as e:
                print('error',e)
                pass

    def on_join(self):
        client, addr = self.proxy.accept()
        print(addr, 'connect   ',end="")
        remotServer = self.getProxyIP()
        print('remot Server : ' + str(remotServer))
        try:
            forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            forward.connect(remotServer)
            self.inputs += [client, forward]
            self.route[client] = forward
            self.route[forward] = client
        except TimeoutError as e:
            print('error',e)
            self.on_quit()
            pass
        except ConnectionRefusedError as e:
            print('error', e)
            self.on_quit()
            pass
        except KeyError as e:
            print('error', e)
            self.on_quit()
            pass
        except Exception as e:
            print('error',e)
            self.on_quit()
            pass

    def on_quit(self):
        try:
            for s in self.sock, self.route[self.sock]:

                self.inputs.remove(s)
                del self.route[s]
                s.close()
                pass
        except KeyError as e:
            print('Error',e)
            pass


if __name__ == '__main__':
    try:
        # proxy_pool访问地址
        proxy_pool_url = 'http://127.0.0.1:5010/get/'
        Proxy(addr=('0.0.0.0', 12345),proxy_pool_url=proxy_pool_url).serve_forever()  # 代理服务器监听的地址
    except KeyboardInterrupt:
        sys.exit(1)
