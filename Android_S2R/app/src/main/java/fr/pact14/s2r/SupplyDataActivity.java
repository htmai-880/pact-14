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

public class SupplyDataActivity extends AppCompatActivity {

    private ImageView go_to_profile;
    private ImageView go_to_supplies;
    private ImageView go_to_search;
    private Button one_day;
    private Button tree_days;
    private Button five_days;
    private Button one_week;
    private Button two_weeks;
    private Button one_month;
    private Button tree_months;
    private Button infinity;
    private Ingredient ingredient;
    private TextView ingredient_name;
    private EditText ingredient_quantity, ingredient_unit, ingredient_category, ingredient_sub_category;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_supply_data);

        this.go_to_profile = (ImageView) findViewById(R.id.to_profile_button);
        this.go_to_supplies = (ImageView) findViewById(R.id.to_supplies_button);
        this.go_to_search = (ImageView) findViewById(R.id.to_search_button);

        this.one_day= (Button) findViewById(R.id.button_1day);
        this.tree_days= (Button) findViewById(R.id.button_3days);
        this.five_days= (Button) findViewById(R.id.button_5days);
        this.tree_months= (Button) findViewById(R.id.button_3months);
        this.one_month= (Button) findViewById(R.id.button_1month);
        this.one_week= (Button) findViewById(R.id.button_1week);
        this.two_weeks= (Button) findViewById(R.id.button_2weeks);
        this.infinity= (Button) findViewById(R.id.button_infinity);

        this.ingredient_name = (TextView) findViewById(R.id.nom_ingredient);
        this.ingredient_quantity = (EditText) findViewById(R.id.quantite_a_entrer);
        this.ingredient_unit = (EditText) findViewById(R.id.unite_a_entrer);
        this.ingredient_category = (EditText) findViewById(R.id.categorie_a_entrer);
        this.ingredient_sub_category = (EditText) findViewById(R.id.subCategory_a_entrer);

        this.ingredient = (Ingredient) GlobalVariables.ingredientToLoad;
        ingredient_name.setText(ingredient.getName());
        //ingredient_quantity.setText(ingredient.getAmount());
        //ingredient_unit.setText(ingredient.getUnit());
        ingredient_category.setText(ingredient.getCategory());
        ingredient_sub_category.setText(ingredient.getSubCategory());


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
}