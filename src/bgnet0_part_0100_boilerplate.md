# 前言
这是一份介绍计算机网络中一系列常见概念的读物，注意，这份文档里面并不是我的另外那本《Beej的网络编程指南--C语言版》[flbg[_Beej的
的网络编程指南_|bgnet]]。这一系列文章旨在让读者对各种繁杂的网络术语有所了解，当然，为了加深理解，文章中会有一些使用python进行的编程练习和例子。

那么可能有人会问了，那这是 _Beej的的网络编程指南--Python版_ 吗？嗯，是也不是。因为那本C语言的网络指南更多的是关于Unix的底层的网络API是怎么运作的，但是这本书，更多的关注点是在计算机网络概念本身，只不过用python作为一个载体。

如果这依然让你感到困惑，也许你可以直接跳到下面的 _观众_ 部分试试找找答案。


## 受众
您是否对网络完全陌生，并且对ISO-OSI、TCP/IP、端口、以太网、局域网等所有这些术语感到困惑?也许您想用Python编写一些具有网络功能的代码?那么恭喜啦，本书是你的不二之选！

但是还是要事先提醒下:本指南假定您已经掌握了一些Python编程知识。

## Official Homepage
## 官方网址
以下是本指南的官方网址
[fl[https://beej.us/guide/bgnet0/|https://beej.us/guide/bgnet0/]].

## Email Policy
## 邮件规则
如果你有问题，欢迎给我发邮件，我很乐意通过邮件收到您的问题。不过因为我平时确实很忙，有些问题我可能没法想出一个合适的答案。所以在这种情况下，我通常会删除这条邮件。这不是针对个人的，我只是永远没有时间给你所需要的合适的答案。 

一般来说，问题的描述越复杂，我回答的可能性就越小。如果您可以在发送问题之前精简你的问题，并如能附上包含任何相关信息(如平台、编译器、报错信息以及您认为可能帮助我定位问题的任何其他信息)，那么将更有助于我回答您的问题。

如果你没有得到回复，那请尝试了解更深入一些，看看能不能寻找到答案。如果仍然难以捉摸，那就把你寻求答案过程中了解到的资料一并发给我，希望我踩能帮你的步伐回答出你的问题。

既然我已经赘述了很多关于写信和不写信给我的信息，我只是想让你知道，我_非常感激_这些年来对本指南所得到的所有赞扬。这真的让我深受鼓舞，特别是听到它对于您有所帮助!`:-)`,谢谢!

## Mirroring
## 备份
欢迎备份本指南，无论是公开的还是您私享。如果您做了一个公开的备份并且想让我给您在主页上加一个链接，请给我写份邮件说明[`beej@beej.us`](mailto:beej@beej.us)。 

## Note for Translators
## 给翻译者的话
如果您想讲本文翻译成其它语言，请给我写份邮件[`beej@beej.us`](beej@beej.us)，我会在首页给您的翻译加上一个入口。随信请加上您的名字和联系信息。

注意，在您的翻译里，请加入下面的版权声明和发布声明章节。(这一部分不翻译，因为要作为版权说明完整的放在翻译里面)
## Copyright and Distribution

Beej's Guide to Networking Concepts is Copyright © 2023 Brian "Beej Jorgensen" Hall.

With specific exceptions for source code and translations, below, this
work is licensed under the Creative Commons Attribution-Noncommercial-No
Derivative Works 3.0 License. To view a copy of this license, visit
[`https://creativecommons.org/licenses/by-nc-nd/3.0/`](https://creativecommons.org/licenses/by-nc-nd/3.0/)
or send a letter to Creative Commons, 171 Second Street, Suite 300, San
Francisco, California, 94105, USA.

One specific exception to the "No Derivative Works" portion of the
license is as follows: this guide may be freely translated into any
language, provided the translation is accurate, and the guide is
reprinted in its entirety. The same license restrictions apply to the
translation as to the original guide. The translation may also include
the name and contact information for the translator.

The programming source code presented in this document is hereby granted
to the public domain, and is completely free of any license restriction.

Educators are freely encouraged to recommend or supply copies of this
guide to their students.

Contact [`beej@beej.us`](beej@beej.us) for more information.

## Dedication
## 题献

在写本指南的过程中，我觉得最难的有如下几点： 

* 理解资料中的每分细节这样我才能准确的解释给读者
* 找到深入浅出解释的方法，这是一个需要不断迭代和自我反馈的过程
* 要求自己把自己当作为所谓的权威，而实际上我只是一个试图理解这一切的普通学习者，正如你们一样
* 世间精彩纷呈，我得要求自己专注于此

在完成本指南过程中，我获得的帮助颇多，再次我想对于这些帮助一一表示感谢。

* 每一个在互联网上决定以某种形式分享他们的知识的人。免费分享有教育意义的信息使互联网成为一个伟大的地方。
* 每一个对于这篇指南给予指正和提出PR指正本文中手误的人。

再次表示深深的感谢！♥
