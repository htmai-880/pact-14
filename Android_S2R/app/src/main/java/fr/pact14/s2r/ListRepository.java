package fr.pact14.s2r;

import android.app.Application;
import android.os.AsyncTask;

import androidx.lifecycle.LiveData;

import java.util.List;

public class ListRepository {
    private ListDao listDao;
    private LiveData<List<fr.pact14.s2r.List>> allLists;

    public ListRepository (Application application){
        ListDatabase database = ListDatabase.getInstance(application);
        listDao = database.listDao();
        allLists = listDao.getAllLists();
    }

    public void insert(fr.pact14.s2r.List list){
        new InsertListAsyncTask(listDao).execute(list);

    }

    public void update (fr.pact14.s2r.List list){
        new UpdateListAsyncTask(listDao).execute(list);

    }

    public void delete (fr.pact14.s2r.List list){
        new DeleteListAsyncTask(listDao).execute(list);

    }

    public void deleteAllLists (){
        new DeleteAllListsAsyncTask(listDao).execute();

    }

    public LiveData<List<fr.pact14.s2r.List>> getAllLists() {
        return allLists;
    }

    private static class InsertListAsyncTask extends AsyncTask<fr.pact14.s2r.List,Void,Void> {
        private ListDao listDao;
        private InsertListAsyncTask(ListDao listDao){
            this.listDao = listDao;
        }

        @Override
        protected Void doInBackground(fr.pact14.s2r.List... lists) {
            listDao.insert(lists[0]);
            return null;
        }
    }

    private static class UpdateListAsyncTask extends AsyncTask<fr.pact14.s2r.List,Void,Void> {
        private ListDao listDao;
        private UpdateListAsyncTask(ListDao listDao){
            this.listDao = listDao;
        }

        @Override
        protected Void doInBackground(fr.pact14.s2r.List... lists) {
            listDao.update(lists[0]);
            return null;
        }
    }

    private static class DeleteListAsyncTask extends AsyncTask<fr.pact14.s2r.List,Void,Void> {
        private ListDao listDao;
        private DeleteListAsyncTask(ListDao listDao){
            this.listDao = listDao;
        }

        @Override
        protected Void doInBackground(fr.pact14.s2r.List... lists) {
            listDao.delete(lists[0]);
            return null;
        }
    }

    private static class DeleteAllListsAsyncTask extends AsyncTask<Void,Void,Void> {
        private ListDao listDao;
        private DeleteAllListsAsyncTask(ListDao listDao){
            this.listDao = listDao;
        }

        @Override
        protected Void doInBackground(Void... voids) {
            listDao.deleteAllLists();
            return null;
        }
    }

}
