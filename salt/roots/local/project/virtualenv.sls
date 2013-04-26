project_user:
  user.present:
    - name: {{ pillar['project_name'] }}
    - groups: [www-data]

# /home/django/mysite.com:
#   virtualenv.managed:
#     - no_site_packages: True
#     - requirements: /home/django/mysite.com/src/mysite/requirements.txt
