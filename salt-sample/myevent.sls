{% set body_json = data['body']|load_json %}
testing_event:
  local.cmd.run:
    - tgt: '*'
    - arg:
       - echo '`date` - {{ data.post.status.description[:37] }} on Host nugget-compute - average cpu.usage {{ data.post.status.metaData.Sample_Value }}' >> /var/log/salt/event/event.log
