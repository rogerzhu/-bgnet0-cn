# Project: A Better Web Server
# 项目：一个更好的的网站服务器

现在，我们可以升级我们的网站服务器，使其可以传输真实的文件！当一个网页客户端（在本项目中，我们将会使用网页浏览器）请求一个特定的文件时，该服务端程序会将文件返回给客户端。在实现的过程中，你会学会相当多有趣的细节。

## 限制

为了能够更好的理解和学习底层套接字API的知识，在本项目中将**不会**使用以下辅助函数:
* `socket.create_connection()` 函数
* `socket.create_server()` 函数
* 任何`urllib`中的模块

当完成此项目时，对于这些辅助函数如何实现将会有更清晰的理解。

## 实现过程

如果你在浏览器中键入如下URL(将端口号替换你正在运行的服务程序):

``` {.default}
http://localhost:33490/file1.txt
```

客户端程序（浏览器）会给你的服务端程序发送一个如下的请求:

``` {.default}
GET /file1.txt HTTP/1.1
Host: localhost
Connection: close

```

请注意，在这个`GET`请求中，第一行里面的文件名！你的服务器程序将会:
1. 解析这个请求头，以拿到这个文件名。
2. 出于安全考虑，将路径剥离。
3. 从该文件中读取数据。
4. 判断文件中的数据类型，是HTML还是文本。
5. 在负载中使用文件数据建立HTTP应答数据包。
6. 将HTTP应答发送回客户端。

该应答如下所示:

``` {.default}
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 357
Connection: close

<!DOCTYPE html>

<html>
<head>
...
```
[在该例子中，HTML文件其余部分已经被截断省去。]

此时，你的网页浏览器应该可以显出这个文件。注意，在应答消息头中，有一些字段需要被计算和判断:`Content-Type`将会设置成保存的文件类型，`Content-Length`将会被设置成数据的长度。在这个项目中，在本项目中，我们会实现至少显示两种文件:HTML和文本文件。

## 解析请求头

在解析数据之前，你的服务器端程序需要读取完整的请求头，所以这里你需要有一些设计。比如使用一个变量中保存所有从`recv()`接收到的数据，并使用string的 `.find()`函数对其进行搜索，以找到标记头结束的`"\r\n\r\n"`。 此时，你可以以`"\r\n"`为参数对消息头中的数据使用`.split()`，这样可以得到独立的每一行。

第一行是`GET`，对于这一行，你可以使用`.split()`函数来将其分割成三部分:请求方法(`GET`)，请求路径（比如`/file1.txt`），以及协议（`HTTP/1.1`）。别忘了对请求的第一行使用`.decode("ISO-8859-1")`，这样你就可以得到一个供处理的字符串，目前，我们确实只需要这个路径。

## 从路径中分离出文件名

**安全隐患** 如果我们不删除其中的路径，恶意攻击者可能会使用它来访问您系统上的任意文件，比如他们可能会建立一个URL试图读取`/etc/password`。真实的web服务器一般检查路径是否被限制在某个目录层次结构中，但在本项目中我们采用简单的方法，去掉所有的路径信息，只提供web服务器运行所在目录中的文件。

由于路径将是用斜杠(`/`)分隔的目录名组成，因此对于此最简单的做法是在路径和文件名上使用`.split('/')`，然后取最后一个元素:

``` {.py}
fullpath = "/foo/bar/baz.txt"

file = fullpath.spl
os.path.split("/foo/bar/baz.txt")
```

该函数将会返回一个含有两个元素的元组，其中第二部分是我们需要的文件名:

``` {.py}
('/foo/bar', 'baz.txt')
```

使用该文件名去获取你想要取得的文件。

## MIME 以及取得`Content-Type`内容

