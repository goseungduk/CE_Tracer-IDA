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
UNIT_UNPACK_BYTE = {
    "1": "b",
    "4": "i",
    "8": "q"
}
ELF_BANNED_SEGMENT_KEYWORD = [".so", "got", "LOAD"]

class Scanner:
    def __init__(self):
        segs_gen = idautils.Segments()
        self.segs = [ s for s in segs_gen ]
        self.seg_list = []
        for seg in self.segs:
            seg_obj = idaapi.getseg(seg)
            if(seg_obj.perm & 2 == 0):
                continue
            seg_name = idc.get_segm_name(seg)
            start_ea = seg_obj.start_ea
            end_ea = seg_obj.end_ea
            self.seg_list.append(
                {
                    "name":seg_name, 
                    "start_addr":start_ea, 
                    "end_addr":end_ea
                }
            )

    def do_scan(self, value, byte_split):
        self.scan_res = []
        for segment in self.seg_list:
            for addr in range(segment["start_addr"], segment["end_addr"], int(byte_split)):
                val = idaapi.dbg_read_memory(addr, int(byte_split))
                try:
                    val = struct.unpack(UNIT_UNPACK_BYTE[byte_split], val)[0]
                except:
                    continue # NoneType Error Handling
                if(val == int(value)):
                    self.scan_res.append({
                        "name":segment["name"],
                        "addr":addr, 
                        "value":val, 
                        "prev":val
                    })
    
    def next_scan(self, value, byte_split):
        removed_idx = []
        for idx in range(0,len(self.scan_res)):
            val = idaapi.dbg_read_memory(self.scan_res[idx]["addr"], int(byte_split))
            val = struct.unpack(UNIT_UNPACK_BYTE[byte_split],val)[0]
            if(val != int(value)):
                removed_idx.append(idx)
            else:
                self.scan_res[idx]["value"] = val
        removed_idx.reverse()
        for idx in removed_idx:
            del self.scan_res[idx]

