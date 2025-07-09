# Makefile for building HTML documentation using MkDocs

# Directory containing markdown source files
SRCDIR=source
# Directory to output built HTML files
BUILDDIR=build

# Default target
all: html

html:
	@echo "Building HTML documentation with MkDocs..."
	@mkdocs build --config-file mkdocs.yml

clean:
	@echo "Cleaning build directory..."
	rm -rf $(BUILDDIR)/*

.PHONY: all html clean
