from collections import deque

inout={}
flipflops={}
cmodules = {}

for line in open(0).readlines():
    if line:=line.strip():
        i, o = line.split(" -> ")
        t=None
        if i.startswith("%") or i.startswith("&"):
            t=i[0]
            i=i[1:]
        if t == "%": flipflops[i] = 0
        elif t == "&": cmodules[i] = {}
        inout[i] = (t, o.split(", "))

for i,(_,o) in inout.items():
    for om in o:
        if om in inout:
            omt, _ = inout[om]
            if omt == "&": cmodules[om][i] = 0

highs, lows = 0,0
rx=0
Q = deque()
def run():
    global highs, lows,rx
    Q.append(("button", "broadcaster", 0))
    while Q:
        emitter, target, lh = Q.popleft()
        #print(emitter, target, lh, inout.get(target))
        if lh == 0:
            lows+=1
            if target == "rx":
                rx+=1
        else:
            highs += 1
        if target in inout:
            t, o = inout[target]
            if t == "%":
                if lh == 1: continue
                if flipflops[target] == 1:
                    flipflops[target] = 0
                    newpulse = 0
                else:
                    flipflops[target] = 1
                    newpulse=1
            elif t == "&":
                cmodules[target][emitter] = lh
                if all(v==1 for v in cmodules[target].values()):
                    newpulse=0
                else:
                    newpulse =1
            elif target == "broadcaster":
                newpulse = lh
            else:
                assert False

            for om in o:
                Q.append((target, om, newpulse))

for _ in range(1000):
    run()

print(lows * highs)

