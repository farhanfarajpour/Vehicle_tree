from vehicle_tree_app.repositories.base_repo import BaseRepo
from vehicle_tree_app.schemas.tree import MenuTreeModelSchema, UpdateMenuTreeModelSchema
from vehicle_tree_app.schemas.users import UpdateUserSchema
from vehicle_tree_app.services.sms.tasks import SendSms
from vehicle_tree_app.models.menus import MenusTree
from typing import List, Optional
from django.db.transaction import atomic
from vehicle_tree_app.models.vehicle import Vehicle
from vehicle_tree_app.models.company import Company


class MenusTreeRepo(BaseRepo):

    # ORM postgresql
    @atomic
    def get_all_tree(self) -> MenusTree:
        return MenusTree.objects.all()

    def get_item_by_id(self, id: int) -> Optional[MenusTree]:
        menu = MenusTree.objects.filter(id=id).first()
        if menu:
            return menu
        return False

    def create_item(self, data: MenuTreeModelSchema) -> Optional[MenusTree]:
        parent_item = self.get_item_by_id(data.parent_id)
        if parent_item:
            new_menu = MenusTree.objects.create(parent_id=parent_item.id, node_name_en=data.node_name_en,
                                                node_name_fa=data.node_name_fa)
            return new_menu

    def update_tree(self, data: UpdateMenuTreeModelSchema) -> Optional[MenusTree]:
        item = self.get_item_by_id(data.id)
        update_data = data.dict(exclude_unset=True)
        for attr, value in update_data.items():
            setattr(item, attr, value)
        item.save()
        return item

    def delete_tree(self, id: int):
        item = self.get_item_by_id(id)
        if item:
            item.delete()
            return True
        else:
            return False
