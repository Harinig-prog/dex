**A drafted `references` picks the right parent.** Once a project is built, a
column joins cleanly to the raw table, its staging model and the dimension
downstream, and the draft used to take whichever join the cache listed first.
It could propose a reference to a raw table no `ref()` reaches, to a model whose
column is not unique, or to the model itself, and an orphaned join listed first
hid a clean one. The draft now passes over a non-unique parent and the model
itself, prefers a model of the project (the nearest one in the project tree),
and names the other clean parents in its evidence. On Snowflake, a model
reported as `STG_CUSTOMERS` is recognised as the project's `stg_customers`.
