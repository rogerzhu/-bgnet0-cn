
# 项目： 用WireShark查看ARP数据包

[fl[WireShark|https://www.wireshark.org/]]是一款常用的查看实时网络流量的工具，我们将利用它来看看是否可以捕获一些ARP请求和应答。

Wireshark是一个超级棒的的 _嗅探_ 网络数据包的工具，它为用户提供了一种跟踪数据包在局域网中传输的方法。我们将在WireShark中设置一个过滤器，以便我们可以只查看来自特定机器的ARP数据包，这样大大减少了大海捞针的成本。

## 需要创建什么

一个含有以下4样东西的文档:
1. 你当前连接的MAC地址。

2. 你当前连接的IP地址。

3. 一个用户可读的WireShark ARP请求数据包。

4. 一个用户可读的WireShark ARP请求回复包。

下面是具体细节！

## 详细步骤

下面是我们将要做的具体事宜:

1. **查找你的以太网(MAC)地址**
   你的计算机可能有很多以太网接口（比如说，一个是WiFi的接口，而另一个是有线接口--电脑机箱旁边的以太网插孔）

   因为现时大概率你正在使用你的无线，所以我们先来查找无线连接接口的MAC地址。（你可能需要上网搜索下怎么样完成这个目标。）

   对于这一步和接下来的步骤二，在Unix类的系统中这些信息都可以用如下命令获得:

   ``` {.sh}
   ifconfig
   ```

   如果你使用的是Windows系统，你可以使用如下命令获得:

   ``` {.sh}
   ipconfig
   ```

2. **查找你的IP地址**

   再次，我们想要知道你当前活动链接的接口的IP地址，大概率也是你的WiFi设备。

3. **打开WireShark**
 
   在初始启动时，设置WireShark来查看你的活跃的以太网设备。在Linux上，这可能是 `wlan0`。在Mac上，它可能是`en0`。在Windows上，可能只是`Wi-Fi`。

4. **查询你子网中更多的IP地址**
   对于本节来说，远端IP上是否有一个真的计算机并不重要，但如果存在对应IP地址的计算机那更好。通过观察一段时间的Wireshark日志，可以查看到你的局域网中还有哪些正在活跃的IP地址。

   > 你的IP地址与上子网掩码就是你的子网号，你可以尝试着将主机号部分替换成各种数字。
   > 还可以使用你的默认网关（去网络上搜索下怎么查看默认网关地址）作为你的测试对象。

   在命令行中，`ping`你局域网上的另一个IP地址:
   ``` {.sh}
   ping [IP address]
   ```

   (可以按下 `CONTROL-C` 来结束你的ping。)
   
   在第一个ping中，你有没有看到经过Wireshark的任何ARP数据包？如果没有，请尝试子网中的其他IP地址，就像上面提及的那样。

   不管你发送了多少ping，你应该只看到一个ARP回复。（如果没有任何应答，你将看到每个ping都有一个请求!）这是因为当第一次获得应答之后，你的电脑会缓存ARP应答，而后面再也不需要发送类似请求了。

   在一到五分钟之后，你的电脑中的ARP缓存项将会过期，这时如果你继续ping那个IP，你将会看到另外一个ARP交换数据包。

5. **记录下请求和回复**
   在该时间轴中，ARP请求过程将看起来像以下的片段(显然真实情况具有不同的IP地址):

   ``` {.default}
   ARP 60 Who has 192.168.1.230? Tell 192.168.1.1
   ```

   如果一切顺利，你将会看到一个类似下面的回复:

   ``` {.default}
   ARP 42 192.168.1.230 is at ac:d1:b8:df:20:85
   ```

   [如果你没有看到任何内容，试着修改你的过滤器，只输入“arp”。观察一会儿，看看你是否看到请求/回复数据包。]

   单击请求并查看左下方面板中的详细信息。展开“Address Resolution Protocol (request)”面板。随意选择一行，并且右击，选择"Copy->All Visible Items"。下面是示例请求（由于一行长度有限，进行了截断）:

   ``` {.default}
   Frame 221567: 42 bytes on wire (336 bits), 42 bytes captured  [...]
   Ethernet II, Src: HonHaiPr_df:20:85 (ac:d1:b8:df:20:85), Dst: [...]
   Address Resolution Protocol (request)
       Hardware type: Ethernet (1)
       Protocol type: IPv4 (0x0800)
       Hardware size: 6
       Protocol size: 4
       Opcode: request (1)
       Sender MAC address: HonHaiPr_df:20:85 (ac:d1:b8:df:20:85)
       Sender IP address: 192.168.1.230
       Target MAC address: 00:00:00_00:00:00 (00:00:00:00:00:00)
       Target IP address: 192.168.1.148
   ```

   点击时间线中的回复数据包，使用上面一样的方法复制回复信息。下面是回复消息的示例（由于一行长度有限，进行了截断）:

   ``` {.default}
   Frame 221572: 42 bytes on wire (336 bits), 42 bytes captured  [...]
   Ethernet II, Src: Apple_63:3c:ef (8c:85:90:63:3c:ef), Dst:    [...]
   Address Resolution Protocol (reply)
       Hardware type: Ethernet (1)
       Protocol type: IPv4 (0x0800)
       Hardware size: 6
       Protocol size: 4
       Opcode: reply (2)
       Sender MAC address: Apple_63:3c:ef (8c:85:90:63:3c:ef)
       Sender IP address: 192.168.1.148
       Target MAC address: HonHaiPr_df:20:85 (ac:d1:b8:df:20:85)
       Target IP address: 192.168.1.230
   ```
<!--
计分表

10
提交的内容包含当前活动连接的MAC地址。

10
提交的内容包含当前活动连接的IP地址。

20
提交的内容包含一个用户可读的WireShark ARP请求数据包。

20
提交的内容包含一个用户可读的WireShark ARP请求回复包。

-->