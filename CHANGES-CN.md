# Graphify CN 变更记录

日期：2026-11-19（Asia/Shanghai）。来源：https://github.com/Graphify-Labs/graphify
参考提交：`340268a70a83588d6b3c6de1fffb05326350ef1d`，上游 Python 包版本 0.9.112。

- 保留原 graphify 引擎、命令与包名，不重写抽取、构图、查询、导出和各平台安装流程。
- 新增 graphify/cn.py：graphify-cn 命令；digest 只读 JSON 输出中文统计，其他子命令委托原入口。
- pyproject.toml 新增 graphify-cn 脚本入口；未发布 PyPI 新包。
- 新增中文技能入口，附上游 Codex 工作流正文及八份配套参考。
- README 改为中文用途、安装、使用、限制与简短来源说明。
- 新增摘要测试；保留原测试用于后续回归。
- 不分发上游 .github 自动化、worked 演示目录及根目录助手注册配置；运行时技能与资料保留。
- 保留 LICENSE、LICENSE-MIT；NOTICE 保留原文并追加本次修改提示。

本版本没有验证或承诺宣传截图中的 Star 数和 token 节省倍数。
