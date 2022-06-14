package fr.pact14.s2r;

import android.content.Context;
import android.content.Intent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

import androidx.recyclerview.widget.RecyclerView;

import java.util.List;

public class RecipesAdapter extends RecyclerView.Adapter<RecipesAdapter.ViewHolder> {

    private List<UserRecipe> mRecipes;
    private Context context;

    public RecipesAdapter(List<UserRecipe> recipes){
        mRecipes = recipes;
    }
    public class ViewHolder extends RecyclerView.ViewHolder{
        public TextView recipeNameTextView;
        public Button go_to_recipe_button;

        public ViewHolder(View itemView){
            super(itemView);

            recipeNameTextView = (TextView) itemView.findViewById(R.id.recipe_title);
            go_to_recipe_button = (Button) itemView.findViewById(R.id.go_to_recipe_button);

            context = itemView.getContext();
        }
    }

    @Override
    public RecipesAdapter.ViewHolder onCreateViewHolder(ViewGroup parent, int viewType){
        Context context = parent.getContext();
        LayoutInflater inflater = LayoutInflater.from(context);

        View recipeView = inflater.inflate(R.layout.recipe_item, parent, false);

        ViewHolder viewHolder = new ViewHolder(recipeView);
        return viewHolder;
    }

    @Override
    public void onBindViewHolder(RecipesAdapter.ViewHolder holder, int position) {
        UserRecipe recipe = mRecipes.get(position);

        TextView textView = holder.recipeNameTextView;
        textView.setText(recipe.getRecipeName());
        Button button = holder.go_to_recipe_button;



        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //textView.setText("nick" + position);
                final Intent intent;
                intent = new Intent(context, RecipeDescriptionActivity.class);
                GlobalVariables.recipeToLoad = recipe;
                context.startActivity(intent);


                //ProfileActivity.switchToDescription();
            }
        });
    }

    public int getItemCount(){
        return mRecipes.size();
    }


}
