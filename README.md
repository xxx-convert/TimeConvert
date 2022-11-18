# TimeConvert
TimeConvert is a simple time convert script(library) for Python, built for human beings.

[![Gitter](https://badges.gitter.im/Brightcells/TimeConvert.svg)](https://gitter.im/Brightcells/TimeConvert?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=body_badge)

# Installation
```shell
pip install TimeConvert
```

# Usage
```python
from TimeConvert import TimeConvert as tc

tc.utc_timestamp()
```

# Comparison
| Function Points | TimeConvert | Other |
| ---- | ---- | ---- |
| TimeStamp | tc.local_timestamp(ms=True) | time.time() |
| ISOFormat | tc.local_isostring() | datetime.datetime.now().isoformat() |


# Variable
```python
# Default Asia/Shanghai & %Y-%m-%d %H:%M:%S
from TimeConvert import TIME_ZONE, TIME_FORMAT

# Deassign TIME_ZONE & TIME_FORMAT
tc.__init__(timezone='Asia/Shanghai', format='%Y-%m-%d %H:%M:%S')
```

# Reference
* isoweek.py - https://github.com/gisle/isoweek
* month.py - https://github.com/kstark/months
