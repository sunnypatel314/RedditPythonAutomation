def doesPostExist(id):
    file_path = "post_ids.txt"
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.strip() == id:
                    return True
        with open(file_path, 'a') as file:
            file.write(id + '\n')
    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return False