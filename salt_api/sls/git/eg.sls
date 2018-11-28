useradd:
  cmd.run:
    - name: |
        echo '1' >> /home/git/123.txt
        echo '2' >> /home/git/123.txt
        echo '3' >> /home/git/123.txt
        echo '4' >> /home/git/123.txt
    - user: git
————————————————————————————————————————————————————————————————————————————
#minion端的git初始化
git_init:
#添加git用户密码无所谓了，可以使用openssl passwd -1 生成密码
  user.present:
    - fullname: git
    - password: '$6$GD3bcTbx$AzVdltmHxCtPFsGLxJlVK1NePRC/j9LjfMSfcfSCA7igNyo2W05sWcLcX9dwTanTTme3eSqMzvSSVLWaSFMvj1'
    - shell: /usr/local/bin/bash
    - gid_from_name: true#保持uid与gid一致
#    - home: /home/git
#    - uid: 1001
#    - gid: 1001
#    - groups:
#      - wheel
#删除用户
jdoe:
  user.absent:
   - purge: True
   - force: True
  cmd.run:
    - cwd: /soft/EC_MY
    - name: |
        echo '1' >> /home/git/123.txt
        echo '2' >> /home/git/123.txt
        echo '3' >> /home/git/123.txt
        echo '4' >> /home/git/123.txt
    - user: git
——————————————————————————————————————————————————————————————
#修改密码
git:
  user.present:
    - password: cTbx$AzVdltmHxCtPFsGLxJlVK1NePRC/j9Lj
____________________________________________________________

