export PYTHONWARNINGS="ignore"

fixed="test_function test_with test_object test_function_definition test_or"

for f in $fixed; do
    echo "-----------------------------------------"
    echo $f
    echo "-----------------------------------------"
    python3 "test_$f.py"
done
