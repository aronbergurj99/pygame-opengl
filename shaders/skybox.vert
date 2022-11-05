attribute vec3 a_position;

uniform mat4 m_view;
uniform mat4 m_proj;

varying vec3 v_uv;

void main()
{
    v_uv = a_position;
    vec4 position = m_proj * m_view * vec4(a_position, 1.0);
    gl_Position = position.xyww;
    gl_Position.z -= 0.0001;
}