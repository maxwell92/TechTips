RESTful API设计原则
=======================

[原文作者：Thomas Hunter](https://codeplanet.io/author/tlhunter/)
[原文链接：Principles of good RESTful API Design](https:#/codeplanet.io/principles-good-restful-api-design/)

想要设计优秀的RESTful API真心很难。每个API都是你和那些使用你的数据的客户间的一份“契约”。如果你破坏了这份契约，你不仅会收到很多愤怒的邮件，还会见到许多无法继续使用移动应用的悲伤的客户。

构建一个API可以帮助你增加服务的价值。通过一个API，你的服务/核心应用便有了成为其他服务平台的潜力。看这些科技巨擘：Facebook，Twitter，Google，Github，Amazon，Netflix等等，他们谁也不曾想到如果他们没有通过API开放他们的数据，是不会拥有今天这般巨大的成就。事实上，作为一个完整的工业体系，它的唯一目标就是前面所说的这样消费数据的平台。

> 你的API越容易使用，会有越多的人们来使用它。

这篇文章将跟随你对API的设计，并且保证你的API的消费者能够理解发生了什么。然后会显著减少你收到的困惑或愤怒的邮件。我把这些组织为一个个的话题，当然你并不需要按顺序阅读。

### RESTful API设计定义
这里是我将会用到的一些关键字：

* 资源（Resource）：对象的一个单独的实例。例如，一个动物。
* 集合（Collection）：同种对象的集合。例如，动物。
* HTTP：跨网络通信协议
* 消费者（Consumer）：一个可以发出HTTP请求的客户端应用。
* 第三方开发者（Third Party Developer）：一个不是你项目组成员但又想使用你的数据的人。
* 服务器（Server）：一个可被消费者跨网络访问的服务器程序。
* 端点（Endpoint）：服务器上一个代表了某种资源或某个集合的API URL。
* 冪等性（Idempotent）：无副作用，可多次执行。
* URL段（URL Segment）：URL中由斜线分隔的信息块。

### 数据设计和抽象
计划好你的API长什么样要比你想的还早开始。首先你要考虑你的数据如何设计，以及你的核心服务/应用如何工作。如果你在进行[API优先开发](http://blog.pop.co/post/67465239611/why-we-chose-api-first-development)，那这就简单了。如果你要将一个API添加到一个已有的项目中，那么你可能需要更多的抽象。

偶尔地，一个集合可以代表一个数据库表，一个资源可以代表这个表里的一行。然而，这不是一般情况。事实上，你的API应该远离你的数据和业务逻辑进行抽象。这是非常重要的，否则第三方开发者会被这么多复杂的应用数据所吞没，除非你不打算让他们用你的API了。

这里还有一些你不应该暴露为API的部分服务。一个常见的例子是许多API不允许创建用户。

### 动词
你当然应该知道GET和POST请求。这是你浏览不同的网页时用到最多的两个请求了。POST非常有用，它甚至被嵌入到一些日常语言中。这样人们即使不知道它到底干了什么也可以说给他们FACEBOOK上的朋友POST了一些东西。

这里还有“四个半”重要的HTTP动词。我说的“半个”指的是PATCH，因为它与PUT非常相似，并且他们常被API开发者混合使用。这些动词，对应了一些数据库调用（我假定大多数读者知道如何操作数据库而不是设计API）。

* GET(SELECT)：接收来自服务器某个特定的资源，或列出一组资源。
* POST(CREATE)：在服务器上创建一个新的资源。
* PUT(UPDATE)：在服务器上更新资源，提供整个资源。
* PATCH(UPDATE)：在服务器上更新资源，仅更新改变的部分。
* DELETE(DELETE)：在服务器上移除资源。

下面是较为罕见的HTTP动词：

* HEAD：接收某个资源的元数据，例如数据的哈希值，或者更新时间。
* OPTIONS：接收允许消费者使用资源的时间。

一个优秀的RESTful API将使用这四个半HTTP动词来允许第三方与它的数据进行交互，并且从不将动作/动词作为URL段。

典型地，GET请求可以被缓存（并且经常是这样）。例如，浏览器将缓存GET请求（依赖于缓存头），并且用户第二次发出POST请求时还有效。一个HEAD请求可以看作是一个没有响应体的GET请求，并且同样可以被缓存。

### 版本控制
不管你是在构建，也不管你有多少要做的事情，你的核心应用要改变，你的数据关系要改变，属性也要被添加到或从资源上移除。软件开发就是如此，并且只要你的项目是活跃的，被很多人使用（比如你构建的API），它一直是这样。

记住API是服务器和消费者之间的一份契约。如果你改变了服务器API，并且这些改变不是向后兼容的，你就破坏了消费者的访问，它们会对你感到生气。继续这样的话，他们就离开了。为了保证你的应用包含了改变，又保证了消费者的心情，你需要偶尔引进新版本的API，并且它仍能被老版本所访问。

作为一个边注，如果你只是给你的API添加了新特性，例如资源上新的属性（不是必须的，没有它资源也能正常工作），或者你正在添加新的端点，你不用增加你的API版本号，因为这些改变不会破坏向后兼容性。你要的只是更新你的文档了。

经过一段时间你可以废弃掉旧的版本。为了废弃一个特性并不意味着将它关闭或减少它的数量，而是告诉消费者这个老版本的API将在某天被移除，他们应该更新为新版本。

一个优秀的RESTful API将在URL中保留版本号，另外通用的做法是将版本号放入请求头，但是当经过与众多的第三方开发者打交道后，我可以告诉你还是把版本号放在URL段里省事。

### 分析
记录消费者使用的你的API的版本/端点。这很简单，你只要在每次收到请求时将它们在数据库里的计数加1即可。记录并分析API的使用是个好主意，例如，你最常用的API应该用起来最高效。

为了构建一个第三方开发者喜爱的API，最重要的事情是当你废弃一个API版本时，你实际上可以联系使用废弃的API特性的开发者，这是提醒他们进行升级的最好方式了。

第三方开发者通知的功能可以是自动化的，例如，每当他们访问10,000次废弃的特性时给他们发送一封邮件。

### API根URL
不管你信不信，API的根的位置很重要。当一个开发者（代码学究）得到一个使用了你的API的老项目，并且需要添加一些新特性，他们可能根本不了解你的服务。可能他们所知道的只有消费者调用的API列表。你API的根入口很重要，它应该尽可能简单。一个冗长的、复杂的URL可能会把你的开发者吓跑。

这里是两个常用的API URL根：

* https://example.org/api/v1/*
* https://api.example.com/v1/*

如果你的应用巨大，或者预料到它会很大，将API放到自己的子域去吧（例如api.），这是个好办法，它会为你提供更大的扩展性。

如果你知道你的应用不会有那么大，或者你希望更简单的应用设置（例如你想要搭建网站和同一套框架下的API），将你的API放到域名中间，用斜线隔开（就像：/api/）一样，这也是个不错的主意。

为你的API添加内容是个好想法。当访问Github API的根时，返回得到一些端点的列表。例如，个人来说，我乐于在根URL处放置一些信息，这样可以帮助到一些开发者。例如如何获取这个API的开发文档。

另外，注意HTTPS前缀。一个优秀的RESTful API，你也应该做成HTTPS的。

### 端点
端点是你的API中的一个URL，它连接到一个特定的资源或一个资源集合。

如果你在搭建一个代表多个不同动物园的虚拟的API，每个包含了许多动物（动物确切地只属于一个动物园），雇员（可以在多个动物园间工作），并且记录每个动物的五种信息，你可能会有下面的端点：

* https://api.example.com/v1/zoos
* https://api.example.com/v1/animals
* https://api.example.com/v1/animal_types
* https://api.example.com/v1/employees

如果你想要列出有效的HTTP动词和端点组合，你需要了解到每个端点的功能。例如，这里有一些“半理解”的动作列表，可以用来模仿访问我们虚拟的API。注意，我将HTTP动词放在每个端点前面，这跟在HTTP请求头里的标记是一样的。

* GET /zoos: 列出所有的动物园（ID，名字，不用太详细）
* POST /zoos: 新建一个动物园
* GET /zoos/ZID: 获取一个完整的动物园对象
* PUT /zoos/ZID: 更新一个动物园（完整对象）
* PATCH /zoos/ZID: 更新一个动物园（部分对象）
* DELETE /zoos/ZID: 删除一个动物园
* GET /zoos/ZID/animals: 获取动物列表（ID和名字）
* GET /animals: 列出所有的动物（ID和名字）
* POST /animals: 创建一种动物
* GET /animals/AID: 获取一个动物对象
* PUT /animals/AID: 更新一个动物（完整对象）
* PATCH /animals/AID: 更新一个动物（部分对象）
* GET /animal_types: 获取所有动物类型的列表（ID和名字）
* GET /animal_types/ATID: 获取一个完整的动物类型对象
* GET /employees: 获取雇员列表
* GET /employees/EID: 获取特定的雇员信息
* GET /zoos/ZID/employees: 获取在此动物园工作的雇员列表（ID和名字）
* POST /employees: 创建一个新雇员
* POST /zoos/ZID/employees: 为特定动物园雇佣雇员
* DELETE /zoos/ZID/employees/EID: 开除特定动物园的一个雇员

在上面的列表里，ZID代表了动物园ID（Zoo ID），AID代表了动物ID（Animal ID），EID代表了雇员ID（Employee ID），以及ATID代表了动物类型ID（Animal Type ID）。在文档里注明这些转换是个好习惯。

为了简便，我省去了剩余的通用API URL前缀。在通信的时候这也没什么问题，在你实际的API文档里。你应该一直显示每个端点的全部URL（例如：GET http://api.example.com/v1/animal_type/ATID）。

注意你的数据关系是怎么显示的，特别是那些动物园和雇员间多对多的关系。通过添加一个特殊的URL段，可以用来表示更特殊的交互。当然这里没有表示“开除”的HTTP动词，但是通过对一个动物园内的雇员执行DELETE，我们能达到同样的效果。

### 过滤
当消费者发出请求一个对象列表时，你返回给他满足请求条件的每个对象组成的列表。这个列表会很大，但是你不应该对这些数据加以任何限制。任意的限制都可能给第三方开发者造成困扰。如果他们请求一个特定的集合，并且需要迭代结果，他们不会看到超过100个记录，现在他们的任务是找出这个限制是什么。是他们ORM的Bug？还是故意限制为100？或者是网络将大包切分了？

>为第三方开发者最小化对数据的任意改动

这是很重要的，然而，你为消费者提供某些特定的排序、过滤后的结果。最重要的原因是网络活动最小以及消费者可以尽快获得结果。第二个重要的原因是这些消费者可能很懒惰，如果服务器可以做过滤和分页，那就更好了。不是很重要的一个原因是（从消费者的角度看），对于服务器端有好处的是请求没有资源那么重。

在一组资源上执行GET请求时，过滤是非常有用的。因为这些是GET请求，过滤信息将通过URL传递。下面是一些你可以想象一下如何进行过滤的例子；

* ?limit=10：减少返回给消费者的结果数量（分页）
* ?offset=10：为消费者发送一组信息（分页）
* ?animal_type_id=1：过滤满足下面条件的记录（WHERE animal_type_id = 1）
* ?sortby=name&order=asc：基于某个属性对结果进行排序（ORDER BY name DESC）

这些过滤可能对于端点URL来说优点多余。例如我前面提到的GET /zoo/ZID/animals。这等同于GET /animals?zoo_id=ZID。贡献出对消费者可用的端点会让他们过得更容易，尤其是当你参与的请求时更是如此。在文档里记录这些多余的信息，这样第三方开发者就不会困惑他们是否有区别了。

另外，不必多言，无论何时你执行一个数据过滤或者排序，确保你的消费者可以过滤或排序的白名单。我们不希望将任何数据库错误返回给消费者。

### 状态码
对于RESTful API来说很重要的一点是它恰当运用了HTTP状态码。毕竟他们是标准的。各种各样的网络设备都能读取到这些状态码。例如负载均衡器可以配置为限制发送请求到一个发出大量50X错误的Web服务器。[HTTP状态码的太多了](http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html)，下面列出一些常用的：

* 200 OK - [GET]
	* 消费者请求数据，服务器找到了它们（幂等）
* 201 CREATED - [POST/PUT/PATCH]
	* 消费者向服务器提交数据，服务器创建了对应的资源
* 204 NO CONTEST - [DELETE]
	* 消费者向服务器请求一个删除了的资源，服务器确实删除了它
* 400 INVALID REQUEST - [POST/PUT/PATCH]
	* 消费者向服务器提交坏数据，服务器也什么都没做（幂等）
* 404 NOT FOUND - [*]
	* 消费者请求了不存在的资源或集合，服务器什么也没做（幂等）
* 500 INTERNAL SERVER ERROR - [*]
	* 服务器发生了一个错误，如果请求成功，消费者并不知情。

#### 状态码范围
1xx范围为底层HTTP保留，你的整个职业生涯可能都不会手动发送这些状态码。

2xx范围为成功消息保留，当所有的情况都如预期发生。仅最大的努力保证你的服务器为消费者返回尽可能多的2xx。

3xx范围为流量重定向保留。大多数API不使用这些请求（不像SEO一样使用），然而新式的Hypermedia风格API将会大量使用它。

4xx范围为响应消费者的错误进行保留。例如他们提交了错误的数据，并且要请求一些不存的资源。这些请求应该是幂等的，不应改变服务器的状态。

5xx范围为响应服务器的错误保留。往往这些错误出自一些底层错误，甚至都不是程序员造成的，来保证消费者获取这种类型的响应。消费者收到5xx状态码时，他不可能知道服务器的状态，这些应该是可避免的。

### 期望返回文档
当使用不同的HTTP动词对一个服务器端点执行动作时，一个消费者需要获取一些返回信息。下面的列表非常典型：

* GET /collection： 返回一组对象资源的列表
* GET /collection/resource：返回一个独立的资源对象
* POST /collection：返回一个新建的资源对象
* PUT /collection/resource：返回完整的资源对象
* PATCH /collection/resource：返回完整的资源对象
* DELETE /collection/resource：返回空文档

注意当一个消费者创建了一个资源，他们通常不知道资源的ID（或者其他创建的属性和修改的时间戳，如果可接受的话）。这些额外的属性被一个子序列请求所返回，并且当然可以作为原始的POST请求的响应。

### 认证
大多数时候，服务器需要知道到底是谁在发请求。当然，一些API提供了可以被（匿名）大众消费的端点，但是多数时候还是需要特定的某人来完成工作。

[OAuth 2.0](https://tools.ietf.org/html/rfc6749)是个很棒的解决方案。对于每个请求，你可以确定哪个消费者在发出请求，哪个用户在请求，并且提供了一个标准化的过期访问和允许用户废除消费者的访问。所有的这些都不需要第三方消费者了解用户登录凭证。

有[OAuth 1.0](http://tools.ietf.org/html/rfc5849)和[xAuth](https://dev.twitter.com/docs/oauth/xauth)来做同样的事情。不管你选择了哪种方式，确保它是通用的，且有很好的文档记载，甚至被多种你的消费者喜爱的语言/平台所实现。

我可以诚恳地告诉你OAuth 1.0a，它是最安全的选择，但是实现起来很蛋疼。我被每个第三方开发者都得自行实现一遍所惊呆，竟然没有他们使用的语言版本的库。我花费了数小时调试这些扑朔迷离的“无效签名”错误来推荐你选择一个合适的。

### 内容类型
现在，最激动人心的莫过于为RESTful接口提供JSON数据类型。包括Facebook，Twitter，Github，或者其他你叫得出名字的公司。XML看起来输掉了这场战争（除了在大型协作环境里）。SOAP，感天谢地它是全部，但它已死。另外我们真的不想看见那么多API提供HTML作为数据被消费（除非你在编写一个scraper）。

开发者使用流行的编程语言和框架，可以将你返回给的内容解释为任何有效的数据。如果你在构建一个通用响应对象，使用一个不同的序列化工具时，你甚至可以轻而易举地将数据表示为上述任何数据格式（不包括SOAP）。好好利用接收头你可以用来说明数据类型，虽然这有一点烦。

一些API创建者给端点后的URL推荐添加一个.json，.xml或.html文件扩展来指定返回的内容类型。尽管我个人不喜欢这样，但是我确定接收头（它是HTTP的一个部分）的那种用法是正确的。

### 超媒体API
超媒体（Hypermedia）API可能是RESTful API设计的未来。他们真的是非常令人惊奇的概念，回到了HTTP和HTML是想要如何工作的这个根本问题。

当使用非超媒体RESTful API进行交互的时候，URL端点是服务器和消费者间契约的一部分。这些端点必须提前被消费者所熟知，并且对他们的改变将导致消费者不能再通过它与服务器进行通信。这样，你可以认为这是一种限制。

现在，API消费者不仅是用户代理来发出HTTP请求。人类，浏览器，都是常用的发送HTTP请求的代理。人类，然而不是被限制到这些预定义的端点URL的RESTful API契约里。是什么让人类如此特别？好吧，人类可以阅读内容，点击看起来很有趣的链接，并且一般浏览网站和理解内容并继续浏览。如果一个URL改变了，人类是不受影响的（除非，他们是个数钱，在这种情况下，人们可能会去主页然后找到他们所喜欢的内容的新链接）。

超媒体API概念像人类一样工作。请求到API的根返回了一系列的API列表，每个URL又代表了一些信息的集合，并且按这种方式将所包含的信息描述给消费者。提供每个资源的ID不重要（或不是必须），只要有URL就够了。

当消费者使用超媒体API链接和获取信息时，URL通常随着响应而更新，并且不会被作为契约的一部分提前被用户了解。如果一个URL被缓存了，那么它的一个子序列请求将返回404，消费者可以轻松地返回根然后重新找到内容。

当获取一个集合内的一系列资源时，为一个独立资源包含了一个完整URL的属性被返回。当执行POST/PATCH/PUT时，响应可能被重定向到3xx。

JSON不能给予我们想要的来指定哪些URL是属性的语义，或者URL如何关联到当前的文档。HTML，你可以猜猜，可以提供这样的信息。我们可能很愿意看到我们的API完整的闭环，然后返回给消费的HTML。考虑一下我们使用了CSS，某天我们可能会看到它成为API的通用实践和网站使用一样的URL和内容。

### 文档
老实说，如果你不能100%遵循这篇文章里的各个标准，你的API可能不会很吓人。然而，如果你没有很好地给你的API编写文档，没人会知道如何使用它，这将会很恐怖。

让你的文档可以被未授权的开发者接受。

不要使用自动化文档生成器，如果你那么做了，至少确定你检查过它，并且它是可展示的。

不要删节示例请求和响应体，在你的文档中使用语法高粱来显示完整的信息。

文档希望响应码和每个端点可能的错误信息，甚至可能导致错误的原因说明。

如果你有空闲时间，构建一个开发者API控制台，这样开发者可以立刻检测你的API。这没你想的那么难，开发者（内部的或第三方）都会因此而喜欢你。

确定你的文档可以被打印。CSS是很有用的，不要打印时隐藏起来的边框。如果没人可以打印一份物理拷贝，你可能会对有多少人愿意为了离线阅读而打印一份PDF的数量而感到吃惊。

### 勘误表：原生HTTP请求包
我们所做的一切都是通过HTTP协议的，我将为你解剖一个HTTP请求包。我通常为那么多人不知道这些是什么而感到吃惊。当消费者向服务器发送了请求时，他们提供了一系列键值对，叫做头，同时还有两个换行字符，并且以请求体结束。这些都在同一个包内被发送。

服务器然后按照键值对格式进行返回，同样有两个换行符和响应体结尾。HTTP是一种典型的请求/响应协议，这里不支持“推”（服务器主动向消费者发送数据），除非你使用了例如Websockets的协议。

当设计你的API的时候，你应该可以使用一些工具让你看到原生的HTTP包。考虑使用Wireshark吧。另外，确保你可以使用一个让你可以读取和改变这些域的框架/Web服务器。

#### HTTP 请求示例
```json
POST /v1/animal HTTP/1.1
Host: api.example.org
Accept: application/json
Content-Type: application/json
Content-Length: 24


{
	"name": "Gir",
	"animal_type": 12
}
```

#### HTTP 响应示例
```json
HTTP/1.1 200 OK
Date: Wed, 18 Dec 2013 06:08:22 GMT
Content-Type: application/json
Access-Control-Max-Age: 1728000
Cache-Control: no-cache


{
	"id": 12,
	"created": 1386363036,
	"modified": 1386363036,
	"name": "Gir",
	"animal_type": 12
}
```
