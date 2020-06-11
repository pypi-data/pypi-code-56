import scrapy


class BaseItem(scrapy.Item):
    # 保存到mongo中的_id
    _id = scrapy.Field()
    # 数据id
    id = scrapy.Field()
    # 数据类型
    data_type = scrapy.Field()
    # 任务id
    task_id = scrapy.Field()
    name = scrapy.Field()
    insert_time = scrapy.Field()