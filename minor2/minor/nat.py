from netfilter.rule import Rule,Match,Target
from netfilter.table import Table

rule = Rule(
    in_interface='eth0',
    #protocol='tcp',
    #matches=[Match('tcp')],
    jump=Target('DNAT','--to-destination 192.168.137.1')
)

#rule.jump.options="--to-source 123.123.123.123"

table = Table('nat')
table.append_rule('PREROUTING', rule)
print rule

#table.delete_rule('POSTROUTING', rule)
