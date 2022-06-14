package fr.pact14.s2r;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import java.util.HashMap;
import java.util.List;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class SearchRecipeActivity extends AppCompatActivity {

    private ImageView go_to_profile;
    private ImageView go_to_supplies;
    private ImageView go_to_search;
    private Button go_to_recipe_description;
    private Button validate_search;
    private TextView textViewResult;
    private JsonApi jsonApi;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_search_recipe);

        this.go_to_profile = (ImageView) findViewById(R.id.to_profile_button);
        this.go_to_supplies = (ImageView) findViewById(R.id.to_supplies_button);
        this.go_to_search = (ImageView) findViewById(R.id.to_search_button);
        this.go_to_recipe_description = (Button) findViewById(R.id.to_recipe_description_button);
        this.validate_search = (Button) findViewById(R.id.validate_search);
        this.textViewResult = findViewById(R.id.recipe_search_label);

        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://pact15.r2.enst.fr/api/")
                //.baseUrl("https://jsonplaceholder.typicode.com/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        jsonApi = retrofit.create(JsonApi.class);

        go_to_profile.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent profileActivity = new Intent(getApplicationContext(), ProfileActivity.class);
                startActivity(profileActivity);
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

        go_to_recipe_description.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent recipeDescriptionActivity = new Intent(getApplicationContext(), RecipeDescriptionActivity.class);
                startActivity(recipeDescriptionActivity);
                finish();
            }
        });

        validate_search.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                //getRecipeSearchResult("[]");
                testGetAi();

            }
        });
    }

    public void getRecipeSearchResult(String research_message){

        Call<List<UserRecipe>> call = jsonApi.getRecipeSearchResult(research_message);

        call.enqueue(new Callback<List<UserRecipe>>() {
            @Override
            public void onResponse(Call<List<UserRecipe>> call, Response<List<UserRecipe>> response) {
                textViewResult.append("\n" + "Code: " + response.code() + "\n");
                textViewResult.append("Body: " + response.body() + "\n");
            }

            @Override
            public void onFailure(Call<List<UserRecipe>> call, Throwable t) {
                textViewResult.append("\n" + "Error message: " + t.getMessage());
            }
        });
    }

    public void testGetAi(){

        Call<HashMap> call = jsonApi.testGetAi();

        call.enqueue(new Callback<HashMap>() {
            @Override
            public void onResponse(Call<HashMap> call, Response<HashMap> response) {
                textViewResult.append("\n" + "Code: " + response.code() + "\n");
                textViewResult.append("Body: " + response.body() + "\n");
            }

            @Override
            public void onFailure(Call<HashMap> call, Throwable t) {
                textViewResult.append("\n" + "Error message: " + t.getMessage());
            }
        });
    }
}