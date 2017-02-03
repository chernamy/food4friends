TEST_FILES = $(wildcard controller_tests/*test.py)
TESTS = $(subst .py,,$(subst /,.,$(TEST_FILES)))

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
