
from io import StringIO
import sys

class capture_stdout_stderr:
    def __enter__ (self):
        self.cs = sys.stdout
        self.ce = sys.stderr

        sys.stdout = StringIO()
        sys.stderr = StringIO()

        return sys.stdout, sys.stderr
    def __exit__ (self, *args, **kwargs):
        sys.stdout = self.cs
        sys.stderr = self.ce
