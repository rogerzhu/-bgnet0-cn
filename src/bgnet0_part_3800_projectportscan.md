# 项目：端口扫描

在本项目中，我们准备做一个端口扫描的项目！

**注意:我们只会在`localhost`上运行这个程序，以避免任何法律上的麻烦**

为了使该项目能够运行，我们需要安装`nmap`。

MacOS:

``` {.sh}
brew install nmap
```

Windows WSL:

``` {.sh}
sudo apt-get update
sudo apt-get install nmap
```

1. **扫描所有常用端口**
   该命令会扫描1000个最常用的端口:

   ``` {.sh}
   nmap localhost
   ```
   该程序，输出会是什么？

2. **扫描所有端口**
   该命令会从`0`开始扫描所有端口:

   ``` {.sh}
   nmap -p0- localhost
   ```
   它的输出会是什么？

3. **运行一个服务器和端口扫描**
   在某个端口上运行前面学习的任何TCP服务器程序，并再次运行前面的端口扫描程序。
   * 注意查看你的服务器端口是否在输出中！
   
   * 你的服务器是否因“连接重置”错误而崩溃?如果是，为什么?如果没看到，那么即使你没有从服务器上看到它，也思考下为什么会发生这种情况。(请参阅[端口扫描章节](# Port - Scanning) !)

<!-- 计分表
20分

5
`nmap localhost`输出正确

5
`nmap -p0- localhost`输出正确

5
`nmap -p0- localhost`输出正确并且可以显示出你服务器上打开的端口

5
正确解释"Connection reset"错误的原因
-->
