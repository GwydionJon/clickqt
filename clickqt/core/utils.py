import re 

def is_nested_list(lst):
        if isinstance(lst, list):
            for item in lst:
                if isinstance(item, list):
                    return True
            return False
        else:
            return False
        
def is_file_path(string):
    # Regular expression pattern to match file paths
    pattern = r'^([a-zA-Z]:)?[\\/](?:[^\0<>:\/\\|?*\n]+[\\/])*[^\0<>:\/\\|?*\n]*$'
    
    # Check if the string matches the pattern
    if re.match(pattern, string):
        return True
    else:
        return False