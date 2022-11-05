attribute vec3 a_position;
attribute vec2 a_texcord0;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

varying vec2 v_uv;

void main(void)
{
	v_uv = a_texcord0;
	gl_Position = m_proj * m_view * m_model * vec4(a_position, 1.0);
}