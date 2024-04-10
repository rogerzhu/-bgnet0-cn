# 项目: 深度探索DNS

`dig` 是一个非常有用的命令行工具，它用于从默认名称服务器或任何名称服务器获取DNS信息。

## 安装

在Mac系统中，运行如下命令安装:

``` {.sh}
brew install bind
```

在WSL中，运行如下命令安装:

``` {.sh}
sudo apt install dnsutils
```

## 试一试

输入:

``` {.sh}
dig example.com
```

来看看它的返回都有些什么。

``` {.default}
; <<>> DiG 9.10.6 <<>> example.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 60465
;; flags: qr rd ra ad; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
;; QUESTION SECTION:
;example.com.                   IN      A

;; ANSWER SECTION:
example.com.            79753   IN      A       93.184.216.34

;; Query time: 23 msec
;; SERVER: 1.1.1.1#53(1.1.1.1)
;; WHEN: Fri Nov 18 18:37:13 PST 2022
;; MSG SIZE  rcvd: 56
```

这真是有很多内容，不过现在让我们先只关注以下的一些行:

``` {.default}
;; ANSWER SECTION:
example.com.            79753   IN      A       93.184.216.34
```

这是`example.com`的IP地址!注意到`A`了吗?这意味着这是一个IP地址记录。你还可以获得其他记录类型。如果你想查询`oregonstate.edu`使用邮件交换服务器呢?你可以把它放在命令行中:

``` {.sh}
dig mx oregonstate.edu
```

然后我们可以得到:

``` {.default}
;; ANSWER SECTION:
oregonstate.edu. 600 IN MX 5 oregonstate-edu.mail.protection.outlook.com.
```

或者我们想要得到`example.com`的域名服务器，我们可以运行:

``` {.sh}
dig ns example.com
```

## 超市时间（TTL）

如果你用`dig`去查询一个`A`记录，你可以看到如下一行数字:

``` {.default}
;; ANSWER SECTION:
example.com.            78236   IN      A       93.184.216.34
```

在这个例子中，是`78236`。这是缓存中条目的TTL。这告诉你，你使用的域名服务器已经缓存了该IP地址，并且该缓存条目直到再过78，236秒才会过期(作为参考，一天有86400秒。)

## 主域名服务器

如果你得到的是一个缓存在你的域名服务器上的条目，你会在`dig`命令的输出中看到`AUTHORITY: 0`:

``` {.default}
;; flags: qr rd ra ad; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1
                                            ^^^^^^^^^^^^
```

如果你看到`dig`命令的输出中的`AUTHORITY: 1`（或者其他正数），说明该条目直接来源于负责该域的域名服务器。

## 获取根域名服务器

只要输入`dig`并按下回车键，你就会看到所有的根DNS服务器信息，其中可能包括它们的IPv4地址(记录类型为`A`)和IPv6地址(记录类型为`AAAA`)。

## 挖掘一个指定的域名服务器

如果你知道要查询的名称服务器名称，则可以使用“`@`符号直接指定该服务器。两个最流行的免费域名服务器是`1.1.1.1` 和 `8.8.8.8`. 

让我们向他们中的一个询问`example.com`的IP地址。

``` {.sh}
dig @8.8.8.8 example.com
```

然后，我们得到了期许的答案。（尽管TTL可能是不同的——毕竟，这些是不同的服务器，它们的缓存条目具有不同的时限。）

## 挖掘一个根域名服务器

互联网上有很多根域名服务器，让我们尝试对着`example.com`用dig命令去查询其中的一个:

``` {.sh}
dig @l.root-servers.net example.com
```

我们可以得到一些有意思的结果:

``` {.default}
com.                    172800  IN      NS      a.gtld-servers.net.
com.                    172800  IN      NS      b.gtld-servers.net.
com.                    172800  IN      NS      c.gtld-servers.net.
com.                    172800  IN      NS      d.gtld-servers.net.
```

这些都不是 `example.com`。。。并且你看--他们都是 `NS`记录，意味着都是域名服务器。这就是根域名服务器要告诉我的: "我不知道谁是`example.com`，不过我知道有一些域名服务器知道 `.com`是什么。“

所以我们可以从中选择一个，并且继续`dig`:

``` {.sh}
dig @c.gtld-servers.net example.com
```

然后我们会得到:

``` {.default}
example.com.            172800  IN      NS      a.iana-servers.net.
example.com.            172800  IN      NS      b.iana-servers.net.
```

同样的情况，会出现更多的`NS`域名服务器，这是`c.gtld-servers.net`域名服务器告诉我们的，我不知道`example.com`的IP地址，不过这里有一些可能知道的域名服务器！所以我们可以继续尝试:

``` {.sh}
dig @a.iana-servers.net example.com
```

终于，我们在 `A` 记录中获得了相应的IP！

``` {.default}
example.com.            86400   IN      A       93.184.216.34
```

你也可以在命令行上使用`+trace`来从头到尾观察整个查询过程:

``` {.sh}
dig +trace example.com
```

## 我们还可以尝试的

试着去寻找以下几个问题的答案:
* `microsoft.com`的IP地址是什么？
* `google.com`的邮件服务器是什么？
* `duckduckgo.com`的域名服务器是什么？
* 按照上一节中从根名称服务器挖掘的过程，从根名称服务器开始，向下挖掘到`www.yahoo.com`(**不是** `yahoo.com`)整个过程。请注意，这整个过程应该在以 `CNAME`记录结束！你需要不断重复从根服务器开始的`CNAME` 记录。在你的文档中记录下使用`dig`命令获取到IP地址的整个过程。每个`dig`命令都应该以 `@`指明从根域名服务器开始的不同的域名服务器。

<!-- 计分表

5
正确显示 www.oregonstate.edu 的IP地址。

5
正确显示 google.com MX记录地址。

5
正确显示oregonstate.edu域名服务器地址。

5
正确显示一路查询到www.yahoo.com路上的所有IP地址。
-->