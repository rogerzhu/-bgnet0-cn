# 附录:JSON {#appendix-json}

在该最终项目中，我们需要完成编码和解码JSON数据。如果你对该格式不是很熟悉，[可以从Wikipedia上查看它的说明](https://en.wikipedia.org/wiki/JSON)。在本节中，我们将会学习，什么叫JSON数据的编码和解码。

## JSON格式和原始格式

下面是一个JSON对象的例子:

``` {.json}
{
    "name": "Ada Lovelace",
    "country": "England",
    "years": [ 1815, 1852 ]
}
```

在Python中，你可以按照下面的方式构造一个`dict`对象:

``` {.json}
d = {
    "name": "Ada Lovelace",
    "country": "England",
    "years": [ 1815, 1852 ]
}
```

但是，这里的关键不同处在于: _所有的JSON数据都是字符串_。 JSON是所需要数据的字符串表示形式。

## 相互转换

如果你有一个JSON字符串，你可以使用Python中的 `json.loads()` 函数将其转换原始数据模式。

``` {.py}
import json

data = json.loads('{ "name": "Ada" }')

print(data["name"])   # Prints Ada
```

同样，如果你一个Python数据，你可以通过调用`json.dumps()`将其转换为一个JSON字符串。

``` {.py}
import json

data = { "name": "Ada" }

json_data = json.dumps(data)

print(json_data)  # Prints {"name": "Ada"}
```

## 优雅输出

如果你有一个完整的对象，`json.dumps()` 会将所有内容放在一行中输出。

比如下面这段代码:

``` {.py}
d = {
    "name": "Ada Lovelace",
    "country": "England",
    "years": [ 1815, 1852 ]
}

json.dumps(d)
```

将会输出:

``` {.default}
'{"name": "Ada Lovelace", "country": "England", "years": [1815, 1852]}'
```

你可以通过向`json.dumps()`传入 `indent`参数来使其变得整齐，给它赋予一个锁进的级别。

``` {.py}
json.dumps(d, indent=4)
```

这个将会输出:

``` {.default}
{
    "name": "Ada Lovelace",
    "country": "England",
    "years": [
        1815,
        1852
    ]
}
```

清楚多了。

## 双引号是十分重要的

JSON需要将字符串和键名都放在双引号中，单引号是无效的，没有引号 _更是_ 非法的。

## 思考题

* JSON对象和Python字典对象的区别是什么？

* 阅读下Wikipedia文章，哪些类型可以被JSON表示？
