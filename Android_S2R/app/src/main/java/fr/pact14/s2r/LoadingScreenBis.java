package fr.pact14.s2r;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.os.Handler;

public class LoadingScreenBis extends AppCompatActivity {


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_loading_screen);

        Runnable runnable = new Runnable() {
            @Override
            public void run() {
                Intent ProfileActivity = new Intent(getApplicationContext(), ProfileActivity.class);
                startActivity(ProfileActivity);
                finish();
            }
        };
        new Handler().postDelayed(runnable, 2000);
    }
}