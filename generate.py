""" Build index from directory listing

make_index.py </path/to/directory> [--header <header text>]
"""

INDEX_TEMPLATE = r"""
<!DOCTYPE html>
<html>
<head>
    <title>${header}</title>
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f9f9f9;
            height: 100vh;
            box-sizing: border-box;
        }
        .explorer-container {
            background: white;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            height: calc(100% - 2px);
            display: flex;
            flex-direction: column;
        }
        .header {
            background: #f0f0f0;
            padding: 10px 15px;
            border-bottom: 1px solid #ddd;
            flex-shrink: 0;
        }
        .header h2 {
            margin: 0;
            color: #333;
            font-size: 16px;
        }
        .tree-view {
            padding: 10px;
            overflow-y: auto;
            flex-grow: 1;
        }
        .folder,
        .file {
            padding: 4px 8px;
            margin: 2px 0;
            display: flex;
            align-items: center;
            cursor: pointer;
            white-space: nowrap;
        }
        .folder:hover,
        .file:hover {
            background-color: #e8e8e8;
        }
        .folder-content {
            margin-left: 20px;
            border-left: 1px dotted #ccc;
            padding-left: 10px;
            display: none;
        }
        .folder-content.open {
            display: block;
        }
        .icon {
            width: 16px;
            height: 16px;
            margin-right: 8px;
            display: inline-block;
            flex-shrink: 0;
        }
        .folder-icon {
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path fill="%23FCD474" d="M1 3v10h14V4H7L6 3z"/></svg>') no-repeat;
        }
        .file-icon {
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path fill="%23A0A0A0" d="M3 1v14h10V5L9 1z"/><path fill="%23FFFFFF" d="M9 1v4h4z"/></svg>') no-repeat;
        }
        .arrow {
            width: 16px;
            height: 16px;
            margin-right: 4px;
            display: inline-block;
            transition: transform 0.2s;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path fill="%23666" d="M6 4l4 4-4 4z"/></svg>') no-repeat center;
        }
        .arrow.open {
            transform: rotate(90deg);
        }
        a {
            color: #333;
            text-decoration: none;
        }
        a:hover {
            color: #0066cc;
        }
        .folder-label {
            font-weight: 500;
        }
    </style>
</head>
<body>
    <div class="explorer-container">
        <div class="header">
            <h2>${header}</h2>
        </div>
        <div class="tree-view">
            % for folder in folders:
                <div class="folder">
                    <span class="arrow"></span>
                    <span class="icon folder-icon"></span>
                    <span class="folder-label">${folder['name']}</span>
                </div>
                <div class="folder-content">
                    % for file in folder['files']:
                        <div class="file">
                            <span class="icon file-icon"></span>
                            <a href="${file['path']}">${file['name']}</a>
                        </div>
                    % endfor
                </div>
            % endfor
        </div>
    </div>
    <script>
        document.addEventListener('DOMContentLoaded', function () {
            const folders = document.querySelectorAll('.folder');
            folders.forEach(folder => {
                folder.addEventListener('click', function (e) {
                    const arrow = this.querySelector('.arrow');
                    const content = this.nextElementSibling;
                    arrow.classList.toggle('open');
                    content.classList.toggle('open');
                    e.stopPropagation();
                });
            });
        });
    </script>
</body>
</html>
"""

EXCLUDED = ['index.html']

import os
import argparse
from mako.template import Template

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    parser.add_argument("--header")
    args = parser.parse_args()

    folders = []
    for root, dirs, files in os.walk(args.directory):
        folder = {
            'name': os.path.relpath(root, args.directory),
            'files': []
        }
        for file in files:
            if file.endswith('.html') and file not in EXCLUDED:
                relative_path = os.path.relpath(os.path.join(root, file), args.directory)
                folder['files'].append({'path': relative_path, 'name': file})
        if folder['files']:
            folders.append(folder)

    header = args.header if args.header else os.path.basename(args.directory)
    rendered_html = Template(INDEX_TEMPLATE).render(folders=folders, header=header)
    
    output_path = os.path.join(args.directory, 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(rendered_html)
    print(f"Index file generated at {output_path}")

if __name__ == '__main__':
    main()