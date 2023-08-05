
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class BiliRoomIdPipeline:

    def __init__(self) -> None:
        self.rooms_li = []

    def close_spider(self, spider):
        with open('../RoomsId_during.txt','w') as f:
            f.writelines(self.rooms_li)
 
    def process_item(self, item, spider):
        roomid = item.get('roomid','')
        roomblock = item.get('roomblock','')
        self.rooms_li.append(str(roomid)+' '+ roomblock + '\n')
        return item