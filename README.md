# python-granatum

## Introduction

**python-granatum** is a Python wrapper for [Granatum Financeiro](https://www.granatum.com.br/financeiro/).

## Quick Start

```
from datetime import date

from granatum import Granatum


g = Granatum('<email>', '<password>')
end_date = date(2019, 8, 31)
start_date = date(2019, 8, 1)
filters = {'conta_id': ['<name of the account>']}
print(g.exportar(end_date, start_date, filters))
```
