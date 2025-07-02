import ast

import openpyxl

from apps.cmdb.constants import INSTANCE, NEED_CONVERSION_TYPE, ORGANIZATION, USER, ENUM
from apps.cmdb.constants import ModelConstraintKey
from apps.cmdb.graph.neo4j import Neo4jClient


class Import:
    def __init__(self, model_id, attrs, exist_items, operator):
        self.model_id = model_id
        self.attrs = attrs
        self.exist_items = exist_items
        self.operator = operator

    def format_excel_data(self, excel_meta: bytes):
        """格式化excel"""

        need_val_to_id_field_map, need_update_type_field_map = {}, {}

        for attr_info in self.attrs:
            if attr_info["attr_type"] in NEED_CONVERSION_TYPE:
                need_update_type_field_map[attr_info["attr_id"]] = attr_info["attr_type"]
                continue

            if attr_info["attr_type"] in {ORGANIZATION, USER, ENUM}:
                need_val_to_id_field_map[attr_info["attr_id"]] = {i["name"]: i["id"] for i in attr_info["option"]}

        # 读取临时文件
        wb = openpyxl.load_workbook(excel_meta)
        # 获取第一个工作表
        sheet1 = wb.worksheets[0]
        # 获取键
        keys = [cell.value for cell in sheet1[2]]
        result = []
        # 从第4行第1列开始遍历
        for row in sheet1.iter_rows(min_row=3, min_col=0):
            # 创建字典
            item = {"model_id": self.model_id}
            # 遍历每一列
            for i, cell in enumerate(row):
                try:
                    value = ast.literal_eval(cell.value)
                except Exception:
                    value = cell.value

                if not value:
                    continue

                # 将需要类型转换的键和值存入字典
                if keys[i] in need_update_type_field_map:
                    method = NEED_CONVERSION_TYPE[need_update_type_field_map[keys[i]]]
                    item[keys[i]] = method(value)
                    continue

                # 将需要枚举字段name与id反转的建和值存入字典
                if keys[i] in need_val_to_id_field_map:
                    if keys[i] in {ORGANIZATION, USER}:
                        if type(value) != list:
                            value_list = [value]
                        else:
                            value_list = value
                        enum_id = [need_val_to_id_field_map[keys[i]].get(j) for j in value_list]
                    else:
                        enum_id = need_val_to_id_field_map[keys[i]].get(value)
                    if enum_id:
                        item[keys[i]] = enum_id
                    continue

                # 将键和值存入字典
                item[keys[i]] = value
            # 将字典添加到结果列表中
            if not item:
                continue
            result.append(item)
        return result

    def get_check_attr_map(self):
        check_attr_map = dict(is_only={}, is_required={}, editable={})
        for attr in self.attrs:
            if attr[ModelConstraintKey.unique.value]:
                check_attr_map[ModelConstraintKey.unique.value][attr["attr_id"]] = attr["attr_name"]
            if attr[ModelConstraintKey.required.value]:
                check_attr_map[ModelConstraintKey.required.value][attr["attr_id"]] = attr["attr_name"]
            if attr[ModelConstraintKey.editable.value]:
                check_attr_map[ModelConstraintKey.editable.value][attr["attr_id"]] = attr["attr_name"]
        return check_attr_map

    def inst_list_save(self, inst_list):
        """实例列表保存"""

        with Neo4jClient() as ag:
            result = ag.batch_create_entity(INSTANCE, inst_list, self.get_check_attr_map(), self.exist_items,
                                            self.operator)
        return result

    def inst_list_update(self, inst_list):
        """实例列表更新"""

        with Neo4jClient() as ag:
            add_results, update_results = ag.batch_save_entity(INSTANCE, inst_list, self.get_check_attr_map(),
                                                               self.exist_items, self.operator)
        return add_results, update_results

    def import_inst_list(self, file_stream: bytes):
        """将excel主机数据导入"""
        inst_list = self.format_excel_data(file_stream)
        result = self.inst_list_save(inst_list)
        return result

    def import_inst_list_support_edit(self, file_stream: bytes):
        """将excel主机数据导入"""
        inst_list = self.format_excel_data(file_stream)
        return self.inst_list_update(inst_list)
