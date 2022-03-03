import rrdtool

def create(name):
    ret = rrdtool.create('./bd/'+name+".rrd",
                         "--start",'N',
                         "--step",'5m',
                         "DS:ifInNUcastPkts:COUNTER:300:U:U",
                         "DS:ipInDelivers:COUNTER:300:U:U",
                         "DS:icmpOutEchoReps:COUNTER:300:U:U",
                         "DS:tcpOutSegs:COUNTER:300:U:U",
                         "DS:udpInErrors:COUNTER:300:U:U",
                         "RRA:AVERAGE:0.5:1:1d",
                         "RRA:AVERAGE:0.5:1:1d",
                         "RRA:AVERAGE:0.5:1:1d",
                         "RRA:AVERAGE:0.5:1:1d",
                         "RRA:AVERAGE:0.5:1:1d"
                         )
    rrdtool.dump('./bd/'+name+'.rrd','./bd/'+name+'.xml')
    if ret:
        print (rrdtool.error())