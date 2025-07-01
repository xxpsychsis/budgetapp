import argparse
import os

from ynab_helper import YNABClient, recommend_changes


def main():
    parser = argparse.ArgumentParser(description="YNAB budget helper")
    parser.add_argument("budget_id", help="YNAB budget ID")
    parser.add_argument(
        "--month", default=None, help="Budget month (YYYY-MM-01). Defaults to current month"
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply recommended changes to YNAB",
    )
    args = parser.parse_args()

    token = os.environ.get("YNAB_TOKEN")
    if not token:
        parser.error("Environment variable YNAB_TOKEN must be set")

    client = YNABClient(token)
    categories = client.get_month_categories(args.budget_id, args.month)
    moves = recommend_changes(categories)

    if not moves:
        print("No recommendations. Budget looks good!")
        return

    print("Recommended moves:")
    for m in moves:
        print(f"  Move {m['amount']/1000:.2f} from {m['from']} to {m['to']}")

    if args.apply:
        month = args.month
        if month is None:
            import datetime

            month = datetime.date.today().strftime("%Y-%m-01")
        current = {c.id: c for c in client.get_month_categories(args.budget_id, month)}
        for m in moves:
            from_cat = current[m["from"]]
            to_cat = current[m["to"]]
            client.update_category_budget(
                args.budget_id, month, from_cat.id, from_cat.budgeted - m["amount"]
            )
            client.update_category_budget(
                args.budget_id, month, to_cat.id, to_cat.budgeted + m["amount"]
            )
        print("Changes applied.")


if __name__ == "__main__":
    main()
