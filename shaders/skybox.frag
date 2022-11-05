uniform samplerCube u_texture0;

varying vec3 v_uv;

void main()
{
    gl_FragColor = texture(u_texture0, v_uv);
}