
class sbkTools():
    def get_one(self, ModlesObj, **kwargs):
        """获取单条记录数据对象"""
        return ModlesObj.objects.get(**kwargs)

    def get_many(self, ModlesObj, **kwargs):
        """获取模型类序列化后参数"""
        return ModlesObj.objects.filter(**kwargs)

    def save_one(self, ModlesObj, **kwargs):
        """新增数据数据"""
        return ModlesObj.objects.create(**kwargs)
