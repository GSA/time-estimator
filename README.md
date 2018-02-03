#### Note: This repository is in its early stages (pre-Alpha) and should not be used yet.

# time-estimator
Estimate time it took to develop source code using machine learning

# columns
This model will train by injesting a table in tsv format.  Here is a list of possible columns in that table:

| name        | description | example |
| ----        | ----------- | ------- |
| html id     | the number of times id was used in HTML | 3 |
| js =        | the number of times = was used in JavaScript | 30 |
| html lines  | the total number of lines written in HTML | 123 |
| total lines | the total number of lines written across all languages | 400 |
| duration    | this is how long it took to write the code and is called the "label" in machine learning context | 27700
