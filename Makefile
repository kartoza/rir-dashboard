SHELL := /bin/bash

default: htmldocs

# We need to declare phony here since the docs dir exists
# otherwise make tries to execute the docs file directly
.PHONY: docs
docs: htmldocs pdfdocs copypdf ## Generate documentation and place results in docs folder.

pdfdocs:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Making sphinx PDF docs"
	@echo "------------------------------------------------------------------"
	$(MAKE) -C sphinx latexpdf

copypdf:
	@cp sphinx/build/latex/rirdashboard.pdf rir-manual.pdf

htmldocs: ## Generate documentation and place results in docs folder.
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Making sphinx HTML docs"
	@echo "------------------------------------------------------------------"
	$(MAKE) -C sphinx html
	@cp -r  sphinx/build/html/* docs

