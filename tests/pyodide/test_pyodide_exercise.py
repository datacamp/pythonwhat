from pythonwhat import PyodideExercise


def test_run_code():
    pec = "x = 10"
    solution = ""
    sct = ""
    exercise = PyodideExercise(pec=pec, solution=solution, sct=sct)
    exercise.run_init()

    result = exercise.run_code("print(x)\nx+1")

    assert result == [
        {"type": "output", "payload": "10"},
        {"type": "result", "payload": "11"},
    ]
