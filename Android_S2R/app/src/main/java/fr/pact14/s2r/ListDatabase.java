package fr.pact14.s2r;

import android.content.Context;
import android.os.AsyncTask;

import androidx.annotation.NonNull;
import androidx.room.Database;
import androidx.room.Room;
import androidx.room.RoomDatabase;
import androidx.sqlite.db.SupportSQLiteDatabase;

@Database(entities = {List.class}, version = 1)
public abstract class ListDatabase extends RoomDatabase {

    private static ListDatabase instance;

    public abstract ListDao listDao();

    public static synchronized ListDatabase getInstance(Context context){
        if(instance == null){
            instance = Room.databaseBuilder(context.getApplicationContext(), ListDatabase.class, "list_database").fallbackToDestructiveMigration().addCallback(roomCallback).build();

        }
        return instance;

    }

    private static RoomDatabase.Callback roomCallback = new RoomDatabase.Callback(){
        @Override
        public void onCreate(@NonNull SupportSQLiteDatabase db) {
            super.onCreate(db);
            new PopulateDbAsyncTask(instance).execute();
        }
    };

    private static class PopulateDbAsyncTask extends AsyncTask<Void, Void, Void>{

        private ListDao listDao;

        private PopulateDbAsyncTask(ListDatabase db){
            listDao = db.listDao();
        }
        @Override
        protected Void doInBackground(Void... voids) {
            listDao.insert(new List("Title 1bis", "Description 1",1));
            listDao.insert(new List("Title 2", "Description 2",2));
            listDao.insert(new List("Title 3", "Description 3",3));
            return null;
        }
    }
}
