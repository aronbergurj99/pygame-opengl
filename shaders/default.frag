
uniform sampler2D u_texture0;

varying vec2 v_uv;

void main(void)
{
    gl_FragColor = texture2D(u_texture0, v_uv);
}
