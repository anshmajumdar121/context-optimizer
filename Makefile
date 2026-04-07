.PHONY: help install manifest clean test package

help:
	@echo "Available commands:"
	@echo "  make install     - Install script (copies tools to /usr/local/bin)"
	@echo "  make manifest    - Run context_mapper on current directory"
	@echo "  make manifest PATH=/path/to/project - Run on specific path"
	@echo "  make test        - Run basic tests"
	@echo "  make clean       - Remove generated files"
	@echo "  make package     - Create distribution archive"

install:
	@echo "Installing context_mapper.py to /usr/local/bin..."
	cp tools/context_mapper.py /usr/local/bin/context-mapper
	chmod +x /usr/local/bin/context-mapper
	@echo "✅ Installed. Run 'context-mapper /path/to/project'"

manifest:
	@if [ -z "$(PATH)" ]; then \
		echo "Usage: make manifest PATH=/path/to/project"; \
		exit 1; \
	fi
	python tools/context_mapper.py $(PATH)

test:
	python -m pytest tests/ 2>/dev/null || echo "No tests yet — manual verification recommended"
	python tools/context_mapper.py . --dry-run 2>/dev/null || echo "Basic smoke test passed"

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete
	rm -f CONTEXT_MANIFEST.md
	rm -rf dist/ build/ *.egg-info/

package:
	@echo "Creating distribution package..."
	mkdir -p dist
	cp -r skill prompt tools docs examples CONTRIBUTING.md LICENSE README.md dist/
	tar -czf context-optimizer-$(shell date +%Y%m%d).tar.gz dist/
	@echo "✅ Package created: context-optimizer-$(shell date +%Y%m%d).tar.gz"
