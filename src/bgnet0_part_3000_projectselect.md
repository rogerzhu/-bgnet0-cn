# 项目： 使用Select函数

在本项目中，我们将要使用`select()`来编写一个同时处理多个连接的服务器端程序。我们已经提供了客户端程序，你只需要完成服务器端代码即可。

## 演示代码

你可以从[fls[this ZIP file|select/select.zip]]获取所有输入文件。`select_client.py` 已经全部完成了，你需要做的是在`select_server.py`填入对应的代码。

## 需要添加的功能

你的服务器端程序需要有如下的功能:

* 当一个客户端连接时，服务器端程序按以下格式打印出客户端连接信息:
  
  ``` {.default}
  ('127.0.0.1', 61457): connected
  ```

* 当一个客户端断开连接时，服务器端程序用以下形式打印出连接信息:
  
  ``` {.default}
  ('127.0.0.1', 61457): disconnected
  ```

  **提示**: 即使已经断开连接，你依然可以在套接字上使用`.getpeername()`方法来获取到远端的ip地址。它将返回一个含有`("host", port)`的元组，就像你传递给`connect()`函数的参数一样。

* 当一个客户端发送数据时，同样，服务器端需要打印出收到的原始字节字符串的数据长度:
  
  ``` {.default}
  ('127.0.0.1', 61457) 22 bytes: b'test1: xajrxttphhlwmjf'
  ```

## 示例运行

运行如下服务器端程序:

``` {.sh}
python select_server.py 3490
```

运行客户端程序:

``` {.sh}
python select_client.py alice localhost 3490
python select_client.py bob localhost 3490
python select_client.py chris localhost 3490
```

客户端的第一个参数可以是任何字符串——服务器端程序会将它与数据一起打印出来，以帮助你识别出它来自哪个客户端程序。

示例输出:
Example output:

``` {.default}
waiting for connections
('127.0.0.1', 61457): connected
('127.0.0.1', 61457) 22 bytes: b'test1: xajrxttphhlwmjf'
('127.0.0.1', 61457) 22 bytes: b'test1: geqtgopbayogenz'
('127.0.0.1', 61457) 23 bytes: b'test1: jquijcatyhvfpydn'
('127.0.0.1', 61457) 23 bytes: b'test1: qbavdzfihualuxzu'
('127.0.0.1', 61457) 24 bytes: b'test1: dyqmzawthxjpkgpcg'
('127.0.0.1', 61457) 23 bytes: b'test1: mhxebjpmsmjsycmj'
('127.0.0.1', 61458): connected
('127.0.0.1', 61458) 23 bytes: b'test2: bejnrwxftgzcgdyg'
('127.0.0.1', 61457) 24 bytes: b'test1: ptcavvhroihmgdfyw'
('127.0.0.1', 61458) 24 bytes: b'test2: qrumcrmqxauwtcuaj'
('127.0.0.1', 61457) 26 bytes: b'test1: tzoitpusjaxljkfxfvw'
('127.0.0.1', 61457) 17 bytes: b'test1: mtcwokwquc'
('127.0.0.1', 61458) 18 bytes: b'test2: whvqnzgtaem'
('127.0.0.1', 61457): disconnected
('127.0.0.1', 61458) 21 bytes: b'test2: raqlvexhimxfgl'
('127.0.0.1', 61458): disconnected
```

<!-- 计分表 

5
服务器端程序打印出正确的客户端连接上的信息

5
服务器端程序打印出正确的客户端断开的信息

5
服务器端程序打印出正确的已收到客户端数据的信息

5
服务器端程序使用select()等待到来的连接

5
服务器端使用select()等待到来的客户端数据
-->