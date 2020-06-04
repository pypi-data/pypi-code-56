from IPython.display import display, Javascript, HTML
import json
from .format import format

def simulate(token, command, progress_reader=None):
    import subprocess, base64
    process = subprocess.Popen(command, shell=True)
    display(Javascript(format("""
        reportProgress('{{|token|}}', {
            status: 'started'
        });
    """, token=token)))
    if progress_reader:
        for progress_message in progress_reader.listen(process):
            display(Javascript(format("""
                reportProgress('{{|token|}}', {
                    status: 'running',
                    progress: {{|progress|}}
                });
            """, token=token, progress=json.dumps(progress_message.__dict__))))
        display(Javascript(format("""
            reportProgress('{{|token|}}', {
                status: 'finished'
            });
        """, token=token)))
