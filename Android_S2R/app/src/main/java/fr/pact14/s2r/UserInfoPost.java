package fr.pact14.s2r;

import java.util.List;

public class UserInfoPost {

    private String username;

    private String email;

    private String password;

    private List<UserRecipe> recipeList;

    private List<Ingredient> ingredientList;

    public UserInfoPost(String userName, String email, String password, List<UserRecipe> recipeList, List<Ingredient> ingredientList) {
        this.username = userName;
        this.email = email;
        this.password = password;
        this.ingredientList = ingredientList;
        this.recipeList = recipeList;
    }

    public String getUserName() {
        return username;
    }

    public String getEmail() {
        return email;
    }

    public String getPassword() {
        return password;
    }

    public List<Ingredient> getIngredientList() {
        return ingredientList;
    }

    public List<UserRecipe> getRecipeList() {
        return recipeList;
    }
}
