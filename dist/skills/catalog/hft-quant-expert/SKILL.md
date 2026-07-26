---
name: hft-quant-expert
description: Quantitative trading expertise for DeFi and crypto derivatives. Use when building trading strategies, signals, risk management. Triggers on signal, backtest, alpha, sharpe, volatility, correlation, position size, risk.
metadata:
  codex_migration: '2026-06-27'
  source_path: skills/.curated/claude-main/.claude/skills/hft-quant-expert/SKILL.md
---

# HFT Quant Expert

## Codex compatibility

- Legacy Claude-specific tool names or paths are conceptual; use Codex shell/editor capabilities and the local `.agents/skills` path.


Quantitative trading expertise for DeFi and crypto derivatives.

## When to Use

- Building trading strategies and signals
- Implementing risk management
- Calculating position sizes
- Backtesting strategies
- Analyzing volatility and correlations

## Workflow

### Step 1: Define Signal

Calculate z-score or other entry signal.

### Step 2: Size Position

Use Kelly Criterion (0.25x) for position sizing.

### Step 3: Validate Backtest

Check for lookahead bias, survivorship bias, overfitting.

### Step 4: Account for Costs

Include gas + slippage in profit calculations.

---

## Quick Formulas
```python
# Z-score
zscore = (value - rolling_mean) / rolling_std

# Sharpe (annualized)
sharpe = np.sqrt(252) * returns.mean() / returns.std()

# Kelly fraction (use 0.25x)
kelly = (win_prob * win_loss_ratio - (1 - win_prob)) / win_loss_ratio

# Half-life of mean reversion
half_life = -np.log(2) / lambda_coef
```

## Common Pitfalls

- **Lookahead bias** - Using future data
- **Survivorship bias** - Only existing assets
- **Overfitting** - Too many parameters
- **Ignoring costs** - Gas + slippage
- **Wrong annualization** - 252 daily, 365*24 hourly
