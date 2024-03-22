import pytest

from apps.core.tests.base_test import BaseModelsTest
from apps.financial_manager.models import Category
from apps.financial_manager.tests.factories import CategoryFactory


class CategoryModelTests(BaseModelsTest):
    def test_create_category_model_instance(self):
        # Given
        expected_attrs = [
            "user",
            "name",
            "description",
            "created_at",
            "updated_at",
            "id",
        ]

        # When
        category = CategoryFactory()
        db_categories = Category.objects.all()
        db_category = db_categories.first()

        # Then
        self.assertIsInstance(category, Category)
        self.assertEqual(len(db_categories), 1)
        self.assertEqual(str(db_category), category.name)

        for attr_name in expected_attrs:
            with self.subTest(attr=attr_name):
                self.assertHasAttr(category, attr_name)
                category_attr = getattr(category, attr_name)
                db_category_attr = getattr(db_category, attr_name)
                self.assertEqual(category_attr, db_category_attr)

    def test_category_model_meta_verbose_names(self):
        # Then
        self.assertEqual(Category._meta.verbose_name, "Categoria")
        self.assertEqual(Category._meta.verbose_name_plural, "Categorias")


@pytest.mark.parametrize("attr_name", ["user", "name"])
def test_create_category_raise_exception_without_required_fields(attr_name):
    # Given
    test_data = {attr_name: None}

    # Then
    with CategoryModelTests().assertRaises(Exception):
        Category.objects.create(**test_data)
