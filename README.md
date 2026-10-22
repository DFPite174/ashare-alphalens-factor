# ashare-alphalens-factor

> **企业级 A 股 Alphalens-cn 因子验证与稳健性评估中台**  
> 专为中国 A 股量化因子研发构建，无缝衔接时点有效性（PIT）财报与日频复权行情，具备 Newey-West / HAC 重叠收益自相关纠偏、分层单调性分析、Benjamini-Hochberg FDR 多重检验及未来函数主动拦截能力。

---

## 核心特性

1. **标准化因子抽象接口**：提供统一的 `(trade_date, symbol)` 因子计算基类与多重索引标准输出。
2. **时点有效性 (PIT) 基本面因子支持**：通过 `asof merge` 严格按照真实公告日（`published_at`）对其财报与日频行情，彻底消除前视偏差。
3. **统计稳健性修正 (HAC / Newey-West)**：消除多日持仓收益交叠产生的自相关性，提供经 Newey-West 修正的真实 t-stat 与 p-value。
4. **单调性与分组收益分析**：计算 Quantile 1 至 Quantile 5 分层年化超额、多空 Spread 与斯皮尔曼单调性得分。
5. **红队未来函数陷阱审查**：内置异常高 IC 与反常因果检测，主动阻断偷窥未来价格与报表的虚假因子。

---

## 快速运行

```bash
# 运行单元测试
pytest tests/ -v
```
