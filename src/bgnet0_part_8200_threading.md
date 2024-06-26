# 附录： 多线程 {#appendix-threading}

_多线程_ 是一个进程能够同时运行多个 _线程_ 的方法。也就是说，它可以同时运行很多个函数。

如果你的不同的函数有的需要等待某事发生，同时有的不需要等待，只需同时运行，那么这个技术就十分有用。对于一个实用的多用户聊天客户端，因为它必须同时做两件事，而这两件事互相之前会有阻塞:

* 一个是等待用户输入自己的聊天消息。
* 一个是等待服务器发送来更多消息。

如果不使用多线程，在等待用户输入时就无法从服务器接收消息，反之亦然。

> 旁注: `select()` 函数实际上也可以将常规文件描述符添加到要侦听的集合中。所以技术上
> 它 _可以_ 同时监听套接字上的数据包 **和** 键盘来的消息。但是在Windows上不行。并且
> 从总体上来说，如果使用这种方法，客户端的难度要小于多线程。

让我们看下在Python中如何实现这个功能。

## 概念

首先，有几个术语我们应该先搞清楚。

* **线程**: “运行线程”的表示形式，即在当前特定时刻正在执行的程序的一部分。如果你想让程序的多个部分同时执行，你可以分别把它们放在单独的线程中。

* **主线程**: 这是默认情况下运行的线程，我们只是从来没给它起过名字。但是你运行的代码都是默认在主线程中运行的。

* **生成线程**: “衍生/生成”一个新线程指的是运行一个特定的函数来运行线程，当程序这样做时，线程函数将与主线程 _同时执行_ 。他们会同时立即执行！

* **Join**:  一个线程可以通过调用`join()`函数来等待另一个线程退出。这在技术上，是将另一个线程和调用线程发生链接。通常主线程会调用 `join()`函数来等待它创建的线程回到自己的执行代码。
  
* **目标线程**: 目标线程指的是一个将要执行的运行线程的函数。当函数返回时，线程即退出。
  
有一个值得注意的是任何 _全局变量都会被所有线程共享_! 这意味着一个线程可以设置全局对象，而其他线程将会看到这些更改。如果共享数据是只读的，则不必担心这个问题，但如果共享数据是可写的，这就成为了一个必须要考虑的问题。

我们将在这里讨论并发和同步，因此对于这个项目，我们将不会使用任何全局共享对象。记住那句古老的谚语:

> Shared Nothing Is Happy Everybody

好吧，这并不是一句古老的谚语。而是我刚编的。现在我又读了一遍，听起来有点自私。

回到主题:局部对象不能在线程之间共享。这意味着线程可以维护自己的局部变量和参数值。每个线程都可以各自维持自己的变量，而这些更改对其他线程是不可见的。

另外，如果多个线程同时运行，它们的执行顺序是不可预测的。而当线程之间存在某种时间或数据依赖时，这就会成为一个问题，那时，再来思考这个问题。但是，我们需要意识到执行的顺序是不可预测的，只是在本项目中，我们暂时不考虑这个。

背景知识介绍的差不多了，下面可以正式开始了。

## Python中的多线程

让我们写一个创建三个线程的程序。

每个线程将运行一个名为 `runner()`的函数(你可以随意调用该函数)。这个函数有两个参数:一个`name`和一个`count`。它循环并输出`name`变量`count`次。线程将在`runner()`函数返回时退出。你可以通过调用 `threading.Thread()`构造函数来创建新线程。

同时，你可以通过调用它的 `.start()`方法来让线程运行。通过调用`.join()` 方法，可以等待线程退出。下面，让我们来具体看一看!

<!-- read in the projects/threaddemo.py file here -->
``` {.py}
import threading
import time

def runner(name, count):
    """ Thread running function. """

    for i in range(count):
        print(f"Running: {name} {i}")
        time.sleep(0.2)  # seconds

# Launch this many threads
THREAD_COUNT = 3

# We need to keep track of them so that we can join() them later. We'll
# put all the thread references into this array
threads = []

# Launch all threads!!
for i in range(THREAD_COUNT):

    # Give them a name
    name = f"Thread{i}"

    # Set up the thread object. We're going to run the function called
    # "runner" and pass it two arguments: the thread's name and count:
    t = threading.Thread(target=runner, args=(name, i+3))

    # The thread won't start executing until we call `start()`:
    t.start()

    # Keep track of this thread so we can join() it later.
    threads.append(t)

# Join all the threads back up to this, the main thread. The main thread
# will block on the join() call until the thread is complete. If the
# thread is already complete, the join() returns immediately.

for t in threads:
    t.join()
```

下面是程序的输出:
And here's the output:

