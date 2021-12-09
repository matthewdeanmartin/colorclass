echo assuming we still want to support python 2!
PROJECT="colorclass"
export PYTHONPATH=$PYTHONPATH:.
pylint "$PROJECT"
flake8 "$PROJECT"
python -m pytest "$PROJECT"
python -m pytest --doctest-glob="$PROJECT/**/*.py"
pytest tests -v --cov-report html:coverage --cov="$PROJECT"
echo not bumping version here, just checking if we can create the wheel
poetry build
check-wheel-contents dist/*.whl