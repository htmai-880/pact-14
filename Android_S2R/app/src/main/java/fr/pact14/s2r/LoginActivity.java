package fr.pact14.s2r;

import androidx.appcompat.app.AppCompatActivity;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProviders;

import android.content.Intent;
import android.os.Bundle;
import android.provider.Settings;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import org.json.JSONObject;

import java.util.HashMap;
import java.util.List;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class LoginActivity extends AppCompatActivity {

    //private Button go_to_profile;
    private Button go_to_sign_in;
    private Button submit,validate;
    private EditText email, password;
    private JsonApi jsonApi;
    private TextView warning_message;
    private TextView textViewResult;
    private Boolean can_connect = false;
    private Boolean validate_clicked = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        //this.go_to_profile = (Button) findViewById(R.id.login_button);
        this.go_to_sign_in = (Button) findViewById(R.id.to_sign_in);
        this.submit = (Button) findViewById(R.id.se_connecter_button);
        this.validate = (Button) findViewById(R.id.validate_button);
        this.email = (EditText) findViewById(R.id.email_edit_text);
        this.password = (EditText) findViewById(R.id.mdp_edit_text);
        this.warning_message = (TextView) findViewById(R.id.warning_message);
        this.textViewResult = (TextView) findViewById(R.id.text_view_result);

        //Gson gson = new GsonBuilder().excludeFieldsWithoutExposeAnnotation().create();

        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://pact15.r2.enst.fr/api/backend/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        jsonApi = retrofit.create(JsonApi.class);

        go_to_sign_in.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent signInActivity = new Intent(getApplicationContext(), SignInActivity.class);
                startActivity(signInActivity);
                finish();
            }
        });

        /*go_to_profile.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent profileActivity = new Intent(getApplicationContext(), ProfileActivity.class);
                startActivity(profileActivity);
                finish();
            }
        });*/

        validate.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                //testPost();

                validate_clicked = true;
                if (password.getText().toString().isEmpty() || email.getText().toString().isEmpty()) {
                    warning_message.setText("Empty fields left");
                }

                else {

                    getLoginResponseTest(email.getText().toString(), password.getText().toString(), jsonApi);

                }


            }
        });

        submit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (can_connect){
                    getUserFromEmail();
                    Intent loadingScreenBis = new Intent(getApplicationContext(), LoadingScreenBis.class);
                    startActivity(loadingScreenBis);
                    finish();
                }

                else{
                    if (validate_clicked){
                        warning_message.setText("Email and password do not match");
                    }
                    else {
                        warning_message.setText("Please validate first");
                    }
                }
            }
        });

    }


    public void testPost() {

        Call<HelloWorld> call = jsonApi.testHelloWorld();

        call.enqueue(new Callback<HelloWorld>() {
            @Override
            public void onResponse(Call<HelloWorld> call, Response<HelloWorld> response) {

                textViewResult.append("response code: " + response.code() + "\n");
                textViewResult.append("body: " + response.body() + "\n");
                textViewResult.append("body.getHello(): " + response.body().getHello() + "\n");
            }

            @Override
            public void onFailure(Call<HelloWorld> call, Throwable t) {
                textViewResult.append("error message: " + t.getMessage());
            }
        });
    }

    public void getLoginResponseTest(String userEmail, String password, JsonApi jsonApi){

        LoginInfoPost loginInfoPost = new LoginInfoPost(userEmail, password);

        Call<LoginResponse> call = jsonApi.getLoginResponse(loginInfoPost);


        call.enqueue(new Callback<LoginResponse>() {
            @Override
            public void onResponse(Call<LoginResponse> call, Response<LoginResponse> response) {
                textViewResult.append("Login code: " + response.code() + "\n");
                //textViewResult.append("Login Body: " + response.body() + "\n");
                if (response.code() == 200){
                    can_connect = true;
                    GlobalVariables.currentToken = (String) response.body().getToken();
                    GlobalVariables.currentUserEmail = (String) email.getText().toString();

                    textViewResult.append("Can connect: " + can_connect + "\n");
                    textViewResult.append("User email: " + GlobalVariables.currentUserEmail + "\n");
                    textViewResult.append("User token: " + GlobalVariables.currentToken + "\n");
                }

                else{

                }

            }

            @Override
            public void onFailure(Call<LoginResponse> call, Throwable t) {
                textViewResult.append("error message: " + t.getMessage() + "\n");
            }
        });

    }

    public void getUserFromEmail() {

        Call<SimpleUserInfoResponse> call = jsonApi.getUserFromEmail(GlobalVariables.currentUserEmail);

        call.enqueue(new Callback<SimpleUserInfoResponse>() {
            @Override
            public void onResponse(Call<SimpleUserInfoResponse> call, Response<SimpleUserInfoResponse> response) {
                System.out.println(response.code());
                System.out.println(response.body());
                UserInfoPost user = response.body().getUser();
                System.out.println(user);
                GlobalVariables.currentUserName = user.getUserName();
                GlobalVariables.ingredientList = user.getIngredientList();
                GlobalVariables.recipeList = user.getRecipeList();
                System.out.println(GlobalVariables.currentUserName);
                System.out.println(GlobalVariables.ingredientList);
                System.out.println(GlobalVariables.recipeList);
            }

            @Override
            public void onFailure(Call<SimpleUserInfoResponse> call, Throwable t) {
                System.out.println(t.getMessage());
            }
        });

    }
}