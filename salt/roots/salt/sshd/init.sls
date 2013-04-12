ssh:
    pkg.installed:
        - name: openssh-server
    service.running:
        - enable: True
        - watch:
            - file: ssh
            - pkg: ssh
    require:
      - group: login 

/etc/ssh/sshd_config:
    file.managed:
        - source: salt://sshd/sshd_config
        - user: root
        - mode: 644

openssh-client:
    pkg.installed


# Github's server public key
/etc/ssh/ssh_known_hosts:
    file.managed:
        - source: salt://sshd/ssh_known_hosts
        - user: root
        - mode: 644
        - require:
            - pkg: openssh-client

login:
    group.present:
        - name: login
        - system: True
