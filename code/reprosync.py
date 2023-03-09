import pydicom as dicom
import glob
import sys

d = sys.argv[1]

jsn_fns = glob.glob("../{}/logs/qr_code_flips*_run-*.jsonl".format(d))
funcs = glob.glob("../{}/dcms/*bold*".format(d))

jsn_fns.sort()
funcs.sort()

runz = []

for fn in jsn_fns:
    run = fn.split('_')[-1]
    run = run.split('.')[0]
    for dc in funcs:
        if run in dc:
            runz.append((fn,dc))



for p in runz:
    print("=======================")
    print("Trigger\tDICOM T\tLAG")
    trig_ts = []
    acqu_ts = []
    jsn = p[0]
    fnc = p[1]
    print(jsn,fnc)
    print("Trigger\t\tDICOM T\t\tLAG")
    
    jsn_lines = open(jsn,'r').readlines()

    for ln in jsn_lines:
        d = eval(ln.strip())
        #print(d)
        if d['event'] == 'trigger' and d['keys'][0] == '5':
            flp_t = d['time_flip_formatted'].split('T')[1]
            flp_t = flp_t.split('-')[0]
            hms,dec = flp_t.split('.')
            h,m,s = hms.split(":")
            t = int(h)*3600. + int(m)*60 + int(s) + int(dec)*0.000001 
            trig_ts.append(t)
    dcms = glob.glob("{}/*dcm".format(fnc))
    dcms.sort()
    for dc_fn in dcms:
        dc = dicom.read_file(dc_fn)
        ac_t = str(dc.AcquisitionTime)
        h = int(ac_t[0:2])
        m = int(ac_t[2:4])
        s = int(ac_t[4:6])
        dec = int(ac_t.split('.')[1])
        acqu_ts.append(h*3600. + m*60. + s + dec*0.000001)


    tts = list(zip(trig_ts,acqu_ts))
    for tt in tts:
        print("{}\t{}\t{}".format(tt[0],tt[1],tt[0]-tt[1]))
