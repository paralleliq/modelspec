.PHONY: validate
validate:
	python tooling/validator/validate.py --schema schema/modelspec.v0.1.json examples/
