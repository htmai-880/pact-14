/*
package fr.pact14.s2r;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.http.Body;

public class JsonApiMethods {

    public static String[] createUserInfoPost(
            String userName,
            String email,
            String password,
            JsonApi jsonApi) {
        UserInfoPost userInfoPost = new UserInfoPost(userName, email, password, null, null);
        final String[] res = new String[4];

        Call<HashMap> call = jsonApi.createUserInfoPost(userInfoPost);

        call.enqueue(new Callback<HashMap>() {
            @Override
            public void onResponse(Call<HashMap> call, Response<HashMap> response) {

                if (response.isSuccessful()) {
                    return;
                }
                HashMap userInfoPostResponse = response.body();

                // Response code
                res[0] = "" + response.code();

                // User Email
                //res[1] = userInfoPostResponse.getEmail();

                // Username
                //res[2] = userInfoPostResponse.getUserName();

            }

            @Override
            public void onFailure(Call<HashMap> call, Throwable t) {
                res[0] = t.getMessage();
            }
        });
    return res;
    }

    public static String[] getUserInfoPost(String userName, JsonApi jsonApi) {

        final String[] res = new String[4];

        Call<HashMap> call = jsonApi.getUserInfoPost(userName, GlobalVariables.currentToken);

        call.enqueue(new Callback<HashMap>() {
            @Override
            public void onResponse(Call<HashMap> call, Response<HashMap> response) {
                if (response.isSuccessful()){
                    res[0] += response.code();
                }
            }

            @Override
            public void onFailure(Call<HashMap> call, Throwable t) {

            }
        });
        return res;
    }

    public static String updateUserInfoPost(int userId, String userName, String email, String password, JsonApi jsonApi) {

        UserInfoPost newUserInfoPost = new UserInfoPost(userName, email, password, null, null);

        Call<UserInfoPost> call = jsonApi.patchUserInfoPost(userId, newUserInfoPost);

        final String[] res = new String[1];

        call.enqueue(new Callback<UserInfoPost>() {
            @Override
            public void onResponse(Call<UserInfoPost> call, Response<UserInfoPost> response) {

                if (!response.isSuccessful()) {
                    res[0] += response.code();
                    return;
                }
            }

            @Override
            public void onFailure(Call<UserInfoPost> call, Throwable t) {
                res[0] = t.getMessage();
            }
        });
    return res[0];
    }

    public static List<Recipe> getRecipeSearchResult(String research_message, JsonApi jsonApi){

        final List<Recipe>[] res = new List[]{new ArrayList<>()};

        Call<List<Recipe>> call = jsonApi.getRecipeSearchResult(research_message);

        call.enqueue(new Callback<List<Recipe>>() {
            @Override
            public void onResponse(Call<List<Recipe>> call, Response<List<Recipe>> response) {
                res[0] = response.body();
            }

            @Override
            public void onFailure(Call<List<Recipe>> call, Throwable t) {

            }
        });

        return res[0];
    }

    public static String[] getLoginResponse(String userEmail, String password, JsonApi jsonApi){

        final String[] res = new String[2];

        Call<HashMap> call = jsonApi.getLoginResponse(new LoginInfoPost(userEmail, password));

        call.enqueue(new Callback<HashMap>() {
            @Override
            public void onResponse(Call<HashMap> call, Response<HashMap> response) {
                res[0] = "" + response.code();
                res[1] = "" + response.body();
            }

            @Override
            public void onFailure(Call<HashMap> call, Throwable t) {
                res[0] = t.getMessage();
            }
        });

        return res;

    }
}

*/
