package fr.pact14.s2r;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;
import java.util.List;

public class ListAdapter extends RecyclerView.Adapter<ListAdapter.ListHolder>{
    private List<fr.pact14.s2r.List> lists = new ArrayList<>();

    @NonNull
    @Override
    public ListHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext()).inflate(R.layout.recipe_test,parent,false);
        return new ListHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull ListHolder holder, int position) {
        fr.pact14.s2r.List currentList = lists.get(position);
        holder.textViewTitle.setText(currentList.getTitle());
        holder.textViewPriority.setText(String.valueOf(currentList.getPriority()));

    }

    @Override
    public int getItemCount() {
        return lists.size();
    }

    public void setLists(List<fr.pact14.s2r.List> lists){
        this.lists = lists;
        notifyDataSetChanged();
    }

    class ListHolder extends RecyclerView.ViewHolder{
        private TextView textViewTitle;
        private TextView textViewPriority;

        public ListHolder(@NonNull View itemView) {
            super(itemView);
            textViewTitle = itemView.findViewById(R.id.text_view_recipe_title);
            textViewPriority = itemView.findViewById(R.id.text_view_priority);
        }
    }


}
