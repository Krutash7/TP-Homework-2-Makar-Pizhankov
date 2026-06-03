import pytest
from recipes import *


def test_ingredient_creation():
    ingredient = Ingredient("Мука", 500, "г")

    assert ingredient.name == "Мука"
    assert ingredient.quantity == 500.0
    assert ingredient.unit == "г"


def test_ingredient_str():
    ingredient = Ingredient("Мука", 500, "г")

    assert str(ingredient) == "Мука: 500.0 г"

test_cases = [
        (
            Ingredient("Мука", 500, "г"),
            Ingredient("Мука", 1000, "г"),
            True,
        ),
        (
            Ingredient("Мука", 500, "г"),
            Ingredient("Сахар", 500, "г"),
            False,
        ),
        (
            Ingredient("Мука", 500, "г"),
            Ingredient("Мука", 500, "кг"),
            False,
        ),
    ]


@pytest.mark.parametrize("first, second, expected", test_cases)
def test_ingredient_eq(first, second, expected):
    assert (first == second) is expected


@pytest.fixture
def flour():
    return Ingredient("Мука", 500, "г")


@pytest.fixture
def water():
    return Ingredient("Вода", 300, "мл")


@pytest.fixture
def recipe(flour, water):
    recipe = Recipe("Пицца Маргарита")
    recipe.add_ingredient(flour)
    recipe.add_ingredient(water)
    return recipe



def test_recipe_creation():
    recipe = Recipe("Пицца Маргарита")

    assert recipe.title == "Пицца Маргарита"
    assert recipe.ingredients == []


def test_add_new_ingredient():
    recipe = Recipe("Пицца")

    ingredient = Ingredient("Мука", 500, "г")
    recipe.add_ingredient(ingredient)

    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0] == ingredient


def test_add_same_ingredient():
    recipe = Recipe("Пицца")

    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    recipe.add_ingredient(Ingredient("Мука", 200, "г"))

    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].quantity == pytest.approx(700.0)


def test_scale(recipe):
    scale = recipe.scale(2)

    assert scale.ingredients[0].quantity == pytest.approx(1000.0)
    assert scale.ingredients[1].quantity == pytest.approx(600.0)

    assert recipe.ingredients[0].quantity == pytest.approx(500.0)
    assert recipe.ingredients[1].quantity == pytest.approx(300.0)


@pytest.mark.parametrize("ratio", [0, -1, -5])
def test_scale_invalid_ratio(recipe, ratio):
    with pytest.raises(ValueError):
        recipe.scale(ratio)


def test_recipe_len(recipe):
    assert len(recipe) == 2


def test_shoppingList_add_recipe():
    recipe = Recipe("Пицца")
    recipe.add_ingredient(Ingredient("Мука", 500, "г"))

    shopping = ShoppingList()
    shopping.add_recipe(recipe, 2)

    result = shopping.get_list()

    assert len(result) == 1
    assert result[0].quantity == pytest.approx(1000.0)


@pytest.mark.parametrize("portions", [0, -1, -2])
def test_add_recipe_invalid_portions(portions):
    recipe = Recipe("Пицца")

    shopping = ShoppingList()

    with pytest.raises(ValueError):
        shopping.add_recipe(recipe, portions)


def test_remove_recipe():
    recipe1 = Recipe("Маргарита")
    recipe1.add_ingredient(Ingredient("Мука", 500, "г"))

    recipe2 = Recipe("4 Сыра")
    recipe2.add_ingredient(Ingredient("Сыр", 300, "г"))

    shopping = ShoppingList()

    shopping.add_recipe(recipe1, 1)
    shopping.add_recipe(recipe2, 1)

    shopping.remove_recipe("Маргарита")

    result = shopping.get_list()

    assert len(result) == 1
    assert result[0].name == "Сыр"


def test_remove_nonexistent_recipe():
    shopping = ShoppingList()

    recipe = Recipe("Маргарита")
    recipe.add_ingredient(Ingredient("Мука", 500, "г"))

    shopping.add_recipe(recipe, 1)

    shopping.remove_recipe("Не существует")

    result = shopping.get_list()

    assert len(result) == 1
    assert result[0].name == "Мука"
    assert result[0].quantity == pytest.approx(500.0)
    assert result[0].unit == "г"


def test_get_list_sums_same_ingredients():
    recipe1 = Recipe("Маргарита")
    recipe1.add_ingredient(Ingredient("Мука", 500, "г"))

    recipe2 = Recipe("4 Сыра")
    recipe2.add_ingredient(Ingredient("Мука", 300, "г"))

    shopping = ShoppingList()

    shopping.add_recipe(recipe1, 1)
    shopping.add_recipe(recipe2, 1)

    result = shopping.get_list()

    assert len(result) == 1
    assert result[0].quantity == pytest.approx(800.0)


def test_get_list_sorted_by_name():
    recipe = Recipe("Пицца")

    recipe.add_ingredient(Ingredient("Сыр", 200, "г"))
    recipe.add_ingredient(Ingredient("Базилик", 10, "г"))
    recipe.add_ingredient(Ingredient("Мука", 500, "г"))

    shopping = ShoppingList()
    shopping.add_recipe(recipe, 1)

    result = shopping.get_list()

    names = [ingredient.name for ingredient in result]

    assert names == sorted(names)


def test_shopping_list_add():
    recipe1 = Recipe("Маргарита")
    recipe1.add_ingredient(Ingredient("Мука", 500, "г"))

    recipe2 = Recipe("4 Сыра")
    recipe2.add_ingredient(Ingredient("Сыр", 300, "г"))

    shopping1 = ShoppingList()
    shopping1.add_recipe(recipe1, 1)

    shopping2 = ShoppingList()
    shopping2.add_recipe(recipe2, 1)

    shopping3 = shopping1 + shopping2

    result = shopping3.get_list()

    assert len(result) == 2

    names = {ingredient.name for ingredient in result}

    assert names == {"Мука", "Сыр"}


def test_shopping_list_add_does_not_modify_originals():
    recipe1 = Recipe("Маргарита")
    recipe1.add_ingredient(Ingredient("Мука", 500, "г"))

    recipe2 = Recipe("4 Сыра")
    recipe2.add_ingredient(Ingredient("Сыр", 300, "г"))

    shopping1 = ShoppingList()
    shopping1.add_recipe(recipe1, 1)

    shopping2 = ShoppingList()
    shopping2.add_recipe(recipe2, 1)

    _ = shopping1 + shopping2

    assert len(shopping1.get_list()) == 1
    assert len(shopping2.get_list()) == 1