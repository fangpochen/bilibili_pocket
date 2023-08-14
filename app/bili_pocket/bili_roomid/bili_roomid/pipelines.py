# useful for handling different item types with a single interface
import datetime
import os
import sqlite3


class BiliRoomIdPipeline:

    def __init__(self) -> None:
        self.rooms_li = []
        basedir = os.path.abspath(os.path.dirname(__file__)).replace(
            "\\app\\bili_pocket\\bili_roomid\\bili_roomid",
            "")
        self.conn = sqlite3.connect(os.path.join(basedir, "app.db"))
        self.cursor = self.conn.cursor()

    def save_room(self, **kwargs):
        room_id = kwargs.get("roomid")
        uuid = kwargs.get("uuid")
        roomblock = kwargs.get("roomblock")
        is_pocket = kwargs.get('if_pocket')
        is_tian = kwargs.get('if_tian')
        total_p = kwargs.get("total_p")
        tag = int(kwargs.get("tag"))
        leave_time = 0
        update_time = datetime.datetime.now()
        end_time = update_time + datetime.timedelta(seconds=30)
        query = "INSERT INTO room (room_id, uuid, roomblock, is_pocket, is_tian, total_p, leave_time, update_time, end_time, tag) VALUES (?, ?, ?, ?, ?, ?, ?, ? ,? ,?)"
        values = (room_id, uuid, roomblock, is_pocket, is_tian, total_p, leave_time, update_time, end_time, tag)
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
        except Exception as e:
            query = "UPDATE room SET uuid = ?, roomblock = ?, is_pocket = ?, is_tian = ?, total_p = ?, leave_time = ?, update_time = ?, end_time = ? , tag=? WHERE room_id = ?"
            values = (uuid, roomblock, is_pocket, is_tian, total_p, leave_time, update_time, end_time, tag, room_id)
            self.cursor.execute(query, values)
            self.conn.commit()

    def close_spider(self, spider):
        index = len(self.rooms_li) / 2
        i = 0
        tag = 0
        for room in self.rooms_li:
            if i > index:
                tag = 1
            self.save_room(tag=tag, **room)
            i += 1
        # 执行插入操作

    def process_item(self, item, spider):
        roomid = item.get('roomid', '')
        roomblock = item.get('roomblock', '')
        uid = item.get('uid', '')
        num_online_person = str(item.get('online_person', ''))
        if_pocket = item.get('if_pocket', '')
        if_tian = item.get('if_tian', '')
        self.rooms_li.append({'roomid': roomid, "roomblock": roomblock, "uuid": uid, "total_p": num_online_person,
                              "if_pocket": if_pocket, "if_tian": if_tian})
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
