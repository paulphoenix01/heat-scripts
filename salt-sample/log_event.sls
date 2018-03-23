testing_event:
  local.cmd.run:
    - tgt: '*'
    - arg:
       - echo '{{ data.post.status.description[:37] }},{{ data.post.status.metaData.Sample_Value }}' >> /var/log/salt/event/{{ data.post.status.description[:37] }}.log
