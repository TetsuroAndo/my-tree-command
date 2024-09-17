import os
import sys

try:
    from colorama import init, Fore, Style
    has_colorama = True
    init(autoreset=True)
except ImportError:
    has_colorama = False

def get_color(path):
    if not has_colorama:
        return ''
    if os.path.isdir(path):
        return Fore.BLUE
    elif os.path.islink(path):
        return Fore.CYAN
    else:
        return Fore.GREEN

def reset_color():
    return Style.RESET_ALL if has_colorama else ''

def tree(directory, prefix=''):
    contents = os.listdir(directory)
    contents.sort()
    dir_count = 0
    file_count = 0
    for i, item in enumerate(contents):
        path = os.path.join(directory, item)
        is_last = i == len(contents) - 1
        
        color = get_color(path)
        
        if os.path.isdir(path):
            item += '/'
            dir_count += 1
        elif os.path.islink(path):
            link_target = os.readlink(path)
            item = f"{item} -> {link_target}"
            file_count += 1
        else:
            file_count += 1
        
        print(f"{prefix}{'└── ' if is_last else '├── '}{color}{item}{reset_color()}")
        
        if os.path.isdir(path) and not os.path.islink(path):
            extension = '    ' if is_last else '│   '
            sub_dir_count, sub_file_count = tree(path, prefix + extension)
            dir_count += sub_dir_count
            file_count += sub_file_count
    
    return dir_count, file_count

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    print(path)
    total_dirs, total_files = tree(path)
    print(f"\n{total_dirs} directories, {total_files} files")
