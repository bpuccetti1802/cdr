package it.sistinf.romacapitale.servicemesh.filters;

import it.sistinf.romacapitale.core.exceptions.TokenExpiredException;
import it.sistinf.romacapitale.core.security.CurrentUser;
import it.sistinf.romacapitale.core.security.JwtManager;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletRequestWrapper;
import jakarta.servlet.http.HttpServletResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Map;

@Slf4j
@Component("AuthenticationFilter")
public class AuthenticationFilter extends OncePerRequestFilter {

    @Autowired
    private JwtManager jwtManager;



    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response,
                                    FilterChain filterChain) throws ServletException, IOException {

        String jwtToken = null;

        CustomHttpServletRequestWrapper customWrappedRequest = new CustomHttpServletRequestWrapper((HttpServletRequest) request);

        //verifica se il bearer è passato nell'header o nel cookie
        //Si cerca prima nei cookie
        Cookie[] cookies = request.getCookies();
        if (cookies != null && cookies.length > 0) {
            for (int i = 0; i < cookies.length; i++) {
                if ("Bearer".equals(cookies[i].getName())) {
                    jwtToken = cookies[i].getValue();
                }
            }
        }
        if(jwtToken == null){
            String authorization = request.getHeader(HttpHeaders.AUTHORIZATION);
            //log.info("AuthenticationFilter: authorization = "+authorization);
            if (authorization != null) {
                if (authorization.startsWith("Bearer ")) {
                    jwtToken = authorization.split(" ")[1];
                }
            }
        }
//        log.info("AuthenticationFilter: jwtToken = "+jwtToken);



        //Inserisce il principal
        if (jwtToken != null && !jwtToken.isBlank()) {
            CurrentUser currentUser = null;
            try {
                currentUser = jwtManager.consumeToken(jwtToken);
            } catch (TokenExpiredException ex) {
                response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
                response.setContentType("plain/text");
                response.getWriter().write(ex.getMessage());
                return;
            }
            currentUser.setToken(jwtToken);
//            log.info("AuthenticationFilter: currentUser = "+currentUser);
            List<SimpleGrantedAuthority> grantedAuthorities = new ArrayList<>();
            for (String authority : currentUser.getAuthorities()) {
                SimpleGrantedAuthority a = new SimpleGrantedAuthority(authority);
                grantedAuthorities.add(a);
            }

            //TODO refresh del token
            Long iat = -1L;
            Long exp = -1L;

            Map<String, String> claims = currentUser.getInfo();
            for (String claimName : claims.keySet()) {//sarebbe ClaimNames
                Object claimValue = claims.get(claimName);//sarebbe ClaimValue
                // Refresh token check
                if ("iat".equals(claimName)) {
                    iat = Long.valueOf((String) claimValue);
                }
                if ("exp".equals(claimName)) {
                    exp = Long.valueOf((String) claimValue);
                }
            }

            String username = (String) claims.get("username");//sarebbe ClaimValue

            if (iat == -1L || exp == -1L) {
                throw new RuntimeException("L'Utente " + username + " non ha una sessione valida.");
            }
            Long ttlToken = 100L;
            if (exp - (new Date().getTime() / 1000) <= ttlToken) {
//                log.info("AuthenticationFilter: refresh del token");
                String token = jwtManager.createToken(currentUser);

                if (cookies != null && cookies.length > 0) {
                    for (int i = 0; i < cookies.length; i++) {
                        if ("Bearer".equals(cookies[i].getName())) {
                            cookies[i].setValue(token);
                        }
                    }
                }

                String authorization = request.getHeader(HttpHeaders.AUTHORIZATION);
                if (authorization != null) {
                    if (authorization.startsWith("Bearer ")) {
                        customWrappedRequest.addHeader(HttpHeaders.AUTHORIZATION, "Bearer " + token);
                    }
                }
            }
            //TODO END refresh del token


            UserDetails ud = new User(currentUser.getUsername(), "fake",grantedAuthorities);
            UsernamePasswordAuthenticationToken authentication =
                    new UsernamePasswordAuthenticationToken(ud,null , ud.getAuthorities());
            authentication.setDetails(currentUser);
            SecurityContextHolder.getContext().setAuthentication(authentication);
        }
        response.setCharacterEncoding("UTF-8");
        filterChain.doFilter(request, response);
    }

    @Override
    protected boolean shouldNotFilterAsyncDispatch() {
        return false;
    }

    @Override
    protected boolean shouldNotFilterErrorDispatch() {
        return false;
    }
}
