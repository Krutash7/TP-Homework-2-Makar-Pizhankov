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

vegan_pizza = DietaryRecipe(
    "Пицца Маргарита",
    "веган"
)

vegan_pizza.add_ingredient(Ingredient("Мука", 500, "г"))
vegan_pizza.add_ingredient(Ingredient("Вода", 300, "мл"))

print(vegan_pizza)

double_pizza = vegan_pizza.scale(2)

print(double_pizza)