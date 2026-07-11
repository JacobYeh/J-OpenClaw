# Profile Schema v4.0

持仓数据的**单一真值源**（Single Source of Truth）。

## 字段定义

```json
{
  "schema_version": "4.0",
  "as_of": "2026-07-05T16:00:00",
  "last_updated_by": "Jacob",

  "income": {
    "monthly_salary_after_tax": 32000,
    "monthly_bonus_after_tax": 0,
    "annual_other_income": 0,
    "monthly_takehome_avg": 32000
  },

  "expenses": {
    "monthly_housing": 7500,
    "monthly_loan": 0,
    "monthly_insurance": 0,
    "monthly_living": 7500,
    "monthly_other": 0,
    "monthly_mortgage_net": 0,
    "monthly_credit_card_payment": 0
  },

  "holdings": {
    "cash": [
      { "name": "余额宝", "value": 66767.95, "last_update": "2026-07-05", "locked_for_debt": 45000 },
      { "name": "建设银行存款", "value": 5480.00, "last_update": "2026-07-05" }
    ],
    "stocks_etfs": [
      {
        "code": "159655",
        "name": "标普ETF",
        "broker": "中信证券",
        "shares": 4500,
        "avg_cost": 1.9072,
        "last_price": 1.909,
        "last_price_update": "2026-07-05",
        "market_value": 8590.50,
        "pnl": 8.20,
        "pnl_pct": 0.09,
        "dca": true,
        "dca_plan": "周一/四 各 100 股"
      }
    ],
    "funds": [
      {
        "code": "019305",
        "name": "摩根标普500(QDII)C",
        "shares": null,
        "market_value": 4019.84,
        "cost": 3690.00,
        "nav": 1.6314,
        "nav_date": "2026-06-25",
        "dca": false,
        "dca_plan": null,
        "watch": true
      }
    ],
    "pension_022983": {
      "name": "华夏沪深300ETF联接Y",
      "shares": 3333.23,
      "current_value": 6104.81,
      "cost": 6000.15,
      "avg_cost": 1.8001,
      "current_price": 1.8315,
      "last_update": "2026-07-05"
    },
    "gold": {
      "grams": 11.3834,
      "current_price_per_gram": 913.31,
      "market_value": 10396.57,
      "cost": 10471.49,
      "avg_cost_per_gram": 919.89,
      "holding_pnl": -74.92,
      "accumulated_pnl": 1627.84,
      "total_pnl": 1552.92,
      "last_update": "2026-07-05"
    }
  },

  "liabilities": {
    "mortgage": 0,
    "car_loan": 0,
    "credit_card": 0,
    "student_loan": 0,
    "short_term_planned": {
      "total": 45000,
      "plan": [{ "month": "2026-08", "from_yu_e_bao": 45000 }]
    }
  },

  "dca_plans": [...],
  "cashflow_plan": {...},

  "investment_goal": "wealth_accumulation",
  "risk_preference": "balanced",
  "target_allocation": {
    "cn_equity": 20, "us_equity": 35, "hk_equity": 5,
    "bond": 25, "gold": 5, "cash": 10
  }
}
```

## 必填字段 (validator 检查)

- `schema_version` (str) - 必须 ≥ "4.0"
- `as_of` (ISO datetime)
- `income.monthly_salary_after_tax` (number)
- `holdings.cash` (array, ≥1)
- `holdings.stocks_etfs` (array)
- `holdings.funds` (array)
- `holdings.gold` (object) - 含 grams + market_value

## 可选字段

- `liabilities.short_term_planned` - 短期计划支出
- `dca_plans` - 定投计划
- `cashflow_plan` - 现金流预测

## 数值更新规则

每个数字字段都需要 `last_update` (YYYY-MM-DD)：
- 持仓市值：每个交易日更新
- 基金净值：T-1 日（QDII 有时 T-2）
- 现金：用户手动更新
- 黄金：每个交易日更新

**>7 天未更新 → 校验脚本标黄警告**

## 校验脚本

`scripts/validate_profile.py` - 检查 schema 合规性 + 数据一致性