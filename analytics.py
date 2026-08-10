from dataclasses import dataclass
from datetime import datetime, timedelta

import pandas as pd
from sqlalchemy import func

from models import Case, PriceEntry, db


@dataclass
class MoverResult:
    case_name: str
    market_code: str
    image_url: str
    start_price: float
    end_price: float
    change_pct: float


def _price_dataframe(days: int | None = None) -> pd.DataFrame:
    query = (
        db.session.query(
            Case.name.label("case_name"),
            Case.market_code.label("market_code"),
            Case.image_url.label("image_url"),
            PriceEntry.recorded_at,
            PriceEntry.price,
        )
        .join(PriceEntry, PriceEntry.case_id == Case.id)
    )

    if days is not None:
        cutoff = datetime.utcnow() - timedelta(days=days)
        query = query.filter(PriceEntry.recorded_at >= cutoff)

    df = pd.read_sql(query.statement, db.engine)
    df["price"] = df["price"].astype(float)
    return df


def top_movers(days: int = 365, limit: int = 5, direction: str = "gainers") -> list[MoverResult]:
    df = _price_dataframe(days=days)
    if df.empty:
        return []

    df = df.sort_values("recorded_at")
    grouped = df.groupby("case_name")

    results = []
    for case_name, group in grouped:
        if len(group) < 2:
            continue
        start_price = group.iloc[0]["price"]
        end_price = group.iloc[-1]["price"]
        if start_price == 0:
            continue
        change_pct = (end_price - start_price) / start_price * 100

        results.append(
            MoverResult(
                case_name=case_name,
                market_code=group.iloc[0]["market_code"],
                image_url=group.iloc[0]["image_url"],
                start_price=round(start_price, 2),
                end_price=round(end_price, 2),
                change_pct=round(change_pct, 2),
            )
        )

    reverse = direction == "gainers"
    results.sort(key=lambda r: r.change_pct, reverse=reverse)
    return results[:limit]


def most_volatile(days: int = 365, limit: int = 5) -> list[dict]:
    df = _price_dataframe(days=days)
    if df.empty:
        return []

    stats = df.groupby("case_name")["price"].agg(["mean", "std"]).dropna()
    stats = stats[stats["mean"] > 0]
    stats["volatility_pct"] = (stats["std"] / stats["mean"] * 100).round(2)
    stats = stats.sort_values("volatility_pct", ascending=False).head(limit)

    return [
        {"case_name": name, "volatility_pct": row["volatility_pct"], "avg_price": round(row["mean"], 2)}
        for name, row in stats.iterrows()
    ]


def all_time_extremes() -> list[dict]:
    subq = (
        db.session.query(
            Case.name.label("case_name"),
            func.max(PriceEntry.price).label("ath"),
            func.min(PriceEntry.price).label("atl"),
        )
        .join(PriceEntry, PriceEntry.case_id == Case.id)
        .group_by(Case.id, Case.name)
        .subquery()
    )
    rows = db.session.query(subq).all()
    return [
        {"case_name": r.case_name, "ath": float(r.ath), "atl": float(r.atl)}
        for r in rows
    ]


def market_index(days: int = 365) -> list[dict]:
    df = _price_dataframe(days=days)
    if df.empty:
        return []

    df["date"] = df["recorded_at"].dt.date
    daily_avg = df.groupby("date")["price"].mean().reset_index()
    daily_avg = daily_avg.sort_values("date")

    base = daily_avg.iloc[0]["price"]
    if base == 0:
        return []

    daily_avg["index"] = (daily_avg["price"] / base * 100).round(2)

    return [
        {"date": row["date"].isoformat(), "index": row["index"]}
        for _, row in daily_avg.iterrows()
    ]