# core/potions.py
class PotionSystem:
    def __init__(self, game_state):
        self.state = game_state
        self.ingredients = {
            "ajenjo": {"potency": 3, "rarity": 1},
            "asfódelo": {"potency": 2, "rarity": 1},
            "bezoar": {"potency": 5, "rarity": 3},
            "crisopos": {"potency": 4, "rarity": 2},
            "díctamo": {"potency": 4, "rarity": 2},
            "flores de lavanda": {"potency": 2, "rarity": 1},
            "raíz de mandrágora": {"potency": 5, "rarity": 3},
            "cuerno de unicornio": {"potency": 6, "rarity": 4}
        }

        self.recipes = {
            "Poción curativa": {
                "ingredients": ["díctamo", "bezoar"],
                "difficulty": 2,
                "effect": "Cura heridas menores y restaura energía"
            },
            "Filtro de paz": {
                "ingredients": ["ajenjo", "flores de lavanda"],
                "difficulty": 1,
                "effect": "Calma la ansiedad y reduce el estrés"
            },
            "Poción vigorizante": {
                "ingredients": ["crisopos", "asfódelo"],
                "difficulty": 3,
                "effect": "Aumenta temporalmente la energía y concentración"
            }
        }

    def brew_potion(self, ingredients_list):
        # Verificar ingredientes
        valid_ingredients = []
        for ingredient in ingredients_list:
            if ingredient.lower() in self.ingredients:
                valid_ingredients.append(ingredient.lower())
            else:
                return f"'{ingredient}' no es un ingrediente conocido."

        # Verificar si los ingredientes coinciden con alguna receta
        for potion_name, recipe in self.recipes.items():
            # Compara los ingredientes (sin importar el orden)
            if set(valid_ingredients) == set(recipe["ingredients"]):
                # Éxito! Poción creada
                self.state.inventory.append(potion_name)

                # Actualizar atributos
                if "inteligencia" in self.state.attributes:
                    self.state.attributes["inteligencia"] += 1
                else:
                    self.state.attributes["inteligencia"] = 1

                return f"¡Has creado correctamente {potion_name}! {recipe['effect']}. Tu inteligencia ha aumentado."

        # Si llegamos aquí, los ingredientes no coinciden con ninguna receta
        return "Estos ingredientes no crean ninguna poción conocida. Intenta con otra combinación."