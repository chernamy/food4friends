TEST_FILES = $(wildcard controller_tests/*test.py)
TESTS = $(subst .py,,$(subst /,.,$(TEST_FILES)))

test:
	@- $(foreach TEST, $(TESTS),\
            echo === Running test: $(TEST); \
            python -m $(TEST);\
            )
