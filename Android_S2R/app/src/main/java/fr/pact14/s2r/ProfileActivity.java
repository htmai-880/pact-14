package fr.pact14.s2r;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.List;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

import static fr.pact14.s2r.ProfileEditorActivity.b;

public class ProfileActivity extends AppCompatActivity {

    private ImageView  go_to_profile_editor;
    private ImageView go_to_supplies;
    private ImageView go_to_search;
    private ImageView profile_picture;
    private JsonApi jsonApi;
    private ImageView disconnect_button;
    private ListViewModel listViewModel;
    //private ArrayList<Recipe> recipes;
    private List<UserRecipe> recipes;
    private Button goToRecipe;
    private TextView identifiant;
    private ImageView add_recipe_btn;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_profile);

        this.go_to_supplies = (ImageView) findViewById(R.id.to_supplies_button);
        this.go_to_search = (ImageView) findViewById(R.id.to_search_button);
        this.go_to_profile_editor = (ImageView ) findViewById(R.id.to_profile_editor_button);
        this.profile_picture = (ImageView) findViewById(R.id.profile_picture);
        this.disconnect_button = (ImageView) findViewById(R.id.disconnect_button);
        this.identifiant = (TextView) findViewById(R.id.id_text_profile2);
        this.add_recipe_btn = (ImageView) findViewById(R.id.add_recipe_btn);

        add_recipe_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent addRecipe = new Intent(getApplicationContext(), AddRecipeActivity.class);
                startActivity(addRecipe);
                finish();
            }
        });



        RecyclerView rvRecipes = findViewById(R.id.favorite_recipies_list);

        //Add a test Recipe for the following code
        GlobalVariables.recipeList = new ArrayList<UserRecipe>();
        int number_of_testRecipe = 15;
        for (int i = 1; i <= number_of_testRecipe; i++){
            GlobalVariables.recipeList.add(new UserRecipe("testRecipe " + i, i*i, new ArrayList<String>(), "provenanceTest " + i));
        }

        if (GlobalVariables.recipeList != null) {
            //recipes = Recipe.createRecipesList(GlobalVariables.recipeList.size());
            recipes = GlobalVariables.recipeList;
            RecipesAdapter adapter = new RecipesAdapter(recipes);
            rvRecipes.setAdapter(adapter);
            rvRecipes.setLayoutManager(new LinearLayoutManager(this));
        }

        this.goToRecipe = (Button) findViewById(R.id.go_to_recipe_button);

        /*goToRecipe.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent RecipeDescription = new Intent(getApplicationContext(), RecipeDescriptionActivity.class );
                startActivity(RecipeDescription);
                finish();
            }
        });*/


        /*recyclerView.setLayoutManager(new LinearLayoutManager(this));
        recyclerView.setHasFixedSize(true);*/

        /*ListAdapter adapter = new ListAdapter();
        recyclerView.setAdapter(adapter);

        listViewModel = ViewModelProviders.of(this).get(ListViewModel.class);
        listViewModel.getAllLists().observe(this, new Observer<List<fr.pact14.s2r.List>>() {
            @Override
            public void onChanged(java.util.List<fr.pact14.s2r.List> lists) {
                adapter.setLists(lists);
            }
        });*/



        profile_picture.setImageBitmap(b);

        disconnect_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent loginActivity = new Intent(getApplicationContext(), LoginActivity.class);
                startActivity(loginActivity);
                finish();
            }
        });

        go_to_profile_editor.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent profileEditorActivity = new Intent(getApplicationContext(), ProfileEditorActivity.class);
                startActivity(profileEditorActivity);
                finish();
            }
        });

        go_to_supplies.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent supplyListActivity = new Intent(getApplicationContext(), SupplyListActivity.class);
                startActivity(supplyListActivity);
                finish();
            }
        });

        go_to_search.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent searchRecipeActivity = new Intent(getApplicationContext(), SearchRecipeActivity.class);
                startActivity(searchRecipeActivity);
                finish();
            }
        });

        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://pact15.r2.enst.fr/api/backend/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        jsonApi = retrofit.create(JsonApi.class);

        identifiant.setText(GlobalVariables.currentUserName);

        //getUserFromEmail();

        //getUserInfo();

        getUserIngredients();

        getUserRecipes();

        //Need to load user recipes from GlobalVariables.recipeLikedList into RecyclerView

    }

    // marche pas encore faut que tan merge
    private void getUserRecipes() {
        Call<getUserRecipesResponse> call = jsonApi.getUserRecipes(GlobalVariables.currentUserName);

        call.enqueue(new Callback<getUserRecipesResponse>() {
            @Override
            public void onResponse(Call<getUserRecipesResponse> call, Response<getUserRecipesResponse> response) {
                System.out.println("Response code: " + response.code());
                System.out.println("Response body: " + response.body());
                System.out.println("User recipes: " + response.body().getRecipes());
            }

            @Override
            public void onFailure(Call<getUserRecipesResponse> call, Throwable t) {
                System.out.println("Error message: " + t.getMessage());
            }
        });
    }

    //IS DONE AT THE END OF LAST ACTIVITY (LOGIN/LOADING SCREEN BIS) TO HAVE THE RIGHT GLOBAL VARIABLES (DUE TO ASYNCHRONOUS PROCESSES)
    /*public void getUserFromEmail() {

        Call<SimpleUserInfoResponse> call = jsonApi.getUserFromEmail(GlobalVariables.currentUserEmail);

        call.enqueue(new Callback<SimpleUserInfoResponse>() {
            @Override
            public void onResponse(Call<SimpleUserInfoResponse> call, Response<SimpleUserInfoResponse> response) {
                System.out.println(response.code());
                System.out.println(response.body());
                UserInfoPost user = response.body().getUser();
                System.out.println(user);
                GlobalVariables.currentUserName = user.getUserName();
                GlobalVariables.ingredientList = user.getIngredientList();
                GlobalVariables.recipeList = user.getRecipeList();
                System.out.println(GlobalVariables.currentUserName);
                System.out.println(GlobalVariables.ingredientList);
                System.out.println(GlobalVariables.recipeList);
                identifiant.setText(GlobalVariables.currentUserName);
            }

            @Override
            public void onFailure(Call<SimpleUserInfoResponse> call, Throwable t) {
                System.out.println(t.getMessage());
            }
        });

    }*/

    public void getUserInfo() {

        Call<UserInfoPost> call = jsonApi.getUserInfoPost(GlobalVariables.currentUserName);

        call.enqueue(new Callback<UserInfoPost>() {
            @Override
            public void onResponse(Call<UserInfoPost> call, Response<UserInfoPost> response) {
                System.out.println("Response code: " + response.code());
                System.out.println("Response body: " + response.body());
            }

            @Override
            public void onFailure(Call<UserInfoPost> call, Throwable t) {
                System.out.println("Error message: " + t.getMessage());
            }
        });

    }

    public void getUserIngredients() {

        Call<getUserIngredientsResponse> call = jsonApi.getUserIngredients(GlobalVariables.currentUserName);

        call.enqueue(new Callback<getUserIngredientsResponse>() {
            @Override
            public void onResponse(Call<getUserIngredientsResponse> call, Response<getUserIngredientsResponse> response) {
                System.out.println("Response code: " + response.code());
                System.out.println("Response body: " + response.body());
                System.out.println("User ingredients: " + response.body().getIngredients());
            }

            @Override
            public void onFailure(Call<getUserIngredientsResponse> call, Throwable t) {
                System.out.println("Error message: " + t.getMessage());
            }
        });

    }


}