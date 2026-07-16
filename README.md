# BudgetWise

BudgetWise is a small Python budgeting app built around the envelope budgeting
method. The project is currently focused on practicing object-oriented design,
service-layer logic, and clear separation between data classes and application
workflows.

## Project Status

This app is early in development. The core model classes are being built first:

- `Budget` stores envelopes and available money.
- `Envelope` stores a spending category, its budgeted limit, and its expenses.
- `Expense` stores one spending record.
- `BudgetService` coordinates user actions such as creating envelopes, adding
  money, recording expenses, and moving money between envelopes.

The command-line interface in `main.py` is still experimental.

## Project Structure

```text
BudgetWise/
├── budget.py
├── budget_service.py
├── envelope.py
├── expense.py
├── main.py
└── README.md
```

## How to Run

This project uses only Python's standard library.

```bash
python3 main.py
```

## Design Notes

The current design separates the app into two main layers:

- Data classes represent the objects in the budget.
- The service class owns validation and workflows that involve multiple
  objects.

For example, an `Envelope` can calculate its own balance, but `BudgetService`
decides whether an expense can be recorded or whether money can be moved between
two envelopes.

## Next Steps

- Finish the `BudgetService` workflows.
- Decide how invalid input should be handled.
- Add dates when recording expenses.
- Build out the command-line menu in `main.py`.
- Add small tests for creating envelopes, recording expenses, and moving money.
