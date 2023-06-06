PYTEST := poetry run pytest
FORMATTER := poetry run black
LINTER := poetry run flake8
IMPORT_SORTER := poetry run isort
TYPE_CHECKER := poetry run mypy
SPHINX_APIDOC := poetry run sphinx-apidoc

PROJECT_DIR := qulacs_dataset
CHECK_DIR := $(PROJECT_DIR) tests
COVERAGE_OPT := --cov $(PROJECT_DIR) --cov-branch
PORT := 8000

# If this project is not ready to pass mypy, remove `type` below.
.PHONY: check
check: format lint type

.PHONY: ci
ci: format_check lint type

.PHONY: test
test:
	$(PYTEST) -v

tests/%.py: FORCE
	$(PYTEST) $@

# Idiom found at https://www.gnu.org/software/make/manual/html_node/Force-Targets.html
FORCE:

.PHONY: format
format:
	$(FORMATTER) $(CHECK_DIR)
	$(IMPORT_SORTER) $(CHECK_DIR)

.PHONY: format_check
format_check:
	$(FORMATTER) $(CHECK_DIR) --check --diff
	$(IMPORT_SORTER) $(CHECK_DIR) --check --diff

.PHONY: cov
cov:
	$(PYTEST) $(COVERAGE_OPT) --cov-report html

.PHONY: cov_ci
cov_ci:
	$(PYTEST) $(COVERAGE_OPT) --cov-report xml

.PHONY: serve_cov
serve_cov: cov
	poetry run python -m http.server --directory htmlcov $(PORT)

.PHONY: lint
lint:
	$(LINTER) $(CHECK_DIR)

.PHONY: type
type:
	$(TYPE_CHECKER) $(CHECK_DIR)

.PHONY: serve
serve: html
	poetry run python -m http.server --directory doc/build/html $(PORT)

.PHONY: doc
html: api
	poetry run $(MAKE) -C doc html

.PHONY: api
api:
	$(SPHINX_APIDOC) -f -e -o doc/source $(PROJECT_DIR)
