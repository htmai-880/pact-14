package fr.pact14.s2r;

import com.google.gson.annotations.Expose;

public class LoginResponse {
    @Expose
    private String message;
    @Expose
    private String token;

    private Boolean authenticated;

    public Boolean getAuthenticated() {
        return authenticated;
    }

    public String getMessage() {
        return message;
    }

    public String getToken() {
        return token;
    }
}
