import idaapi, idautils, idc
import struct
'''
idaapi.dbg_read_memory(address, size)
segs_gen = idautils.Segments()
segs = [ s for s in segs_gen ]
seg = idaapi.getseg(segs[0])
seg.perm # 권한
idc.get_segm_name(segs[0]) # 이름
''' 
BANNED_PERM = [5,4,1,0]
class Segment:
    def __init__(self,**kwargs):
        self.seg_name = kwargs['name']
        self.seg_start = kwargs['start_addr']
        self.seg_end = kwargs['end_addr']

class ScanResult:
    def __init__(self, **kwargs):
        self.name = kwargs["name"]
        self.addr = kwargs["addr"]
        self.value = kwargs["value"]
        self.prev = kwargs["prev"]
    def set_current_value(self, val):
        self.value = val

class Scanner:
    def __init__(self):
        segs_gen = idautils.Segments()
        self.segs = [ s for s in segs_gen ]
        self.seg_list = []
        for seg in self.segs:
            seg_name = idc.get_segm_name(seg)
            seg_obj = idaapi.getseg(seg)
            if(seg_obj.perm in BANNED_PERM):
                continue
            start_ea = seg_obj.start_ea
            end_ea = seg_obj.end_ea
            self.seg_list.append(
                Segment(
                    name=seg_name, 
                    start_addr=start_ea, 
                    end_addr=end_ea
                )
            )

    def do_scan(self, value):
        self.scan_res = []
        for segment in self.seg_list:
            for addr in range(segment.seg_start, segment.seg_end, 8):
                val = idaapi.dbg_read_memory(addr, 8)
                try:
                    val = struct.unpack("q",val)[0]
                except:
                    continue # NoneType Error Handling
                if(val == int(value)):
                    self.scan_res.append(ScanResult(name=segment.seg_name,addr=addr, value=val, prev=val))
    
    def next_scan(self, value):
        removed_idx = []
        for idx in range(0,len(self.scan_res)):
            val = idaapi.dbg_read_memory(self.scan_res[idx].addr, 8)
            val = struct.unpack("q",val)[0]
            if(val != int(value)):
                removed_idx.append(idx)
            else:
                self.scan_res[idx].set_current_value(val)
        removed_idx.reverse()
        for idx in removed_idx:
            del self.scan_res[idx]

