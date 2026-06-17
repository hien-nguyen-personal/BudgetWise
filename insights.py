class SpendingInsights:
    """Calculates spending summaries from a list of items."""

    def __init__(self, items):
        self.items = items

    def total_spending(self):
        return sum(item.price for item in self.items)

    def spending_by_category(self):
        return self._group_spending_by("category")

    def spending_by_store(self):
        return self._group_spending_by("store")

    def _group_spending_by(self, attribute):
        totals = {}

        for item in self.items:
            key = getattr(item, attribute)
            totals[key] = totals.get(key, 0) + item.price

        return totals
