TEST_FILE := tests/run_all.py
ALL_TESTS = $(patsubst %.py,%,$(wildcard tests/test_*.py)) 		# e.g. tests/test_content tests/...

# Run the test of a single file
test: export PYTHONWARNINGS=ignore
test: $(TEST_FILE)
	-python $^

# Run submake for testing each test file
test_parallel: $(ALL_TESTS)

$(ALL_TESTS)::
	@$(MAKE) test TEST_FILE="$@.py"
