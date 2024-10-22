package com.example.study.user;

import com.example.study.user.dto.GoogleReponse;
import com.example.study.user.dto.NaverResponse;
import com.example.study.user.dto.OAuth2Response;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.oauth2.client.userinfo.DefaultOAuth2UserService;
import org.springframework.security.oauth2.client.userinfo.OAuth2UserRequest;
import org.springframework.security.oauth2.core.OAuth2AuthenticationException;
import org.springframework.security.oauth2.core.user.OAuth2User;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Map;

@Service
public class CustomOAuth2UserService extends DefaultOAuth2UserService {
    //DefaultOAuth2UserService OAuth2UserService의 구현체

    private final UserRepository userRepository;

    public CustomOAuth2UserService(UserRepository userRepository) {

        this.userRepository = userRepository;
    }

    @Override
    public OAuth2User loadUser(OAuth2UserRequest userRequest) throws OAuth2AuthenticationException {


        OAuth2User oAuth2User = super.loadUser(userRequest);
        System.out.println(oAuth2User.getAttributes());

        String registrationId = userRequest.getClientRegistration().getRegistrationId();
        OAuth2Response oAuth2Response = null;

        if (registrationId.equals("naver")) {

            oAuth2Response = new NaverResponse(oAuth2User.getAttributes());
        }
        else if (registrationId.equals("google")) {

            oAuth2Response = new GoogleReponse(oAuth2User.getAttributes());
        }
        else {

            return null;
        }

        String username = oAuth2Response.getProvider()+" "+oAuth2Response.getProviderId();
        User existData = userRepository.findByUsername(username);

        String role = "ROLE_USER";

        if (existData == null) {

            User user = User.builder()
                    .username(username)
                    .email(oAuth2Response.getEmail())
                    .role(role)
                    .build();

            userRepository.save(user);
        }
        else {

            existData.updatOauthUser(username, oAuth2Response.getEmail());
            role = existData.getRole();

            userRepository.save(existData);
        }


        return new CustomOAuth2User(oAuth2Response, role);
    }

    public static class CustomOAuth2User implements OAuth2User {

        private final OAuth2Response oAuth2Response;
        private final String role;

        public CustomOAuth2User(OAuth2Response oAuth2Response, String role) {

            this.oAuth2Response = oAuth2Response;
            this.role = role;
        }

        @Override
        public Map<String, Object> getAttributes() {

            return null;
        }

        @Override
        public Collection<? extends GrantedAuthority> getAuthorities() {

            Collection<GrantedAuthority> collection = new ArrayList<>();

            collection.add(new GrantedAuthority() {

                @Override
                public String getAuthority() {

                    return role;
                }
            });

            return collection;
        }

        @Override
        public String getName() {

            return oAuth2Response.getName();
        }

        public String getUsername() {

            return oAuth2Response.getProvider()+" "+oAuth2Response.getProviderId();
        }
    }
}