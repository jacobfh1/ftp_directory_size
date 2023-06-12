from ftplib import FTP
import os


def get_directory_size(ftp, directory):
    size = 0

    # Retrieve a listing of files and directories within the current directory
    file_list = []
    ftp.retrlines('LIST ' + directory, file_list.append)

    for line in file_list:
        # Split the line into separate fields
        fields = line.split(maxsplit=8)
        if len(fields) < 6:
            continue

        # Extract the file/directory name
        name = fields[-1].lstrip()

        # Extract the file/directory permissions
        permissions = fields[0]

        # Check if it is a directory
        if permissions.startswith('d'):
            # Recursively calculate the size of the subdirectory
            size += get_directory_size(ftp, directory + '/' + name)
        else:
            # Retrieve the size of the file
            file_size = ftp.size(directory + '/' + name)
            size += file_size

    return size


def bytes_to_gigabytes(size_in_bytes):
    return size_in_bytes / (1024 * 1024 * 1024)


def get_file_sizes_by_type(ftp, directory):
    file_sizes = {}

    # Retrieve a listing of files and directories within the current directory
    file_list = []
    ftp.retrlines('LIST ' + directory, file_list.append)

    for line in file_list:
        # Split the line into separate fields
        fields = line.split(maxsplit=8)
        if len(fields) < 6:
            continue

        # Extract the file/directory name
        name = fields[-1].lstrip()

        # Extract the file extension
        file_extension = os.path.splitext(name)[1]
        if file_extension:
            # Retrieve the size of the file
            file_size = ftp.size(directory + '/' + name)
            file_sizes[file_extension] = file_sizes.get(file_extension, 0) + file_size

    return file_sizes


def main():
    # FTP server details
    ftp_host = 'ftp.example.com'
    ftp_user = 'username'
    ftp_password = 'password'

    # Directory to calculate the size
    directory_path = '/path/to/directory/'

    # Connect to the FTP server
    ftp = FTP(ftp_host)
    ftp.login(ftp_user, ftp_password)

    # Calculate the size of the directory
    total_size = get_directory_size(ftp, directory_path)
    size_in_gb = bytes_to_gigabytes(total_size)

    size_for_excel = f'{size_in_gb:.2f} GB'

    # Get the file sizes by type
    file_sizes = get_file_sizes_by_type(ftp, directory_path)

    # Disconnect from the FTP server
    ftp.quit()

    # Print the total size of the directory
    print(f"Total Size: {size_for_excel}")

    # Print the file sizes by type
    print("File Sizes by Type:")
    for file_type, size in file_sizes.items():
        size_in_gb = bytes_to_gigabytes(size)
        print(f"{file_type}: {size_in_gb:.2f} GB")


if __name__ == '__main__':
    main()
