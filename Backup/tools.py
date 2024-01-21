from abc import ABC, abstractmethod
import random
import string
import hashlib
import traceback
import subprocess
import code
import sys
import io


class AbstractTool(ABC):
    def __init__(self):
        self.object_id = hashlib.sha256(
            "".join(random.choices(string.ascii_letters + string.digits, k=10)).encode()
        ).hexdigest()

    def use(self, *args, **kwargs):
        try:
            return self._use_tool(*args, **kwargs)
        except Exception as e:
            return self.error_feedback(e)

    @abstractmethod
    def _use_tool(self):
        pass

    def error_feedback(self, error):
        return f"Error occurred while using the tool:\n{error}\n{traceback.format_exc()}"


class CommandTool(AbstractTool):
    def __init__(self):
        super().__init__()

    def _use_tool(self, command):
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        output, error = process.communicate()

        if process.returncode != 0:
            return f"Error occurred: {error.decode().strip()}"
        else:
            return f"Output: {output.decode().strip()}"


class PythonInteractiveTool(AbstractTool):
    def __init__(self):
        super().__init__()
        self.interpreter = code.InteractiveInterpreter(locals=locals())

    def _use_tool(self, code_str):
        old_stdout, old_stderr = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = io.StringIO(), io.StringIO()

        try:
            code_obj = code.compile_command(code_str, symbol="exec")
            if code_obj is None:
                raise SyntaxError("Invalid syntax")

            self.interpreter.runcode(code_obj)
            output = sys.stdout.getvalue()
            error = sys.stderr.getvalue()
        except Exception as e:
            output = ""
            error = f"Error occurred: {e}"
        finally:
            sys.stdout, sys.stderr = old_stdout, old_stderr
            if error:
                return error
            else:
                return output


class PythonScriptTool(AbstractTool):
    def __init__(self):
        super().__init__()

    def _use_tool(self, filepath, script):
        # Create or overwrite the Python script file
        with open(filepath, 'w') as file:
            file.write(script)

        # Run the Python script file
        try:
            output = subprocess.check_output(['python', filepath], stderr=subprocess.STDOUT)
            return output.decode('utf-8')
        except subprocess.CalledProcessError as e:
            return f"Error occurred: {e.output.decode('utf-8')}"

def main():
    # test PythonScriptTool
    tool = PythonScriptTool()
    output = tool.use("test5.py", "print('Hello, World!')")
    print(output)

    # test error case
    output = tool.use("test5.py", "print('Hello, World!'")
    print(output)
    
    # test with checking python version
    output = tool.use("test5.py", "import sys\nprint(sys.version)")
    print(output)

if __name__ == "__main__":
    main()