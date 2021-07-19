all: build

format:
	prettier -w content sass static templates

build:
	zola check
	zola build
	find public -type f -name "*.html" -exec htmlmin -c {} {} \;
	cleancss -o public/index.css public/index.css
	$(RM) public/syntax-*.css  # Inlined by cleancss.

deploy: build
	netlify deploy --prod

clean:
	$(RM) -r public

.PHONY: format build deploy clean
