# Graphify CN

**把代码、文档和图片里的关系串起来，用中文读懂项目。**

保留 Graphify 的知识图谱引擎：代码结构提取、文档语义提取、图查询、路径追踪、社区发现，以及 HTML、Wiki、Obsidian 等导出。新增中文使用入口和无需模型的图谱速览。

## 能做什么

| 任务 | 使用方式 |
|---|---|
| 看懂代码结构与调用关系 | 本地 AST 提取，再查询图谱 |
| 关联代码、Markdown、PDF 和图片 | 通过助手或配置的模型提取语义关系 |
| 查两个概念怎么联系 | `query`、`path`、`explain` |
| 快速查看已有图谱 | 新增 `digest`，输出中文节点、关系与证据统计 |
| 持续使用同一份项目地图 | 沿用增量更新、导出和 MCP 能力 |

**代码 AST 提取在本地运行。文档、PDF、图片等语义提取需要助手模型或配置的后端，可能产生费用；所用服务是否接收文件内容取决于你的配置。** 本地图谱速览只读 JSON，不调用模型，不发送数据。

## 安装

需要 Python 3.11–3.14 和 Git。推荐使用 uv 的独立工具环境，从这个仓库安装：

```bash
uv tool install "graphifyy[chinese,pdf] @ git+https://github.com/batespaige357-tech/graphify-cn.git"
```

仓库名是 `graphify-cn`；为兼容现有引擎，Python 包名仍为 `graphifyy`，原命令 `graphify` 与新增的 `graphify-cn` 都可用。这里的命令从 GitHub 安装，不表示 PyPI 上另有 `graphify-cn` 包。已有安装时，在独立环境中使用本仓库，避免替换正在工作的项目环境。

只想使用中文助手入口，也可以安装技能；**这一步不安装 Python 引擎**：

```bash
npx skills add batespaige357-tech/graphify-cn --skill graphify-cn
```

## 开始使用

让助手读取指定文件夹，并明确需要代码结构还是文档、图片的语义关系：

```text
用 graphify-cn 为这个项目建立知识图谱。
先看输入类型和已有图谱；用中文解释节点来源、直接提取关系和推断关系。
```

技能包含完整工作流和配套参考。引擎安装完成后，原平台安装流程仍可用，例如 `graphify install --platform codex`；它注册的是原 `graphify` 入口。新增入口在 Codex 中可用 `$graphify-cn`，其他助手按各自技能调用方式使用。

在已有 `graphify-out/graph.json` 的项目根目录查询：

```bash
graphify-cn query "订单与支付的关系" --budget 1500
graphify-cn path "Order" "Payment"
graphify-cn explain "Order"
```

查询、抽取、导出等命令继续使用现有引擎和参数，详细说明见 [Graphify 文档](https://docs.graphify.com)。本版本没有把全部命令输出翻译成中文。

## 中文图谱速览

```bash
graphify-cn digest
graphify-cn digest ./graphify-out/graph.json --top 15 --output ./图谱速览.md
```

输出节点数、关系数、孤立节点、来源字段覆盖、端点缺失的关系、连接较多的节点，以及 `EXTRACTED / INFERRED / AMBIGUOUS / UNKNOWN` 的数量。它保留未知证据，不把缺失标记默认为已验证。

默认输出到终端；`--output` 写入新的 UTF-8 Markdown 文件，已有文件不会覆盖。连接数高不代表业务重要，原图谱标记也不等于重新核实；摘要不能证明图谱仍是最新版本。

## 验证范围

新增摘要的自动化检查覆盖中文与 BOM 输入、证据分类、孤立节点、平行关系、自环、无效数据、输出转义、文件防覆盖和命令转发。上游核心引擎保留，未全面重跑上游测试；PDF、图片语义提取、真实模型调用、MCP 与各平台安装仍需按环境验收。

不承诺固定的 token 节省倍数。效果取决于材料、图谱质量、问题和模型使用方式。验证记录见 [VALIDATION-CN.md](VALIDATION-CN.md)。

## 来源与许可

基于 [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify)，由本仓库维护中文入口与图谱速览。保留上游版权、[Apache-2.0](LICENSE)、[历史 MIT 许可](LICENSE-MIT) 与 [NOTICE](NOTICE)。来源提交和改动见 [CHANGES-CN.md](CHANGES-CN.md)。
