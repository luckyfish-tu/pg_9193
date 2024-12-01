import winrm

host = 'http://*.*.*.*:5985/wsman'
user = 'user'
pwd = 'pwd'
s = winrm.Session(host, auth=(user, pwd), transport='ntlm')

# cmd_str='ipconfig'
# cmd_str = 'whoami & ipconfig'
cmd_str = r'bitsadmin /transfer jb1 http://*.*.*.*:8000/1.txt  C:\Users\Administrator\Documents\p1.txt'
rlt = s.run_cmd(cmd_str)

print(f"Status code: {rlt.status_code}")
print(f"Standard Output: {rlt.std_out.decode(('utf-8'))}")
print(f"Standard Error: {rlt.std_err.decode(('utf-8'))}")
