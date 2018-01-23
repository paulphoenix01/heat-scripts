testing_event:
  local.cmd.run:
    - tgt: '*'
    - arg:
      - echo '{{ data.post.status.description[:37] }} on Host nugget-compute - average cpu.usage {{ data.post.status.metaData.Sample_Value }}' >> /root/test1.log
