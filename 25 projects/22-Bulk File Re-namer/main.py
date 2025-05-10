import os
from pathlib import Path

def get_valid_folder():
    """Prompt for and validate folder path."""
    while True:
        folder = input("Enter folder path (e.g., C:\\Users\\YourName\\Documents\\test_folder): ").strip()
        folder_path = Path(folder)
        if folder_path.exists() and folder_path.is_dir():
            return folder_path
        print("Invalid folder path. Please try again.")

def list_files(folder_path):
    """Return list of files (not directories) in the folder."""
    return [f for f in folder_path.iterdir() if f.is_file()]

def add_prefix(folder_path, prefix):
    """Add prefix to all filenames."""
    files = list_files(folder_path)
    renamed_count = 0
    
    for file_path in files:
        new_name = f"{prefix}{file_path.name}"
        new_path = file_path.parent / new_name
        try:
            file_path.rename(new_path)
            print(f"Renamed: {file_path.name} -> {new_name}")
            renamed_count += 1
        except (OSError, FileExistsError) as e:
            print(f"Error renaming {file_path.name}: {e}")
    
    return renamed_count

def remove_substring(folder_path, substring):
    """Remove specified substring from filenames."""
    files = list_files(folder_path)
    renamed_count = 0
    
    for file_path in files:
        new_name = file_path.name.replace(substring, "")
        if new_name == file_path.name:
            continue  # No change needed
        new_path = file_path.parent / new_name
        try:
            file_path.rename(new_path)
            print(f"Renamed: {file_path.name} -> {new_name}")
            renamed_count += 1
        except (OSError, FileExistsError) as e:
            print(f"Error renaming {file_path.name}: {e}")
    
    return renamed_count

def sequential_rename(folder_path, base_name):
    """Rename files sequentially (e.g., base_name_001.ext)."""
    files = list_files(folder_path)
    renamed_count = 0
    
    for index, file_path in enumerate(files, 1):
        # Preserve file extension
        ext = file_path.suffix
        new_name = f"{base_name}_{index:03d}{ext}"
        new_path = file_path.parent / new_name
        try:
            file_path.rename(new_path)
            print(f"Renamed: {file_path.name} -> {new_name}")
            renamed_count += 1
        except (OSError, FileExistsError) as e:
            print(f"Error renaming {file_path.name}: {e}")
    
    return renamed_count

def main():
    print("Bulk File Renamer")
    folder_path = get_valid_folder()
    
    while True:
        print("\nChoose a renaming option:")
        print("1. Add prefix to all files")
        print("2. Remove substring from filenames")
        print("3. Rename files sequentially (e.g., file_001.txt)")
        print("4. Exit")
        
        choice = input("Enter choice (1-4): ").strip()
        
        if choice == "1":
            prefix = input("Enter prefix to add (e.g., doc_): ").strip()
            count = add_prefix(folder_path, prefix)
            print(f"Renamed {count} files.")
        
        elif choice == "2":
            substring = input("Enter substring to remove (e.g., copy_): ").strip()
            count = remove_substring(folder_path, substring)
            print(f"Renamed {count} files.")
        
        elif choice == "3":
            base_name = input("Enter base name for sequential rename (e.g., file): ").strip()
            count = sequential_rename(folder_path, base_name)
            print(f"Renamed {count} files.")
        
        elif choice == "4":
            print("Exiting.")
            break
        
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()