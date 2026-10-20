package it.sistinf.romacapitale.auth.interceptor;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.http.HttpHeaders;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

@Component
public class HeaderInterceptor implements HandlerInterceptor {

    private final ThreadLocal<HttpHeaders> headersHolder = new ThreadLocal<>();

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) {
        HttpHeaders httpHeaders = new HttpHeaders();
        if (request.getCookies() != null) {
            for (jakarta.servlet.http.Cookie cookie : request.getCookies()) {
                httpHeaders.add("Cookie", cookie.getName() + "=" + cookie.getValue());
            }
        }
        headersHolder.set(httpHeaders);
        return true;
    }

    public HttpHeaders getHeaders() {
        return headersHolder.get();
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) {
        headersHolder.remove();
    }
}