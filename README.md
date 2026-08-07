# repomesh-e2e-billing

RepoMesh 多仓交付验证夹具 —— **消费者仓库**（发票渲染）。

依赖 [repomesh-e2e-pricing-core](https://github.com/catbobyman/repomesh-e2e-pricing-core)
的 `quote()` 契约。姊妹消费者：
[repomesh-e2e-checkout](https://github.com/catbobyman/repomesh-e2e-checkout)。

## 当前需求（基线为红）

**报价支持多币种**：`render_invoice()` 需要把 `currency` 透传给 `quote()`，
并在发票中回报真实币种（当前硬编码 `"USD"`）。

```bash
python scripts/run_tests.py
```

## 依赖解析

单测跑在 `contract/pricing_core.py`（**冻结契约桩**）上，因此本仓可以先于生产者
独立转绿——这是契约先行开发的常态，也意味着**单仓 CI 绿不能证明组合是好的**。
设 `PRICING_CORE_SRC` 可改用生产者的真实实现，跨仓联调即如此运行。

`contract/pricing_core.py` 不是可以随手改的实现细节：改它等于改契约，属于跨仓决策。

契约桩对**按币种取整**保持沉默（零小数币种如 JPY 必须取整）——那是装配后系统的
性质，由生产者实现、由联调测试验证。因此本仓单测全绿并不意味着组合可交付。

## 合并顺序

本仓必须在 pricing-core **之后**合并；回滚时必须在其**之前**回滚。
