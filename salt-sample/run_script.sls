run_script:
  local.cmd.run:
    - tgt: '*'
    - arg:
      - python /srv/salt/reactor/event_reactor.py
