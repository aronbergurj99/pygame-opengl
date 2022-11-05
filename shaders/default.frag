
struct Light {
    vec3 position;
    vec3 Ia;
    vec3 Id;
    vec3 Is;
};

uniform sampler2D u_texture0;
uniform Light u_light;
uniform vec3 u_cam_pos;

varying vec2 v_uv;
varying vec3 v_position;
varying vec3 v_normal;

vec3 getLight(vec3 color) {
    vec3 Normal = normalize(v_normal);
    
    vec3 ambient = u_light.Ia;
    
    //diffuse
    vec3 lightDir = normalize(u_light.position - v_position);
    float diff = max(0, dot(lightDir, Normal));
    vec3 diffuse = diff * u_light.Id;
    
    //specular
    vec3 viewDir = normalize(u_cam_pos - v_position);
    vec3 reflectDir = reflect(-lightDir, Normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0), 32);
    vec3 specular = spec * u_light.Is;
    
    return color * (ambient + diffuse + specular);
}   

void main(void)
{
    vec3 color = texture2D(u_texture0, v_uv).rgb;
    color = getLight(color);
    
    gl_FragColor = vec4(color, 1.0);
}
