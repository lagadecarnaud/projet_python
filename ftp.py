from ftplib import FTP
def connectionFtp(username : str, password : str,address:str):
    ftp = FTP(address)     # connect to host, default port
    error = ftp.login(username,password)
