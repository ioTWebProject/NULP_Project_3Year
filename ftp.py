from pymongo import MongoClient
import ftplib
import gridfs


def refresh():
    #  Connect and login to the FTP server.
    ftp = ftplib.FTP("192.168.0.127")
    ftp.login(user='pi', passwd='feedus321')
    ftp.cwd('/files')
    for filename in get_list(ftp):
        if size_check(filename, ftp):
            fp = grab_file(ftp)
            load_to_db_by_name(fp)
            delete_file(ftp, filename)    


def get_list(ftp):
    # Create list of photos
    files = []

# Print list of files in remote directory
    try:
        files = ftp.nlst()
    except ftplib.error_perm as resp:
        if str(resp) == "550 No files found":
            return tuple()
        else:
            raise

    for line in files:
        print(line)


def size_check(filename, ftp):
    # Check if file exists
    ftp.cwd('/home/pi/ftp/files')
    ftp.sendcmd("TYPE i")
    file_size = ftp.size(filename)
    if file_size < 0:
        print("file does not exist")
    else:
        print("file exists and is " + str(file_size) + " bytes in size")


def grab_file(ftp):
    # Get file from the remote directory
    ftp.cwd('/home/pi/ftp/files')
    filename = "photo.jpg"
    local_file = open(filename, 'rb')
    ftp.retrbinary('RETR' + filename, local_file.write, 1024)
    return filename
 #   ftp.quit()
 #   local_file.close()


def load_to_db_by_name(fp):
    my_db = MongoClient().test
    fs = gridfs.GridFS(my_db)
    # Get file to write to
    fs.put(fp)


def delete_file(ftp, filename):
    ftp.delete(filename)

