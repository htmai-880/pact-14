package fr.pact14.s2r;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.graphics.Color;
import android.graphics.PorterDuff;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import java.util.HashMap;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class SignInActivity extends AppCompatActivity {

    private Button go_to_login;
    private Button valider_btn;
    private EditText username, email, mdp, repeter_mdp;
    private TextView warning_msg2;
    private JsonApi jsonApi;
    private TextView textViewResult;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sign_in);

        this.go_to_login = (Button) findViewById(R.id.sign_in_button);
        this.username = (EditText) findViewById(R.id.username);
        this.email = (EditText) findViewById(R.id.email);
        this.mdp = (EditText) findViewById(R.id.mdp);
        this.repeter_mdp = (EditText) findViewById(R.id.repeter_mdp);
        this.warning_msg2 = (TextView) findViewById(R.id.warning_message2);
        this.valider_btn = (Button) findViewById(R.id.valider_button);
        this.textViewResult = findViewById(R.id.sign_in_text_view_result);

        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://pact15.r2.enst.fr/api/backend/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();
        jsonApi = retrofit.create(JsonApi.class);

        go_to_login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                repeter_mdp.getBackground().setColorFilter(Color.BLACK, PorterDuff.Mode.SRC_ATOP);
                username.getBackground().setColorFilter(Color.BLACK,PorterDuff.Mode.SRC_ATOP);
                email.getBackground().setColorFilter(Color.BLACK,PorterDuff.Mode.SRC_ATOP);
                mdp.getBackground().setColorFilter(Color.BLACK,PorterDuff.Mode.SRC_ATOP);
                Intent loginActivity = new Intent(getApplicationContext(), LoginActivity.class);
                startActivity(loginActivity);
                finish();
            }
        });

        valider_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (repeter_mdp.getText().toString().isEmpty()){
                    repeter_mdp.getBackground().setColorFilter(Color.RED, PorterDuff.Mode.SRC_ATOP);
                }
                if (username.getText().toString().isEmpty()){
                    username.getBackground().setColorFilter(Color.RED, PorterDuff.Mode.SRC_ATOP);
                }
                if (email.getText().toString().isEmpty()){
                    email.getBackground().setColorFilter(Color.RED, PorterDuff.Mode.SRC_ATOP);
                }
                if(mdp.getText().toString().isEmpty()){
                    mdp.getBackground().setColorFilter(Color.RED, PorterDuff.Mode.SRC_ATOP);
                }
                if (!repeter_mdp.getText().toString().isEmpty() && !username.getText().toString().isEmpty() && !email.getText().toString().isEmpty() && !mdp.getText().toString().isEmpty()){
                    warning_msg2.setText("");
                }
                else{
                    warning_msg2.setText("Please complete every field");
                }
                if (!repeter_mdp.getText().toString().isEmpty()){
                    repeter_mdp.getBackground().setColorFilter(Color.BLACK, PorterDuff.Mode.SRC_ATOP);
                }
                if (!username.getText().toString().isEmpty()){
                    username.getBackground().setColorFilter(Color.BLACK,PorterDuff.Mode.SRC_ATOP);
                }
                if (!email.getText().toString().isEmpty()){
                    email.getBackground().setColorFilter(Color.BLACK,PorterDuff.Mode.SRC_ATOP);
                }
                if (!mdp.getText().toString().isEmpty()){
                    mdp.getBackground().setColorFilter(Color.BLACK,PorterDuff.Mode.SRC_ATOP);
                }
                if (warning_msg2.getText() == ""){
                    //String[] userInfoPost = JsonApiMethods.createUserInfoPost(username.getText().toString(),email.getText().toString(),mdp.getText().toString(),jsonApi);
                    createUserInfoPost(username.getText().toString(),email.getText().toString(),mdp.getText().toString(),jsonApi);
                }

            }
        });

    }

    public void createUserInfoPost(
            String userName,
            String email,
            String password,
            JsonApi jsonApi) {
        UserInfoPost userInfoPost = new UserInfoPost(userName, email, password, null, null);

        Call<HashMap> call = jsonApi.createUserInfoPost(userInfoPost);

        call.enqueue(new Callback<HashMap>() {
            @Override
            public void onResponse(Call<HashMap> call, Response<HashMap> response) {

                textViewResult.append("SignIn code: " + response.code() + "\n");
                textViewResult.append("SignIn Body: " + response.body() + "\n");

            }

            @Override
            public void onFailure(Call<HashMap> call, Throwable t){
                textViewResult.append("error message: " + t.getMessage() + "\n");
            }
        });
    }
}