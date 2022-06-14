package fr.pact14.s2r;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class SupplyListActivity extends AppCompatActivity {

    private ImageView go_to_profile;
    private ImageView go_to_search;
    private ImageView go_to_supplies;
    private Button go_to_add_supply;
    private Button load_supplies;
    private JsonApi jsonApi;
    private TextView textViewResult;
    private Button goToSupplyData;
    private List<Ingredient> ingredients;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_supply_list);


        this.go_to_profile = (ImageView) findViewById(R.id.to_profile_button);
        this.go_to_supplies = (ImageView) findViewById(R.id.to_supplies_button);
        this.go_to_search = (ImageView) findViewById(R.id.to_search_button);
        this.go_to_add_supply = (Button) findViewById(R.id.to_add_supply_button);
        this.load_supplies = (Button) findViewById(R.id.load_supplies_button);
        this.textViewResult = (TextView) findViewById(R.id.supply_list_label);


        RecyclerView rvSupplies = findViewById(R.id.supplies_list);

        //Add a test Recipe for the following code
        GlobalVariables.ingredientList = new ArrayList<Ingredient>();
        int number_of_testRecipe = 15;
        for (int i = 1; i <= number_of_testRecipe; i++){
            GlobalVariables.ingredientList.add(new Ingredient("testIngredient " + i, "testCategory " + i, "testSubCategory " + i, new Ingredient.IngredientProperties(2*i, 1, "testUnit " + i,"")));
        }

        if (GlobalVariables.ingredientList != null) {
            //recipes = Recipe.createRecipesList(GlobalVariables.recipeList.size());
            ingredients = GlobalVariables.ingredientList;
            SuppliesAdapter adapter = new SuppliesAdapter(ingredients);
            rvSupplies.setAdapter(adapter);
            rvSupplies.setLayoutManager(new LinearLayoutManager(this));
        }

        this.goToSupplyData = (Button) findViewById(R.id.change_supply_data);



        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://pact15.r2.enst.fr/api/backend/")
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

        go_to_add_supply.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent addSupplyActivity = new Intent(getApplicationContext(), AddSupplyActivity.class);
                startActivity(addSupplyActivity);
                finish();
            }
        });

        //test of getting userIngredients from backend
        load_supplies.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //testGetSupply("test4");
            }
        });

        //Need to load the supplies from GlobalVariables.ingredientList into RecyclerView

    }

    public void testGetSupply(String username){

        Call<HashMap> call = jsonApi.testGetIngredientsFromBackend(username);

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