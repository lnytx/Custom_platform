useradd:
 cmd.run:
  - cwd: /soft/EC_MY
  - name: |
#执行多个命令
     git log -p
     echo '123' >> /home/git/123.txt
  - user: git
