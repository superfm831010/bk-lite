# ****快速入门****

**如何创建一个知识问答机器人**

## ****背景说明****

企业中有大量知识和信息，包括政策、产品说明、流程文档和技术支持等。员工在日常工作中经常需要这些信息，以做出决策或解决问题。传统的查找方式（如手动搜索文档或向同事咨询）可能耗时且效率低下，可以借助OpsPilot，集中管理企业知识，并创建对外使用的机器人，结合大模型提供智能化回答，提升用户体验。

## 第一步：新建知识库

为了更好的使用机器人，需要对机器人引用的知识进行上传-存储-训练-检索，这些可在“OpsPilot-知识库”中实现。在“知识库”中创建一个知识库，以存储和管理机器人所需的所有信息和数据。

### ****创建知识库****

输入知识库的名称和描述，选择归属的组织（知识库的查看和操作权限和所属组织有关，可多选），选择Embed模型（用于知识库知识的存储，以便后续高效搜索）
![功能图片1.png](https://static.cwoa.net/0cbbf72e17774d4bbd6a23792cf9fa6b.png)
### ****进行知识库文档的上传****

- 知识库文档的上传分为三类，每一类上传有其对应数据需提供。
    - 本地文档（支持上传word、Excel、pdf等格式的文档）
    - 网页文档（直接引用网站信息）
    - 自定义文档（自行撰写的文档）
![功能图片2.png](https://static.cwoa.net/bd68106b63f14a03b202cc5bfb10df1f.png)
#### ****选择——提供知识本体****

- 支持三种方式上传：本地文件、网页链接、自定义文本
    - **本地文件**：点击提示区域自动打开资源管理器，打开需要上传文件夹选取文件上传；或者提前打开文件夹，选取文件直接拖拽到有效区域内。
    - **网页文档**：为此文档定义名称方便理解，输入需要上传的网址链接，选择对于该网址需要跳转的网址数量（深度）。
    - **自定义文本**：一些零散或者自创的内容可通过手动输入创建。
![功能图片3.png](https://static.cwoa.net/265554dfa00740158aba2f256341bd26.png)
#### ****提取——文档****预处理1

上传的文件首先需要将文件内的文本提取出来，系统会根据文件类型初始匹配推荐方式，在配置操作中可修改。
![功能图片4.png](https://static.cwoa.net/df8e5ad878c34335a29cba0d9adab7c3.png)
一共4种提取方式，包括：全文提取、章节提取、工作表提取、行级提取，分别使用不同情况，可根据提取说明中的文字说明和示例图选取想要的提取方式。（全文提取中，pdf文件不可编辑的一类可启动OCR增强识别图像中的文字）

#### ****分块****——文档预处理2

- 提取出文本之后，会进一步预处理知识内容，将文本分块以便后续检索能精准快速找到需要的内容。
    - 提供4种分块方法，每种方法配备参数设置和分块示例以供调整。点击【查看块】可查看分块效果：
    - 包括定长分块、循环分块、语义分块、不分块。
    - 定长分块可设定固定的分块长度，循环分块在此基础上可设置分块之间可重叠的长度以保留前后文衔接；
    - 语义分块启用Embed模型基于算法分析文字意思、逻辑分块。
 ![功能图片5.png](https://static.cwoa.net/37eca88272524c35bc4da5dd96322c25.png)
- **完成阶段**
    - **训练状态**：返回文档列表查看上传知识的状态。文档上传-切片完成后，会对所有的文档进行切片和训练，状态为“就绪”时，说明该文档可使用。
    - **测试**：文档创建好后，对该知识库的检索进行设置，并测试效果。
![功能图片6.png](https://static.cwoa.net/71fd949be73849db871df03a6bff57b8.png)
![功能图片7.png](https://static.cwoa.net/00f1621a70d1421ba0f475f58a32a086.png)
![功能图片8.png](https://static.cwoa.net/25e749af059c44d9ad62f05b52f8d433.png)
#### ****分块界面****

分块界面增加“批量生成Q&A”和“批量删除”。

可编辑分块、单个生成问答对、单个删除。

卡片支持展示每个分块的对应问答对的数量和字符的数量。

支持对分块进行删除，支持单个/批量，可以仅删除分块、也可同时删除关联的问答对。
![功能图片9.png](https://static.cwoa.net/c79e7bb831bc433687908ae37f195144.png)
#### ****问答对****——文档预处理3

##### ****生成问答对****

问答对的生成方式主要为LLM大模型对分块数据智能生成问答对。并且在知识库的文档中，用户可自行选择文件或网页链接并通过LLM模型自动生成问答对。
![功能图片10.png](https://static.cwoa.net/73eb9e2315bb4244869ce026bb25af43.png)
![功能图片11.png](https://static.cwoa.net/ef4eb27bec2b48bab895d7689961727f.png)
![功能图片12.png](https://static.cwoa.net/951a230a0659492e9d7c3c898320214c.png)
##### ****查看问答对****

在知识库中，用户可直观的查看所有问答对。问答对的信息包括名称，问答对数量，创建时间，创建者，操作等，同时可以点击查看每一份问答对拆解的详情问题和答案。
![功能图片13.png](https://static.cwoa.net/0f9ba4d8cf7744718cc21eb876c7f8fd.png)
问答对界面：问答对要是关联了分块，在卡片标注“chunk”代表与原始分块关联，查看问答对详情时，也可以查看源分块的详情。
![功能图片14.png](https://static.cwoa.net/dc0bc0b49bfd4b858b9179f5c44d8c25.png)
![功能图片15.png](https://static.cwoa.net/fbf312e261364c51abe940cc73aba3f9.png)
#### ****知识图谱****——文档预处理4

##### ****生成知识图谱****

知识图谱的生成方式主要为LLM大模型，重排模型，Embed模型智能生成知识图谱。（注意：这里的embed模型要选择与知识库创建的时候一样的embed模型）在知识库的文档中，用户可自行选择文件并通过LLM模型自动生成知识图谱。
![功能图片16.png](https://static.cwoa.net/98178ac3ae0348d199344dc35880d46a.png)
##### ****查看知识图谱****

选中的源文件汇总成知识图谱，图谱由节点和关联组成，节点分为实体，分块和社区。节点与节点之间的连线称为关联。在知识库中，用户可直观的查看所有知识图谱，同时可以点击具体查看知识图谱的节点，关系，总结等。
![功能图片17.png](https://static.cwoa.net/14b9bfab5ce34f57a546c9474f1966af.png)
#### 结果****检索****

用户提出问题时，智能运维OpsPilot会通过灵活路由，选择调用知识图谱，还是知识分块，问答对作为召回结果，确保用户始终能获得最优答案。
![功能图片18.png](https://static.cwoa.net/a81070b4edb440f999d0c054de7e60ad.png)
## ****第二步：新建****智能体

接下来，需要定义机器人的智能体，可以创建空白智能体，也可以直接选择内置好的模板创建智能体。根据需求设定智能体的逻辑和流程，以确保机器人能够有效地响应用户请求。
![功能图片19.png](https://static.cwoa.net/05f5a3423f2c498f8e4f021e63d2f316.png)
- 在配置机器人的智能体信息时，需要填写的参数如下：
    - 基本信息：名称/分组/简介,可以进行修改
    - LLM模型：支持选择内置的LLM大模型，大模型可以根据在知识库搜索到的结果，进行再次总结，并且回复。
    - LLM的温度参数：默认为0.7，用于控制文本生成的随机性和创造性；低温度（比如0.2）会生成更确定的结果，而高温度（比如0.9）则会增加文本的多样性和随机性。通过调节温度，用户可以根据需求平衡生成内容的准确性和创新性。
    - 提示：可以输入相关的提示语，引导模型生成特定的回复，通过提供上下文或问题以调节输出内容的方向和质量。
    - 对话历史：默认是10:，聊天历史数量指的是系用户与机器人之间互动的对话轮次或消息总数。这一数量可以帮助机器人理解上下文，并增强回复的相关性和连贯性。
    - RAG：RAG是一种将信息检索与生成模型结合的架构，先从知识库中检索相关信息，然后使用生成模型产生上下文相关的回答。
    - RAG来源：开启后，在对话时可以显示引用的知识来源
    - 知识库：支持选择同一分组下的知识库作为知识来源，并为知识库调整阈值，从而提高回答的准确性和可靠性。
    - 工具：给智能体获取外部数据或者执行操作的能力，具体调用哪个工具，由大模型自主决定。

完成设置后，用户可通过与智能体对话来测试和优化智能体效果。
![功能图片20.png](https://static.cwoa.net/df09a76ceb2247089a2668b169ef1b6f.png)
## ****第三步：新建应用机器人****

当智能体创建完成后，我们需要在工作室正式创建应用机器人，并且把应用发布出去，以供大家使用。
![功能图片21.png](https://static.cwoa.net/29d1953acdf54777a882430c6e390447.png)
应用需要填写名称、分组和介绍等信息，并且选择使用的模型（目前只用内置核心模型可使用），并选择这个应用使用的技能（智能体）以及发布的渠道。
![功能图片22.png](https://static.cwoa.net/0988212bd6c547f2974b7bc66908f774.png)
应用的渠道目前支持四类，需要提前在通知（Channel）中设置好需要使用渠道的参数信息。
![功能图片23.png](https://static.cwoa.net/b7a35d04ba4d42c7b5cb967eb64e7f35.png)
全部设置完后，点击“保存&发布”按钮，在配置好的渠道即可使用该应用。
![功能图片24.png](https://static.cwoa.net/8d70fc528aa743859d569c18bf853dee.png)
## ****第四步：使用****应用

目前OpsPilOt支持 Web，企微和钉钉、网页四类通知渠道，可以按照设定的机器人域名/端口等信息，在此四类渠道上发布。

比如在企微工作台创建应用，并且接入机器人，即可实现对话。
![功能图片25.png](https://static.cwoa.net/353e3a275da44f248cddcb15145526c7.png)
## ****第五步：查看对话情况****

当用户对话完成后，可以在应用中查看所有用户的对话记录以及用户对机器人的使用和调用情况。
![功能图片26.png](https://static.cwoa.net/4925fdad23e44661979115dddf67f346.png)
![功能图片27.png](https://static.cwoa.net/aafcffb33abd46a7a740fa9472cd8239.png)
# ****功能介绍****

## 模型

在模型模块，可以对OpsPilot能够使用的相关模型进行管理和配置，目前已经内置常用模型，支持配置和新增模型。

模型管理前端展示优化：分为左右结构（llm、embed、rerank、ocr均已修改）

左侧：用树形图展示；分为全部和分组名，并备注好了每个分类模型总数;支持拖拽重新排序；支持模型分组的新增，但内置分组的不支持编辑和删除。

右侧：该分组下所有的模型，搜索和新增未变，但是模型分组的字段可进行动态获取。
![功能图片28.png](https://static.cwoa.net/db0eabe75aae49e4a1919a4a0216ede3.png)
### LLM模型

LLM模型用于配置模型的基础配置，如凭据，方便后续的“技能”所使用，OpsPilot内置以下LLM模型的支持：

| **HuggingFace** | **DeepSeek** | **OpenAI** |
| --- | --- | --- |
| QwQ | DeepSeek-R1:1.5b | GPT-3.5-Turbo-16K |
|     |     | GPT-4-32K |
|     |     | GPT-4o |

LLM模型支持编辑、开关、添加等操作:

LLM大模型的标签优化，顶部的搜索可以筛选类别的标签，一类是所属模型分组、一类是该模型的类别。  
大模型编辑时，支持选择模型分组或者模型类别。
![功能图片29.png](https://static.cwoa.net/cc45125eba1b43048f6b51718ad42f0e.png)
- **基础信息**：包括名称、模型名称和类型，以供分组展示。
- **网址**：用户可以通过配置特定的API URL来接入供应商的LLM模型，这样应用程序能够与模型进行通信，从而发送请求和接收响应。
- **API密钥** ：为了确保数据安全和访问控制，用户需要配置API密钥。这个密钥用于验证用户的身份，确保只有授权的用户能够访问和使用模型。
- **开启/关闭**功能 ：用户可以根据需要启用或禁用LLM模型，这样可以灵活使用相关模型。
- **分组**：控制大模型的可见范围和使用，可多选，只有选择了的分组才可以看见该模型。
- **配额分配组**：大模型的使用需要token，配额分配组用来控制大模型使用哪个分组的token，不一定要和分组的组相同，仅单选。

### Embed模型

Embed模型为知识提供向量化的能力，是知识库能够进行语义检索的支撑功能，OpsPilot内置以下Embed模型，内置的这些模块可以在“知识库“中进行使用。

- [FastEmbed](https://qdrant.github.io/fastembed/"%20\t%20"_blank)
    - bge-small-zh-v1.5
- [BCEmbedding](https://github.com/netease-youdao/BCEmbedding"%20\t%20"_blank)
    - bec-embedding-base_v1
![功能图片30.png](https://static.cwoa.net/5392e6b560ab4430903e108b9afcf5e3.png)
### ReRank模型

ReRank模型可以对检索出来的知识进行重排序，让大模型在使用RAG能力的时候，知识检索效果更好。OpsPilot内置以下ReRank模型，内置的这些模块可以在“知识库”中进行使用，用于知识库检索效果的优化。

- BCEReranker
    - bce-reranker-base_v1
![功能图片31.png](https://static.cwoa.net/ed717fd08a50455eacbc91b4178dd971.png)
### OCR模型

OCR（光学字符识别）模型是一种用于将图像中的文本信息转化为可编辑文本数据的技术，广泛应用于文档数字化和信息提取。主要用于“知识库-知识上传”时，识别知识时使用。OpsPilot内置以下模型

- OlmOCR
- AzureOCR
- PaddleOCR
![功能图片32.png](https://static.cwoa.net/09bcd43d1c804b15aad445cb30bb58b1.png)
## 工具

### 工具页面

OpsPilot采用 **MCP 协议工具化数据接入**工具，实现了异构系统间的数据贯通。通过这一技术，OpsPilot 能够将企业各个业务系统的真实数据接入平台，结合联网检索获取的实时外部知识与私域知识库沉淀的专业经验，形成立体化的知识网络。
![功能图片33.png](https://static.cwoa.net/4022e16d2d4045489025e0951f915e58.png)
Opspilot内置了一批通用的工具，包括k8s、Jenkins、节假日检索、联网检索等通用工具，Weops等业务专用的工具等。详见OpsPilot能力介绍文档【工具】介绍。

### 编辑、添加工具

MCP协议采用标准化接口设计，**支持随时扩展工具类型**，用户可根据实际需要添加新工具。其中变量类型下拉选择有2类：文本、密码，可选择是否为必填项，通过右边“＋”即可增加变量。
![功能图片34.png](https://static.cwoa.net/8c5b40d982c141c0a0667c6068f36158.png)
- 编辑和添加的参数相同：
    - **标签**：为该工具标识分类，比如：运维工具、媒体工具、通用工具等，方便检索使用该工具；
    - **MCP链接**：用户可在别的平台里开发工具，或者使用开源工具，使用MCP链接的统一接口接入，不需要单独为工具开发一个API接口，降低开发使用成本；
    - **变量**：支持用户为该工具定义使用时需要变更，传递给后台的变量。比如：可以通过jenkins_url（Jenkins 服务的访问地址）、jenkins_username （登录的用户名）和 jenkins_password （登录密码）这三个变量的值，来连接到不同的 Jenkins 服务并进行操作。
    - **分组**：控制能看见、使用该工具的分组。

### 工具检索

用户可以在搜索栏选择标签、输入工具名称对工具进行检索，支持多选。
![功能图片35.png](https://static.cwoa.net/4933cd50f02b4bf1bfab68ed13dbbe7c.png)
## 知识库

知识管理模块提供了对知识库的管理，支持用户上传文件型知识、人工录入的知识、URL爬取的知识，由多个种类的知识聚合而成，并且利用各种算法提升知识索引的准确性。

知识库管理解决了以下问题

- 1、哪些知识组成了这个知识库：支持上传/爬取多种类型、多个领域的专业知识。
- 2、如何对知识使用怎么样的分块模式：内置
- 3、如何检索准确：使用混合检索+ReRank，让检索变得更加准确，混合搜索的时候，语义检索和文本检索的权重可以灵活分配

总的来说，在知识库这里对知识进行上传、管理和加工，进行精细化的配置，以供LLM技能使用。

### 知识库列表

知识库列表以卡片的形式展示用户有权限的知识库，普通用户可以查看/操作自己所在组织的所有知识库；超管可以查看/操作所有的知识库。知识库卡片右下角显示当前知识库的所有者和分组，方便管理。
![功能图片36.png](https://static.cwoa.net/4f5ad3ae212d4117b4c8b3bf96dacb00.png)
#### ****知识库创建****
![功能图片37.png](https://static.cwoa.net/3a48210e82164dc08e1accd1eaee85fc.png)
- 名称：输入知识库名称
- **分组**：选择该知识库所属的分组，其他用户只有在这个分组下，才能查看到该知识库
- **Embed模型**：主要用于词汇和数据的向量化，以便计算机更好的理解，目前内置两个模型，可以根据实际情况进行切换使用（对于已经训练好的知识库，切换模型后将会重新训练）。
- 简介 ：输入该知识库的详细介绍。

#### ****知识库编辑/删除****

知识库可以进行内容的重新编辑，包括重新更新名称/分组/简介，其中可以切换Embed模型，切换后整个知识库将会根据新选择的Embed模型进行所有知识的重新训练，训练的进度可在知识库详情中查看。
![功能图片38.png](https://static.cwoa.net/c3dc1900eeb644ebb89925d73f5e3108.png)
### 知识库文档管理

OpsPilot能够管理知识，包括 本地文件、网页链接、自定义文本，并供知识库使用。可以在文档列表里查看上传的知识的状态、提取方式、分块方式，不满需求的方式可以在设置里调整提取、分块方式后重新训练。
![功能图片39.png](https://static.cwoa.net/90ba770761d84f2dbf4f52a985b31c0e.png)
源文档重新训练时，会给二次提示：重新训练后，分块的id将会改变，所以请确定是否保留与源文档分块关联的问答对：如果删除，则与源文档分块关联的问答对均被删除；如果保留问答对，则会切断与分块的关联，但是问答对仍保存。

源文档删除时，会给二次提示：源文档删除后，分块将会被删除，则与源文档分块关联的问答对均被删除。

整个知识库切换embed模型的时候，也会给二次提示：在切换Embed模型后，需要重新训练知识库文档，所以请确定是都保留与源文档分块关联的问答对：如果删除，则与源文档分块关联的问答对均被删除；如果保留问答对，则会切断与分块的关联，但是问答对仍保存。
![功能图片40.png](https://static.cwoa.net/cce1b679c388469d9a628eb0cdd084cb.png)
#### 文本分块

##### ****文档上传****

新增知识的第一步是知识上传，包括三类，文档类的知识可以直接上传、网页知识需要填写对应URL、自定义文本需要手动录入

###### 本地文件

在日常运维过程中，会产生多种类型的知识，他们一般会以文件类型存在，这也是OpsPilot知识库中最主要的私域知识来源，根据需求自行上传多个本地文件。
![功能图片41.png](https://static.cwoa.net/b32bf3a203414a68a5a5cbef6877d762.png)
###### 网页知识

- 互联网上有非常多有用的知识，例如RabbitMQ的官方文档、Redis的官方文档，这些软件会因为对应版本的不一样，具备不一样的特性，或者具备不一样的命令行参数，可以使用网页知识，对他们进行快速、持续的知识捕获。
- **深度**：输入的网址内部有多个可以进一步跳转的网址，以此类推深入，选择需要跳转多少次。1次——只打开输入的网址，获取此页面内容；2次——获取输入网址的页面内容，并打开此网址内可跳转的链接，打开这些链接去获取这些页面的内容。以此类推。
![功能图片42.png](https://static.cwoa.net/054b3ffd7b144dd9bcc516449785b7ab.png)
###### 自定义文本

运维脚本的代码段、零散的碎片知识，都适合用手工录入的方式形成知识，让OpsPilot能够对其进行使用
![功能图片43.png](https://static.cwoa.net/02602a90b7c14a0b903bdb0d445c8acd.png)
##### 文本****提取****

- 新增知识的第二步是将文件内的文本提取出来，系统会根据文件类型初始匹配推荐方式：
    - 全文提取推荐格式：pdf、txt(包括自定义文本)、MD、网页链接；
    - 章节提取：word；
    - 工作表提取、行级提取：表格（xlsx、csv）。
![功能图片44.png](https://static.cwoa.net/ed08bbaac3dc463aa67d139d27f75a82.png)
一共4种提取方式，包括：全**文提取、章节提取、工作表提取、行级提取**，分别使用不同情况，可根据提取说明中的**文字说明和示例图**选取想要的提取方式。（全文提取中，pdf文件不可编辑的一类可启动OCR增强识别图像中的文字）

- 全文提取：
    - 适用格式: PDF、Markdown（.md）、TXT(.txt)等
    - 保留原始文本格式和段落结构，确保完整覆盖内容（PDF需OCR处理扫描内容，MD/TXT直接提取）。
    - 可配置参数：OCR（Optical Character Recognition，光学字符识别）增强是指在图像或扫描文档中提取文本信息的过程。OCR增强不仅提高了文本识别的准确性，还可以结合其他处理技术，如图像预处理和后处理，以优化结果。
![功能图片45.png](https://static.cwoa.net/ecf673c09abb406094a35a871b42649b.png)
- 章节提取
    - 适用格式: Word（.doc）等
    - 利用文档的目录结构（如标题、分节符）提取内容，保持章节逻辑完整性，适合技术文档、论文等长文本。
![功能图片46.png](https://static.cwoa.net/67085da70b264dbdaf13d1124d6c635b.png)
- 工作表提取
    - 适用格式: Excel（.xlsx/.csv）等
    - 提取和解析Excel文档中的各个工作表，保留表格的完整结构和数据（如公式、合并单元格），会遍历每一个单元格，提取其中的所有数据，并根据需要重新组织或格式化。适合需要完整表格信息的场景。
![功能图片47.png](https://static.cwoa.net/043b46a6fe08422bb14c322023e4b1d5.png)
- 行级提取
    - 适用格式: Excel（.xlsx/.csv）等
    - “Excel标题 + 行组合解析”提取Excel表格的标题（通常是第一行的列名），然后将后续的每一行数据与相应的标题进行组合。适配数据清洗、分析或机器学习需求，便于动态更新和关联操作。
![功能图片48.png](https://static.cwoa.net/18af22ccbc21455c865f04e36ff26fa8.png)
##### 四种文本****分块****方法

- 提取出文本之后，会进一步处理知识内容，对传入的知识进行分块处理。通过将知识进行分块，可以更有效地组织和存储数据，使得搜索引擎在查找相关信息时能够更快地定位目标数据，从而提高检索效率。
    - 提供4种分块方法，每种方法配备参数设置和分块示例以供调整。点击**【查看块】可查看分块效果**，不满意分块效果可返回上一步重新调整配置。
- **定长分块：**将输入的文本或数据划分成较小的、易于处理的部分或“块”。**可设定固定的分块长度，块大小决定了每个分块所包含的文本量**，默认每块是256个字符。
    - 适用格式: 文本文件（TXT）、PPT、PDF、Excel等
    - 规则明确、处理高效，适合快速批量处理数据。但可能因机械分割导致语义断裂（如截断句子或表格），需权衡效率与内容完整性。
![功能图片49.png](https://static.cwoa.net/35cc9c15ee2a4be9bfbd2e212d227142.png)
- **循环分块：**在定长分块的基础上，**可设置分块之间的块重叠的长度以保留前后文衔接**。块重叠是指在分块时，前一个块与下一个块之间的内容重叠部分，默认是0的，即相邻的两个分块之间不会有任何重叠部分。
    - 适用格式: 长文本（PDF、TXT）。
    - 通过重叠减少语义断裂，适合需要连续上下文的任务（如文本分析），但可能因重复内容导致存储冗余。
![功能图片50.png](https://static.cwoa.net/ca58e6b14d4a4d3692541fa9193b93e5.png)
- **语义分块：**启用Embed模型，**基于算法，可以进一步考虑文本或数据的上下文和意义**。通过分析句子、段落或数据块的语义关系，该算法可以更准确地识别出相关内容，从而确保信息的一致性和逻辑性。
    - 适用格式: 结构化文档（Word、Markdown）、技术文档（PDF 带目录）。
    - 保留完整语义单元（如章节、段落、函数模块），适合需逻辑关联的长文本处理，但对文档结构或算法依赖性较高。
![功能图片51.png](https://static.cwoa.net/16567c64785848659ac375cffff8005c.png)
- **不分块**：即不作任何分块处理，直接上传提取出来的全部文本。
    - 适用格式: 短文本（邮件、摘要）、小型文件（单页 PPT、简单表格、短文 TXT）。
    - 将整个文保留内容的全局关联性，适合需要整体理解的场景（如摘要生成、全文检索）。但对计算资源要求较高，长文本处理效率低。
![功能图片52.png](https://static.cwoa.net/e47b7101b08543dfa150b5d62e3fa6c5.png)
##### ****完成阶段****

**训练状态**：返回文档列表查看上传知识的状态。文档上传-切片完成后，会对所有的文档进行切片和训练，状态为“就绪”时，说明该文档可使用。
![功能图片53.png](https://static.cwoa.net/2aa7ba55f94e4454aa90e46cf2cfd17a.png)
![功能图片54.png](https://static.cwoa.net/787e97a4d15444b18b1a557141862d48.png)
#### ****问答对****

为了能够更加精准、专业地回答用户问题，我们还运用了问答对和知识图谱。用户提出问题时，智能运维OpsPilot会通过灵活路由，选择使用知识分块，问答对还是知识图谱作为召回结果，确保用户始终能获得最优答案。

##### ****生成问答对****

问答对的生成方式主要为LLM大模型对分块数据智能生成问答对。并且在知识库的文档中，用户可自行选择文件或网页链接并通过LLM模型自动生成问答对。
![功能图片55.png](https://static.cwoa.net/a1de171eb3664344900cb88770f9a618.png)
![功能图片56.png](https://static.cwoa.net/50d4d17918bf49c7a3a129774ee4302e.png)
![功能图片57.png](https://static.cwoa.net/88911533b3424bc88dfc29e06062f409.png)
##### ****查看问答对****

在知识库中，用户可直观地查看所有问答对。问答对的信息包括名称，问答对数量，创建时间，创建者，操作等，同时可以点击查看每一份问答对拆解的详情问题和答案
![功能图片58.png](https://static.cwoa.net/1778afc25dc542faa4cc6d0d4f2ba413.png)
在问答对的详情页面，可以多选问题再执行问题的单个/批量的生成，原来有答案的，覆盖原来答案，问答对详情页面可以筛选（全部问题、已生成答案、未生成答案）
![功能图片59.png](https://static.cwoa.net/d20ba6d8da634a00b5a43692ca396851.png)
##### ****检索问答对****

用户提出问题时，OpsPilot会通过灵活路由，选择使用知识分块还是问答对作为召回结果，确保用户始终能获得最优答案。
![功能图片60.png](https://static.cwoa.net/6aadfcd93f944d1ebc39fb7c34a08577.png)
**问答对导入**

问答对导入新增模板下载：json、csv。
![功能图片61.png](https://static.cwoa.net/da6f883123094f65a67bfb1478f4f7e7.png)
**问答对导出**

问答对可进行导出。
![功能图片62.png](https://static.cwoa.net/9900da0ef49f4a1584ae6b73a6c5d7a1.png)
**问答对编辑**

分块生成的问答对支持重新设置。
![功能图片63.png](https://static.cwoa.net/7e7296a3a3544a1492cf9390b404ac94.png)
#### 知识图谱

##### ****生成知识图谱****

知识图谱的生成方式主要为LLM大模型，重排模型，Embed模型智能生成知识图谱。用户可通过点击“设置”自行选择文件并通过LLM模型自动生成知识图谱。
![功能图片64.png](https://static.cwoa.net/790aa7de2cd24dfbac1502606e2fd2ba.png)
![功能图片65.png](https://static.cwoa.net/3bf45d1bcc474e3785207bce90da87c1.png)
##### ****查看知识图谱****

选中的源文件汇总成知识图谱，图谱由节点和关联组成，节点分为实体，分块和社区。节点与节点之间的连线称为关联。在知识库中，用户可直观的查看所有知识图谱，同时可以点击具体查看知识图谱的节点，关系，总结等。
![功能图片66.png](https://static.cwoa.net/23ae7b6bb2bc4c488dbf77b0f5cbbcc5.png)
##### ****检索知识图谱****

用户提出问题时，OpsPilot会通过灵活路由，选择调用知识图谱，还是知识分块，问答对作为召回结果，确保用户始终能获得最优答案。
![功能图片67.png](https://static.cwoa.net/e1ecfba89b1e419f8cb25c0272c0b934.png)
### 知识库设置

支持对知识库进行配置
![功能图片68.png](https://static.cwoa.net/382a78a9f57b43f596c5def2b39096a1.png)
- 知识库基础模型
    - 知识库使用Embedding模型通过将文本转化为语义向量，为知识库赋予智能检索、语义关联与跨语言理解能力，实现精准匹配与隐含关系挖掘，使用的embed模型如下：FastEmbed、bce-embedding。
-   知识库的检索设置
    - 返回类型分为三类，分别为知识分块，问答对，知识图谱。可同时选择多种返回类型。还可以自行选择召回数量，召回数量指检索返回块的数量，表示每次搜索后返回的块的数量的上限。
    - 设置检索参数以优化搜索结果，支持如下三类检索模式
        - 文本检索 ：主要基于关键词匹配，可以调整文本检索的权重及匹配模式。
        - 向量检索 ：主要通过语义进行匹配，设置参数如检索权重、返回数量和候选数量。
        - 混合检索：结合了文本检索和向量检索的优点，灵活配置两者的权重
![功能图片69.png](https://static.cwoa.net/a3e79da66d67424998b1c7dc94584a11.png)
1.  知识库检索：使用Elasticsearch数据库，基于倒排索引实现毫秒级响应，支持复杂查询（如全文搜索、模糊匹配、范围查询）
2.  最后，还支持对知识库检索结果进行重排序，以提升搜索结果的相关性

**知识库顶部菜单**

知识库顶部菜单栏增加“自定义文本”按钮，可进行自定义文本设置。
![功能图片70.png](https://static.cwoa.net/d0b66dbc35794418980647684aeccf70.png)
## 智能体

在OpsPilot里面，智能体是指应用机器人的能力，包括可以调用什么知识库、使用什么工具等，智能体创建完成后，可以被应用所使用。

### 智能体列表

- 智能体列表以卡片的形式展示用户有权限的技能，普通用户可以查看/操作自己所在组织的所有技能；超管可以查看/操作所有的技能。
- 每个智能体卡片左下角展示使用的LLM大模型和类别tab，右下角展示分组和所有者，方便选取智能体、通过类别检索智能体和分组别溯源管理。
![功能图片71.png](https://static.cwoa.net/f487859e10ca4b6daadefa0d341bd369.png)
### ****智能体创建/编辑****

- 可以创建空白智能体，也可以直接选择内置好的模板创建智能体。根据需求设定智能体的逻辑和流程，以确保机器人能够有效地响应用户请求。
- 智能体目前分为四类：
    - **知识问答智能体：**结合检索与生成技术，能够从外部知识库中检索相关信息，并生成精准的问答内容，适用于开放领域的动态知识问答。
    - **基础工具智能体：**将推理与行动结合，通过逻辑推导和工具调用来解决任务，适合需要实时交互与多步骤操作的场景。
    - **计划分解智能体：**将任务分解为多个可执行步骤，逐步完成复杂任务，适合需要层次化规划的情境。
    - **复杂决策智能体：**通过树搜索算法，模拟多步决策路径，适用于高复杂度、高不确定性的决策场景。

**创建空白智能体：**选择类型后，填写名称、分组、简介这三个基本信息，进一步的配置等新建完成后再进行。
![功能图片72.png](https://static.cwoa.net/c376ddd742e34ac89fb118b168aea191.png)
**从模板新建智能体:**根据类型和用途，配置好各项参数，包括调用知识库、工具和提示词等等。

点击【使用该模板】即新建成功，进入该智能体可看到已经配置好基本信息，只需调整分组、知识库等。
![功能图片73.png](https://static.cwoa.net/fd336af615c94b06a991249c90ab0dec.png)
![功能图片74.png](https://static.cwoa.net/e2e3b438abbf41b09b1bba5ecd2d3425.png)
![功能图片75.png](https://static.cwoa.net/6ea51e28e6b34acf96d7770b0da64797.png)

### 智能体设置

#### ****基本信息****

可以对智能体的基本信息进行配置
![功能图片76.png](https://static.cwoa.net/a1fa1e5a150e4882a1d523e996717dd0.png)
- 基本信息：名称/分组/简介,可以进行修改
    - **LLM模型：**支持选择内置的LLM大模型，大模型可以根据在知识库搜索到的结果，进行再次总结，并且回复。
    - **LLM的温度参数：**默认为0.7，用于控制文本生成的随机性和创造性；低温度（比如0.2）会生成更确定的结果，而高温度（比如0.9）则会增加文本的多样性和随机性。通过调节温度，用户可以根据需求平衡生成内容的准确性和创新性。
    - **提示：**可以输入相关的提示语，引导模型生成特定的回复，通过提供上下文或问题以调节输出内容的方向和质量。

#### ****聊天增强****

对于**知识问答智能体**，聊天增强包括【聊天历史】，【RAG】。聊天历史可以帮助机器人理解上下文，并增强回复的相关性和连贯性。RAG开启后先从知识库中检索相关信息，然后使用生成模型产生上下文相关的回答。适用于企业知识库查询，专业问答等。
![功能图片77.png](https://static.cwoa.net/b160d4e8df1541edaaf1e6456ef1c395.png)
对于**基础工具智能体**，聊天增强包括【聊天历史】，【RAG】，【工具】。聊天历史可以帮助机器人理解上下文，并增强回复的相关性和连贯性。RAG开启后先从知识库中检索相关信息，然后使用生成模型产生上下文相关的回答。工具给智能体获取外部数据或者执行操作的能力。适用于数据分析，自动化办公，问答增强等。
![功能图片78.png](https://static.cwoa.net/cbd50077a03e4949a3beb4fdf214da0b.png)
对于**计划分解智能体**，聊天增强包括【聊天历史】，【RAG】。聊天历史可以帮助机器人理解上下文，并增强回复的相关性和连贯性。RAG开启后先从知识库中检索相关信息，然后使用生成模型产生上下文相关的回答。适用于项目管理，产品研发，日常规划等。
![功能图片79.png](https://static.cwoa.net/4231564cea364a238fc360028b84c1cc.png)
对于**复杂决策智能体**，聊天增强包括【聊天历史】，【RAG】。聊天历史可以帮助机器人理解上下文，并增强回复的相关性和连贯性。RAG开启后先从知识库中检索相关信息，然后使用生成模型产生上下文相关的回答。适用于投资分析，战略规划等。
![功能图片80.png](https://static.cwoa.net/37a33eeb0abe44a4ae2571a3a3143d56.png)
- **聊天历史**：默认数量是10，聊天历史数量指的是系用户与机器人之间互动的对话轮次或消息总数。这一数量可以帮助机器人理解上下文，并增强回复的相关性和连贯性。
- **RAG**：RAG是一种将信息检索与生成模型结合的架构，先从知识库中检索相关信息，然后使用生成模型产生上下文相关的回答。
    - **RAG来源**：开启后，在对话时可以显示引用的知识来源
    - **知识库**：支持选择**同一分组下的知识库**作为知识来源，每个知识库**支持调整阈值**，阈值通常表示知识库中匹配答案的相关性要求，数值越高代表匹配结果需要与用户问题更加相关，**只有高相关的答案才会被选取出来作为来源**。
    - 添加知识库后点击它的编辑按钮，可直接跳转到该知识库进行修改。
- **工具**：给智能体获取外部数据或者执行操作的能力，可以选取多个工具，具体调用哪个工具，由大模型自主决定。
    - 支持在此处**给该工具设置的变量赋值**，实现传递参数设置控制，比如通过变更jenkins_url、jenkins_username 和 jenkins_password 这三个变量的值，来连接到不同的 Jenkins 服务并进行操作。

#### ****技能测试****

当基础信息和对话增强设置好后，可以通过与机器人对话的方式，测试一下效果。

### 智能体规则

- 支持设定规则，以便为指定人员和用户提供个性化的服务。目前内置的规则设定为：
    - 1、设定规则触发条件：
        - 支持多条件，使用连接词AND、OR控制条件之间的关系；
        - 通过使用途径（如企业微信）+特定内容（用户与应用的聊天中的关键词）触发下面的动作
    - 2、动作：为触发规则的人群使用特定的的提示词（prompt）和特定知识库
![功能图片81.png](https://static.cwoa.net/0d217937cc0b4e549c6d256c1e27b901.png)
### 智能体日志

可管理查看调用当前智能体的调用时间、客户端、状态和消息内容。
![功能图片82.png](https://static.cwoa.net/4fb54c39b49d4af4a86d8d0349a94f75.png)

### 智能体API调用

提供智能体的对外接口，用户可以调用接口实现智能体的使用。
![功能图片83.png](https://static.cwoa.net/8644653c0b1b4feaaeaf35b71c91d93a.png)
## 工作室

工作室模块主要用于对应用机器人进行管理，在这里可以对应用进行上线、下线，回复规则与对话记录管理等操作。为了适用不同的场景，比如服务台知识库问答，运维专门问答等场景，可以设置不同的应用。

### 应用机器人列表

应用机器人列表展示了所有创建的应用，支持对应用进行上线/下线。上线的应用可以正常运行，通过配置前端对话框响应与其交互的请求；下线的应用则停止工作，不再响应请求。
![功能图片84.png](https://static.cwoa.net/3671a9485a6f4acc82b6f9ddfaff375c.png)
### 基础配置

对每个应用机器人进行基础模型和LLM技能的配置，让该应用具备对应能力

- **基本信息**
    - **描述：**针对每个应用机器人，可以设置其名称、描述等基本信息。基本信息有助于理解应用机器人的作用和状态，并且可以作为识别和搜索的条件。
    - **模型**：为该应用选择使用的Rasa小模型，进行简单问题的过滤和闭环，减少大模型的API调用和token消耗。
    - **副本数量：**表示为AI应用运行的Pilot实例数量，通过增加实例数量提升应用的容错性和可用性，默认为1
- **技能**：为该应用机器人选择智能体，比如WeOps问答等等，智能体是在基础模型上增加的技能包，可以提供更精细、更高级的语言理解和任务执行。只能选择一个。
- **渠道：**为对外提供应用的使用渠道，在【通知】已经配置好，配置好且开启的渠道可以在这里进行勾选。
- **保存和上线：**应用都设置好后，可以进行发布和上线，上线后，可以通过选择的渠道方式和应用进行对话。
![功能图片85.png](https://static.cwoa.net/f22faf6199cc4163bac44191902e4761.png)
### 通知

为了满足使用者多渠道的使用需求，应用支持设置与用户进行交互的通道，比如Web网站、企业微信、钉钉、公众号等通道配置，可以使应用更好地为用户提供服务。OpsPilot内置了多种消息通道，让应用能够与用户进行交流，支持的消息通道包含：

#### ****企业微信应用****

- **参数配置**：需要选择类型填写配置参数，所有参数需在企业微信的后台管理中查询到。
![功能图片86.png](https://static.cwoa.net/e73da737236445c297b51f4d047b9955.png)
- **1.**在企业微信中**创建应用**
    - 在网页中登录企业微信后台管理：https://work.weixin.qq.com/wework_admin
    - 在应用管理中找到”自建“，创建新的应用
![功能图片87.png](https://static.cwoa.net/419c8ef760ab41178b5ca5dc2f85143b.png)
- **2.**根据需求，**自定义**机器人的logo、命名、介绍，选择本企业微信中可见本应用的成员。
![功能图片88.png](https://static.cwoa.net/53a181bbd94b4b69be2e329b7d03309a.png)
- **3.获取参数——agent id、secret**
    - AgentId即**agent id**，直接复制粘贴即可
    - secret获取
        - 点击查看后，在弹出的弹窗中点击发送
        - 企业微信软件中收到该消息，在企业微信团队的聊天框中获取
![功能图片89.png](https://static.cwoa.net/d52b54445a2e4f409aa87bf1de6d658b.png)
- 4.参数获取——**corp id**
    - 在”我的企业“中，找到企业ID。企业ID即**corp id**
![功能图片90.png](https://static.cwoa.net/0a9aa85d9b7f47eb9d353e65b823c92f.png)
- 5.参数获取——**token**、**aes key**
    - 回到”应用管理-应用-自建-刚刚建立的应用“中
    - 在该应用的详情页找到”功能- 设置API接收”即可生成token和aes Key
    - URL一栏填入：https://ops-pilot.canway.net/opspilot/studio，实现机器人和企业微信应用的双向交流
    - **token**\=Token 、**aes key**\=EncodingAESKey，点击随机生成保存即可。
![功能图片91.png](https://static.cwoa.net/8f1e9d53cc1c4be4ae3b42785ed59632.png)
#### 钉钉

- 1.需要填写参数如下
![功能图片92.png](https://static.cwoa.net/a4c00b8b93d74cfa8db0bf2d681d0559.png)
- 2.创建应用以提供与机器人的交流接口
    - 进入钉钉的开发者后台，网址：https://open-dev.dingtalk.com/
    - 登陆后，进入“应用开发”页，选择创建“H5微应用”，填写基础信息
![功能图片93.png](https://static.cwoa.net/b79e7b03570240718136677ea2e02abc.png)
- 3.参数获取client id、client secret

创建完成后，在“凭证与基础信息”中，可获得Client ID（即client id）、Client Secret （即client secret）
![功能图片94.png](https://static.cwoa.net/398ada6323f44a219ceb06ff351c3383.png)
- 4.参数enable eventbus
    - 此参数一般情况下默认为false，即仅与大模型AI进行交流，不需要更改设置。
    - 在有进一步需求的情况下设置为true。
        - 你希望 **接收钉钉的事件** 并自动处理（如智能回复、自动审批）。
        - 你的大模型应用 **需要监听用户消息、审批流、考勤等行为** 并基于此做出智能响应。

#### Web

可以通过嵌入WebChat组件，在网页中与应用进行交流

#### 公众号

- 1.需要填写参数如下：appid、secret、token、aes key
![功能图片95.png](https://static.cwoa.net/5befdbdde6ab44f1a5b38151f1ccb36c.png)
- 2.登录服务号后台（企业公众号）
    - 访问微信公众平台：https://mp.weixin.qq.com/，登录企业账号
    - 若无服务号，根据企业自身信息进行填写注册后再操作
![功能图片96.png](https://static.cwoa.net/38561709839a44b3ad56a6412f860c15.png)
- 3.参数获取：appid、secret
    - 找到”设置与开发“-“开发接口管理”-"基本配置"
    - 开发者ID(AppID)即appid，开发者密码(AppSecret)即secret
![功能图片97.png](https://static.cwoa.net/6e3679c2fed64ca4b2ae3f6d75ab0f01.png)
- 4.参数获取：token、aes key
    - 找到”账户开发信息“下方的”服务器配置“
    - 未启用服务器配置——修改配置
        - URL填入我们的OpsPilot网址：https://opspilot-dev.deadgay.cn/
        - token自定义一串英文/数字
        - 随机生成AESKEY
        - 点击”启用“即完成配置
 ![功能图片98.png](https://static.cwoa.net/836e7f7cda0a488eb5feface792a8dd9.png)
- 已启用配置：直接获取：令牌(Token)即token、消息加解密密钥 (EncodingAESKey)即aes key
![功能图片99.png](https://static.cwoa.net/dfd9b84a8c3043ef9005979d14c311a8.png)
### 应用日志

对话记录里面记录了应用与用户的对话记录，可以用于对话记录的审计等场景，点击详情可以查看每轮对话的细节。目前同一个渠道的同一个用户一天内的所有对话会聚合成一条记录。
![功能图片100.png](https://static.cwoa.net/6959a0c9392f46ecb447d9d3a05b8bce.png)
![功能图片101.png](https://static.cwoa.net/9df92e138edd49d29c9966e09bca8d09.png)
### 应用统计

应用的运营统计，用于分析用户对应用的使用和调用情况。
![功能图片102.png](https://static.cwoa.net/5a014e70a40742c1bebaba27416f14c3.png)
## 设置

### 管理凭据

为了控制资源使用量，控制成本，支持对各个模块设置定额（包括知识库文件大小、Skil数量、Bot数量、Token量），超过设置的定额则无法继续使用。超级管理员可以在此界面为不同角色设置不同的配额。
![功能图片103.png](https://static.cwoa.net/ea26a0f655234c2ca7470e1e33e2b086.png)
- 针对分组：
    - **目标**：选择此次配置配额方案应用到哪些分组上；
    - **规则**：
        - 统一配额：组织内每个个体均适用的配额；
        - 共享配额：给定一个较大的配额，组织内个体共享此配额，不限定个人使用的配额大小；
    - **机器人、技能**：控制可以建立的机器人、技能的数量，添加的数量超过当前设置的数字；
    - **知识库**：限制可以上传到知识库的文件的大小，所有知识库共享此额度。单位有MB、GB，当上传资源的总大小超过额度，将会报错；
    - **Token数**：控制当前对象对各个大模型的使用的额度，未分配到额度的大模型不可使用，每个大模型使用时消耗Token数，使用完额度之后不可再使用，需要续费等操作。支持对多个大模型设置Token。

### 我的凭据

- 显示我的总配额使用量,若有针对个人的配额管理方案则显示个人配额；
- 若无，则跟随当前所在分组的配额管理方案，会随着分组的改变而改变。
- 当配额不足时，可以联系管理员申请增加。
![功能图片104.png](https://static.cwoa.net/91dd0686d90f428ab538af66e9bf55ad.png)
### API密钥

用于身份验证和授权的安全凭证，允许用户访问特定的 API 服务。为了防止API滥用，请保护你的API密钥。
![功能图片105.png](https://static.cwoa.net/31aefb291d7e42dcb126eceb5e0317f1.png)
# ****API调用说明****

## 技能API调用

### API调用说明[​](https://wedoc.canway.net/weops-lab/opspilot/function-introduction"%20\l%20"api%E8%B0%83%E7%94%A8%E8%AF%B4%E6%98%8E-1)

提供技能的对外接口，用户可以调用接口实现技能的使用。

### API调用示例[​](https://wedoc.canway.net/weops-lab/opspilot/function-introduction"%20\l%20"api%E8%B0%83%E7%94%A8%E7%A4%BA%E4%BE%8B)

#### 获取技能列表[​](https://wedoc.canway.net/weops-lab/opspilot/function-introduction"%20\l%20"1%E8%8E%B7%E5%8F%96%E6%8A%80%E8%83%BD%E5%88%97%E8%A1%A8)

**请求参数**

| **参数名称** | **是否必须** | **示例** |
| --- | --- | --- |
| name | 否   | 技能1 |
| page_size | 是   | 10  |
| page | 是   | 1   |

**返回数据**

{

"result": true,

"code": "20000",

"message": "success",

"data": {

"count": 1,

"items": \[

{

"id": 10,

"team_name": \[

"游客"

\],

"created_by": "1406489435@qq.com",

"updated_by": "1406489435@qq.com",

"name": "你好hello",

"skill_id": null,

"skill_prompt": null,

"enable_conversation_history": false,

"conversation_window_size": 10,

"enable_rag": false,

"enable_rag_knowledge_source": false,

"rag_score_threshold": 0.7,

"introduction": "56",

"team": \[

"8bb5627e-3a25-45b9-850b-62d570a9282b"

\],

"llm_model": null,

"knowledge_base": \[\]

}

\]

}

}

字段说明如下:

- result: true 指示请求是否成功。
- code: "20000" 状态码，表示请求成功。
- message: "success" 请求结果的描述信息。
- data: 数据对象，包含具体的返回数据。
- count: 1 返回的条目数量。
- items: \[...\] 数据条目的数组，包含具体的记录信息。
- id: 10 唯一标识符，表示该对象的 ID。
- team_name: \["游客"\] 团队名称的数组，表示该对象所属的团队。
- created_by: "1406489435@qq.com" 创建该记录的用户的邮箱地址。
- updated_by: "1406489435@qq.com" 最后更新该记录的用户的邮箱地址。
- name: "你好hello" 名称。
- skill_id: null 技能标识符，当前为空，表示没有关联技能。
- skill_prompt: null 技能提示，当前为空，表示没有关联技能提示。
- enable_conversation_history: false 布尔值，指示是否启用对话历史。
- conversation_window_size: 10 指定对话窗口的大小，即可回顾的聊天记录条数。
- enable_rag: false 布尔值，指示是否启用 RAG（Retrieval-Augmented Generation）。
- enable_rag_knowledge_source: false 布尔值，指示是否启用 RAG 知识来源。
- rag_score_threshold: 0.7 RAG 分数阈值，决定哪些知识被纳入对话中。
- introduction: "56" 记录的简介信息。
- team: \["8bb5627e-3a25-45b9-850b-62d570a9282b"\] 团队的唯一标识 ID，用于关联团队。
- llm_model: null 大语言模型的标识符，当前为空。
- knowledge_base: \[\] 知识库的数组，当前为空，表示没有关联的知识内容。

#### 技能测试[​](https://wedoc.canway.net/weops-lab/opspilot/function-introduction"%20\l%20"2%E6%8A%80%E8%83%BD%E6%B5%8B%E8%AF%95)

**请求参数**

Headers：

| **参数名称** | **是否必须** | **示例** |
| --- | --- | --- |
| Content-Type | 是 | application/json   |

Query：

| **参数名称** | **是否必须** | **示例** |
| --- | --- | --- |
| name | 否   | 技能1 |
| page_size | 是   | 10  |
| page | 是   | 1   |

Body:

{

"user_message": "你好", // 用户消息

"llm_model": 1, // 大模型ID

"skill_prompt": "abc", // Prompt

"enable_rag": true, // 是否启用RAG

"enable_rag_knowledge_source": true, // 是否显示RAG知识来源

"rag_score_threshold": \[{"knowledge_base": 1, "score": 0.7}\], // RAG分数阈值

"chat_history": \[{"event": "user", "text": "abc"}, {"event": "bot", "text": "ab"}\], // 对话历史

"conversation_window_size": 10, // 对话窗口大小

"temperature": 0.7,

"show_think": true, // 展示think内容

"tools": \["shell", "duckduckgo-search", "prometheus-search"\] // 目前只支持这三种

}

字段说明：

- user_message: "你好" 用户消息，表示传递给大模型的信息。
- llm_model: 1 大模型ID，表示选择的大语言模型的标识符。
- skill_prompt: "abc" Prompt，用于引导大语言模型的提示信息。
- enable_rag: true 布尔值，指示是否启用RAG（Retrieval-Augmented Generation）。
- enable_rag_knowledge_source: true 布尔值，指示是否显示RAG知识来源。
- rag_score_threshold: \[{"knowledge_base": 1, "score": 0.7}\] RAG分数阈值，包含知识库ID和分数的数组。
- chat_history: \[{"event": "user", "text": "abc"}, {"event": "bot", "text": "ab"}\] 对话历史，包含用户和机器人的聊天记录。
- conversation_window_size: 10 对话窗口大小，即可回顾的聊天记录条数。
- temperature: 0.7 大语言模型生成文本时的温度参数，控制输出的随机性。
- show_think: true 布尔值，指示是否展示think内容,\`false\`时不展示思考过程。
- tools: \["shell", "duckduckgo-search", "prometheus-search"\] 工具的数组，目前支持shell, duckduckgo-search, prometheus-search。

**返回数据**

{

"result": true,

"code": "20000",

"message": "success",

"data": {

"count": 1,

"items": \[

{

"id": 10,

"team_name": \[

"游客"

\],

"created_by": "1406489435@qq.com",

"updated_by": "1406489435@qq.com",

"name": "你好hello",

"skill_id": null,

"skill_prompt": null,

"enable_conversation_history": false,

"conversation_window_size": 10,

"enable_rag": false,

"enable_rag_knowledge_source": false,

"rag_score_threshold": 0.7,

"introduction": "56",

"team": \[

"8bb5627e-3a25-45b9-850b-62d570a9282b"

\],

"llm_model": null,

"knowledge_base": \[\]

}

\]

}

}

字段说明

- result: true 指示请求是否成功。
- code: "20000" 状态码，表示请求成功。
- message: "success" 请求结果的描述信息。
- data: 数据对象，包含具体的返回数据。
- count: 1 返回的条目数量。
- items: \[...\] 数据条目的数组，包含具体的记录信息。
- id: 10 唯一标识符，用于标识该数据对象。
- team_name: \["游客"\] 团队名称的数组，表示该记录所属的团队是“游客”。
- created_by: "1406489435@qq.com" 创建用户的邮箱地址。
- updated_by: "1406489435@qq.com" 最后更新该记录的用户的邮箱地址。
- name: "你好hello" 名称，表明这是一个对话主题或标识。
- skill_id: null 技能标识符，当前为空，表示此记录并未指定任何技能。
- skill_prompt: null 技能提示，当前为空，表示没有为该记录提供技能提示。
- enable_conversation_history: false 布尔值，指示是否启用对话历史记录。
- conversation_window_size: 10 对话窗口大小，即可回顾的聊天记录条数。
- enable_rag: false 布尔值，指示是否启用 RAG（Retrieval-Augmented Generation）。
- enable_rag_knowledge_source: false 布尔值，指示是否启用 RAG 知识来源。
- rag_score_threshold: 0.7 RAG 分数阈值，决定哪些知识会被纳入对话中。
- introduction: "56" 记录的简介信息。
- team: \["8bb5627e-3a25-45b9-850b-62d570a9282b"\] 团队的唯一标识 ID，用于关联团队。
- llm_model: null 大语言模型的标识符，当前为空。
- knowledge_base: \[\] 知识库的数组，当前为空，表示没有关联的知识内容。

#### 技能设置保存[​](https://wedoc.canway.net/weops-lab/opspilot/function-introduction"%20\l%20"3%E6%8A%80%E8%83%BD%E8%AE%BE%E7%BD%AE%E4%BF%9D%E5%AD%98)

**请求参数**

路径参数：

| **参数名称** | **示例** | **备注** |
| --- | --- | --- |
| id  | 1   |     |

Headers：

| **参数名称** | **参数值** | **是否必须** |
| --- | --- | --- |
| Content-Type | application/json | 是   |

Query：

| **参数名称** | **是否必须** | **示例** |
| --- | --- | --- |
| name | 否   | 技能1 |
| page_size | 是   | 10  |
| page | 是   | 1   |

Body:

{  
"name": "abc",  
"team": \["11", "22"\],  
"introduction": "introduction", // 用户消息  
"llm_model": 1, // 大模型ID  
"skill_prompt": "abc", // Prompt  
"enable_conversation_history": true,  
"enable_rag": true, // 是否启用RAG  
"enable_rag_knowledge_source": true, // 是否显示RAG知识来源  
"rag_score_threshold": \[{"knowledge_base": 1, "score": 0.7}\], // RAG分数阈值  
"temperature": 0.7,  
"conversation_window_size": 10 // 对话窗口大小  
}

**返回数据**

{  
"result": true  
}

## 知识库API调用

### API调用说明[​](https://wedoc.canway.net/weops-lab/opspilot/function-introduction"%20\l%20"api%E8%B0%83%E7%94%A8%E8%AF%B4%E6%98%8E-2)

提供知识库的对外接口，用户可以基于关键字进行检索相关知识库内容

### API调用示例[​](https://wedoc.canway.net/weops-lab/opspilot/function-introduction"%20\l%20"api%E8%B0%83%E7%94%A8%E7%A4%BA%E4%BE%8B-1)

#### 1.查询知识库[​](https://wedoc.canway.net/weops-lab/opspilot/function-introduction"%20\l%20"1%E6%9F%A5%E8%AF%A2%E7%9F%A5%E8%AF%86%E5%BA%93)

**请求参数**

| **参数名称** | **是否必须** | **示例** |
| --- | --- | --- |
| name | 否   | 12  |

**输出示例**

{

"result": true,

"data": \[

{

"id": 1,

"team_name": \[

"admin"

\],

"created_at": "2024-09-04 15:52:21",

"updated_at": "2024-09-04 15:52:21",

"created_by": "admin",

"updated_by": "",

"name": "知识库测试",

"introduction": "abcjde",

"team": "2135b2b5-cbb4-4aea-8350-7329dcb6671a",

"enable_vector_search": true,

"vector_search_weight": 0.1,

"enable_text_search": true,

"text_search_weight": 0.9,

"enable_rerank": false,

"embed_model": 2,

"rerank_model": 1

}

\]

}

字段说明如下：

- result: \`true\` 请求是否成功，\`true\` 为成功。
- data: \`\[...\]\` 数据条目的数组，包含具体的记录信息。
- id: \`1\` 唯一标识符，表示该对象的 ID。
- team_name: \`\["admin"\]\` 团队名称的数组，表示该对象所属的团队。
- created_at: \`"2024-09-04 15:52:21"\` 创建时间。
- updated_at: \`"2024-09-04 15:52:21"\` 最后更新时间。
- created_by: \`"admin"\` 创建该记录的用户。
- updated_by: \`""\` 最后更新该记录的用户。
- name: \`"知识库测试"\` 知识库名称。
- introduction: \`"abcjde"\` 知识库简介。
- team: \`"2135b2b5-cbb4-4aea-8350-7329dcb6671a"\` 团队的唯一标识 ID，用于关联团队。
- enable_vector_search: \`true\` 布尔值，指示是否启用向量搜索。
- vector_search_weight: \`0.1\` 向量搜索权重，取值0.0~1.0。
- enable_text_search: \`true\` 布尔值，指示是否启用文本搜索。
- text_search_weight: \`0.9\` 文本搜索权重，取值0.0~1.0。
- enable_rerank: \`false\` 布尔值，指示是否启用重新排序。
- embed_model: \`2\` 嵌入模型的标识符。
- rerank_model: \`1\` 重新排序模型的标识符。

#### 2\. 查询知识库文章

**请求参数**

Query：

|     |     |     |     |
| --- | --- | --- | --- |
| 参数名称 | 是否必须 | 示例  | 备注  |
| knowledge_base_id | 是   | 1   | 知识库ID |
| name | 否   | aa  |     |
| page | 是   | 1   | 当前页码 |
| page_size | 是   | 1   | 每页条数 |
| knowledge_source_type | 是   | file | 知识来源类型，file, web_page, manual |
| train_status | 否   | 0   | 0：正在训练，1: 训练完成，2： 训练失败 |

**返回数据**

{

"result": true,

"data": {

"count": 11,

"items": \[

{

"name": "文章1.doc",

"status": "Training",

"chunk_size": 11,

"created_at": "2021-12-12 12:12:12",

"created_by": "admin"

}

\]

}

}

- count: \`11\` 数据条目数量。
- items: \`\[...\]\` 数据条目的数组，包含具体的记录信息。
- name: \`"文章1.doc"\` 文章名称。
- status: \`"Training"\` 文章状态。
- chunk_size: \`11\` 文章分块大小。
- created_at: \`"2021-12-12 12:12:12"\` 文章创建时间。
- created_by: \`"admin"\` 创建该文章的用户。

#### 3\. 文件上传

**请求参数**

Headers：

|     |     |     |     |     |
| --- | --- | --- | --- | --- |
| 参数名称 | 参数值 | 是否必须 | 示例  | 备注  |
| Content-Type | application/json | 是   |     |     |

Query：

|     |     |     |     |
| --- | --- | --- | --- |
| 参数名称 | 是否必须 | 示例  | 备注  |
| knowledge_base_id | 是   | 1   | 知识库ID |
| name | 否   | aa  |     |
| page | 是   | 1   | 当前页码 |
| page_size | 是   | 1   | 每页条数 |
| source_type | 是   | file | 知识来源类型，file, web_page, manual |

Body:

{

"knowledge_base_id": 1,

"files": \[\] // 文件列表，以file的形式传参，多选

}

**返回数据**

{

"result": true,

"data": \[1, 2, 3, 4\] // 文件的ID列表

}

**字段说明**

- knowledge_base_id: 1 知识库的唯一标识符，用于与具体知识库关联。
- files: \[\] 文件列表，以 file 的形式传参，可以多选上传。
- result: \`true\` 请求是否成功。
- data: \`\[1, 2, 3, 4\]\` 文件的ID列表。

#### 4\. 新增网页

**请求参数**

Headers：

|     |     |     |     |     |
| --- | --- | --- | --- | --- |
| 参数名称 | 参数值 | 是否必须 | 示例  | 备注  |
| Content-Type | application/json | 是   |     |     |

Query：

|     |     |     |     |
| --- | --- | --- | --- |
| 参数名称 | 是否必须 | 示例  | 备注  |
| knowledge_base_id | 是   | 1   | 知识库ID |
| name | 否   | aa  |     |
| page | 是   | 1   | 当前页码 |
| page_size | 是   | 1   | 每页条数 |
| source_type | 是   | file | 知识来源类型，file, web_page, manual |

Body:

{

"knowledge_base_id": 1,

"name": "abcd",

"url": "http://wewewe.wewe",

"max_depth": 1

}

**返回数据**

{

"result": true,

"data": 1 // 网页知识库的ID

}

**字段说明**

- knowledge_base_id: 1 知识库的唯一标识符，用于与具体知识库关联。
- name: "abcd" 新增网页数据的名称。
- url: "http://wewewe.wewe" 网页地址的 URL。
- max_depth: 1 网页爬取的最大深度，限制爬取范围。
- result: \`true\` 请求是否成功。
- data: \`1\` 新增网页的ID。

#### 5\. 新增自定义内容

**请求参数**

Headers：

|     |     |     |     |     |
| --- | --- | --- | --- | --- |
| 参数名称 | 参数值 | 是否必须 | 示例  | 备注  |
| Content-Type | application/json | 是   |     |     |

Query：

|     |     |     |     |
| --- | --- | --- | --- |
| 参数名称 | 是否必须 | 示例  | 备注  |
| knowledge_base_id | 是   | 1   | 知识库ID |
| name | 否   | aa  |     |
| page | 是   | 1   | 当前页码 |
| page_size | 是   | 1   | 每页条数 |
| source_type | 是   | file | 知识来源类型，file, web_page, manual |

Body:

{

"knowledge_base_id": 1,

"name": "abcd",

"content": "abcd"

}

**返回数据**

{

"result": true,

"data": 1 // 自定义内容的ID

}

**字段说明**

- knowledge_base_id: 1 知识库的唯一标识符，用于与具体知识库关联。
- name: "abcd" 自定义内容的名称。
- content: "abcd" 自定义添加的内容，文本记录。
- result: \`true\` 请求是否成功。
- data: \`1\` 自定义内容的ID。

#### 6\. 知识库文章批量训练

**请求参数**

Headers：

|     |     |     |
| --- | --- | --- |
| 参数名称 | 参数值 | 是否必须 |
| Content-Type | application/json | 是   |

Query：

|     |     |     |     |
| --- | --- | --- | --- |
| 参数名称 | 是否必须 | 示例  | 备注  |
| knowledge_base_id | 是   | 1   | 知识库ID |
| name | 否   | aa  |     |
| page | 是   | 1   | 当前页码 |
| page_size | 是   | 1   | 每页条数 |
| source_type | 是   | file | 知识来源类型，file, web_page, manual |

Body:

{

"knowledge_document_ids": \[

1,

2,

3

\]

}

**返回数据**

{

"result": true

}

**字段说明**

- knowledge_document_ids: \[1, 2, 3\] 知识文档的 ID 列表，指定要训练的文档。
- result: \`true\` 请求是否成功。

#### 7\. 知识库文章Testing

**请求参数**

Headers：

|     |     |     |
| --- | --- | --- |
| 参数名称 | 参数值 | 是否必须 |
| Content-Type | application/json | 是   |

Body:

{

"knowledge_base_id": 1,

"query": "",

"embed_model": 1, // 所选的模型

"enable_rerank": true, // 启用rerank

"rerank_model": 1, // 所选的rerank_model

"enable_text_search": true,

"text_search_weight": 0.9, // 文本权重

"enable_vector_search": true,

"vector_search_weight": 0.1, // 混合权重

"rag_k": 50, // 返回结果数量

"rag_num_candidates": 1000, //候选数量

"text_search_mode": "match" // match 模糊，match_phrase 完整匹配

}

**返回数据**

{

"result": true,

"data": \[

{

"id": 1,

"name": "acb",

"knowledge_source_type": "file",

"created_by": "admin",

"created_at": "2020-12-12 12:21:12",

"content": "",

"score": 1000,

}

\]

}

**字段说明**

- knowledge_base_id: 1 知识库的唯一标识符，用于与具体知识库关联。
- query: "" 查询关键字。
- embed_model: 1 指定特定嵌入模型的 ID。
- enable_rerank: true 是否启用重排序功能。
- rerank_model: 1 重排序启用时所选的模型 ID。
- enable_text_search: true 是否启用文本搜索功能。
- text_search_weight: 0.9 文本搜索的权重。
- enable_vector_search: true 是否启用向量搜索功能。
- vector_search_weight: 0.1 向量搜索的权重。
- rag_k: 50 返回结果的数量。
- rag_num_candidates: 1000 候选结果数量。
- text_search_mode: "match" 文本搜索模式，match 表示模糊匹配，match_phrase 表示完整匹配。
- result: \`true\` 请求是否成功。
- data: \`\[...\]\` 数据条目的数组，包含具体的记录信息。
- id: \`1\` 唯一标识符，表示该对象的 ID。
- name: \`"acb"\` 文章名称。
- knowledge_source_type: \`"file"\` 文章来源类型。
- created_by: \`"admin"\` 创建该记录的用户。
- created_at: \`"2020-12-12 12:21:12"\` 创建时间。
- content: \`""\` 文章内容。
- score: \`1000\` 文章评分。

#### 8\. 知识库文章块删除

**请求参数**

路径参数：

|     |     |     |
| --- | --- | --- |
| 参数名称 | 示例  | 备注  |
| id  | 1   | 文档ID |

Headers：

|     |     |     |     |     |
| --- | --- | --- | --- | --- |
| 参数名称 | 参数值 | 是否必须 | 示例  | 备注  |
| Content-Type | application/json | 是   |     |     |

Query：

|     |     |     |     |
| --- | --- | --- | --- |
| 参数名称 | 是否必须 | 示例  | 备注  |
| search_text | 否   | 123 | 查询文本 |

Body:

{

"chunk_id": "35196cd0-bda7-49be-91f0-8b2983109685"

}

**返回数据**

{

"result": true

}

**字段说明**

- chunk_id: "35196cd0-bda7-49be-91f0-8b2983109685" 要删除的块的唯一标识符。
- result: \`true\` 请求是否成功。

#### 9\. 知识库文章配置调整

**请求参数**

Headers：

|     |     |     |     |     |
| --- | --- | --- | --- | --- |
| 参数名称 | 参数值 | 是否必须 | 示例  | 备注  |
| Content-Type | application/json | 是   |     |     |

Query：

|     |     |     |     |
| --- | --- | --- | --- |
| 参数名称 | 是否必须 | 示例  | 备注  |
| knowledge_base_id | 是   | 1   | 知识库ID |
| name | 否   | aa  |     |
| page | 是   | 1   | 当前页码 |
| page_size | 是   | 1   | 每页条数 |
| source_type | 是   | file | 知识来源类型，file, web_page, manual |

Body:

{

"preview": false, // 是否预览，预览为true的情况下会文档分块返回

"knowledge_source_type": "file", // 本地文件：file, 网络链接： web_page, 自定义文本： manual

"knowledge_document_ids": \[1, 2, 3\], // 文章ID列表，文件上传时是多个，其它两个为单数字列表

"enable_general_parse": true, // 开启分块解析

"general_parse_chunk_size": 256, // 块大小

"general_parse_chunk_overlap": 32, // 分块重叠

"enable_semantic_chunk_parse": true,

"semantic_chunk_parse_embedding_model": 1,

"enable_ocr_parse": true,

"ocr_model": 1,

"enable_excel_parse": true,

"excel_header_row_parse": true,

"excel_full_content_parse": false,

"is_save_only": false // 是否仅保存

}

**返回数据**

{

"result": true,

"data": \[\]

}

**字段说明**

- preview: false 是否预览，预览状态下文档会分块返回。
- knowledge_source_type: "file" 知识源类型，可选值为：本地文件（file）、网络链接（web_page）、自定义文本（manual）。
- knowledge_document_ids: \[1, 2, 3\] 知识文档的 ID 列表，设置训练或配置的文档。
- enable_general_parse: true 是否启用分块解析。
- general_parse_chunk_size: 256 块大小，定义每块的最大字符数。
- general_parse_chunk_overlap: 32 块重叠大小，定义块之间的重叠字符数。
- enable_semantic_chunk_parse: true 是否启用语义分块解析。
- semantic_chunk_parse_embedding_model: 1 使用的语义嵌入模型 ID。
- enable_ocr_parse: true 是否启用 OCR（光学字符识别）解析。
- ocr_model: 1 OCR 模型的 ID。
- enable_excel_parse: true 是否启用 Excel 文件解析。
- excel_header_row_parse: true 是否仅解析 Excel 文件的标题行。
- excel_full_content_parse: false 是否解析 Excel 的完整内容。
- is_save_only: false 是否仅保存配置，false 表示执行配置调整。
- result: \`true\` 请求是否成功。
- data: \`\[\]\` 返回的数据，当前为空。