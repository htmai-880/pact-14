package fr.pact14.s2r;

import java.util.ArrayList;
import java.util.List;

public class UserRecipe {

    //userrecipes?username=Rion
    //{'user_recipes': [{'id': 0, 'instructions': ['Mix everything at once.', 'Eat.', 'Perish.'], 'provenance': "Rion's deadly recipes", 'title': 'Blessed dip'}, {'id': 26, 'instructions': ['Mix everything.', 'Serve.'], 'provenance': "Rion's deadly recipes", 'title': 'Cursed dip'}]}

    private String title;

    private int id;

    private List<String> instructions;

    private String provenance;

    public UserRecipe(String recipeName, int recipeId, List<String> recipeInstructions, String recipeProvenance){
        title = recipeName;
        id = recipeId;
        instructions = recipeInstructions;
        provenance = recipeProvenance;
    }

    private List<Ingredient> ingredients;

    /*private ArrayList<String> Instructions;*/
    public String getRecipeName(){
        return title;
    }

    private static int lastRecipeId =0;

    public static ArrayList<UserRecipe> createRecipesList(int numRecipes){
        ArrayList<UserRecipe> recipes = new ArrayList<UserRecipe>();

        for (int i =1; i<= numRecipes; i++){
            recipes.add(new UserRecipe("Recipe " + ++lastRecipeId, lastRecipeId, new ArrayList<String>(), ""));
        }
        return recipes;
    }
}
