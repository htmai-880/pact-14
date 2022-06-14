package fr.pact14.s2r;

import java.util.List;

public class LoginInfoPost {
    private String email;
    private String password;

    public LoginInfoPost(String email, String password) {
        this.password = password;
        this.email = email;
    }

    public String getEmail() {
        return email;
    }

    public String getPassword() {
        return password;
    }
}
