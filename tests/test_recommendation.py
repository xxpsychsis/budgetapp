import sys
import types
sys.modules["requests"] = types.ModuleType("requests")
sys.modules["requests"].Session = lambda: None
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import ynab_helper as yh


def test_recommend_changes_basic():
    cats = [
        yh.Category(id="a", name="A", budgeted=1000, balance=2000),
        yh.Category(id="b", name="B", budgeted=1000, balance=-500),
        yh.Category(id="c", name="C", budgeted=1000, balance=1000),
        yh.Category(id="d", name="D", budgeted=1000, balance=-300),
    ]
    moves = yh.recommend_changes(cats)
    total_move = sum(m["amount"] for m in moves)
    assert total_move == 800
    # after applying moves to categories, no overspent remains
    balances = {c.id: c.balance for c in cats}
    for m in moves:
        balances[m["from"]] -= m["amount"]
        balances[m["to"]] += m["amount"]
    assert all(b >= 0 for b in balances.values())
