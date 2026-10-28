**A declaration no longer crashes on a column that already lists tests.**
Declaring a grain, `null_rule: never` or `references` on a column whose
`tests:` list was written one item per line failed with an import error instead
of adding the new test beneath the existing ones.
