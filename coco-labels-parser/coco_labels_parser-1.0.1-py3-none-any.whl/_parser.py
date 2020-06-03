import os
import json
import shutil

class CocoBoxesParser(object):
    def __init__(self,instances_json_path,labels_text_path):
        super(CocoBoxesParser,self).__init__()
        self.instances_json_path = instances_json_path
        if not os.path.isfile(self.instances_json_path):
            print(f"{self.instances_json_path} not found!")
            exit(0)

        self.labels_text_path = labels_text_path
        if not os.path.exists(self.labels_text_path):
            os.makedirs(self.labels_text_path)
        else:
            shutil.rmtree(self.labels_text_path)
            os.mkdir(self.labels_text_path)
        print(f"Loading {self.instances_json_path} ...")
        self.json_data = json.loads(open(self.instances_json_path).read())
        self.keys_list = list(self.json_data.keys())
        print(self.keys_list)
        self.imgs_len,self.labels_len = self.json_data["images"].__len__(),self.json_data["annotations"].__len__()
        print(f"img len:{self.imgs_len},labels len:{self.labels_len}")
    def get_categories_id(self):
        categories_list = self.json_data["categories"]
        with open("categories_ids.txt","w") as fp:
            for id,item_dict in enumerate(categories_list):
                cls_super,cls_id,cls_name = item_dict["supercategory"],item_dict["id"],item_dict["name"]
                fp.write(f"{cls_id}\t{cls_name}\t{cls_super}\n")
        print(f"Generating Category Done....")
    def get_labels(self):
        print(f"label text message:")
        print(f"cls_id box_topx box_topy box_w box_h img_w img_h")
        for id, img_dict in enumerate(self.json_data["images"]):
            img_id, img_name = img_dict["id"], img_dict["file_name"]
            bboxes = [[anno_msg_dict['bbox'], anno_msg_dict["category_id"]] for anno_msg_dict in self.json_data["annotations"] if
                      anno_msg_dict['image_id'] == img_id and anno_msg_dict['bbox']]
            if bboxes:
                for bb in bboxes:
                    (x, y, w, h), cls_id = bb[0], bb[1]
                    with open(f"{self.labels_text_path}/{img_name[:-4]}.txt", "a") as fp:
                        img_w, img_h = img_dict["width"], img_dict["height"]
                        fp.write(f"{cls_id} {x} {y} {w} {h} {img_w} {img_h}\n")
            if (id + 1) % 100 == 0:
                print(f"processing:{id + 1}")
        print(f"Done...")