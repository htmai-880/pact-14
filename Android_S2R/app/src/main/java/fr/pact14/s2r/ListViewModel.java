package fr.pact14.s2r;

import android.app.Application;

import androidx.annotation.NonNull;
import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.LiveData;

import java.util.List;

public class ListViewModel extends AndroidViewModel {
    private ListRepository repository;
    private LiveData<List<fr.pact14.s2r.List>> allLists;
    public ListViewModel(@NonNull Application application) {
        super(application);
        repository = new ListRepository(application);
        allLists = repository.getAllLists();
    }

    public void insert (fr.pact14.s2r.List list){
        repository.insert(list);
    }

    public void update (fr.pact14.s2r.List list){
        repository.update(list);
    }

    public void delete (fr.pact14.s2r.List list){
        repository.delete(list);
    }

    public void deleteAllNotes(){
        repository.deleteAllLists();
    }

    public LiveData<List<fr.pact14.s2r.List>> getAllLists() {
        return allLists;
    }



}
