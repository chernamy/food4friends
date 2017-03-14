TEST_FILES = $(wildcard controller_tests/*test.py) fb_test.py
TESTS = $(subst .py,,$(subst /,.,$(TEST_FILES)))

db_setup:
	@read -p "Database username: " username; \
	echo Username: $$username; \
	mysql -u $$username -p < db_setup.sql; \

run:
	python app.py

test:
	@- $(foreach TEST, $(TESTS),\
            echo === Running test: $(TEST); \
            python -m $(TEST);\
            )

buy_test:
	python -m controller_tests.buy_test

sell_test:
	python -m controller_tests.sell_test

login_test:
	python -m controller_tests.login_test

user_test:
	python -m controller_tests.user_test

fb_test:
	python fb_test.py

community_test:
	python -m controller_tests.community_test

rating_test:
	python -m controller_tests.rating_test
