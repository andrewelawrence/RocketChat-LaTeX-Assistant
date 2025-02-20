import sys, os
from llmproxy import pdf_upload

'''
Reminder, export environment variables prior to running this function.
```bash
$ export apiKey="x"
$ export endPoint="y"
'''

if len(sys.argv) < 2:
    print("Usage: python script.py <pdf filepath> [<pdf filepath>]")
    sys.exit(1)

for file_path in sys.argv[1:]:
    desc = os.path.basename(file_path)
    response = pdf_upload(path = file_path,
                          description = desc,
                          session_id = 'hw04')
    print(f"Response for {desc}: {response}")
