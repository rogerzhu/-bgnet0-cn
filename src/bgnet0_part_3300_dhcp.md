# 动态主机配置协议(DHCP)

当你第一次在咖啡店打开笔记本电脑时，它没有IP地址。它甚至不知道它 _应该_ 有什么IP地址。或者它的域名服务器是什么。或者它的子网掩码是多少。当然，你可以手工配置它！只要输入收银员递给你的咖啡上的数字就行了!

这肯定不会发生，没人会在意。他们会用一个重复的地址。事情就行不通了。大部分很可能会狂饮咖啡，然后再也不会光顾同一家店。如果有一种方法可以自动配置刚接入网络的计算机，那就更好了，不是吗?

这就是 _动态主机配置协议_ (DHCP) 的作用。

## 具体过程

概述:

``` {.default}
Client --> [DHCPDISCOVER packet] --> Server

Client <-- [DHCPOFFER packet] <-- Server

Client --> [DHCPREQUEST packet] --> Server

Client <-- [DHCPACK packet] <-- Server
```

其中的细节是:

当你的笔记本电脑第一次尝试连接到网络时，它通过UDP发送一个`DHCPDISCOVER`包到广播地址(`255.255.255.255`)的`67`号端口，也就是DHCP服务器端口。

回想一下，广播地址只在局域网内传播——默认网关并不会转发它。

在局域网上，有另外的一个机器作为DHCP服务器，在这个服务器上有一个进程一直等待在`67`号端口上。

DHCP服务器进程看到DISCOVER消息后，会决定如何处理它。

典型的用法是客户机需要一个IP地址，我们称之为从DHCP服务器租用的IP地址。DHCP服务会记录池中哪些IP已经分配，哪些是空闲的。

作为对`DHCPDISCOVER`报文的响应，DHCP服务器在端口`68`上向客户端发送`DHCPOFFER`响应消息。
In response to the `DHCPDISCOVER` packet, the DHCP server sends a
`DHCPOFFER` response back to the client on port `68`.

offer消息中包含一个IP地址和很多潜在的需要的信息，包括但是不限于:
* 子网掩码
* 默认网关地址
* 松弛时间
* DNS服务器地址

客户端可以选择接受或忽略该offer消息。(可能有多个DHCP服务器发出offer消息，但客户端可能只接受其中一个。)

如果offer消息被接收了，客户端会发送回一个`DHCPREQUEST`消息到服务器端来通知对方，自己想要那个特定的IP地址。

最后，如果一切都成功的话，服务器会回复一个确认数据包，`DHCPACK`。

此时，客户端拥有参与到网络交流所需的一切信息。

## 思考题

* 与手动配置LAN上的设备相比，使用DHCP之类的机制有什么优势？

* DHCP客户端会从DHCP服务器接收到哪些类型的信息?
