git_view_version:
 cmd.run:
  - cwd: /opt/OMS
  - name: git log --stat -1 --abbrev-commit --graph --decorate
