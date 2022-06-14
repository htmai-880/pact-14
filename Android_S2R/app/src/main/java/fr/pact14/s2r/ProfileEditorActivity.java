package fr.pact14.s2r;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.content.Context;
import android.content.ContextWrapper;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.HashMap;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class ProfileEditorActivity extends AppCompatActivity {

    private ImageView go_to_profile;
    private ImageView go_to_supplies;
    private ImageView go_to_search;
    private final static int REQUEST_CODE_STORAGE_PERMISSION =1;
    private final static int REQUEST_CODE_SELECT_IMAGE = 2;
    private ImageView imageSelected;
    private Button enreg_btn;
    private Bitmap bitmap;
    public static Bitmap b;
    private String path;
    private TextView confirmation_profile_picture;
    private ImageView profile_picture_profile_editor;
    private EditText change_username;
    private JsonApi jsonApi;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_profile_editor);

        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://pact15.r2.enst.fr/api/backend/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        jsonApi = retrofit.create(JsonApi.class);

        this.go_to_profile = (ImageView) findViewById(R.id.to_profile_button);
        this.go_to_supplies = (ImageView) findViewById(R.id.to_supplies_button);
        this.go_to_search = (ImageView) findViewById(R.id.to_search_button);
        this.confirmation_profile_picture = (TextView) findViewById(R.id.confirmation_profile_picture);
        this.profile_picture_profile_editor = (ImageView) findViewById(R.id.profile_picture_profile_editor);
        this.change_username = (EditText) findViewById(R.id.plain_text_input);

        profile_picture_profile_editor.setImageBitmap(b);

        imageSelected = findViewById(R.id.profile_picture_profile_editor);

        enreg_btn = (Button)findViewById(R.id.profile_editor_button);

        enreg_btn.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View v) {
                ContextWrapper cw = new ContextWrapper(getApplicationContext());
                File directory = cw.getDir("ImageDir", Context.MODE_PRIVATE);
                File mypath = new File(directory,"profile_editor.jpg");

                FileOutputStream fos = null;

                try{
                    fos = new FileOutputStream(mypath);
                    bitmap.compress(Bitmap.CompressFormat.PNG, 100, fos);
                } catch (Exception e){
                    e.printStackTrace();
                } finally {
                    try{
                        fos.close();
                    } catch (IOException e){
                        e.printStackTrace();
                    }
                }
                path = directory.getAbsolutePath();
                loadImageFromStorage(path);

                if (!change_username.getText().toString().isEmpty()) {
                    changeUserName(change_username.getText().toString());
                }

            }

            private void loadImageFromStorage(String path) {
                try{
                    File f = new File(path,"profile_editor.jpg");
                    b = BitmapFactory.decodeStream(new FileInputStream(f));
                    confirmation_profile_picture.setText("Photo enregistrée !");
                    confirmation_profile_picture.setTextSize(25);


                } catch (FileNotFoundException e){
                    e.printStackTrace();
                }
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

        findViewById(R.id.modify_profile_picture).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (ContextCompat.checkSelfPermission(getApplicationContext(), Manifest.permission.READ_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED){
                    ActivityCompat.requestPermissions(
                            ProfileEditorActivity.this,
                            new String[]{Manifest.permission.READ_EXTERNAL_STORAGE},
                            REQUEST_CODE_STORAGE_PERMISSION
                    );
                }else{
                    selectImage();
                }
            }
        });
    }

    private void selectImage(){
        Intent intent = new Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
        if (intent.resolveActivity(getPackageManager()) != null){
            startActivityForResult(intent, REQUEST_CODE_SELECT_IMAGE);
        }

    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);

        if (requestCode == REQUEST_CODE_STORAGE_PERMISSION && grantResults.length >0){
            if (grantResults[0] == PackageManager.PERMISSION_GRANTED){
                selectImage();
            }
            else{
                Toast.makeText(this, "Permission denied", Toast.LENGTH_SHORT).show();
            }
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if(requestCode == REQUEST_CODE_SELECT_IMAGE && resultCode == RESULT_OK){
            if (data != null){
                Uri selectedImageUri = data.getData();
                if (selectedImageUri != null){
                    try{
                        InputStream inputStream = getContentResolver().openInputStream(selectedImageUri);
                        bitmap = BitmapFactory.decodeStream(inputStream);
                        imageSelected.setImageBitmap(bitmap);

                    }catch (Exception exception){
                        Toast.makeText(this, exception.getMessage(), Toast.LENGTH_SHORT).show();
                    }
                }
            }
        }
    }


    public void changeUserName(String newUsername){

        Call<HashMap> call = jsonApi.changeUserName(GlobalVariables.currentUserEmail, newUsername);

        call.enqueue(new Callback<HashMap>() {
            @Override
            public void onResponse(Call<HashMap> call, Response<HashMap> response) {

                System.out.println("response code: " + response.code());
                System.out.println("body: " + response.body());
            }

            @Override
            public void onFailure(Call<HashMap> call, Throwable t) {
                System.out.println("error message: " + t.getMessage());
            }
        });

    }


}