all: build

format:
	prettier -w content sass static templates

build:
	zola check
	zola build
	find public -name "*.html" -exec htmlmin -c {} {} \;

deploy: build
	netlify deploy --prod

clean:
	$(RM) -r public

.PHONY: format build deploy clean
