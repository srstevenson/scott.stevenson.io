all: build

build:
	zola check
	zola build
	find public -name "*.html" -exec htmlmin -c {} {} \;

deploy: build
	netlify deploy --prod

clean:
	$(RM) -r public

.PHONY: build deploy clean
