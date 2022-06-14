package fr.pact14.s2r;

import android.content.Context;
import android.content.Intent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.RecyclerView;

import java.util.List;

public class SuppliesAdapter extends RecyclerView.Adapter<SuppliesAdapter.ViewHolder> {

    private List<Ingredient> mSupplies;
    private Context context;

    public SuppliesAdapter(List<Ingredient> supplies){
        mSupplies = supplies;
    }

    public class ViewHolder extends RecyclerView.ViewHolder{
        public TextView supplyNameTextView;
        public Button go_to_supply_button;
        public Button delete_supply_button;

        public ViewHolder(View itemView){
            super(itemView);

            supplyNameTextView = (TextView) itemView.findViewById(R.id.supply_name);
            go_to_supply_button = (Button) itemView.findViewById(R.id.change_supply_data);
            delete_supply_button = (Button) itemView.findViewById(R.id.delete_supply);

            context = itemView.getContext();
        }
    }

    @Override
    public SuppliesAdapter.ViewHolder onCreateViewHolder(ViewGroup parent, int viewType){
        Context context = parent.getContext();
        LayoutInflater inflater = LayoutInflater.from(context);

        View supplyView = inflater.inflate(R.layout.supply_item, parent, false);

        ViewHolder viewHolder = new ViewHolder(supplyView);
        return viewHolder;
    }

    @Override
    public void onBindViewHolder(SuppliesAdapter.ViewHolder holder, int position) {
        Ingredient supply = mSupplies.get(position);

        TextView textView = holder.supplyNameTextView;
        textView.setText(supply.getName());
        Button change_data_button = holder.go_to_supply_button;
        Button suppress_ingredient_button = holder.delete_supply_button;



        change_data_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //textView.setText("nick" + position);
                final Intent intent;
                intent = new Intent(context, SupplyDataActivity.class);
                GlobalVariables.ingredientToLoad = supply;
                context.startActivity(intent);


                //ProfileActivity.switchToDescription();
            }
        });

        suppress_ingredient_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //textView.setText("nick" + position);
                //GlobalVariables.ingredientList.remove(holder.getAdapterPosition());
                deleteItem(holder.getAdapterPosition());
                System.out.println(GlobalVariables.ingredientList);
            }
        });

    }

    public int getItemCount(){
        return mSupplies.size();
    }

    void deleteItem(int index) {
        mSupplies.remove(index);
        notifyItemRemoved(index);
    }


}