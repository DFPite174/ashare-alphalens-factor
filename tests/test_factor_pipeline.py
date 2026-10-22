"""
独立因子管道单元测试 - 验证时序收益、动量与反转因子计算、IC 指标与 HAC 纠偏
"""

import pytest
import numpy as np
import pandas as pd
from alphalens_factor import (
    MomentumFactor,
    MeanReversionFactor,
    LookaheadLeakageFactor,
    AlphalensAdapter,
    FactorReporter,
)


@pytest.fixture
def sample_market_data():
    # 构造标准合成测试行情 (100 天，3 只股票)
    dates = pd.date_range("2025-01-01", periods=100, freq="B")
    symbols = ["000001.SZ", "600519.SH", "688981.SH"]
    rows = []
    for s in symbols:
        base_p = 100.0 if s == "600519.SH" else (10.0 if s == "000001.SZ" else 50.0)
        drift = 0.001 if s == "600519.SH" else -0.0005
        prices = base_p * np.exp(np.cumsum(np.random.normal(drift, 0.015, len(dates))))
        for dt, p in zip(dates, prices):
            rows.append({
                "symbol": s,
                "trade_date": dt.strftime("%Y-%m-%d"),
                "open": p * 0.99,
                "high": p * 1.01,
                "low": p * 0.98,
                "close": p,
                "volume": 100000.0,
                "adj_factor": 1.0,
            })
    return pd.DataFrame(rows)


def test_momentum_and_alphalens_metrics(sample_market_data):
    bars = sample_market_data
    prices = AlphalensAdapter.prepare_prices_matrix(bars)
    
    factor = MomentumFactor(lookback=10)
    series = factor.compute(bars)
    assert not series.empty

    clean = AlphalensAdapter.clean_factor_data(
        factor_series=series,
        prices=prices,
        periods=(1, 5),
        quantiles=3,
        max_loss=0.40,
    )
    assert not clean.empty

    metrics = AlphalensAdapter.evaluate_factor_metrics(clean, periods=(1, 5))
    assert "periods" in metrics
    assert "5D" in metrics["periods"]
    assert "t_stat_hac" in metrics["periods"]["5D"]


def test_leakage_detection(sample_market_data):
    bars = sample_market_data
    prices = AlphalensAdapter.prepare_prices_matrix(bars)

    trap = LookaheadLeakageFactor()
    series = trap.compute(bars)

    clean = AlphalensAdapter.clean_factor_data(
        factor_series=series,
        prices=prices,
        periods=(1,),
        quantiles=3,
        max_loss=0.40,
    )
    audit = AlphalensAdapter.audit_leakage_and_traps(clean)
    assert audit["is_lookahead_leaking"] is True
    assert audit["status"] == "FAIL_LEAKAGE_DETECTED"
