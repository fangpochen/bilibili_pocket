
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class BiliRoomIdPipeline:

    def __init__(self) -> None:
        self.rooms_li = []

    def close_spider(self, spider):
        self.rooms_li = self._deldupliroom(self.rooms_li)
        with open('../RoomsId_during.txt','w') as f:
            f.writelines(self.rooms_li)
 
    def process_item(self, item, spider):
        roomid = item.get('roomid','')
        roomblock = item.get('roomblock','')
        uid = item.get('uid','')
        self.rooms_li.append(str(roomid)+' '+ str(uid) + ' ' + roomblock + '\n')
        return item
    
    def _deldupliroom(self, room_li):
        cur_room_li = []
        final_room_li = []
        for room_line in room_li:
            room_id = room_line.split(' ')[0]
            if room_id in cur_room_li:
                print('filter room line', room_line)
                continue
            else:
                cur_room_li.append(room_id)
                final_room_li.append(room_line)
        return final_room_li