![Fairyfly](https://raw.githubusercontent.com/ladybug-tools/artwork/refs/heads/master/icons_bugs/png/fairyfly-small.png)
<img src="https://raw.githubusercontent.com/ladybug-tools/artwork/refs/heads/master/icons_components/fairyfly/png/therm.png" alt="THERM" width="200" height="200">

[![Build Status](https://github.com/ladybug-tools/fairyfly-therm/workflows/CI/badge.svg)](https://github.com/ladybug-tools/fairyfly-therm/actions)
[![Python 3.10](https://img.shields.io/badge/python-3.10-pink.svg)](https://www.python.org/downloads/release/python-3100/)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Python 2.7](https://img.shields.io/badge/python-2.7-green.svg)](https://www.python.org/downloads/release/python-270/)
[![IronPython](https://img.shields.io/badge/ironpython-2.7-red.svg)](https://github.com/IronLanguages/ironpython2/releases/tag/ipy-2.7.8/)

# fairyfly-therm

Fairyfly extension for energy modeling with LBNL THERM.

[THERM](https://windows.lbl.gov/software-tools#therm-heading) is a widely used and accepted freeware for modeling two-dimensional heat-transfer in building components such as windows, walls, foundations, etc.

## Installation

`pip install -U fairyfly-therm`

## QuickStart

```console
import fairyfly_therm
```

## [API Documentation](http://ladybug-tools.github.io/fairyfly-therm/docs)

## Local Development

1. Clone this repo locally
```console
git clone git@github.com:ladybug-tools/fairyfly-therm

# or

git clone https://github.com/ladybug-tools/fairyfly-therm
```
2. Install dependencies:
```
cd fairyfly-therm
pip install -r dev-requirements.txt
pip install -r requirements.txt
```

3. Run Tests:
```console
python -m pytest tests/
```

4. Generate Documentation:
```console
sphinx-apidoc -f -e -d 4 -o ./docs ./fairyfly_therm
sphinx-build -b html ./docs ./docs/_build/docs
```