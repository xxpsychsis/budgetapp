import datetime
from dataclasses import dataclass
from typing import List, Dict

import requests


@dataclass
class Category:
    id: str
    name: str
    budgeted: int
    balance: int


class YNABClient:
    """Simple client for the YNAB API."""

    BASE_URL = "https://api.youneedabudget.com/v1"

    def __init__(self, access_token: str):
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {access_token}"})

    def get_budgets(self) -> Dict:
        resp = self.session.get(f"{self.BASE_URL}/budgets")
        resp.raise_for_status()
        return resp.json()

    def get_month_categories(self, budget_id: str, month: str = None) -> List[Category]:
        if month is None:
            month = datetime.date.today().strftime("%Y-%m-01")
        url = f"{self.BASE_URL}/budgets/{budget_id}/months/{month}"
        resp = self.session.get(url)
        resp.raise_for_status()
        data = resp.json()
        categories = []
        for grp in data["data"]["month"]["categories"]:
            categories.append(
                Category(
                    id=grp["id"],
                    name=grp["name"],
                    budgeted=grp["budgeted"],
                    balance=grp["balance"],
                )
            )
        return categories

    def update_category_budget(self, budget_id: str, month: str, category_id: str, amount: int) -> Dict:
        url = f"{self.BASE_URL}/budgets/{budget_id}/months/{month}/categories/{category_id}"
        body = {"category": {"budgeted": amount}}
        resp = self.session.put(url, json=body)
        resp.raise_for_status()
        return resp.json()


def recommend_changes(categories: List[Category]) -> List[Dict]:
    """Suggest budget moves from positive categories to cover negatives."""
    overspent = [c for c in categories if c.balance < 0]
    surplus = [c for c in categories if c.balance > 0]
    overspent.sort(key=lambda c: c.balance)
    surplus.sort(key=lambda c: c.balance, reverse=True)
    moves = []
    for o in overspent:
        needed = -o.balance
        for s in surplus:
            if s.balance <= 0:
                continue
            amount = min(needed, s.balance)
            if amount <= 0:
                continue
            moves.append({"from": s.id, "to": o.id, "amount": amount})
            s.balance -= amount
            needed -= amount
            if needed == 0:
                break
    return moves
