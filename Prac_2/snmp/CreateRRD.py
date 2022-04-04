import rrdtool

def create(name):
    ret = rrdtool.create('./bd/'+name+".rrd",
                         "--start",'N',
                         "--step",'1m',
                         "DS:tcpInSegs:COUNTER:120:U:U",
                         "DS:tcpOutSegs:COUNTER:120:U:U",
                         "RRA:LAST:0.5:1:1d"
                         )
    rrdtool.dump('./bd/'+name+'.rrd','./bd/'+name+'.xml')
    if ret:
        print (rrdtool.error())