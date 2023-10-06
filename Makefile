install:
	pipenv install

install-dev:
	pipenv install --dev

run:
	PYTHONPATH=. streamlit run main.py

test:
	pipenv run pytest tests/
