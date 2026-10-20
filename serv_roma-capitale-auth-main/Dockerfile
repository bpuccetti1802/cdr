# Stage 1: Build the application
FROM registry.access.redhat.com/ubi8/openjdk-21 AS BUILD_IMAGE

WORKDIR /app

# Proxy settings
ENV http_proxy=http://10.173.21.20:3128 
ENV https_proxy=http://10.173.21.20:3128 

# Create the Maven settings directory
USER root
RUN mkdir -p /root/.m2 
RUN microdnf install -y maven && microdnf clean all
RUN mkdir -p /app/target && chown jboss:jboss /app && chmod -R 777 /app
USER jboss

# Copy Maven settings and project files
COPY settings.xml /root/.m2
COPY pom.xml .
COPY src ./src

# Verify JAVA_HOME and Java version, and build the project
RUN mvn -B clean package -Dmaven.test.skip=true --settings /root/.m2/settings.xml

# Stage 2: Run the application
FROM registry.access.redhat.com/ubi8/openjdk-21-runtime:latest

WORKDIR /app

# Localization settings
ENV TZ=Europe/Rome
ENV LANG=it_IT.UTF-8
ENV LC_CTYPE="it_IT.UTF-8"
ENV LC_COLLATE="it_IT.UTF-8"
ENV LC_MESSAGES="it_IT.UTF-8"
ENV LC_NUMERIC=it_IT.UTF-8
ENV LC_TIME=it_IT.UTF-8
ENV LC_MONETARY=it_IT.UTF-8
ENV LC_PAPER=it_IT.UTF-8
ENV LC_NAME=it_IT.UTF-8
ENV LC_ADDRESS=it_IT.UTF-8
ENV LC_TELEPHONE=it_IT.UTF-8
ENV LC_MEASUREMENT=it_IT.UTF-8
ENV LC_IDENTIFICATION=it_IT.UTF-8

USER root
RUN ln -s -f /usr/share/zoneinfo/Europe/Rome /etc/localtime
RUN mkdir -p /var/log
RUN chmod 777 /var/log
USER 185

# Copy the built JAR from the build stage
COPY --from=BUILD_IMAGE /app/target/*.jar app.jar

# Expose application port and set entry point
EXPOSE 8081
ENTRYPOINT ["java", "-jar", "app.jar"]
