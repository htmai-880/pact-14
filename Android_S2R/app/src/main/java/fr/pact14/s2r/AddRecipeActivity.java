package fr.pact14.s2r;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.List;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class AddRecipeActivity extends AppCompatActivity {

    private ImageView go_to_profile;
    private ImageView go_to_supplies;
    private ImageView go_to_search;
    private Button validateNewRecipe;
    private JsonApi jsonApi;
    private EditText recipe_name_edit_text;
    private EditText ingredient_name;
    private EditText recipe_quantity_edit_text;
    private EditText recipe_unit_edit_text;
    private EditText recipe_instructions;
    private TextView debug_textview;
    private Button cancel_button;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_recipe);

        this.go_to_profile = (ImageView) findViewById(R.id.to_profile_button);
        this.go_to_supplies = (ImageView) findViewById(R.id.to_supplies_button);
        this.go_to_search = (ImageView) findViewById(R.id.to_search_button);
        this.validateNewRecipe = (Button) findViewById(R.id.confirm_recipe_button);
        this.recipe_name_edit_text = (EditText) findViewById(R.id.username2);
        this.ingredient_name = (EditText) findViewById(R.id.recipe_name_edit_text);
        this.recipe_quantity_edit_text = (EditText) findViewById(R.id.recipe_quantity_edit_text);
        this.recipe_unit_edit_text = (EditText) findViewById(R.id.recipe_unity_edit_text);
        this.recipe_instructions = (EditText) findViewById(R.id.username4);
        this.debug_textview = (TextView) findViewById(R.id.debug_recipe);
        this.cancel_button = (Button) findViewById(R.id.cancel_recipe_button);

        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://pact15.r2.enst.fr/api/backend/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        jsonApi = retrofit.create(JsonApi.class);

        cancel_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                recipe_name_edit_text.setText("");
                ingredient_name.setText("");
                recipe_quantity_edit_text.setText("");
                recipe_unit_edit_text.setText("");
                recipe_instructions.setText("");
            }
        });

        validateNewRecipe.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String uEmail = GlobalVariables.currentUserEmail;
                String rcTitle = recipe_name_edit_text.getText().toString();
                List<String> rcInstructions = new ArrayList<String>();
                rcInstructions.add(recipe_instructions.getText().toString());
                List<Ingredient> ingredientsList = new ArrayList<Ingredient>();
                int qte = Integer.parseInt(recipe_quantity_edit_text.getText().toString());
                Ingredient onlyIngredient = new Ingredient(ingredient_name.getText().toString(), null, null, new Ingredient.IngredientProperties(1,qte, recipe_unit_edit_text.getText().toString(), ""));
                postNewRecipe(uEmail, rcTitle, rcInstructions, ingredientsList);
            }
        });


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
    }

    private void postNewRecipe(String userEmail, String recipeTitle, List<String> recipeInstructions, List<Ingredient> recipeIngredients) {
        Call<UserRecipe> call = jsonApi.addRecipe(userEmail, recipeTitle, recipeInstructions, recipeIngredients);

        call.enqueue(new Callback<UserRecipe>() {
            @Override
            public void onResponse(Call<UserRecipe> call, Response<UserRecipe> response) {
                debug_textview.append("\n" + "Response code: " + response.code() + "\n");
                debug_textview.append("Response body: " + response.body() + "\n");
            }

            @Override
            public void onFailure(Call<UserRecipe> call, Throwable t) {
                debug_textview.append("\n" + "Error message: " + t.getMessage());
            }
        });
    }
}