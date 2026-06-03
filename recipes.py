class Ingredient:
    def __init__(self, name: str, quantity: float, unit: str):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        value = float(value)
        if value <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = value

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"

    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"

    def __eq__(self, other):
        if not isinstance(other, Ingredient):
            return NotImplemented
        return self.name == other.name and self.unit == other.unit
    

class Recipe:
    def __init__(self, title: str, ingredients=None):
        self.title = title
        self.ingredients = ingredients if ingredients is not None else []

    def add_ingredient(self, ingredient: Ingredient):
        for i in self.ingredients:
            if i == ingredient:
                i.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio):
        return isinstance(ratio, (int, float)) and ratio > 0

    def scale(self, ratio: float):
        if not self.is_valid_ratio(ratio):
            raise ValueError("Коэффициент должен быть положительным числом")

        recipe = Recipe(self.title)

        for i in self.ingredients:
            recipe.add_ingredient(Ingredient(i.name, i.quantity * ratio, i.unit))

        return recipe

    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        st = "; ".join(str(ingredient) for ingredient in self.ingredients)
        return f"{self.title}. Ингредиенты: {st}"
    

class DietaryRecipe(Recipe):
    def __init__(self, title: str, diet_type: str, ingredients=None):
        super().__init__(title, ingredients)
        self.diet_type = diet_type

    def scale(self, ratio: float):
        scale_recipe = super().scale(ratio)

        return DietaryRecipe(scale_recipe.title, self.diet_type, scale_recipe.ingredients)

    def __str__(self):
        st = "; ".join(str(ingredient) for ingredient in self.ingredients)
        return f"[{self.diet_type}] " + super().__str__()
    

class ShoppingList:
    def __init__(self):
        self._items = []

    def add_recipe(self, recipe: Recipe, portions: float):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")

        scale_recipe = recipe.scale(portions)

        for i in scale_recipe.ingredients:
            self._items.append((i, recipe.title))

    def remove_recipe(self, title: str):
        self._items = [item for item in self._items if item[1] != title]

    def get_list(self):
        dict = {}

        for ingredient, _ in self._items:
            key = (ingredient.name, ingredient.unit)

            if key in dict:
                dict[key] += ingredient.quantity
            else:
                dict[key] = ingredient.quantity

        an = [Ingredient(name, quantity, unit) for (name, unit), quantity in dict.items()]
        an.sort(key=lambda ingredient: ingredient.name)

        return an

    def __add__(self, other):
        if not isinstance(other, ShoppingList):
            return NotImplemented
        an = ShoppingList()
        an._items = self._items.copy() + other._items.copy()

        return an