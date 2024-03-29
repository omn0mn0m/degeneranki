all: install degeneranki.ankiaddon

degeneranki.ankiaddon:
	(cd src/degeneranki; \
	rm -r __pycache__; \
	zip $@ -FSr . -x *~ meta.json *__pycache__/* @; \
	mv $@ ../../build/)

install: vendoring

venv: venv/touchfile

venv/touchfile: pyproject.toml
	test -d venv || python -m venv venv
	. venv/bin/activate; pip install .[dev]
	touch venv/touchfile

vendoring: venv/touchfile
	. venv/bin/activate; vendoring sync