``` {.default}
Running: Thread0 0
Running: Thread1 0
Running: Thread2 0
Running: Thread1 1
Running: Thread0 1
Running: Thread2 1
Running: Thread1 2
Running: Thread0 2
Running: Thread2 2
Running: Thread1 3
Running: Thread2 3
Running: Thread2 4
```

可以看到，这些线程都是同时执行！

注意，线程的执行顺序并不一致。每一次运行顺序可能都不会一样。这对于这个程序来说没有问题，因为线程之间没有任何依赖。

## 守护线程

Python定义了两种不同类型的线程:
* 普通线程
* 守护线程

它的思想是守护线程将永远运行并且永远不会从其函数返回。与非守护线程不同，一旦所有的非守护线程死亡，这些线程将被Python程序自动终止。

### 一些关于`CTRL-C`的小知识

如果你使用`CTRL-C` 来终止主线程，并且没有其他非守护线程正在执行，所有的守护线程也会被终止。但是，但是如果你有一些非守护线程，你需要一直按`CTRL-C`，直到所有的线程被终止而看到提示符。

在最后一个项目中，我们将永远运行一个线程来监听来自服务器的传入消息。所以这应该是一个守护线程。

你可以通过如下代码来创建一个守护线程:

``` {.py}
t = threading.Thread(target=runner, daemon=True)
```

这样，至少`CTRL-C`会让你方便的退出客户端。

## 思考题

* 描述下线程可以解决哪些问题。

* 在Python中，守护线程和非守护线程的区别是什么？
  
* 在Python中创建主线程需要做些什么?

## 多线程项目

如果你想展示一下你的编程水平，这里有一个可以参考的小项目。

### 我们将要完成什么

在这个项目中客户会提供一些值域范围，要求是位于所有值域范围内的数的总和。 比如，有如下这些值域:

``` {.py}
[
    [1,5],
    [20,22]
]
```

我们想要得到的是:

* 首先执行`1+2+3+4+5`得到`15`。
* 接着执行`20+21+22`得到`63`。
* 最后将`15+63` 得到`78`，这就是最终我们需要的结果。

需求方想要打印出各个值域的所有值的总和。对于上面的例子，他们希望输出:

``` {.default}
[15, 63]
78
```

### 总体架构

程序必须使用线程来解决这个问题，因为对于这个问题需求发起方非常喜欢并行程序。

你应该写一个函数把一段数字相加。然后，你将为每对值域生成一个线程，并让该线程在相应的范围上工作。如果有10个值域，则将有10个线程，每个值域用一个线程处理。

主线程将会是:

* 首先为结果分配一个数组，这个数组长度应该与值域对的数量相同(与线程的数量相同)。每个线程都有自己的空间来存储数组中的结果。
  ``` {.py}
  result = [0] * n   # Create an array of `n` zeros
  ```
  
* 在一个循环中，运行所有线程。传入线程的参数是:
  * 线程ID是`0..(n-1)`，其中`n` 是线程数量。这也是线程用于在结果数组中存储其结果的索引值。

  * 值域的开始值。
  
  * 值域的结束值。
  
  * 存放每个线程计算结果的数组。
  
  * 主线程应该保存数组中从`threading.Thread()` 返回的所有线程对象，因为后续步骤还需要它们。

* 在之后的另一个循环中，对所有线程调用 `.join()` 。这可以使得主线程等待所有子线程完成。

* 打印结果，当所有的线程都`join()`之后，结果数组里将会有所有的值的和。

### 有用的函数

* `threading.Thread()`: 创建一个线程。

* `range(a, b)`: 生成`[a, b)` 之内的所有数的迭代器。

* `sum()`: 计算可迭代对象的和。

* `enumerate()`: 在可迭代对象上生成索引和值。

### 运行一个线程函数需要知道的所有事情

所有线程的结果都将写入共享数组。这个数组可以提前设置为所有元素都为零。每个线程应该都对应一个元素，以便每个线程可以正确的填入对应的结果。

要做到这一点，你必须将线程的索引号传递给它的运行函数，以便它知道将结果放入共享数组中的哪个元素!

### 运行示例

示例输入（你可以直接在你的程序中直接硬编码这些）:

``` {.py}
ranges = [
    [10, 20],
    [1, 5],
    [70, 80],
    [27, 92],
    [0, 16]
]
```

对应的正确输出是:

``` {.default}
[165, 15, 825, 3927, 136]
5068
```

### 扩展题

* 如果在一个`for`循环中使用`sum()`函数，那么你的时间复杂度是多少？
  
* 从1到n的整数和的计算方程为`n*(n+1)//2`，你能用它得到更好的时间复杂度吗?可以好多少?


<!-- 计分表
10分
正确创建了线程，每个线程对应一个值域

5分
在主线程中，使用join() 等待所有创建的线程

5分
每个线程的结果正确的填入了结果数组的对应位置

5分
输出了正确的各个值域和的数组

5分
正确输出了最后的结果
-->
