package fr.pact14.s2r;

import java.util.HashMap;
import java.util.List;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.PATCH;
import retrofit2.http.POST;
import retrofit2.http.PUT;
import retrofit2.http.Path;
import retrofit2.http.Query;

public interface JsonApi {

    // ECRAN 2 LOGIN
    // Test POST request at http://pact15.r2.enst.fr/api/backend/helloword that should return Hashmap{hello=world} code 200
    @POST("helloworld")
    Call<HelloWorld> testHelloWorld();

    // POST request at http://pact15.r2.enst.fr/api/backend/login that should return Hashmap{token=...} in case of a successful login and Hashmap{message=...} in case of a login failure
    @POST("login")
    Call<LoginResponse> getLoginResponse(@Body LoginInfoPost loginInfoPost);

    // ECRAN 3 SIGN IN
    // POST request at http://pact15.r2.enst.fr/api/backend/register that should return Hashmap{message=Username <name> registered successfully} code = 201
    @POST("register")
    Call<HashMap> createUserInfoPost(@Body UserInfoPost userInfoPost);

    // ECRAN 4 PROFILE
    // GET request at http://pact15.r2.enst.fr/api/backend/userfromemail?email={mail} that should return Hashmap{user=...}, code 200 (success) et Hashmap{message=No such user found}, code 400 (failure)
    @GET("userfromemail")
    Call<SimpleUserInfoResponse> getUserFromEmail(@Query("email") String userEmail);

    // GET request at http://pact15.r2.enst.fr/api/backend/profile?username={name} that should return a Hashmap with the user info (recipes, supplies, etc.)
    @GET("profile")
    Call<UserInfoPost> getUserInfoPost(@Query("username") String userName);

    // GET request at http://pact15.r2.enst.fr/api/backend/useringredients?username={name} that should return Hashmap{ingredients=...}, code 200
    @GET("useringredients")
    Call<getUserIngredientsResponse> getUserIngredients(@Query("username") String userName);

    // GET request at http://pact15.r2.enst.fr/api/backend/userrecipes?username={name} that should return Hashmap{ingredients=...}, code 200
    @GET("userrecipes")
    Call<getUserRecipesResponse> getUserRecipes(@Query("username") String userName);

    // ECRAN 5 PROFILE EDITOR
    // PATCH request at http://pact15.r2.enst.fr/api/backend/userfromemail?email={userEmail} to change the username
    @PATCH("userfromemail")
    Call<HashMap> changeUserName(@Query("email") String userEmail, @Body String newUsername);

    // IMPLEMENT FOLLOWING
    // ECRAN 6 SUPPLY LIST
    // PATCH request at http://pact15.r2.enst.fr/api/backend/useringredients?username={userName} to update supply list
    @PATCH("useringredients")
    Call<HashMap> updateUserIngredients(@Query("username") String userName,@Body List<Ingredient> ingredients);

    // ECRAN 7 ADD SUPPLY
    // GET request at http://pact15.r2.enst.fr/api/backend/searchingredients?name={name}
    @GET("searchingredients?name={name}")
    Call<HashMap> searchIngredient(@Path("name") String ingredientName, @Body Object token);

    // ECRAN 8 QUICK ADD
    // On prend pour ingrédients les plus utilisés les ingrédients déjà dans le frigo pour le moment

    // ECRAN 9 SCAN ADD
    // Je suppose que c une GET request avec un identifiant récupéré à partir du code barres
    // GET request at http://pact15.r2.enst.fr/api/ai... ?

    // ECRAN 10

    // test GET request at http://pact15.r2.enst.fr/api/ai/ingredients that should return 1 ingredient recipes, code in the 200s
    @GET("ai/?ingredients=[]")
    Call<HashMap> testGetAi();

    // test GET request at http://pact15.r2.enst.fr/api/backend/useringredients
    @GET("useringredients?username={name}")
    Call<HashMap> testGetIngredientsFromBackend(@Path("name") String username);

    @GET("backend/recipebyid?id={id}")
    Call<UserRecipe> getRecipeInfoWithId(@Path("id") int recipe_id, @Body String token);

    @GET("ai")
    Call<List<UserRecipe>> getRecipeSearchResult(@Query("ingredients") String ingredient);

    @PATCH("posts/{id}")
    Call<UserInfoPost> patchUserInfoPost(@Path("id") int id, @Body UserInfoPost userInfoPost);

    @PUT("posts/{id}")
    Call<UserInfoPost> putPost(@Path("id") int id, @Body UserInfoPost userInfoPost);

    @GET("posts")
    Call<List<Post>> getPosts();

    @GET("getunitforingredient?ingredient={ingredientName}")
    Call<HashMap> getUnitForIngredient(@Path("ingredientName") String ingredient_name);

    @POST("addrecipe")
    Call<UserRecipe> addRecipe(@Query("email") String userEmail, @Query("title") String recipeTitle,
                               @Query("instructions") List<String> recipeInstructions,
                               @Query("ingredients") List<Ingredient> recipeIngredients);

}
