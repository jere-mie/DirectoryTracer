import os, sys
sys.setrecursionlimit(10000)

# getting ignored files and folders
ignored = ['.fileignore']
if os.path.exists('.fileignore'):
    ignored = set(open('.fileignore', 'r').read().split('\n') + ['.fileignore'])

# boilerplate used in the output html file
boilerplate1 = """<html>
<head>
    <title>Files</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <style>
        body {
            margin: 2rem;
            font-family: sans-serif;
        }
        ul {
            list-style-type: none;
        }
        a, a:visited {
            color: blue;
        }
        a:hover {
            background-color: yellow;
        }
        .dir {
            font-size: 20px;
        }
        .file {
            font-size: 18px;
        }
    </style>
</head>
<body>
    <h2>View Directory Contents</h2>
    <h1>{{ directory }}</h1>
    <ul>
"""
boilerplate2 = "    </ul>\n</body>\n</html>"

# recursive function that writes index.html and calls indexFolder for subdirectories
def indexFolder(directory):
    folder_list = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))] # Source: https://www.codegrepper.com/code-examples/python/get+list+of+folders+in+directory+python
    if len(folder_list) > 0:
        for i in range(len(folder_list)):
            indexFolder(os.path.join(directory, folder_list[i]))

    file_list = [n for n in os.listdir(directory) if not n in folder_list] # anything not in folder_list is a file

    f = open(str(directory) + "\\index.html", "w", encoding="utf8")
    f.write(boilerplate1)

    # Write folder contents.
    if directory!='.':
        f.write("        <li class=\"dir\"><b><a href=\"..\">⬆ Parent</a></b></li></br>\n")
    for i in range(len(folder_list)):
        if folder_list[i] not in ignored:
            f.write("        <li class=\"dir\"><b><a href=\"" + folder_list[i] + "\">📁 " + folder_list[i] + "/</a></b></li>\n")

    # separate folders from files
    f.write("        <br />\n")

    # Write file contents.
    for i in range(len(file_list)):
        if file_list[i] not in ignored and file_list[i] != "index.html":
            f.write("        <li class=\"file\"><a target=\"_blank\" href=\"" + file_list[i] + "\">📄 " + file_list[i] + "</a></li>\n")

    # ending off the html file
    f.write(boilerplate2)
    f.close()

    # replacing {{ directory }} with the actual directory name
    with open(str(directory) + "\\index.html", "r", encoding="utf8") as f:
        contents = f.read().replace('{{ directory }}', directory.replace('\\', '/'))
    with open(str(directory) + "\\index.html", "w", encoding="utf8") as f:
        f.write(contents)

# base case, where we index the current folder
indexFolder(os.curdir)