在HTTP中，负载可以是任何东西--任何字节的集合，那么，网页浏览器是怎么知道怎么去展示它呢？ 答案就藏在字节头里面的`Content-Type`里面，在[MIME](https://en.wikipedia.org/wiki/MIME)对于数据的类型有详细定义。这些信息对于客户端足够知道怎样去显示它。下面是一些MIME类型的实例:
<!-- 示例: MIME 类型 -->
|MIME 类型名|描述|
|-|-|
|`text/plain`|明文文件|
|`text/html`|HTML 文件|
|`application/pdf`|PDF 文件|
|`image/jpeg`|JPEG 图像|
|`image/gif`|GIF 图片|
|`application/octet-stream`|未分类字节流|

除此之外，还有[很多MIME类型](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types)对应很多不同类型的数据，你只需要将正确的HTTP应答放在`Content-Type`头字段。

``` {.default}
Content-Type: application/pdf
```

但是你怎么知道一个文件含有的是什么数据呢？比较通用的方法是查看文件的的后缀名，就是文件名点号之后的所有部分。幸运的是，函数[`os.path.splitext()`](https://docs.python.org/3/library/os.path.html#os.path.splitext)可以方便的让我们从文件名中解析出最后一部分。

``` {.py}
os.path.splitext('keyboardcat.gif')
```

返回一个元组包含:

``` {.py}
('keyboardcat', '.gif')
```

对于下面的后缀部分，你可以直接做如下映射:
<!-- 示例: 延伸映射 -->
|后缀|MIME 类型|
|-|-|
|`.txt`|`text/plain`|
|`.html`|`text/html`|

所以如果一个文件拥有`.txt`后缀，确保发送的回复中是:

``` {.default}
Content-Type: text/plain
```

如果你想万无一失，在消息头中加入`charset`来指定字符编码:

``` {.default}
Content-Type: text/plain; charset=iso-8859-1
```

不过这不是必须的，因为一般来说浏览器默认会设置上面的字符编码方式。

## 读取文件， `Content-Length`和处理未发现

下面是一段读取整个文件并且检查错误的示例代码:

``` {.py}
try:
    with open(filename, "rb") as fp:
        data = fp.read()   # Read entire file
        return data

except:
    # File not found or other error
    # TODO send a 404
```

从`.read()`返回的数据将会成为负载，并且可以使用`len()`来计算字节的长度，字节的长度将会包含在`Content-Length`头部并且被送回，比如(包含你文件中的字节数):

``` {.default}
Content-Length: 357
```

> 你可能对于`open()`函数中的`"rb"`参数感到好奇，它表示使用二进制模式读取文件。
> 在Python中，一个以二进制模式打开读取的文件将会返回一个可以通过套接字直接发送二进制字节字符串。

如果遇到了`404 Not Found`怎么办？它很常见，你可能在日常的网络访问中不时会看到它。它表示你正在请求的文件或者其他资源并不存在，在我们的例子中，我们将会检测到一些这样文件打开时的错误(位于上面的`except`块中)，此时，它将会返回`404`。`404`是一种HTTP应答值，除此之外还有:

``` {.default}
HTTP/1.1 200 OK
```

我们的应答将会以此开始

``` {.default}
HTTP/1.1 404 Not Found
```

所以当你尝试去打开一个文件但是失败的时候，你应该返回如下(一字不差的)信息并且关闭连接:

``` {.default}
HTTP/1.1 404 Not Found
Content-Type: text/plain
Content-Length: 13
Connection: close

404 not found
```

(在这种情况下，内容长度和有效负载都可以硬编码,当然需要对原始字节调用`.encode()`函数。)

## 附加题

如果你有时间，可以试试下面额外的挑战来更好地理解本章，加油!

* 增加对其他文件类型的MIME支持，使得程序可以支持JPEG图像和其他文件。
* 增加显示文件夹列表的功能，如果一个用户不在URL中指定一个文件名，显示一个指向每个文件名的文件列表。
  一些提示:
  [`os.listdir`](https://docs.python.org/3/library/os.html#os.listdir)
  和
  [`os.path.join()`](https://docs.python.org/3/library/os.path.html#os.path.join)
* 相较于简单粗暴的放弃整个路径，支持请求服务器上根目录下的指定子路径。
  **安全风险!** 请确保程序不会通过路径中一连串的`..`来损坏根目录！

  通常，你可能会通过配置变量将服务器根目录指定为绝对路径。但如果你上的时我的课，在我来批改你的作业的时候就惨了。因此，如果是这种情况，请为你的服务器根目录使用相对路径，并使用[`os.path.abspath()`](https://docs.python.org/3/library/os.path.html#os.path.abspath)函数。

  ``` {.py}
  server_root = os.path.abspath('.')        # This...
  server_root = os.path.abspath('./root')   # or something like this
  ```

  这将会把`server_root`设置成一个运行的服务程序的完整路径，比如，在我的机器上，我可能会得到:

  ``` {.default}
  /home/beej/src/webserver                  # This...
  /home/beej/src/webserver/root             # or something like this
  ```

  然后，用户尝试去`GET`一些路径，你可以通过将其增加到服务程序运行路径之后来得到文件的全路径。

  ``` {.py}
  file_path = os.path.sep.join(server_root, get_path)
  ```

  所以，如果客户端尝试去`GET /foo/bar/index.html`，将会得到的`file_path`为:

  ```
  /home/beej/src/webserver/foo/bar/index.html
  ```

  **现在又到了安全问题！** 你需要确保`file_path`是位于服务器的根目录，不然，坏人可能会这么做:

  ``` {.http}
  GET /../../../../../etc/passwd HTTP/1.1
  ```
  
  如果它们真的如此，服务器端将无脑的请求如下文件:
  ```
  /home/beej/src/webserver/../../../../../etc/passwd
  ```
  
  这将获取到位于`/etc/passwd`中我的的密码，我可以不想发送这样的事情。所以我需要保证无论路径如何，最终都不会超出`server_root`层级，那么，怎么做到这一点呢？我们可以再次使用`abspath()`。

  如果我通过`abspath()`疯狂对着以上的路径使用`..`，对于我它只会返回`/etc/passwd`，它将解析路径中类似 `..`并且返回“真正的“地址。但是，我知道在这个例子中，我的路径根目录时`/home/beej/src/webserver`，所以，我可以将上面的相对路径赋予其后，并且返回404表示其并不存在。

  ``` {.py}
  # Convert to absolute path
  file_path = os.path.abspath(file_path)

  # See if the user is trying to break out of the server root
  if not file_path.startswith(server_root):
      send_404()
  ```

## 示例文件

以下是一些可以直接复制拷贝到文件中作为返回测试文件的例子:

### `file1.txt`

``` {.default}
This is a sample text file that has all kinds of words in it that
seemingly go on for a long time but really don't say much at all.

And as that weren't enough, here is a second paragraph that continues
the tradition. And then goes for a further sentence, besides.
```

### `file2.html`

``` {.html}
<!DOCTYPE html>

<html>
<head>
<title>Test HTML File</title>
</head>

<body>
<h1>Test HTML</h1>

<p>This is my test file that has <i>some</i> HTML in in that the browser
should render as HTML.

<p>If you're seeing HTML tags that look like this <tt>&lt;p&gt;</tt>,
you're sending it out as the wrong MIME type! It should be
<tt>text/html</tt>!

<hr>
</body>
```

可以通过下面这些URL可以取到上述文件(使用正确的端口号):

``` {.default}
http://localhost:33490/file1.txt
http://localhost:33490/file2.html
```

<!--
评分表

100 分

10 从请求头中解析出了文件名
20 文件路径要么被剥离，要么被适当地沙盒化
10 从URL中指定的文件中读取到数据
15 在消息头中正确的设置了Content-Type
15 在消息头中正确的设置了Content-Length
15 HTTP应答头被正确的构造并且编码为ISO-8859-1
15 HTTP的应答负载被正确的构造出来
-->
