from streamlit.testing.v1 import AppTest

at = AppTest.from_file("app.py").run()
if at.exception:
    print("EXCEPTION:", at.exception[0])
    raise at.exception[0]
else:
    print("Run completed successfully")
