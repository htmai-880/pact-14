package fr.pact14.s2r;

import androidx.lifecycle.LiveData;
import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.Query;
import androidx.room.Update;

@Dao
public interface ListDao {

    @Insert
    void insert(List list);

    @Update
    void update(List list);

    @Delete
    void delete(List list);

    @Query("DELETE FROM list_table")
    void deleteAllLists();

    @Query("SELECT * FROM list_table ORDER BY priority DESC")
    LiveData<java.util.List<List>> getAllLists();
}
